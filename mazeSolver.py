# houAStar/mazeSolver.py
import hou

# try absolute first, fallback to relative (when testing locally in the terminal environment)
try:
    from houAStar.aStar import AStarPathFinding
except ImportError:
    from .aStar import AStarPathFinding

# ---------------------------------------------------------------------------
#  Gather grid info
# ---------------------------------------------------------------------------

def get_grid_data(node):
    """
    Load the grid geometry, read rows/cols, then:
      1) Gather all hou.Prim objects
      2) Sort them by prim.number()
      3) Verify count == rows*cols
      4) Build:
         - idx2prim: list of prim numbers in row-major order
         - prim2idx: inverse map
      5) Read each prim’s 'open' flag into a flat list, then slice into 2D maze
    """
    grid_path = node.parm('maze_grid_path').eval()
    geo       = hou.node(grid_path).geometry()
    rows      = geo.attribValue('rows')
    cols      = geo.attribValue('cols')
    total     = rows * cols

    # Collect and sort primitives by their numeric ID
    prims = list(geo.prims())
    prims.sort(key=lambda p: p.number())

    # Sanity check
    if len(prims) != total:
        hou.ui.displayMessage(
            f"Expected {total} primitives (rows*cols), but found {len(prims)}.",
            severity=hou.severityType.Warning
        )

    # Build index mappings
    idx2prim = [p.number() for p in prims]
    prim2idx = {pnum: idx for idx, pnum in enumerate(idx2prim)}

    # Read open flags in that same order
    flags = [geo.prim(pnum).intAttribValue('open') for pnum in idx2prim]

    # Build 2D maze (1=open, 0=blocked)
    maze = [ flags[r*cols:(r+1)*cols] for r in range(rows) ]

    return geo, maze, rows, cols, prim2idx, idx2prim


# ---------------------------------------------------------------------------
#  Get index (r, c) of agents' (NPCs) geo using primitive number of the grid
#  cell they sit on. Each NPC is expected to be seprated by "name" attribute. 
#  This allows instancing & easy rendering in USD (solaris) land.
# ---------------------------------------------------------------------------

def read_agent_cells(node, geo, cols, prim2idx):
    """
    Group the Agents SOP’s points by `name`, then for each agent:
     - compute the average point position
     - call nearestPrim() once (unpack the tuple)
     - map primnum→(r,c)
    """
    agents_path = node.parm('agents_geo').eval().strip()
    sop         = hou.node(agents_path)
    if not sop:
        hou.ui.displayMessage(
            f"Agents SOP not found: {agents_path}",
            severity=hou.severityType.Warning
        )
        return {}

    pts = sop.geometry().points()
    buckets = {}
    for pt in pts:
        name = pt.stringAttribValue('name')
        buckets.setdefault(name, []).append(pt)

    mapping = {}
    for name, group in buckets.items():
        sumP = hou.Vector3(0,0,0)
        for pt in group:
            sumP += pt.position()
        centroid = sumP / len(group)

        # nearestPrim returns (prim, u, v, w)
        prim, _, _, _ = geo.nearestPrim(centroid)
        if not prim:
            hou.ui.displayMessage(
                f"Agent {name} at {centroid} not over any grid cell",
                severity=hou.severityType.Warning
            )
            continue

        primnum = prim.number()
        idx     = prim2idx.get(primnum)
        if idx is None:
            hou.ui.displayMessage(
                f"Agent {name} on prim {primnum} not in prim2idx",
                severity=hou.severityType.Warning
            )
            continue

        mapping[name] = divmod(idx, cols)

    return mapping
# ---------------------------------------------------------------------------
#  Get index (r, c) of target geo using primitive number on which it sits on
# ---------------------------------------------------------------------------

def read_target_cell(node, geo, cols, prim2idx):
    """
    Map the Target SOP’s geometry → single centroid → primnum → (r,c).
    """
    path = node.parm('target_geo').eval().strip()
    sop  = hou.node(path)
    if not sop:
        hou.ui.displayMessage(
            f"Target path not found: {path}",
            severity=hou.severityType.Warning
        )
        return None

    pts = sop.geometry().points()
    if not pts:
        hou.ui.displayMessage(
            "Target SOP has no points!",
            severity=hou.severityType.Warning
        )
        return None

    sumP = hou.Vector3(0,0,0)
    for pt in pts:
        sumP += pt.position()
    centroid = sumP / len(pts)

    prim, _, _, _ = geo.nearestPrim(centroid)
    if not prim:
        hou.ui.displayMessage(
            f"Target at {centroid} not over any grid cell",
            severity=hou.severityType.Warning
        )
        return None

    primnum = prim.number()
    idx     = prim2idx.get(primnum)
    if idx is None:
        hou.ui.displayMessage(
            f"Target on prim {primnum} not in prim2idx",
            severity=hou.severityType.Warning
        )
        return None

    return divmod(idx, cols)


# ---------------------------------------------------------------------------
#  Turn cell-paths into polylines so that we can stash within the HDA
# ---------------------------------------------------------------------------
def build_path_geometry(paths, grid_geo, rows, cols, idx2prim):
    g        = hou.Geometry()
    agent_at = g.addAttrib(hou.attribType.Point, "agent", "")
    step_at  = g.addAttrib(hou.attribType.Point, "step", 0)

    for agent_name, cell_path in paths.items():
        pts = []
        for step_id, (r, c) in enumerate(cell_path):
            idx     = r * cols + c
            primnum = idx2prim[idx]
            P       = grid_geo.prim(primnum).positionAtInterior(0.5, 0.5, 0.0)

            pt = g.createPoint()
            pt.setPosition(P)
            pt.setAttribValue(agent_at, agent_name)
            pt.setAttribValue(step_at, step_id)
            pts.append(pt)

        poly = g.createPolygon(is_closed=False)
        for pt in pts:
            poly.addVertex(pt)

    return g


# ---------------------------------------------------------------------------
#  solve_all RETURNS the geometry to stash
# ---------------------------------------------------------------------------
def solve_all(node):
    grid_geo, maze, rows, cols, prim2idx, idx2prim = get_grid_data(node)

    agents_map = read_agent_cells(node, grid_geo, cols, prim2idx)
    target_rc  = read_target_cell(node, grid_geo, cols, prim2idx)
    if target_rc is None:
        return None

    paths = {}
    for name, start_rc in agents_map.items():
        solver = AStarPathFinding(maze, start_rc, target_rc)
        path   = solver.find_path()
        if not path:
            hou.ui.displayMessage(
                f"No path found for {name}",
                severity=hou.severityType.Warning
            )
            continue
        paths[name] = path

    if not paths:
        return None

    # build the polyline geometry and hand it back
    return build_path_geometry(paths, grid_geo, rows, cols, idx2prim)

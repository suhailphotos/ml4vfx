# houAStar/mazeSolver.py
import hou

# try absolute first, fallback to relative
try:
    from houAStar.aStar import AStarPathFinding
except ImportError:
    from .aStar import AStarPathFinding

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

    # 4) Read open flags in that same order
    flags = [geo.prim(pnum).intAttribValue('open') for pnum in idx2prim]

    # 5) Build 2D maze (1=open, 0=blocked)
    maze = [ flags[r*cols:(r+1)*cols] for r in range(rows) ]

    return geo, maze, rows, cols, prim2idx, idx2prim


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


def write_paths(node, paths, geo, rows, cols, idx2prim):
    """
    Convert each (r,c) back to primnum via idx2prim, sample P, 
    and write detail-level path_<name> = [x0,y0,z0, x1,y1,z1, ...]
    """
    out_geo = node.geometry()

    for name, cell_path in paths.items():
        attr_name = f"path_{name}"

        # 1) Declare the detail attribute if needed, with a non-empty default
        if not out_geo.findGlobalAttrib(attr_name):
            # Use a single float default to satisfy Houdini’s requirement
            out_geo.addAttrib(hou.attribType.Global, attr_name, [0.0])

        # 2) Build the flat float list
        flat = []
        for (r, c) in cell_path:
            idx     = r * cols + c
            primnum = idx2prim[idx]
            P       = geo.prim(primnum).positionAtInterior(0.5, 0.5, 0.0)
            flat.extend((P.x, P.y, P.z))

        # 3) Overwrite the default with your full list
        out_geo.setGlobalAttribValue(attr_name, flat)

def solve_all(node):
    geo, maze, rows, cols, prim2idx, idx2prim = get_grid_data(node)

    agents_map = read_agent_cells(node, geo, cols, prim2idx)
    target_rc  = read_target_cell(node, geo, cols, prim2idx)
    if target_rc is None:
        return

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


    write_paths(node, paths, geo, rows, cols, idx2prim)

# houAStar/mazeSolver.py
import hou

# try absolute import first (HDA PythonModule context),
# else fall back to relative package import (local script testing)
try:
    from houAStar.aStar import AStarPathFinding
except ImportError:
    from .aStar import AStarPathFinding

def get_grid_data(node):
    grid_path = node.parm('maze_grid_path').eval()
    geo = hou.node(grid_path).geometry()
    rows = geo.detailAttribValue('rows')
    cols = geo.detailAttribValue('cols')
    wall_flags = [geo.prim(i).intAttribValue('open') for i in range(rows*cols)]
    maze = [wall_flags[r*cols:(r+1)*cols] for r in range(rows)]
    return geo, maze, rows, cols

#def worldpos_from_cell(geo, primnum):
#    prim = geo.prim(primnum)
#    # sample the world-space position at the center of the quad
#    return prim.positionAtInterior(0.5, 0.5, 0.0)
#
#def read_agent_cells(node, rows, cols):
#    agents_path = node.parm('agents_geo').eval()
#    agents_geo  = hou.node(agents_path).geometry()
#    mapping = {}
#    for pt in agents_geo.points():
#        name = pt.stringAttribValue('name')
#        P    = pt.position()
#        c = int(P.x + 0.5)
#        r = int(P.z + 0.5)
#        mapping[name] = (r, c)
#    return mapping
#
#def read_target_cell(node):
#    tgt_path = node.parm('target_geo').eval()
#    tgt_geo  = hou.node(tgt_path).geometry()
#    pt = tgt_geo.points()[0]
#    P  = pt.position()
#    return (int(P.z + 0.5), int(P.x + 0.5))
#
#def write_paths(node, paths, geo, rows, cols):
#    out_geo = node.geometry()
#    for name, cell_path in paths.items():
#        attr_name = f'path_{name}'
#        flat = []
#        for (r, c) in cell_path:
#            primnum = r*cols + c
#            P = worldpos_from_cell(geo, primnum)
#            flat.extend([P.x, P.y, P.z])
#        out_geo.setGlobalAttribValue(attr_name, flat)
#
def solve_all(node):
    pass

#    geo, maze, rows, cols = get_grid_data(node)
#    agents_map           = read_agent_cells(node, rows, cols)
#    target_rc            = read_target_cell(node)
#
#    paths = {}
#    for name, start_rc in agents_map.items():
#        solver = AStarPathFinding(maze, start_rc, target_rc)
#        path = solver.find_path()
#        if not path:
#            hou.ui.warning(f"No path found for {name}")
#            continue
#        paths[name] = path
#
#    write_paths(node, paths, geo, rows, cols)

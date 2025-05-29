# solver_py Python SOP script
import hou
from houAStar.mazeSolver import solve_all

node  = hou.pwd()     
hda   = node.parent()     

geo_out = solve_all(hda)
g = node.geometry()  

g.clear()
if geo_out is not None:
    g.merge(geo_out)

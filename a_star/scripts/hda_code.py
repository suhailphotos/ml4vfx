import hou
import math
import sys
sys.path.append(r"C:\Users\felpserver\development\games\HoudiniStuff\a_start_test\scripts")

from a_star import AStarPathfinding

class Test:
    def __init__(self):
        pass
    def printer(self):
        print("Hello from the node")
        
def onClickExecute(kwargs):
    util = Test()
    util.printer()
  
def get_maze_from_grid():
    grid = hou.pwd().parm('grid_path').eval()
    geo = hou.node(grid).geometry()
    
    prims = geo.prims()
    num_rows = num_columns = int(math.sqrt(len(prims)))
    
    # Initialize the matrix
    grid_matrix = []

    # Populate the matrix
    for row in range(num_rows):
        row_data = []
        for col in range(num_columns):
            prim_index = row * num_columns + col
            prim = geo.prim(prim_index)
            color = prim.attribValue("Cd")  
            row_data.append(1 if color == (1.0,1.0,1.0) else 0)  
        grid_matrix.append(row_data)
 
    return grid_matrix
    
def position_object(obj_path, row, col,cell_size=1): 
    
    main_char = hou.node(obj_path)
    world_x = col * cell_size
    world_z = row * cell_size
    
    center = main_char.parmTuple("t").eval()
    main_char.parmTuple("t").set((world_x, 0, world_z))
    
    pos = (row, col)
    return pos

def solve_maze():
    
    main_char_path = hou.pwd().parm("main_char").eval()
    npc1_char_path = hou.pwd().parm("npc_1").eval()
    
    #start_pos = (0, 3)
    #target_pos = (6, 1)
    start_pos = position_object(obj_path=npc1_char_path, row=0, col=3)
    target_pos = position_object(obj_path=main_char_path, row=6, col=1)
    
    maze1 = get_maze_from_grid()
    print("")
    for row in maze1:
        print(row)
   
    
    pathfinder = AStarPathfinding(maze1, start_pos, target_pos)
    path = pathfinder.find_path()
    
    if path:
        print("Path found:", path)
    else:
        print("No path found.")

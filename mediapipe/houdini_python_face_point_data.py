import json
import hou
# Path to your JSON file
json_file = "/Users/felipepesantez/development/ml/rebelwayAppliedML/mediapipe/face_landmarks.json"

with open(json_file, "r") as f:
    data = json.load(f)

geo = hou.pwd().geometry()

for entry in data[0]:
    pt = geo.createPoint()
    pt.setPosition((entry['x'], entry['y'], entry['z']))

points = geo.points()

current_frame = int(hou.frame()) - 1

if current_frame < len(data):
    for i in range(len(data[current_frame])):
        pt = points[i]
        pos_val = data[current_frame][i]
        pt.setAttribValue("P", hou.Vector3(pos_val['x'], pos_val['y'], pos_val['z']))
import bpy
import json
import os

output_file = "/Users/felipepesantez/development/ml/rebelwayAppliedML/blender_data/animation_data.json"

armature = bpy.context.object
if armature.type != 'ARMATURE':
    raise Exception('Selected object is not an armature')

scene = bpy.context.scene
frame_start = scene.frame_start
frame_end = scene.frame_end

bone_data = []

for frame in range(frame_start, frame_end + 1):
    scene.frame_set(frame)

    frame_data = {'frame': frame, 'bones': {}}

    for bone in armature.pose.bones:
        location = bone.location.copy()
        rotation = bone.rotation_quaternion.copy()

        frame_data['bones'][bone.name] = {
            'location': [location.x, location.y, location.z],
            'rotation': [rotation.w, rotation.x, rotation.y, rotation.z]
        }

    bone_data.append(frame_data)

with open(output_file, 'w') as file:
    json.dump(bone_data, file, indent=4)

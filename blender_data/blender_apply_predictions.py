import bpy
import json
from mathutils import Vector, Quaternion

with open('/Users/felipepesantez/development/ml/rebelwayAppliedML/blender_data/predicted_future_frames.json', 'r') as f:
    predicted_frames = json.load(f)

armature = bpy.data.objects['Armature']

bpy.context.scene.frame_set(243)

for frame_data in predicted_frames:
    frame_number = frame_data['frame']

    bpy.context.scene.frame_set(frame_number)

    for bone_name, bone_data in frame_data['bones'].items():
        if bone_name in armature.pose.bones:
            bone = armature.pose.bones[bone_name]


            bone.location = Vector(bone_data['location'])

            bone.rotation_quaternion = Quaternion(bone_data['rotation'])

            bone.keyframe_insert(data_path="location", frame=frame_number)
            bone.keyframe_insert(data_path="rotation_quaternion", frame=frame_number)

bpy.context.scene.frame_end = frame_number
bpy.context.view_layer.update()


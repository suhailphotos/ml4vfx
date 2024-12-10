import json
import numpy as np
from scipy.spatial.transform import Rotation as R

def normalize_position(position, mean_position, std_position):
    return (position - mean_position) / std_position

def normalize_rotation(quaternion):
    return quaternion / np.linalg.norm(quaternion)

with open('animation_data.json') as f:
    animation_data = json.load(f)

all_frames = []
bone_names = list(animation_data[0]['bones'].keys())

all_positions = []
for frame_data in animation_data:
    for bone_name in bone_names:
        all_positions.append(frame_data['bones'][bone_name]['location'])

all_positions = np.array(all_positions)
mean_position = np.mean(all_positions, axis=0)
std_position = np.std(all_positions, axis=0)

std_position[std_position == 0] = 1

for frame_data in animation_data:
    frame_info = []
    for bone_name  in bone_names:
        bone_data = frame_data['bones'][bone_name]
        position = np.array(bone_data['location'])
        rotation = np.array(bone_data['rotation'])

        normalized_position = normalize_position(position, mean_position, std_position)
        normalized_rotation = normalize_rotation(rotation)
        bone_vector = np.concatenate([normalized_position, normalized_rotation])
        frame_info.extend(bone_vector)

    all_frames.append(frame_info)

all_frames = np.array(all_frames)

np.save("all_frames_normalized.npy", all_frames)
np.save("bone_names.npy", np.array(bone_names))
np.save("normalization_params.npy", {'mean_position': mean_position, 'std_position': std_position})

print("Data prepared and saved")

    
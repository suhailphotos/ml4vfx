import json
import numpy as np
import tensorflow as tf
from rnn_model import create_rnn_model

# Load the normalized data and normalization parameters
all_frames_normalized = np.load('all_frames_normalized.npy')
bone_names = np.load('bone_names.npy')
normalization_params = np.load('normalization_params.npy', allow_pickle=True).item()

# Recreate the model architecture
sequence_length = 10
num_bones = len(bone_names)
features_per_bone = all_frames_normalized.shape[1] // num_bones

num_predictions = 10
model = create_rnn_model(sequence_length, num_bones, features_per_bone, num_future_frames=num_predictions)

# Load the weights from the saved model
model.load_weights('rnn_animation_predictor.h5')

# Prepare input sequences
X = []
for i in range(len(all_frames_normalized) - sequence_length):
    X.append(all_frames_normalized[i:i + sequence_length])
X = np.array(X)

# Predict future frames
input_sequence = X[-1:]  
predicted_frames = []

for _ in range(num_predictions):
    prediction = model.predict(input_sequence)
    print(prediction)
    predicted_frame = prediction[0, -1]  

    predicted_frames.append(predicted_frame)

    # Update input_sequence for the next prediction
    input_sequence = np.roll(input_sequence, -1, axis=1)
    input_sequence[0, -1] = predicted_frame

predicted_frames = np.array(predicted_frames)

# Denormalize the predictions
mean_position = normalization_params['mean_position']
std_position = normalization_params['std_position']

def denormalize_position(normalized_position):
    return normalized_position * std_position + mean_position

def denormalize_rotation(normalized_quaternion):
    return normalized_quaternion / np.linalg.norm(normalized_quaternion)

# Convert predictions to JSON format
last_known_frame = len(all_frames_normalized)
predicted_json = []
for i, frame in enumerate(predicted_frames):
    frame_dict = {"frame": last_known_frame + i + 1, "bones": {}}
    for j, bone_name in enumerate(bone_names):
        start_idx = j * 7
        #print(frame[start_idx: start_idx + 3])
        position = denormalize_position(frame[start_idx:start_idx + 3]).tolist()
        rotation = denormalize_rotation(frame[start_idx + 3:start_idx + 7]).tolist()
        frame_dict["bones"][bone_name] = {"location": position, "rotation": rotation}
    predicted_json.append(frame_dict)

# Save the predicted frames to a JSON file
with open('predicted_future_frames.json', 'w') as f:
    json.dump(predicted_json, f, indent=4)

print("Predictions saved to predicted_future_frames.json")
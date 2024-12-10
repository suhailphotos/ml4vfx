import numpy as np
import tensorflow as tf
from tensorflow.keras import layers

def create_rnn_model(sequence_length, num_bones, features_per_bone, num_future_frames=1, rnn_units=512):
    input_shape = (sequence_length, num_bones * features_per_bone)
    input_layer = layers.Input(shape=input_shape)

    x = layers.LSTM(rnn_units, return_sequences=True)(input_layer)
    x = layers.LSTM(rnn_units, return_sequences=True)(x)

    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dropout(0.1)(x)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dropout(0.1)(x)

    output = layers.Dense(num_bones * features_per_bone)(x[:, -1, :])
    output = layers.RepeatVector(num_future_frames)(output)

    model = tf.keras.Model(inputs=input_layer, outputs=output)
    model.compile(optimizer='adam', loss='mse')

    return model

if __name__ == "__main__":

    #load the data
    all_frames_normalized = np.load("all_frames_normalized.npy")
    bone_names = np.load("bone_names.npy")
    normalization_params = np.load("normalization_params.npy", allow_pickle=True).item()

    sequence_length = 10
    num_bones = len(bone_names)
    features_per_bone = all_frames_normalized.shape[1] // num_bones

    num_future_frames = 10

    X = []
    y = []

    for i in range(len(all_frames_normalized) - sequence_length - num_future_frames + 1):
        X.append(all_frames_normalized[i:i + sequence_length])
        y.append(all_frames_normalized[i + sequence_length: i + sequence_length + num_future_frames])

    X = np.array(X)
    y = np.array(y)

    print("Shape of X: ", X.shape)
    print("Shape of y: ", y.shape)


    model = create_rnn_model(sequence_length, num_bones, features_per_bone, num_future_frames=num_future_frames)
    model.summary()

    early_stopping = tf.keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)
    lr_scheduler = tf.keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=0.5)

    history = model.fit(
        X, y, 
        epochs=100,
        batch_size=32,
        validation_split=0.2,
        #callbacks=[early_stopping, lr_scheduler]
    )

    model.save("rnn_animation_predictor.h5")
    print("Model saved!!")

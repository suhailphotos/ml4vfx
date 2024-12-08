import cv2
import json
import numpy as np
import mediapipe as mp

source = "/Users/felipepesantez/Movies/inference/face2.mp4"

cap = cv2.VideoCapture(source)

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
drawSpec1 = mpDraw.DrawingSpec(color=(0,255,0), thickness=1, circle_radius=2)
drawSpec2 = mpDraw.DrawingSpec(color=(0,0,255), thickness=1, circle_radius=2)


landmarks_data = []

while cap.isOpened():

    ret, img = cap.read()

    if ret:
        scale_val = 0.8
        x1 = int(img.shape[1] * scale_val)
        x2 = int(img.shape[0] * scale_val)
        img = cv2.resize(img, (x1, x2))

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        detections = faceMesh.process(imgRGB)

        if detections.multi_face_landmarks:
            face_landmark = detections.multi_face_landmarks[0]
            frame_landmarks = []

            for landmark in face_landmark.landmark:
                frame_landmarks.append({
                    "x": landmark.x,
                    "y": landmark.y,
                    "z": landmark.z
                })

            landmarks_data.append(frame_landmarks) 
            
            mpDraw.draw_landmarks(img, face_landmark, mpFaceMesh.FACEMESH_CONTOURS, drawSpec1, drawSpec2)

        cv2.imshow("Face Mesh", img)

        if cv2.waitKey(1) == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()

output_file = "face_landmarks.json"

with open(output_file, "w") as f:
    json.dump(landmarks_data, f, indent=4)

print("Landmarks saved")

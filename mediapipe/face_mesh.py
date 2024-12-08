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
            for face_landmark in detections.multi_face_landmarks:
                print(face_landmark)
                mpDraw.draw_landmarks(img, face_landmark, mpFaceMesh.FACEMESH_CONTOURS, drawSpec1, drawSpec2)

        cv2.imshow("Face Mesh", img)

        if cv2.waitKey(1) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()


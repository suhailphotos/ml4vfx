import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import time

model = YOLO("yolov8s.pt")

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        colorsBGR = [x, y]
        print(colorsBGR)

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

cap = cv2.VideoCapture('carpark.mp4')

coco_classes = open('coco.txt', 'r')
data = coco_classes.read()
class_list = data.split('\n')

ret, frame = cap.read()
width, height = frame.shape[1], frame.shape[0]

area = [(width - 600, 300), (width - 540, 450), (width - 400, 450), (width - 460, 300)]

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(frame)
    a = results[0].boxes.data
    px = pd.DataFrame(a.cpu()).astype('float')

    area_list = []

    for index,row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
        c = class_list[d]
        if 'car' in c:
            cx = int(x1 + x2) //2
            cy = int(y1+y2) // 2

            results_area = cv2.pointPolygonTest(np.array(area, np.int32), ((cx, cy)), False)
            if results_area == 1:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.circle(frame, (cx, cy), 3, (0, 0, 255), -1)
                area_list.append(c)

    al = (len(area_list))

    if al == 1:
        cv2.polylines(frame, [np.array(area, np.int32)], True, (0, 0, 255), 2)
    else:
        cv2.polylines(frame, [np.array(area, np.int32)], True, (0, 255, 0), 2)

    cv2.imshow('RGB', frame)

    if cv2.waitKey(20) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
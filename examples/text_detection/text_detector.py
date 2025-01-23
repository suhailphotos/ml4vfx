import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np

image_path = "last.jpg"

img = cv2.imread(image_path)

reader = easyocr.Reader(['en'], gpu=False)

result = reader.readtext(img)

threshold = 0.25

for i, t in enumerate(result):
    print(t)
    bbox, text, score = t

    if score > threshold:
        start_point = tuple(map(int, bbox[0]))
        end_point = tuple(map(int, bbox[2]))
        cv2.rectangle(img, start_point, end_point, (0, 255, 0), 2)
        cv2.putText(img, text, start_point, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()

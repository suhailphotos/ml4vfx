import cv2
import mediapipe as mp
import numpy as np

class FaceDetector:
    def __init__(self, minimumDetectionConfidence=0.5):
        self.minDectCon = minimumDetectionConfidence
        self.draw_mp = mp.solutions.drawing_utils
        self.faceDetection = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=self.minDectCon)

    def findFaces(self, img, draw=True):
        img.flags.writeable = False
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.detection_results = self.faceDetection.process(image)

        detections = []
        img.flags.writeable = True

        if self.detection_results.detections:
            for id, detection in enumerate(self.detection_results.detections):
                bbox_data = detection.location_data.relative_bounding_box
                h, w, c = img.shape
                bbox = int(bbox_data.xmin * w), int(bbox_data.ymin * h), int(bbox_data.width * w), int(bbox_data.height * h)

                detections.append([id, bbox, detection.score])

                if draw:
                    img = self.drawShapes(img, bbox)
                    cv2.putText(img, f'{int(detection.score[0] * 100)}%', (bbox[0], bbox[1]), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)

        return img, detections


    def drawShapes(self, img, bbox):
        x, y, w, h = bbox

        cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0),2)

        return img


def main():
    video_path = 0
    cap = cv2.VideoCapture(video_path)
    detector = FaceDetector()

    while cap.isOpened():
        ret, img = cap.read()

        if ret:
            img, bbox = detector.findFaces(img)
            cv2.imshow("Faces", cv2.flip(img,1))
            if cv2.waitKey(1) == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()


import cv2
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50

model = torch.hub.load("intel-isl/MiDaS", "MiDaS_small")

model.eval()
device = torch.device("mps")
model.to(device)

transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((384,384)),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

source = "/Users/felipepesantez/Movies/inference/face2.mp4"
cap = cv2.VideoCapture(source)

if not cap.isOpened():
    print("Error reading source video")
    exit()

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Error reading frame")
        break

    input_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    input_image = transform(input_image).unsqueeze(0).to(device)

    #depth estimation
    with torch.no_grad():
        depth_map = model(input_image)

    frame_height, frame_width = frame.shape[:2]
    depth_map = depth_map.squeeze().cpu().numpy()
    depth_map = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    depth_map = cv2.resize(depth_map, (frame_width, frame_height))

    cv2.imshow("Depth Map", depth_map)
    cv2.imshow("Feed", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



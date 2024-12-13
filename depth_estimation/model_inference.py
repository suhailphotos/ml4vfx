import os
import pandas as pd
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import torch.nn as nn
import torch.optim as optim
from prepare_data import NYUDepthDataset, NYUDepthTransform
import matplotlib.pyplot as plt
from model_build import DepthEstimationModel

device = "cuda" if torch.cuda.is_available() else "cpu"

# class DepthEstimationModel(nn.Module):
#     def __init__(self):
#         super(DepthEstimationModel, self).__init__()

#         self.encoder = nn.Sequential(
#             nn.Conv2d(3, 64, kernel_size=3, padding=1),
#             nn.ReLU(),
#             nn.MaxPool2d(2),  # 224 -> 112
#             nn.Conv2d(64, 128, kernel_size=3, padding=1),
#             nn.ReLU(),
#             nn.MaxPool2d(2),  # 112 -> 56
#             nn.Conv2d(128, 256, kernel_size=3, padding=1),
#             nn.ReLU(),
#             nn.MaxPool2d(2),  # 56 -> 28
#         )

#         self.decoder = nn.Sequential(
#             nn.ConvTranspose2d(256, 128, kernel_size=4, stride=2, padding=1),  # 28 -> 56
#             nn.ReLU(),
#             nn.ConvTranspose2d(128, 64, kernel_size=4, stride=2, padding=1),   # 56 -> 112
#             nn.ReLU(),
#             nn.ConvTranspose2d(64, 1, kernel_size=4, stride=2, padding=1),     # 112 -> 224
#             nn.Sigmoid(),  # To normalize depth output to [0, 1]
#         )

#     def forward(self, x):
#         x = self.encoder(x)
#         x = self.decoder(x)
#         return x


model = DepthEstimationModel()
model.load_state_dict(torch.load("depth_estimation_model.pth" , weights_only=True))
model.to(device)

def predict_depth(model, image_path, transform, output_path="predicted_depth.png"):
    model.eval()

    image = Image.open(image_path).convert("RGB")
    
    # Apply only the image transformations, not the depth transformations
    input_tensor = transform.img_transform(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        predicted_depth = model(input_tensor)
        predicted_depth = predicted_depth.squeeze().cpu().numpy()
    
    plt.imsave(output_path, predicted_depth, cmap="gray")
    print(f"Predicted depth saved to {output_path}")

image_path = "./00000_colors.png"
predict_depth(model, image_path, NYUDepthTransform())
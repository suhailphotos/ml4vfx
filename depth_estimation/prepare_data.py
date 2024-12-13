import os
import pandas as pd
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

class NYUDepthDataset(Dataset):
    def __init__(self, csv_file, transform=None):
        self.data = pd.read_csv(csv_file)
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_path = self.data.iloc[idx, 0]
        depth_path = self.data.iloc[idx, 1]

        image = Image.open(img_path).convert("RGB")  
        depth = Image.open(depth_path).convert("L")  

        sample = {"image": image, "depth": depth}

        if self.transform:
            sample = self.transform(sample)

        return sample


class NYUDepthTransform:
    def __init__(self, img_size=(224, 224)):
        self.img_transform = transforms.Compose([
            transforms.Resize(img_size),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  
        ])
        self.depth_transform = transforms.Compose([
            transforms.Resize(img_size),
            transforms.ToTensor()
        ])

    def __call__(self, sample):
        image = self.img_transform(sample["image"])
        depth = self.depth_transform(sample["depth"])
        return {"image": image, "depth": depth}
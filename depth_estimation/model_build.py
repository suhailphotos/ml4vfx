import torch
import torch.nn as nn
import torch.optim as optim
from prepare_data import NYUDepthDataset, NYUDepthTransform
from torch.utils.data import DataLoader

# Paths to the CSV files
train_csv_path = "data/nyu2_train.csv"
test_csv_path = "data/nyu2_test.csv"

# Dataset and DataLoader for training
train_dataset = NYUDepthDataset(csv_file=train_csv_path, transform=NYUDepthTransform())
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)

# Dataset and DataLoader for testing
test_dataset = NYUDepthDataset(csv_file=test_csv_path, transform=NYUDepthTransform())
test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

class DepthEstimationModel(nn.Module):
    def __init__(self):
        super(DepthEstimationModel, self).__init__()

        # Encoder (down-sampling)
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),  # 224 -> 112
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),  # 112 -> 56
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),  # 56 -> 28
        )

        # Decoder (up-sampling)
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(256, 128, kernel_size=4, stride=2, padding=1),  # 28 -> 56
            nn.ReLU(),
            nn.ConvTranspose2d(128, 64, kernel_size=4, stride=2, padding=1),   # 56 -> 112
            nn.ReLU(),
            nn.ConvTranspose2d(64, 1, kernel_size=4, stride=2, padding=1),     # 112 -> 224
            nn.Sigmoid(),  # To normalize depth output to [0, 1]
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

if __name__ == "__main__":
    criterion = nn.MSELoss()

    model = DepthEstimationModel().to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    num_epochs = 5

    for epoch in range(num_epochs):
        model.train()
        train_loss = 0
        for batch in train_loader:
            images = batch["image"].to(device)
            depths = batch["depth"].to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, depths)
            loss.backward()
            optimizer.step()

            train_loss += loss.item()

        train_loss /= len(train_loader)
        print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {train_loss:.4f}")
   
        model.eval()
        test_loss = 0
        with torch.no_grad():
            for batch in test_loader:
                images = batch["image"].to(device)
                depths = batch["depth"].to(device)

                outputs = model(images)
                loss = criterion(outputs, depths)
                test_loss += loss.item()

        test_loss /= len(test_loader)
        print(f"Test Loss: {test_loss:.4f}")

    torch.save(model.state_dict(), "depth_estimation_model.pth")
    print("Model saved as depth_estimation_model.pth")

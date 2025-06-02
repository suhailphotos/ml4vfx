from pathlib import Path
import torch, torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from src.model import Net

BATCH   = 64
EPOCHS  = 8
DEVICE  = torch.device("cuda" if torch.cuda.is_available() else "cpu")
ROOT    = Path(__file__).resolve().parents[1]   
MODEL_F = ROOT / "models" / "fashion_mnist.pt"

def main() -> None:
    # 1 · data
    train_ds = datasets.FashionMNIST(
        root=ROOT / "data", train=True, download=True,
        transform=transforms.Compose([
            transforms.RandomRotation(10),
            transforms.RandomAffine(0, translate=(.1,.1)),
            transforms.ToTensor()])
    )
    test_ds  = datasets.FashionMNIST(
        root=ROOT / "data", train=False, download=True,
        transform=transforms.ToTensor()
    )
    train_dl = DataLoader(train_ds, batch_size=BATCH, shuffle=True)
    test_dl  = DataLoader(test_ds , batch_size=BATCH)

    # 2 · model
    model = Net().to(DEVICE)
    loss_fn  = nn.CrossEntropyLoss()
    opt      = torch.optim.Adam(model.parameters(), 1e-3)
    sched    = torch.optim.lr_scheduler.ReduceLROnPlateau(opt, "min", patience=2)

    for epoch in range(EPOCHS):
        model.train()
        for X,y in train_dl:
            X,y = X.to(DEVICE), y.to(DEVICE)
            opt.zero_grad()
            loss_fn(model(X), y).backward()
            opt.step()
        # quick val
        model.eval(); correct=0; total=0; val_loss=0
        with torch.no_grad():
            for X,y in test_dl:
                X,y = X.to(DEVICE), y.to(DEVICE)
                out = model(X)
                val_loss += loss_fn(out,y).item()
                correct += (out.argmax(1)==y).sum().item()
                total   += y.size(0)
        sched.step(val_loss/len(test_dl))
        acc = 100*correct/total
        print(f"Epoch {epoch+1}: acc={acc:5.2f}% loss={val_loss/len(test_dl):.4f}")

    MODEL_F.parent.mkdir(exist_ok=True)
    torch.save(model.state_dict(), MODEL_F)
    print(f"Saved weights → {MODEL_F}")

if __name__ == "__main__":
    main()

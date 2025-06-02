from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import io, torch
from PIL import Image
from torchvision import transforms
from pathlib import Path
from src.model import Net        # reuse code

ROOT      = Path(__file__).resolve().parents[1]
MODEL_F   = ROOT / "models" / "fashion_mnist.pt"
DEVICE    = torch.device("cuda" if torch.cuda.is_available() else "cpu")
LABELS    = ["T-shirt/top","Trouser","Pullover","Dress","Coat",
             "Sandal","Shirt","Sneaker","Bag","Ankle boot"]

app = FastAPI(title="fashion-mnist-api")

# load once at startup
model = Net().to(DEVICE)
model.load_state_dict(torch.load(MODEL_F, map_location=DEVICE))
model.eval()

transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((28,28)),
    transforms.ToTensor()
])

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if file.content_type not in ("image/png","image/jpeg"):
        raise HTTPException(415, "Only png or jpeg accepted")
    img_bytes = await file.read()
    img = Image.open(io.BytesIO(img_bytes)).convert("L")
    x   = transform(img).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        logits = model(x)
    idx      = int(logits.argmax(1).item())
    return JSONResponse({"class_id": idx, "label": LABELS[idx]})

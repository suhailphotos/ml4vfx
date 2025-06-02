import numpy as np
from pathlib import Path
from keras.datasets import fashion_mnist
from PIL import Image

# User input: number of images to save
num_images = 50  # Change this to your desired number
ROOT = Path(__file__).resolve().parents[1]

# Output directory
output_dir = ROOT / "data" / "samples"
output_dir.mkdir(parents=True, exist_ok=True)

# Load Fashion-MNIST data
(_, _), (x_test, _) = fashion_mnist.load_data()

# Randomly select indices
indices = np.random.choice(x_test.shape[0], size=num_images, replace=False)

for i, idx in enumerate(indices):
    img_array = x_test[idx]  # shape (28, 28), dtype=uint8
    img = Image.fromarray(img_array)
    img.save(output_dir / f"sample_{i+1}.png")

print(f"Saved {num_images} images to '{output_dir}' directory.")



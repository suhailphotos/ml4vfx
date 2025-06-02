# FashionMNIST + Houdini Integration via Docker API

Welcome to the **FashionMNIST + Houdini Integration** project — a small-scale, production-style demonstration of machine learning inference inside Houdini, powered by a containerized FastAPI backend. This repository showcases how to bridge procedural tools with modern ML workflows across a local network.

---

## Project Objective

While the model used here is a basic 28x28 FashionMNIST classifier (the "Hello World" of ML), the core goal of this project is to simulate a **real-world deployment setup**. This includes:

* Training and serving an ML model via a **FastAPI** app.
* Hosting the model inside a **GPU-enabled Docker container**.
* **Calling the model from Houdini** (running on a separate macOS client) through a REST API across a local network.

This project was part of a course assignment, but its architecture reflects scalable and modular design patterns found in professional environments.

---

## Features

* PyTorch model trained on the FashionMNIST dataset
* Dockerized FastAPI server with GPU support
* Seamless integration with **SideFX Houdini** for inference
* Automatic Houdini SOP-to-image conversion and prediction
* Prebuilt Docker image available via Docker Hub

---

## Folder Structure

```
fashionMNIST/
├── api/                # FastAPI app serving predictions
├── data/               # Downloaded dataset and extracted sample images
├── docker/             # Dockerfile and docker-compose.yml
├── env/                # Conda environment definition
├── hda/                # Houdini Digital Asset and client prediction scripts
├── models/             # Trained model (.pt file)
├── src/                # Model definition, training, and image export scripts
├── README.md           # This file
├── LICENSE             # MIT License
```

---

## How It Works

### 1. Model Training (`src/train.py`)

Trains a simple fully connected neural network on the FashionMNIST dataset. Model weights are saved to `models/fashion_mnist.pt`.

### 2. API Serving (`api/main.py`)

The FastAPI app loads the trained model and exposes a `/predict` endpoint, accepting PNG or JPEG images and returning the predicted class label.

### 3. Dockerized Deployment (`docker/Dockerfile`, `docker-compose.yml`)

The API is packaged inside a Docker container with GPU support. Once deployed, it runs on port `8000` and can serve prediction requests across the network.

### 4. Houdini Client Integration

* `hda/gridims.h`: VEX script used in an Attribute Wrangle SOP to calculate grid dimensions
* `hda/pythonsop.py`: Python SOP script that calls `predict_from_grid()`
* `hda/predictor.py`: Reads color data, builds image, and sends it to the API for prediction

---

## Getting Started

### Set Up Local Environment (optional)

```bash
conda env create -f env/conda.yaml
conda activate fashionmnist
```

### Run API via Docker

```bash
cd docker
docker-compose up -d
```

Make sure the server is reachable at: `http://<your-server-ip>:8000/predict`

### Houdini Setup

* Load the `fashion_mnist.hipnc` file.
* Use the provided HDA in your SOP network.
* Make sure to run `gridims.h` in an Attribute Wrangle and follow it with `pythonsop.py` inside a Python SOP.
* Set the `FASHION_API_URL` environment variable in Houdini to match your server IP.

---

## Scripts Overview

| Script             | Description                                 |
| ------------------ | ------------------------------------------- |
| `src/train.py`     | Trains the PyTorch model                    |
| `src/model.py`     | Neural network architecture                 |
| `src/extImages.py` | Extracts sample PNGs from test set          |
| `api/main.py`      | FastAPI app for prediction                  |
| `hda/gridims.h`    | VEX script to calculate grid layout         |
| `hda/pythonsop.py` | Houdini Python SOP wrapper for inference    |
| `hda/predictor.py` | Core function for exporting SOPs to the API |

---

## Docker Image

A prebuilt image is available:

```
docker pull suhailphotos/fashion-mnist-api:1.0.0
```

Run it manually with:

```bash
docker run --rm -it \
  -v $(pwd)/models:/app/models:ro \
  -v $(pwd)/data:/app/data:ro \
  -p 8000:8000 \
  --gpus all \
  suhailphotos/fashion-mnist-api:1.0.0
```

---

## Demo Video

Watch the full walkthrough:
**[YouTube: FashionMNIST Inference from Houdini](https://youtu.be/yChNWctqAac)**

---

## TL;DR

* Trained a simple FashionMNIST model.
* Served predictions via FastAPI inside Docker (with GPU).
* Called prediction from Houdini via SOP grid-to-image logic.
* Shared project as a mock production pipeline.

You’re welcome to fork, experiment, or integrate this workflow into your own creative tools.

---

## License

MIT License — see `LICENSE` file for details.

---

## Acknowledgements

* [Fashion MNIST](https://github.com/zalandoresearch/fashion-mnist) — by Zalando Research
* [SideFX Houdini](https://www.sidefx.com/)
* [PyTorch](https://pytorch.org/)
* [FastAPI](https://fastapi.tiangolo.com/)


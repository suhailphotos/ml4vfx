# FashionMNIST + Houdini Integration via Docker API

This project started as a course assignment, but I wanted to take it a bit further and simulate what a small-scale, production-like setup might look like for integrating machine learning with Houdini. Instead of just training a model and calling it a day, I’ve built out a complete workflow that includes a FastAPI server running inside a Docker container (with GPU support), and Houdini acting as the client that sends image data and gets predictions back—all over a local network.

The model itself is simple (just FashionMNIST), but the architecture is meant to reflect how something like this could be extended or used in a real-world scenario.

---

## Project Objective

While this is based on the "Hello World" of machine learning (FashionMNIST), the real focus is on demonstrating how to:

* Train and serve a model using **FastAPI**
* Package and deploy it inside a **GPU-enabled Docker container**
* Use **Houdini as a remote client** to request predictions
* Set everything up in a way that mimics a lightweight production environment

---

## Features

* PyTorch model trained on the FashionMNIST dataset
* FastAPI-based prediction server running in Docker
* Houdini integration via Python SOP and Attribute Wrangle
* Tested locally across a Mac (Houdini) and Linux (Docker server)
* Prebuilt Docker image available for quick deployment

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

Trains a simple fully connected neural network on the FashionMNIST dataset and saves the weights to `models/fashion_mnist.pt`.

### 2. API Serving (`api/main.py`)

Starts a FastAPI app with a `/predict` endpoint. It accepts PNG or JPEG images and returns a class prediction.

### 3. Dockerized Deployment (`docker/Dockerfile`, `docker-compose.yml`)

Everything’s wrapped inside a Docker image that supports GPU acceleration. You can build and run the server with Docker Compose.

### 4. Houdini Client Integration

* `hda/gridims.h`: Attribute Wrangle code that calculates grid dimensions
* `hda/pythonsop.py`: Python SOP that runs the inference call
* `hda/predictor.py`: Handles rasterizing the grid and calling the API

The result is a procedural SOP network that can send a grid of color data to the API and receive a prediction label as a global attribute.

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

Check that the server is running at `http://<your-server-ip>:8000/predict`

### Houdini Setup

* Open `fashion_mnist.hipnc`
* Add the HDA into your network
* Run `gridims.h` in an Attribute Wrangle SOP
* Run `pythonsop.py` in a Python SOP (or use the provided setup)
* Make sure the `FASHION_API_URL` environment variable is pointing to your server

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

You can pull the prebuilt image from Docker Hub:

```
docker pull suhailphotos/fashion-mnist-api:1.0.0
```

Or run it manually like this:

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

Check out the walkthrough video with commentary:
**[YouTube: FashionMNIST Inference from Houdini](https://youtu.be/yChNWctqAac)**

---

## TL;DR

* Train a FashionMNIST model
* Serve it via FastAPI inside Docker (with GPU support)
* Use Houdini as a client to request predictions from procedural color data
* Mimic a basic production pipeline with local-network setup

---

## License

MIT License — see `LICENSE` file

---

## Acknowledgements

* [Fashion MNIST](https://github.com/zalandoresearch/fashion-mnist) — Zalando Research
* [SideFX Houdini](https://www.sidefx.com/)
* [PyTorch](https://pytorch.org/)
* [FastAPI](https://fastapi.tiangolo.com/)


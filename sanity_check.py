# save this as sanity_check.py  (or just paste into a fresh Jupyter cell)

import os, sys, importlib, warnings
warnings.filterwarnings("ignore")

def section(title):
    print(f"\n\033[1m{title}\033[0m".ljust(60, "─"))

# -------------------------------------------------------------------
section("System & CUDA runtime")
import subprocess, platform
print("Python   :", sys.version.split()[0])
print("Platform :", platform.platform())
try:
    nvcc_v = subprocess.check_output(["nvcc", "--version"]).decode().split()[-1]
    print("nvcc     :", nvcc_v)
except Exception:
    print("nvcc     : (not installed, fine)")

# -------------------------------------------------------------------
section("PyTorch")
import torch
print("PyTorch  :", torch.__version__)
print("GPU avail:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("CUDA dev :", torch.cuda.get_device_name(0))
    print("torch add:", (torch.tensor([1.]) + 1).item())

# -------------------------------------------------------------------
section("TensorFlow")
import tensorflow as tf
print("TF       :", tf.__version__)
gpus = tf.config.list_physical_devices("GPU")
print("TF GPUs  :", gpus)
if gpus:
    x = tf.constant([1.])
    print("tf add   :", (x + 1).numpy())

# -------------------------------------------------------------------
section("JAX")
import jax, jax.numpy as jnp
print("JAX      :", jax.__version__)
print("JAX devs :", jax.devices())
print("jax add  :", jnp.add(1, 1).item())

# -------------------------------------------------------------------
section("scikit-learn & SciPy stack")
import numpy as np, pandas as pd, scipy, sklearn
print("NumPy    :", np.__version__)
print("Pandas   :", pd.__version__)
print("SciPy    :", scipy.__version__)
print("sklearn  :", sklearn.__version__)
print("sklearn 1+1:", sklearn.utils.validation.check_array([[1,1]]).sum())

# -------------------------------------------------------------------
section("Computer-Vision / 3D")
import cv2, open3d as o3d, trimesh
print("OpenCV   :", cv2.__version__)
print("Open3D   :", o3d.__version__)
print("Trimesh  :", trimesh.__version__)
print("cv2 add  :", cv2.add(np.array([1]), np.array([1]))[0])

# -------------------------------------------------------------------
section("NLP / Transformers")
from transformers import AutoTokenizer
print("transformers :", importlib.metadata.version('transformers'))
tok = AutoTokenizer.from_pretrained("bert-base-uncased", trust_remote_code=True)
print("Tokenizer OK :", tok("hello world")["input_ids"][:5])

# -------------------------------------------------------------------
section("Reinforcement-Learning")
import gymnasium as gym
import stable_baselines3 as sb3
print("gymnasium      :", gym.__version__)
print("stable-baselines3:", sb3.__version__)
env = gym.make("CartPole-v1")
obs, _ = env.reset(seed=0)
print("gym obs shape  :", obs.shape)

# -------------------------------------------------------------------
section("API & dashboard libs")
import fastapi, uvicorn, streamlit
print("FastAPI  :", fastapi.__version__)
print("Uvicorn  :", uvicorn.__version__)
print("Streamlit:", streamlit.__version__)

print("\n\033[92mAll imports succeeded — environment looks healthy!\033[0m")

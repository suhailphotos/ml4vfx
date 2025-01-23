import torch
from pathlib import Path

def save_model(model, target_dir, model_name):
    target_dir_path = Path(target_dir)
    target_dir_path.mkdir(parents=True, exist_ok=True)

    assert model_name.endswith(".pth") or model_name.endswith(".pt"), "model_name should end with '.pth' or '.pt'"
    
    model_path = target_dir_path / model_name
    torch.save(model.state_dict(), model_path)
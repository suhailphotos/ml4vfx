# Fashion MNIST + Houdini Integration

Welcome to the `fasionMNIST` worktree! This project demonstrates the application of machine learning using the Fashion MNIST dataset, with a unique focus on integrating the results into Houdini for creative and technical workflows.

---

## Project Overview

- **Train machine learning models** on the Fashion MNIST dataset, exploring different neural network architectures and training strategies.
- **Visualize and analyze results** using standard ML tools and custom scripts.
- **Bridge the gap between ML and 3D/VFX** by exporting model outputs to Houdini, enabling novel creative possibilities for artists and technical directors.

---

## Key Features

- Self-contained codebase for end-to-end experimentation with Fashion MNIST.
- Modular Python scripts and/or Jupyter notebooks for:
    - Data loading and preprocessing
    - Model definition and training
    - Evaluation and visualization
    - Exporting predictions or features for Houdini
    - *(Planned)* Python tools for automating Houdini integration (e.g., loading predictions into SOPs, driving procedural assets, etc.)

---

## Usage

1. Clone the repository and add this worktree (see `How to Use Git Worktrees.md` in the root for details)
2. Set up your environment (see `environment.yml` or `requirements.txt` if provided)
3. Explore the notebooks and scripts
4. Run the ML training and export results
5. Open Houdini and use the provided scripts/tools to import and visualize results

---

## Folder Structure (Typical)

```
fasionMNIST/
├── notebooks/            # Jupyter notebooks for experiments
├── scripts/              # Standalone Python scripts
├── houdini_tools/        # Scripts/tools for Houdini integration
├── data/                 # (optional) Data management scripts or sample datasets
├── README.md             # This file
└── environment.yml       # (or requirements.txt) for dependencies
```

---

## Goals & Vision

- Provide a **practical ML showcase** using an industry-standard dataset
- Demonstrate **cross-disciplinary integration** by linking ML outputs with a professional 3D tool (Houdini)
- Serve as a **foundation** for future experiments in ML-driven VFX, procedural content, or technical art

---

## Credits

- **Fashion MNIST dataset:** https://github.com/zalandoresearch/fashion-mnist
- **Houdini:** https://www.sidefx.com/
- Additional credits as appropriate

---

*This worktree is intended as a portfolio-ready project for demonstrating machine learning, code organization, and Houdini pipeline integration.*


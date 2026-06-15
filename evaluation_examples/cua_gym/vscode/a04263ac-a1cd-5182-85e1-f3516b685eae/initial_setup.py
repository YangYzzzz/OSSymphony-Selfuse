"""
Initial Setup: Create ML project with requirements.txt, open in VSCode
Task ID: vscode_gf5_027
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_027'
PROJECT_DIR = f'{WORKDIR}/projects/ml-project'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # Create project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/data', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/notebooks', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)

    # requirements.txt
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write("""tensorflow==2.15.0
torch==2.1.2
pandas==2.1.4
jupyter==1.0.0
jupyterlab==4.0.9
numpy==1.26.2
scikit-learn==1.3.2
matplotlib==3.8.2
""")

    # README.md
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write("""# ML Project - Image Classification Pipeline

## Overview
This project implements a deep learning pipeline for image classification
using both TensorFlow and PyTorch backends. The pipeline supports training,
evaluation, and inference on custom datasets.

## Team
- Lead: Dr. Sarah Chen (ML Architecture)
- Engineer: Marcus Johnson (Data Pipeline)
- Engineer: Priya Sharma (Model Training)
- Engineer: Alex Rivera (Deployment)

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Place training data in `data/` directory
3. Run training: `python src/train.py`

## Structure
- `src/` - Source code for training and inference
- `data/` - Training and validation datasets
- `notebooks/` - Jupyter notebooks for exploration
""")

    # src/train.py - ML training script
    with open(f'{PROJECT_DIR}/src/train.py', 'w') as f:
        f.write("""#!/usr/bin/env python3
\"\"\"Training script for image classification model.\"\"\"

import os
import numpy as np
import pandas as pd
from pathlib import Path


def load_dataset(data_dir: str) -> tuple:
    \"\"\"Load and preprocess the training dataset.\"\"\"
    metadata = pd.read_csv(os.path.join(data_dir, 'metadata.csv'))
    print(f"Loaded {len(metadata)} samples from {data_dir}")
    return metadata


def train_model(epochs: int = 50, batch_size: int = 32, learning_rate: float = 0.001):
    \"\"\"Train the classification model.\"\"\"
    print(f"Training config: epochs={epochs}, batch_size={batch_size}, lr={learning_rate}")
    print("Starting training loop...")

    for epoch in range(epochs):
        train_loss = np.random.exponential(0.5) * (1.0 / (epoch + 1))
        val_acc = min(0.95, 0.5 + epoch * 0.01)
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}/{epochs} - loss: {train_loss:.4f} - val_acc: {val_acc:.4f}")

    print("Training complete!")


if __name__ == '__main__':
    train_model()
""")

    # src/__init__.py
    with open(f'{PROJECT_DIR}/src/__init__.py', 'w') as f:
        f.write("")

    # data/metadata.csv
    with open(f'{PROJECT_DIR}/data/metadata.csv', 'w') as f:
        f.write("""image_id,label,split,width,height
img_0001,cat,train,224,224
img_0002,dog,train,224,224
img_0003,bird,train,224,224
img_0004,cat,val,224,224
img_0005,dog,val,224,224
img_0006,bird,train,224,224
img_0007,cat,train,224,224
img_0008,dog,test,224,224
img_0009,bird,val,224,224
img_0010,cat,train,224,224
img_0011,dog,train,224,224
img_0012,bird,test,224,224
""")

    # notebooks/exploration.ipynb (simple notebook placeholder as plain text)
    with open(f'{PROJECT_DIR}/notebooks/exploration.ipynb', 'w') as f:
        import json
        notebook = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": ["# Data Exploration\\n", "\\n", "Initial exploration of the image classification dataset."]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": ["import pandas as pd\\n", "import matplotlib.pyplot as plt\\n", "\\n", "df = pd.read_csv('../data/metadata.csv')\\n", "print(df.describe())"]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "name": "python",
                    "version": "3.10.0"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 5
        }
        json.dump(notebook, f, indent=2)

    # .gitignore
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write("""__pycache__/
*.pyc
.env
data/raw/
*.egg-info/
dist/
build/
.ipynb_checkpoints/
wandb/
""")

    # Ensure NO .devcontainer directory exists (negative constraint)
    import shutil
    devcontainer_dir = f'{PROJECT_DIR}/.devcontainer'
    if os.path.exists(devcontainer_dir):
        shutil.rmtree(devcontainer_dir)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'Contents: {os.listdir(PROJECT_DIR)}')

    # GUI-ready: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

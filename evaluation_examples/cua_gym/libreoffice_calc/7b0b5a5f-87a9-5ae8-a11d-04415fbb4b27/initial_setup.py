"""
Initial Setup: Configure devcontainer for Python data science environment
Task ID: vscode_gf1_081
Domain: vscode (devcontainer configuration)

Creates a basic project structure with a minimal devcontainer.json and Dockerfile
that the agent must enhance with GPU support, resource limits, port forwarding, and sudo access.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf1_081'
PROJECT_DIR = f'{WORKDIR}/projects/data-science'
DEVCONTAINER_DIR = f'{PROJECT_DIR}/.devcontainer'


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
    os.makedirs(DEVCONTAINER_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/notebooks', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/data', exist_ok=True)

    # Create a minimal devcontainer.json (intentionally incomplete)
    # Missing: GPU args, memory limits, port forwarding, user config, Dockerfile build
    devcontainer = {
        "name": "Data Science Environment",
        "image": "python:3.11-slim"
    }

    devcontainer_path = f'{DEVCONTAINER_DIR}/devcontainer.json'
    with open(devcontainer_path, 'w') as f:
        json.dump(devcontainer, f, indent=4)
    print(f'Initial devcontainer.json created: {devcontainer_path}')

    # Create a basic Dockerfile (minimal, not yet configured for data science)
    dockerfile_path = f'{DEVCONTAINER_DIR}/Dockerfile'
    with open(dockerfile_path, 'w') as f:
        f.write('FROM python:3.11-slim\n\n')
        f.write('# Base Python image for development\n')
        f.write('RUN apt-get update && apt-get install -y --no-install-recommends \\\n')
        f.write('    git \\\n')
        f.write('    curl \\\n')
        f.write('    && rm -rf /var/lib/apt/lists/*\n')
    print(f'Initial Dockerfile created: {dockerfile_path}')

    # Create sample project files for realistic context
    # requirements.txt
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write('numpy>=1.24.0\n')
        f.write('pandas>=2.0.0\n')
        f.write('matplotlib>=3.7.0\n')
        f.write('scikit-learn>=1.3.0\n')
        f.write('seaborn>=0.12.0\n')

    # Sample notebook placeholder
    with open(f'{PROJECT_DIR}/notebooks/exploration.ipynb', 'w') as f:
        notebook = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": ["# Data Exploration\n", "\n", "Initial exploration of the dataset."]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": ["import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n"]
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
                    "version": "3.11.0"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 5
        }
        json.dump(notebook, f, indent=2)

    # Sample Python module
    with open(f'{PROJECT_DIR}/src/__init__.py', 'w') as f:
        f.write('')

    with open(f'{PROJECT_DIR}/src/train.py', 'w') as f:
        f.write('"""Training pipeline for deep learning models."""\n\n')
        f.write('import torch\n')
        f.write('import torch.nn as nn\n')
        f.write('from torch.utils.data import DataLoader\n\n\n')
        f.write('def train_epoch(model, dataloader, optimizer, criterion, device):\n')
        f.write('    """Train for one epoch."""\n')
        f.write('    model.train()\n')
        f.write('    total_loss = 0.0\n')
        f.write('    for batch_idx, (data, target) in enumerate(dataloader):\n')
        f.write('        data, target = data.to(device), target.to(device)\n')
        f.write('        optimizer.zero_grad()\n')
        f.write('        output = model(data)\n')
        f.write('        loss = criterion(output, target)\n')
        f.write('        loss.backward()\n')
        f.write('        optimizer.step()\n')
        f.write('        total_loss += loss.item()\n')
        f.write('    return total_loss / len(dataloader)\n')

    with open(f'{PROJECT_DIR}/src/model.py', 'w') as f:
        f.write('"""Neural network model definitions."""\n\n')
        f.write('import torch\n')
        f.write('import torch.nn as nn\n\n\n')
        f.write('class SimpleNet(nn.Module):\n')
        f.write('    """A simple feedforward neural network."""\n\n')
        f.write('    def __init__(self, input_dim, hidden_dim, output_dim):\n')
        f.write('        super().__init__()\n')
        f.write('        self.fc1 = nn.Linear(input_dim, hidden_dim)\n')
        f.write('        self.relu = nn.ReLU()\n')
        f.write('        self.fc2 = nn.Linear(hidden_dim, output_dim)\n\n')
        f.write('    def forward(self, x):\n')
        f.write('        x = self.fc1(x)\n')
        f.write('        x = self.relu(x)\n')
        f.write('        x = self.fc2(x)\n')
        f.write('        return x\n')

    # README for the project
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write('# Data Science Project\n\n')
        f.write('A deep learning project for training and evaluating neural network models.\n\n')
        f.write('## Project Structure\n\n')
        f.write('```\n')
        f.write('data-science/\n')
        f.write('├── .devcontainer/      # Dev container configuration\n')
        f.write('├── data/               # Dataset files\n')
        f.write('├── notebooks/          # Jupyter notebooks\n')
        f.write('├── src/                # Source code\n')
        f.write('│   ├── model.py        # Model definitions\n')
        f.write('│   └── train.py        # Training pipeline\n')
        f.write('└── requirements.txt    # Python dependencies\n')
        f.write('```\n\n')
        f.write('## Setup\n\n')
        f.write('Configure the devcontainer for GPU-accelerated development.\n')

    print(f'Project structure created at: {PROJECT_DIR}')

    # Open VSCode with the devcontainer.json file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{devcontainer_path}"', delay_sec=1.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

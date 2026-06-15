"""
Initial Setup: Create ML project structure for Jupyter magic commands task
Task ID: vscode_gf2_032
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_032'
PROJECT_DIR = f'{WORKDIR}/projects/jupyter-ml'


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
    # --- Create project directory structure ---
    dirs = [
        f'{PROJECT_DIR}/notebooks',
        f'{PROJECT_DIR}/src',
        f'{PROJECT_DIR}/data',
        f'{PROJECT_DIR}/models',
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # --- src/data_loader.py ---
    with open(f'{PROJECT_DIR}/src/data_loader.py', 'w') as f:
        f.write('''"""Data loading utilities for ML pipeline."""

import os
import csv


def load_training_data(filepath):
    """Load training data from CSV file."""
    data = []
    with open(filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append({
                'features': [float(row['feature_1']), float(row['feature_2']),
                             float(row['feature_3'])],
                'label': int(row['label'])
            })
    return data


def split_dataset(data, train_ratio=0.8):
    """Split dataset into training and validation sets."""
    split_idx = int(len(data) * train_ratio)
    return data[:split_idx], data[split_idx:]


def normalize_features(features):
    """Min-max normalize feature values."""
    min_vals = [min(col) for col in zip(*features)]
    max_vals = [max(col) for col in zip(*features)]
    normalized = []
    for row in features:
        norm_row = []
        for val, mn, mx in zip(row, min_vals, max_vals):
            if mx - mn > 0:
                norm_row.append((val - mn) / (mx - mn))
            else:
                norm_row.append(0.0)
        normalized.append(norm_row)
    return normalized
''')

    # --- src/model.py ---
    with open(f'{PROJECT_DIR}/src/model.py', 'w') as f:
        f.write('''"""Simple neural network model definition."""

import math
import random


class SimpleClassifier:
    """A basic 2-layer classifier for demonstration."""

    def __init__(self, input_dim=3, hidden_dim=8, output_dim=2, lr=0.01):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.lr = lr
        self._init_weights()

    def _init_weights(self):
        """Xavier initialization."""
        scale_1 = math.sqrt(2.0 / (self.input_dim + self.hidden_dim))
        self.w1 = [[random.gauss(0, scale_1) for _ in range(self.hidden_dim)]
                    for _ in range(self.input_dim)]
        self.b1 = [0.0] * self.hidden_dim

        scale_2 = math.sqrt(2.0 / (self.hidden_dim + self.output_dim))
        self.w2 = [[random.gauss(0, scale_2) for _ in range(self.output_dim)]
                    for _ in range(self.hidden_dim)]
        self.b2 = [0.0] * self.output_dim

    def forward(self, x):
        """Forward pass through the network."""
        hidden = [0.0] * self.hidden_dim
        for j in range(self.hidden_dim):
            for i in range(self.input_dim):
                hidden[j] += x[i] * self.w1[i][j]
            hidden[j] += self.b1[j]
            hidden[j] = max(0.0, hidden[j])  # ReLU

        output = [0.0] * self.output_dim
        for j in range(self.output_dim):
            for i in range(self.hidden_dim):
                output[j] += hidden[i] * self.w2[i][j]
            output[j] += self.b2[j]
        return output

    def predict(self, x):
        """Return predicted class."""
        output = self.forward(x)
        return output.index(max(output))
''')

    # --- src/__init__.py ---
    with open(f'{PROJECT_DIR}/src/__init__.py', 'w') as f:
        f.write('"""ML project source package."""\n')

    # --- data/training_samples.csv ---
    with open(f'{PROJECT_DIR}/data/training_samples.csv', 'w') as f:
        f.write('feature_1,feature_2,feature_3,label\n')
        samples = [
            (0.23, 1.45, 0.67, 0), (1.89, 0.34, 1.12, 1),
            (0.56, 1.78, 0.89, 0), (2.01, 0.12, 1.56, 1),
            (0.34, 1.92, 0.45, 0), (1.67, 0.45, 1.34, 1),
            (0.78, 1.56, 0.23, 0), (2.34, 0.67, 1.78, 1),
            (0.12, 2.01, 0.56, 0), (1.45, 0.89, 1.23, 1),
            (0.45, 1.34, 0.78, 0), (2.12, 0.23, 1.45, 1),
            (0.67, 1.67, 0.34, 0), (1.78, 0.56, 1.67, 1),
            (0.89, 1.23, 0.12, 0), (2.45, 0.78, 1.89, 1),
        ]
        for s in samples:
            f.write(f'{s[0]},{s[1]},{s[2]},{s[3]}\n')

    # --- README.md ---
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write('''# Jupyter ML Project

A machine learning pipeline for binary classification using custom neural networks.

## Project Structure

```
jupyter-ml/
├── notebooks/       # Jupyter notebooks for experimentation
├── src/             # Source code modules
│   ├── data_loader.py
│   └── model.py
├── data/            # Training and evaluation data
└── models/          # Saved model checkpoints
```

## Getting Started

1. Open the project in VSCode
2. Create notebooks in the `notebooks/` directory
3. Use IPython magic commands for interactive development

## Requirements

- Python 3.8+
- matplotlib
- numpy (optional, for advanced operations)
''')

    # --- requirements.txt ---
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write('matplotlib>=3.5.0\nnumpy>=1.21.0\nscikit-learn>=1.0.0\npandas>=1.4.0\n')

    print(f'Project structure created at: {PROJECT_DIR}')

    # --- GUI-ready: open VSCode with the project ---
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

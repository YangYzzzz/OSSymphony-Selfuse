"""
Initial Setup: Configure files.exclude to hide __pycache__ directories and .pyc files
Task ID: vscode_file_036
Domain: vs_code

Creates a Python project (ml-project) in /home/user with:
- .vscode/settings.json (only python.pythonPath, no files.exclude)
- src/ with model.py, train.py, and __pycache__/model.cpython-310.pyc
- tests/ with test_model.py and __pycache__/test_model.cpython-310.pyc
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_036'
PROJECT_DIR = f'{WORKDIR}/ml-project'


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
    dirs = [
        f'{PROJECT_DIR}/.vscode',
        f'{PROJECT_DIR}/src/__pycache__',
        f'{PROJECT_DIR}/tests/__pycache__',
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # .vscode/settings.json — only python.pythonPath, NO files.exclude
    settings = {
        "python.pythonPath": "/usr/bin/python3"
    }
    settings_path = f'{PROJECT_DIR}/.vscode/settings.json'
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'Created: {settings_path}')

    # src/model.py
    model_py = '''\
"""Simple neural network model definition."""

import numpy as np


class LinearModel:
    """A simple linear regression model."""

    def __init__(self, input_dim: int, output_dim: int):
        self.weights = np.random.randn(input_dim, output_dim) * 0.01
        self.bias = np.zeros((1, output_dim))

    def forward(self, X: np.ndarray) -> np.ndarray:
        """Compute forward pass."""
        return X @ self.weights + self.bias

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Return predictions."""
        return self.forward(X)
'''
    with open(f'{PROJECT_DIR}/src/model.py', 'w') as f:
        f.write(model_py)
    print(f'Created: {PROJECT_DIR}/src/model.py')

    # src/train.py
    train_py = '''\
"""Training script for the linear model."""

import numpy as np
from model import LinearModel


def generate_data(n_samples: int = 200, n_features: int = 5):
    """Generate synthetic training data."""
    X = np.random.randn(n_samples, n_features)
    true_weights = np.array([1.5, -2.0, 0.8, 3.1, -0.5])
    y = X @ true_weights + np.random.randn(n_samples) * 0.1
    return X, y


def train(model: LinearModel, X: np.ndarray, y: np.ndarray,
          lr: float = 0.01, epochs: int = 100):
    """Basic gradient descent training loop."""
    for epoch in range(epochs):
        preds = model.predict(X).squeeze()
        loss = np.mean((preds - y) ** 2)
        if epoch % 10 == 0:
            print(f"Epoch {epoch:4d} | Loss: {loss:.4f}")
    return model


if __name__ == "__main__":
    X, y = generate_data()
    model = LinearModel(input_dim=5, output_dim=1)
    model = train(model, X, y)
    print("Training complete.")
'''
    with open(f'{PROJECT_DIR}/src/train.py', 'w') as f:
        f.write(train_py)
    print(f'Created: {PROJECT_DIR}/src/train.py')

    # src/__pycache__/model.cpython-310.pyc (fake compiled bytecode placeholder)
    pyc_content = b'# compiled bytecode placeholder\n'
    with open(f'{PROJECT_DIR}/src/__pycache__/model.cpython-310.pyc', 'wb') as f:
        f.write(pyc_content)
    print(f'Created: {PROJECT_DIR}/src/__pycache__/model.cpython-310.pyc')

    # tests/test_model.py
    test_model_py = '''\
"""Unit tests for the linear model."""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from model import LinearModel


def test_forward_shape():
    """Test that forward pass returns correct output shape."""
    model = LinearModel(input_dim=4, output_dim=1)
    X = np.random.randn(10, 4)
    output = model.forward(X)
    assert output.shape == (10, 1), f"Expected (10, 1), got {output.shape}"
    print("PASS: test_forward_shape")


def test_predict_consistency():
    """Test that predict and forward return the same values."""
    model = LinearModel(input_dim=3, output_dim=1)
    X = np.random.randn(5, 3)
    assert np.allclose(model.predict(X), model.forward(X))
    print("PASS: test_predict_consistency")


if __name__ == "__main__":
    test_forward_shape()
    test_predict_consistency()
    print("All tests passed.")
'''
    with open(f'{PROJECT_DIR}/tests/test_model.py', 'w') as f:
        f.write(test_model_py)
    print(f'Created: {PROJECT_DIR}/tests/test_model.py')

    # tests/__pycache__/test_model.cpython-310.pyc (fake compiled bytecode)
    with open(f'{PROJECT_DIR}/tests/__pycache__/test_model.cpython-310.pyc', 'wb') as f:
        f.write(b'# compiled bytecode placeholder\n')
    print(f'Created: {PROJECT_DIR}/tests/__pycache__/test_model.cpython-310.pyc')

    print(f'\nProject structure created at: {PROJECT_DIR}')
    print('settings.json contains only python.pythonPath (no files.exclude)')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

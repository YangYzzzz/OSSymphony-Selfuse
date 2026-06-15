"""
Initial Setup: VSCode notebook with default Python 3 kernel; ml-env conda kernel available
Task ID: vscode_rf_041
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rf_041'
PROJECT_DIR = f'{WORKDIR}/projects/ml'
NOTEBOOK_PATH = f'{PROJECT_DIR}/train.ipynb'

# Paths for the ml-env virtual environment (simulates conda env)
ML_ENV_DIR = f'{WORKDIR}/miniconda3/envs/ml-env'
ML_ENV_PYTHON = f'{ML_ENV_DIR}/bin/python3'

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

def create_ml_env():
    """Create a virtual environment that mimics a conda ml-env and register it as a Jupyter kernel."""
    # Create the venv at a path that looks like a conda environment
    os.makedirs(os.path.dirname(ML_ENV_DIR), exist_ok=True)

    # Use --without-pip since ensurepip may not be available
    subprocess.run(['python3', '-m', 'venv', '--without-pip', ML_ENV_DIR], check=True)

    # Bootstrap pip into the venv
    subprocess.run(
        [ML_ENV_PYTHON, '-c',
         'import urllib.request; urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", "/tmp/get-pip.py")'],
        check=True,
    )
    subprocess.run(
        [ML_ENV_PYTHON, '/tmp/get-pip.py'],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Install ipykernel in the ml-env
    subprocess.run(
        [ML_ENV_PYTHON, '-m', 'pip', 'install', 'ipykernel', 'numpy', 'pandas', 'scikit-learn'],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Register the kernel with Jupyter
    subprocess.run(
        [ML_ENV_PYTHON, '-m', 'ipykernel', 'install', '--user',
         '--name', 'ml-env', '--display-name', 'ml-env (Python)'],
        check=True,
    )
    print(f'ml-env kernel registered')

def create_notebook():
    """Create train.ipynb with default Python 3 kernel and a sys.executable cell."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Also create some supporting project files for realism
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write('numpy>=1.24.0\npandas>=2.0.0\nscikit-learn>=1.3.0\nmatplotlib>=3.7.0\n')

    with open(f'{PROJECT_DIR}/config.yaml', 'w') as f:
        f.write('# ML Training Configuration\nmodel:\n  type: random_forest\n  n_estimators: 100\n  max_depth: 10\n\ndata:\n  train_split: 0.8\n  random_seed: 42\n  input_path: ./data/train.csv\n  output_path: ./models/\n')

    os.makedirs(f'{PROJECT_DIR}/data', exist_ok=True)
    with open(f'{PROJECT_DIR}/data/train.csv', 'w') as f:
        f.write('feature_1,feature_2,feature_3,label\n')
        f.write('0.52,1.34,0.88,1\n0.73,0.21,1.45,0\n0.19,2.01,0.33,1\n1.05,0.67,0.91,0\n0.88,1.12,1.67,1\n')

    os.makedirs(f'{PROJECT_DIR}/models', exist_ok=True)

    # Create the notebook with default python3 kernel
    notebook = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": None,
                "id": "cell-001",
                "metadata": {},
                "outputs": [],
                "source": [
                    "import sys; print(sys.executable)"
                ]
            },
            {
                "cell_type": "markdown",
                "id": "cell-002",
                "metadata": {},
                "source": [
                    "## ML Training Pipeline\n",
                    "\n",
                    "This notebook uses the `ml-env` conda environment for training.\n",
                    "Make sure to switch to the correct kernel before running."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "id": "cell-003",
                "metadata": {},
                "outputs": [],
                "source": [
                    "import numpy as np\n",
                    "import pandas as pd\n",
                    "from sklearn.ensemble import RandomForestClassifier\n",
                    "\n",
                    "# Load training data\n",
                    "df = pd.read_csv('./data/train.csv')\n",
                    "print(f'Dataset shape: {df.shape}')\n",
                    "df.head()"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "id": "cell-004",
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Train model\n",
                    "X = df[['feature_1', 'feature_2', 'feature_3']]\n",
                    "y = df['label']\n",
                    "\n",
                    "model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)\n",
                    "model.fit(X, y)\n",
                    "print(f'Training accuracy: {model.score(X, y):.4f}')"
                ]
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
                "version": "3.10.12"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    with open(NOTEBOOK_PATH, 'w') as f:
        json.dump(notebook, f, indent=1)

    print(f'Notebook created: {NOTEBOOK_PATH}')

def main():
    # Step 1: Create the ml-env and register its kernel
    create_ml_env()

    # Step 2: Create the notebook and project files
    create_notebook()

    # Step 3: Launch VSCode with the project folder and notebook open
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    launch_gui(f'code "{NOTEBOOK_PATH}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with project folder and notebook')

main()

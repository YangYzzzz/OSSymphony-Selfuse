"""
Initial Setup: Python development environment task
Task ID: os_gf5_021
Domain: os (Python dev environment with pyenv)

Initial state: Ubuntu 22.04 desktop with system Python 3.10 only.
- pyenv is NOT installed
- No virtualenv exists
- No VS Code project settings
- ~/projects/ml-project exists as a starter data science project
- pyenv build dependencies are pre-installed so the agent can build Python
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'os_gf5_021'

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
    # -------------------------------------------------------
    # 1. Install build dependencies for pyenv/Python compilation
    #    (so the agent can successfully run 'pyenv install 3.11.7')
    # -------------------------------------------------------
    subprocess.run(["sudo", "apt-get", "update", "-qq"], check=True,
                    capture_output=True, text=True, timeout=120)
    subprocess.run([
        "sudo", "apt-get", "install", "-y", "-qq",
        "make", "build-essential", "libssl-dev", "zlib1g-dev",
        "libbz2-dev", "libreadline-dev", "libsqlite3-dev", "wget",
        "curl", "llvm", "libncursesw5-dev", "xz-utils", "tk-dev",
        "libxml2-dev", "libxmlsec1-dev", "libffi-dev", "liblzma-dev",
        "git"
    ], check=True, capture_output=True, text=True, timeout=300)
    print("Build dependencies installed.")

    # -------------------------------------------------------
    # 2. Ensure pyenv is NOT installed (clean state)
    # -------------------------------------------------------
    pyenv_dir = os.path.join(WORKDIR, '.pyenv')
    if os.path.exists(pyenv_dir):
        subprocess.run(["rm", "-rf", pyenv_dir], check=True)

    # Remove any pyenv references from .bashrc
    bashrc_path = os.path.join(WORKDIR, '.bashrc')
    if os.path.exists(bashrc_path):
        with open(bashrc_path, 'r') as f:
            lines = f.readlines()
        with open(bashrc_path, 'w') as f:
            for line in lines:
                if 'pyenv' not in line.lower():
                    f.write(line)

    # -------------------------------------------------------
    # 3. Create project directory with realistic data science files
    # -------------------------------------------------------
    project_dir = os.path.join(WORKDIR, 'projects', 'ml-project')
    os.makedirs(project_dir, exist_ok=True)
    os.makedirs(os.path.join(project_dir, 'data'), exist_ok=True)
    os.makedirs(os.path.join(project_dir, 'models'), exist_ok=True)
    os.makedirs(os.path.join(project_dir, 'notebooks'), exist_ok=True)
    os.makedirs(os.path.join(project_dir, 'src'), exist_ok=True)

    # README.md
    with open(os.path.join(project_dir, 'README.md'), 'w') as f:
        f.write("""# ML Project - Customer Churn Prediction

## Overview
This project builds a machine learning model to predict customer churn
for a telecommunications company. We use gradient boosting and neural
network approaches to identify at-risk customers.

## Requirements
- Python 3.11.7 (required for TensorFlow 2.15 compatibility)
- See requirements.txt for package dependencies

## Project Structure
```
ml-project/
├── data/           # Raw and processed datasets
├── models/         # Trained model artifacts
├── notebooks/      # Jupyter exploration notebooks
├── src/            # Source code modules
└── requirements.txt
```

## Setup Instructions
1. Install Python 3.11.7 using pyenv
2. Create a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Run training: `python src/train.py`
""")

    # requirements.txt
    with open(os.path.join(project_dir, 'requirements.txt'), 'w') as f:
        f.write("""tensorflow==2.15.0
numpy==1.26.2
pandas==2.1.4
scikit-learn==1.3.2
matplotlib==3.8.2
seaborn==0.13.0
jupyter==1.0.0
xgboost==2.0.3
shap==0.44.0
mlflow==2.9.2
""")

    # src/__init__.py
    with open(os.path.join(project_dir, 'src', '__init__.py'), 'w') as f:
        f.write("")

    # src/train.py
    with open(os.path.join(project_dir, 'src', 'train.py'), 'w') as f:
        f.write("""#!/usr/bin/env python3
\"\"\"Training script for customer churn prediction model.\"\"\"

import argparse
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"
MODEL_DIR = Path(__file__).parent.parent / "models"


def load_data(filepath: str) -> pd.DataFrame:
    \"\"\"Load and preprocess the customer dataset.\"\"\"
    df = pd.read_csv(filepath)
    logger.info(f"Loaded {len(df)} records from {filepath}")
    return df


def train_model(X_train, y_train):
    \"\"\"Train the churn prediction model.\"\"\"
    from xgboost import XGBClassifier

    model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
    )
    model.fit(X_train, y_train)
    return model


def main():
    parser = argparse.ArgumentParser(description="Train churn model")
    parser.add_argument("--data", default=str(DATA_DIR / "customers.csv"))
    parser.add_argument("--output", default=str(MODEL_DIR / "churn_model.json"))
    args = parser.parse_args()

    logger.info("Starting model training pipeline")
    # Placeholder - actual data loading would go here
    logger.info("Training complete")


if __name__ == "__main__":
    main()
""")

    # src/preprocess.py
    with open(os.path.join(project_dir, 'src', 'preprocess.py'), 'w') as f:
        f.write("""#!/usr/bin/env python3
\"\"\"Data preprocessing utilities for the ML pipeline.\"\"\"

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder


def encode_categorical(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    \"\"\"Encode categorical columns using LabelEncoder.\"\"\"
    df = df.copy()
    for col in columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
    return df


def scale_features(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    \"\"\"Standardize numerical features.\"\"\"
    df = df.copy()
    scaler = StandardScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df


def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    \"\"\"Handle missing values with median/mode imputation.\"\"\"
    df = df.copy()
    for col in df.columns:
        if df[col].dtype in ['float64', 'int64']:
            df[col].fillna(df[col].median(), inplace=True)
        else:
            df[col].fillna(df[col].mode()[0], inplace=True)
    return df
""")

    # Sample data CSV
    with open(os.path.join(project_dir, 'data', 'customers.csv'), 'w') as f:
        f.write("customer_id,name,tenure_months,monthly_charges,total_charges,contract_type,churn\n")
        f.write("C001,Sarah Chen,24,79.50,1908.00,Two year,No\n")
        f.write("C002,Marcus Johnson,8,89.95,719.60,Month-to-month,Yes\n")
        f.write("C003,Elena Rodriguez,36,54.25,1953.00,Two year,No\n")
        f.write("C004,James O'Brien,3,95.00,285.00,Month-to-month,Yes\n")
        f.write("C005,Aisha Patel,48,62.75,3012.00,One year,No\n")
        f.write("C006,Thomas Weber,12,78.30,939.60,One year,No\n")
        f.write("C007,Li Wei,2,102.50,205.00,Month-to-month,Yes\n")
        f.write("C008,Maria Santos,60,45.00,2700.00,Two year,No\n")
        f.write("C009,David Kim,6,88.75,532.50,Month-to-month,Yes\n")
        f.write("C010,Anna Kowalski,18,71.20,1281.60,One year,No\n")

    # .gitignore
    with open(os.path.join(project_dir, '.gitignore'), 'w') as f:
        f.write("""# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.venv/

# Data
data/*.csv
!data/.gitkeep

# Models
models/*.json
models/*.pkl

# IDE
.vscode/
.idea/

# Jupyter
.ipynb_checkpoints/
""")

    # Ensure NO .venv or .vscode directories exist (clean initial state)
    import shutil
    venv_dir = os.path.join(project_dir, '.venv')
    if os.path.exists(venv_dir):
        shutil.rmtree(venv_dir)
    vscode_dir = os.path.join(project_dir, '.vscode')
    if os.path.exists(vscode_dir):
        shutil.rmtree(vscode_dir)

    print(f'Initial project created: {project_dir}')
    print(f'System Python: ', end='')
    subprocess.run(["python3", "--version"])

    # -------------------------------------------------------
    # 4. GUI-ready startup: open terminal and file manager
    # -------------------------------------------------------
    launch_gui('gnome-terminal', delay_sec=1.5)
    launch_gui(f'nautilus "{os.path.join(WORKDIR, "projects", "ml-project")}"', delay_sec=1.5)
    print('GUI_READY: launched terminal and file manager with DISPLAY=:0')

create_initial()

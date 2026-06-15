"""
Initial Setup: Create a Python ML pipeline project in VSCode without devcontainer config
Task ID: vscode_rrt_011
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_011'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'ml-pipeline')


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
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'data'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'tests'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'models'), exist_ok=True)

    # Main pipeline script
    with open(os.path.join(PROJECT_DIR, 'src', 'pipeline.py'), 'w') as f:
        f.write('''"""
ML Pipeline - Data processing and model training pipeline.
Handles data ingestion, feature engineering, and model training.
"""

import os
import logging
from dataclasses import dataclass
from typing import List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PipelineConfig:
    data_path: str = "data/raw"
    output_path: str = "models/trained"
    batch_size: int = 64
    learning_rate: float = 0.001
    epochs: int = 50
    random_seed: int = 42


class DataLoader:
    """Loads and validates input datasets for the ML pipeline."""

    def __init__(self, config: PipelineConfig):
        self.config = config
        self.data_cache = {}

    def load_csv(self, filename: str) -> List[dict]:
        filepath = os.path.join(self.config.data_path, filename)
        logger.info(f"Loading dataset from {filepath}")
        # Placeholder for actual CSV loading
        return []

    def validate_schema(self, data: List[dict], required_columns: List[str]) -> bool:
        if not data:
            return False
        return all(col in data[0] for col in required_columns)


class FeatureEngineer:
    """Transforms raw data into features for model training."""

    def __init__(self, config: PipelineConfig):
        self.config = config
        self.transformations = []

    def add_transformation(self, name: str, func):
        self.transformations.append((name, func))
        logger.info(f"Added transformation: {name}")

    def apply_all(self, data: List[dict]) -> List[dict]:
        result = data
        for name, func in self.transformations:
            logger.info(f"Applying transformation: {name}")
            result = [func(row) for row in result]
        return result


class ModelTrainer:
    """Trains and evaluates ML models."""

    def __init__(self, config: PipelineConfig):
        self.config = config
        self.model = None
        self.metrics = {}

    def train(self, features: List[dict], labels: List[float]):
        logger.info(f"Training model with {len(features)} samples")
        logger.info(f"Batch size: {self.config.batch_size}, LR: {self.config.learning_rate}")
        # Placeholder for actual training logic

    def evaluate(self, test_features: List[dict], test_labels: List[float]) -> dict:
        logger.info("Evaluating model performance")
        return {"accuracy": 0.0, "f1_score": 0.0, "precision": 0.0, "recall": 0.0}


def run_pipeline(config: Optional[PipelineConfig] = None):
    if config is None:
        config = PipelineConfig()

    logger.info("Starting ML pipeline execution")
    loader = DataLoader(config)
    engineer = FeatureEngineer(config)
    trainer = ModelTrainer(config)

    logger.info("Pipeline setup complete")
    return loader, engineer, trainer


if __name__ == "__main__":
    run_pipeline()
''')

    # Data preprocessing utilities
    with open(os.path.join(PROJECT_DIR, 'src', 'preprocessing.py'), 'w') as f:
        f.write('''"""
Data preprocessing utilities for the ML pipeline.
"""

import re
from typing import List, Dict, Any, Optional
from datetime import datetime


def clean_text(text: str) -> str:
    """Remove special characters and normalize whitespace."""
    text = re.sub(r'[^a-zA-Z0-9\\s]', '', text)
    return ' '.join(text.split()).strip().lower()


def normalize_numeric(values: List[float], method: str = "minmax") -> List[float]:
    """Normalize numeric values using specified method."""
    if not values:
        return []
    if method == "minmax":
        min_val, max_val = min(values), max(values)
        if max_val == min_val:
            return [0.0] * len(values)
        return [(v - min_val) / (max_val - min_val) for v in values]
    elif method == "zscore":
        mean_val = sum(values) / len(values)
        std_val = (sum((v - mean_val) ** 2 for v in values) / len(values)) ** 0.5
        if std_val == 0:
            return [0.0] * len(values)
        return [(v - mean_val) / std_val for v in values]
    raise ValueError(f"Unknown normalization method: {method}")


def parse_date(date_str: str, fmt: str = "%Y-%m-%d") -> Optional[datetime]:
    """Parse date string with error handling."""
    try:
        return datetime.strptime(date_str, fmt)
    except (ValueError, TypeError):
        return None


def encode_categorical(values: List[str]) -> Dict[str, int]:
    """Create label encoding for categorical values."""
    unique = sorted(set(values))
    return {val: idx for idx, val in enumerate(unique)}
''')

    # Requirements file
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write('''numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.3.0
matplotlib>=3.7.0
seaborn>=0.12.0
pytest>=7.4.0
black>=23.0.0
flake8>=6.0.0
''')

    # Test file
    with open(os.path.join(PROJECT_DIR, 'tests', 'test_preprocessing.py'), 'w') as f:
        f.write('''"""Tests for preprocessing utilities."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from preprocessing import clean_text, normalize_numeric, parse_date, encode_categorical


def test_clean_text():
    assert clean_text("Hello, World!") == "hello world"
    assert clean_text("  multiple   spaces  ") == "multiple spaces"
    assert clean_text("special@#$chars") == "specialchars"


def test_normalize_numeric_minmax():
    result = normalize_numeric([10, 20, 30, 40, 50])
    assert result[0] == 0.0
    assert result[-1] == 1.0


def test_normalize_numeric_empty():
    assert normalize_numeric([]) == []


def test_parse_date():
    dt = parse_date("2025-03-15")
    assert dt is not None
    assert dt.year == 2025
    assert dt.month == 3


def test_encode_categorical():
    encoding = encode_categorical(["red", "blue", "green", "red"])
    assert len(encoding) == 3
    assert encoding["blue"] < encoding["green"] < encoding["red"]


if __name__ == "__main__":
    test_clean_text()
    test_normalize_numeric_minmax()
    test_normalize_numeric_empty()
    test_parse_date()
    test_encode_categorical()
    print("All tests passed!")
''')

    # README
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write('''# ML Pipeline

A modular machine learning pipeline for data processing and model training.

## Project Structure

```
ml-pipeline/
  src/           - Source code
  data/          - Raw and processed datasets
  models/        - Trained model artifacts
  tests/         - Unit tests
```

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```python
from src.pipeline import run_pipeline, PipelineConfig

config = PipelineConfig(
    data_path="data/raw",
    batch_size=128,
    epochs=100
)
run_pipeline(config)
```
''')

    # .gitignore
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write('''__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.env
.venv/
models/trained/
data/processed/
*.csv
*.pkl
.pytest_cache/
''')

    # __init__.py files
    with open(os.path.join(PROJECT_DIR, 'src', '__init__.py'), 'w') as f:
        f.write('')
    with open(os.path.join(PROJECT_DIR, 'tests', '__init__.py'), 'w') as f:
        f.write('')

    # Ensure NO .devcontainer directory exists (negative constraint)
    import shutil
    devcontainer_dir = os.path.join(PROJECT_DIR, '.devcontainer')
    if os.path.exists(devcontainer_dir):
        shutil.rmtree(devcontainer_dir)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'Verified: No .devcontainer directory exists')

    # Install Dev Containers extension
    try:
        subprocess.run(['code', '--install-extension', 'ms-vscode-remote.remote-containers'],
                       check=True, capture_output=True, timeout=60)
        print('Dev Containers extension installed')
    except Exception as e:
        print(f'Warning: Could not install Dev Containers extension: {e}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with project folder')


create_initial()

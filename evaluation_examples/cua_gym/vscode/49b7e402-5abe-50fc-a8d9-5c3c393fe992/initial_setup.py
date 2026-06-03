"""
Initial Setup: Create ML pipeline project with tests for VSCode tasks.json task
Task ID: vscode_td_025
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'ml-pipeline')
TESTS_DIR = os.path.join(PROJECT_DIR, 'tests')
SRC_DIR = os.path.join(PROJECT_DIR, 'src')


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
    # Create project structure
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(TESTS_DIR, exist_ok=True)

    # Remove any existing .vscode/tasks.json to ensure clean initial state
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    tasks_path = os.path.join(vscode_dir, 'tasks.json')
    if os.path.exists(tasks_path):
        os.remove(tasks_path)

    # --- src/data_loader.py ---
    with open(os.path.join(SRC_DIR, '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(SRC_DIR, 'data_loader.py'), 'w') as f:
        f.write('''"""Data loading utilities for the ML pipeline."""

import csv
import os
from typing import List, Dict, Optional


class DataLoader:
    """Handles loading and preprocessing of training data."""

    def __init__(self, data_dir: str, batch_size: int = 32):
        self.data_dir = data_dir
        self.batch_size = batch_size
        self._cache = {}

    def load_csv(self, filename: str) -> List[Dict[str, str]]:
        """Load a CSV file from the data directory."""
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Data file not found: {filepath}")
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def preprocess(self, records: List[Dict], columns: List[str]) -> List[List[float]]:
        """Extract and convert specified columns to float arrays."""
        result = []
        for record in records:
            row = []
            for col in columns:
                val = record.get(col)
                if val is None:
                    raise ValueError(f"Missing column: {col}")
                row.append(float(val))
            result.append(row)
        return result

    def get_batches(self, data: List, batch_size: Optional[int] = None):
        """Split data into batches."""
        bs = batch_size or self.batch_size
        for i in range(0, len(data), bs):
            yield data[i:i + bs]
''')

    # --- src/model.py ---
    with open(os.path.join(SRC_DIR, 'model.py'), 'w') as f:
        f.write('''"""Simple ML model implementation."""

import math
from typing import List, Tuple


class LinearRegression:
    """Basic linear regression model for the pipeline."""

    def __init__(self, n_features: int, learning_rate: float = 0.01):
        self.weights = [0.0] * n_features
        self.bias = 0.0
        self.learning_rate = learning_rate
        self.n_features = n_features

    def predict(self, features: List[float]) -> float:
        """Predict output for a single sample."""
        if len(features) != self.n_features:
            raise ValueError(
                f"Expected {self.n_features} features, got {len(features)}"
            )
        return sum(w * x for w, x in zip(self.weights, features)) + self.bias

    def train_step(self, features: List[float], target: float) -> float:
        """Perform a single gradient descent step. Returns loss."""
        prediction = self.predict(features)
        error = prediction - target
        loss = error ** 2

        # Update weights
        for i in range(self.n_features):
            self.weights[i] -= self.learning_rate * 2 * error * features[i]
        self.bias -= self.learning_rate * 2 * error

        return loss

    def evaluate(self, data: List[Tuple[List[float], float]]) -> dict:
        """Evaluate model on a dataset. Returns metrics dict."""
        if not data:
            return {"mse": 0.0, "rmse": 0.0, "mae": 0.0}

        total_se = 0.0
        total_ae = 0.0
        for features, target in data:
            pred = self.predict(features)
            total_se += (pred - target) ** 2
            total_ae += abs(pred - target)

        n = len(data)
        mse = total_se / n
        return {
            "mse": mse,
            "rmse": math.sqrt(mse),
            "mae": total_ae / n,
        }
''')

    # --- src/pipeline.py ---
    with open(os.path.join(SRC_DIR, 'pipeline.py'), 'w') as f:
        f.write('''"""End-to-end ML pipeline orchestration."""

from .data_loader import DataLoader
from .model import LinearRegression


class Pipeline:
    """Orchestrates data loading, training, and evaluation."""

    def __init__(self, data_dir: str, n_features: int, epochs: int = 100):
        self.loader = DataLoader(data_dir)
        self.model = LinearRegression(n_features)
        self.epochs = epochs
        self.history = []

    def run(self, train_file: str, test_file: str, target_col: str,
            feature_cols: list) -> dict:
        """Execute the full pipeline."""
        # Load data
        train_records = self.loader.load_csv(train_file)
        test_records = self.loader.load_csv(test_file)

        # Preprocess
        train_features = self.loader.preprocess(train_records, feature_cols)
        train_targets = [float(r[target_col]) for r in train_records]

        test_features = self.loader.preprocess(test_records, feature_cols)
        test_targets = [float(r[target_col]) for r in test_records]

        # Train
        for epoch in range(self.epochs):
            epoch_loss = 0.0
            for features, target in zip(train_features, train_targets):
                loss = self.model.train_step(features, target)
                epoch_loss += loss
            avg_loss = epoch_loss / len(train_features)
            self.history.append(avg_loss)

        # Evaluate
        test_data = list(zip(test_features, test_targets))
        metrics = self.model.evaluate(test_data)
        return metrics
''')

    # --- tests/__init__.py ---
    with open(os.path.join(TESTS_DIR, '__init__.py'), 'w') as f:
        f.write('')

    # --- tests/test_data_loader.py ---
    with open(os.path.join(TESTS_DIR, 'test_data_loader.py'), 'w') as f:
        f.write('''"""Tests for the data loading module."""

import os
import tempfile
import pytest
from src.data_loader import DataLoader


@pytest.fixture
def sample_csv(tmp_path):
    csv_content = "name,age,salary\\nAlice,30,75000\\nBob,25,62000\\nCarla,35,88000\\n"
    csv_file = tmp_path / "employees.csv"
    csv_file.write_text(csv_content)
    return str(tmp_path), "employees.csv"


class TestDataLoader:
    def test_load_csv_returns_records(self, sample_csv):
        data_dir, filename = sample_csv
        loader = DataLoader(data_dir)
        records = loader.load_csv(filename)
        assert len(records) == 3
        assert records[0]["name"] == "Alice"

    def test_load_csv_missing_file_raises(self):
        loader = DataLoader("/nonexistent/path")
        with pytest.raises(FileNotFoundError):
            loader.load_csv("missing.csv")

    def test_preprocess_extracts_columns(self, sample_csv):
        data_dir, filename = sample_csv
        loader = DataLoader(data_dir)
        records = loader.load_csv(filename)
        result = loader.preprocess(records, ["age", "salary"])
        assert len(result) == 3
        assert result[0] == [30.0, 75000.0]

    def test_preprocess_missing_column_raises(self, sample_csv):
        data_dir, filename = sample_csv
        loader = DataLoader(data_dir)
        records = loader.load_csv(filename)
        with pytest.raises(ValueError, match="Missing column"):
            loader.preprocess(records, ["nonexistent"])

    def test_get_batches(self):
        loader = DataLoader("/tmp", batch_size=2)
        data = [1, 2, 3, 4, 5]
        batches = list(loader.get_batches(data))
        assert len(batches) == 3
        assert batches[0] == [1, 2]
        assert batches[-1] == [5]
''')

    # --- tests/test_model.py ---
    with open(os.path.join(TESTS_DIR, 'test_model.py'), 'w') as f:
        f.write('''"""Tests for the ML model module."""

import pytest
from src.model import LinearRegression


class TestLinearRegression:
    def test_initial_prediction_is_zero(self):
        model = LinearRegression(n_features=3)
        assert model.predict([1.0, 2.0, 3.0]) == 0.0

    def test_predict_wrong_features_raises(self):
        model = LinearRegression(n_features=2)
        with pytest.raises(ValueError, match="Expected 2 features"):
            model.predict([1.0, 2.0, 3.0])

    def test_train_step_reduces_loss(self):
        model = LinearRegression(n_features=2, learning_rate=0.001)
        features = [1.0, 2.0]
        target = 5.0
        loss1 = model.train_step(features, target)
        loss2 = model.train_step(features, target)
        assert loss2 < loss1

    def test_evaluate_empty_data(self):
        model = LinearRegression(n_features=2)
        metrics = model.evaluate([])
        assert metrics["mse"] == 0.0

    def test_evaluate_returns_metrics(self):
        model = LinearRegression(n_features=1)
        # Manually set weights for predictable output
        model.weights = [2.0]
        model.bias = 1.0
        # predict([3.0]) = 2*3+1 = 7.0; target = 7.0 => error = 0
        data = [([3.0], 7.0)]
        metrics = model.evaluate(data)
        assert metrics["mse"] == 0.0
        assert metrics["rmse"] == 0.0
        assert metrics["mae"] == 0.0
''')

    # --- tests/test_pipeline.py ---
    with open(os.path.join(TESTS_DIR, 'test_pipeline.py'), 'w') as f:
        f.write('''"""Tests for the pipeline orchestration."""

import os
import pytest
from src.pipeline import Pipeline


@pytest.fixture
def data_dir(tmp_path):
    train = "x1,x2,y\\n1,2,5\\n2,3,8\\n3,4,11\\n4,5,14\\n5,6,17\\n"
    test = "x1,x2,y\\n6,7,20\\n7,8,23\\n"
    (tmp_path / "train.csv").write_text(train)
    (tmp_path / "test.csv").write_text(test)
    return str(tmp_path)


class TestPipeline:
    def test_run_returns_metrics(self, data_dir):
        pipe = Pipeline(data_dir, n_features=2, epochs=50)
        metrics = pipe.run("train.csv", "test.csv", "y", ["x1", "x2"])
        assert "mse" in metrics
        assert "rmse" in metrics
        assert "mae" in metrics

    def test_history_recorded(self, data_dir):
        pipe = Pipeline(data_dir, n_features=2, epochs=10)
        pipe.run("train.csv", "test.csv", "y", ["x1", "x2"])
        assert len(pipe.history) == 10

    def test_missing_train_file_raises(self, data_dir):
        pipe = Pipeline(data_dir, n_features=2)
        with pytest.raises(FileNotFoundError):
            pipe.run("nonexistent.csv", "test.csv", "y", ["x1", "x2"])
''')

    # --- requirements.txt ---
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write('pytest>=7.0\npytest-cov>=4.0\n')

    # --- README.md ---
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write('''# ML Pipeline

A lightweight machine learning pipeline for tabular data regression tasks.

## Structure

- `src/data_loader.py` - Data loading and preprocessing utilities
- `src/model.py` - Linear regression model implementation
- `src/pipeline.py` - End-to-end pipeline orchestration
- `tests/` - Test suite (pytest)

## Running Tests

```bash
pytest tests/ -v
```
''')

    # --- conftest.py at project root for pytest path resolution ---
    with open(os.path.join(PROJECT_DIR, 'conftest.py'), 'w') as f:
        f.write('''"""Root conftest for pytest path resolution."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
''')

    # Ensure NO .vscode/tasks.json exists
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    tasks_path = os.path.join(vscode_dir, 'tasks.json')
    if os.path.exists(tasks_path):
        os.remove(tasks_path)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'Tests directory: {TESTS_DIR}')
    print(f'.vscode/tasks.json does NOT exist (as required)')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

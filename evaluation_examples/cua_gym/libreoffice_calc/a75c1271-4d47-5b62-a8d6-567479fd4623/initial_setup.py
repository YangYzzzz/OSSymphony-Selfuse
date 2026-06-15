"""
Initial Setup: Configure VSCode Python debugging with pytest-xdist
Task ID: vscode_gf1_085
Domain: vscode

Creates the project directory with sample pytest files and opens VSCode.
Does NOT create launch.json — that is the agent's task.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf1_085'
PROJECT_DIR = f'{WORKDIR}/projects/parallel-tests'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'


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
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # Create pyproject.toml with pytest-xdist config
    pyproject_content = """\
[project]
name = "parallel-tests"
version = "1.0.0"
description = "Data pipeline with parallel test suite"
requires-python = ">=3.9"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-n auto"
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
]

[tool.pytest-xdist]
numprocesses = "auto"
"""
    with open(f'{PROJECT_DIR}/pyproject.toml', 'w') as f:
        f.write(pyproject_content)

    # Create conftest.py
    conftest_content = """\
import pytest
import os
import tempfile

@pytest.fixture
def temp_data_dir():
    \"\"\"Create a temporary directory for test data.\"\"\"
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

@pytest.fixture
def sample_config():
    \"\"\"Return sample configuration for pipeline tests.\"\"\"
    return {
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "pipeline_test_db",
        },
        "batch_size": 1000,
        "max_retries": 3,
        "timeout_seconds": 30,
    }

@pytest.fixture
def mock_api_response():
    \"\"\"Return mock API response data.\"\"\"
    return {
        "status": "success",
        "data": [
            {"id": 1, "name": "Widget A", "price": 29.99},
            {"id": 2, "name": "Widget B", "price": 45.50},
            {"id": 3, "name": "Gadget X", "price": 89.00},
        ],
        "total_count": 3,
    }
"""
    with open(f'{PROJECT_DIR}/tests/conftest.py', 'w') as f:
        f.write(conftest_content)

    # Create main source module
    src_init = """\
\"\"\"Parallel Tests - Data Pipeline Package.\"\"\"

__version__ = "1.0.0"
"""
    with open(f'{PROJECT_DIR}/src/__init__.py', 'w') as f:
        f.write(src_init)

    pipeline_content = """\
\"\"\"Data pipeline processing module.\"\"\"

import csv
import json
import os
from typing import Any, Dict, List, Optional


class DataPipeline:
    \"\"\"Main data pipeline class for ETL operations.\"\"\"

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.batch_size = config.get("batch_size", 500)
        self.max_retries = config.get("max_retries", 3)
        self._processed_count = 0

    def extract(self, source_path: str) -> List[Dict[str, Any]]:
        \"\"\"Extract data from a CSV source file.\"\"\"
        records = []
        with open(source_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(dict(row))
        return records

    def transform(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        \"\"\"Apply transformations to extracted records.\"\"\"
        transformed = []
        for record in records:
            t = {k.lower().replace(" ", "_"): v for k, v in record.items()}
            if "price" in t:
                t["price"] = float(t["price"])
            if "quantity" in t:
                t["quantity"] = int(t["quantity"])
            transformed.append(t)
        self._processed_count += len(transformed)
        return transformed

    def load(self, records: List[Dict[str, Any]], output_path: str) -> int:
        \"\"\"Load transformed records to JSON output.\"\"\"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(records, f, indent=2)
        return len(records)

    @property
    def processed_count(self) -> int:
        return self._processed_count

    def validate_record(self, record: Dict[str, Any]) -> bool:
        \"\"\"Validate a single record has required fields.\"\"\"
        required = {"id", "name"}
        return required.issubset(record.keys())

    def process_batch(self, records: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        \"\"\"Split records into batches.\"\"\"
        return [
            records[i : i + self.batch_size]
            for i in range(0, len(records), self.batch_size)
        ]
"""
    with open(f'{PROJECT_DIR}/src/pipeline.py', 'w') as f:
        f.write(pipeline_content)

    # Create test files
    test_pipeline_content = """\
\"\"\"Tests for the data pipeline module.\"\"\"

import json
import os
import csv
import pytest
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from pipeline import DataPipeline


class TestDataPipelineExtract:
    def test_extract_csv_records(self, temp_data_dir):
        csv_path = os.path.join(temp_data_dir, "input.csv")
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "name", "price"])
            writer.writeheader()
            writer.writerow({"id": "1", "name": "Widget A", "price": "29.99"})
            writer.writerow({"id": "2", "name": "Widget B", "price": "45.50"})
        pipe = DataPipeline({"batch_size": 100})
        records = pipe.extract(csv_path)
        assert len(records) == 2
        assert records[0]["name"] == "Widget A"

    def test_extract_empty_file(self, temp_data_dir):
        csv_path = os.path.join(temp_data_dir, "empty.csv")
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "name"])
            writer.writeheader()
        pipe = DataPipeline({"batch_size": 100})
        records = pipe.extract(csv_path)
        assert len(records) == 0


class TestDataPipelineTransform:
    def test_transform_lowercase_keys(self):
        pipe = DataPipeline({"batch_size": 100})
        records = [{"Product Name": "Gadget", "Price": "19.99"}]
        result = pipe.transform(records)
        assert "product_name" in result[0]

    def test_transform_numeric_conversion(self):
        pipe = DataPipeline({"batch_size": 100})
        records = [{"price": "99.95", "quantity": "10"}]
        result = pipe.transform(records)
        assert result[0]["price"] == 99.95
        assert result[0]["quantity"] == 10

    def test_processed_count_increments(self):
        pipe = DataPipeline({"batch_size": 100})
        pipe.transform([{"a": "1"}, {"b": "2"}])
        pipe.transform([{"c": "3"}])
        assert pipe.processed_count == 3


class TestDataPipelineLoad:
    def test_load_to_json(self, temp_data_dir):
        pipe = DataPipeline({"batch_size": 100})
        output = os.path.join(temp_data_dir, "out", "data.json")
        records = [{"id": 1, "name": "Test Item"}]
        count = pipe.load(records, output)
        assert count == 1
        with open(output) as f:
            loaded = json.load(f)
        assert loaded[0]["name"] == "Test Item"


class TestDataPipelineValidation:
    def test_valid_record(self):
        pipe = DataPipeline({})
        assert pipe.validate_record({"id": 1, "name": "Item"}) is True

    def test_invalid_record_missing_name(self):
        pipe = DataPipeline({})
        assert pipe.validate_record({"id": 1}) is False

    @pytest.mark.slow
    def test_large_batch_processing(self):
        pipe = DataPipeline({"batch_size": 50})
        records = [{"id": i, "name": f"Item {i}"} for i in range(200)]
        batches = pipe.process_batch(records)
        assert len(batches) == 4
        assert all(len(b) == 50 for b in batches)
"""
    with open(f'{PROJECT_DIR}/tests/test_pipeline.py', 'w') as f:
        f.write(test_pipeline_content)

    test_integration_content = """\
\"\"\"Integration tests for the full pipeline workflow.\"\"\"

import csv
import json
import os
import pytest
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from pipeline import DataPipeline


@pytest.mark.integration
class TestPipelineIntegration:
    def test_full_etl_workflow(self, temp_data_dir, sample_config):
        # Setup source CSV
        csv_path = os.path.join(temp_data_dir, "sales.csv")
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "name", "price", "quantity"])
            writer.writeheader()
            writer.writerow({"id": "101", "name": "Laptop Stand", "price": "49.99", "quantity": "5"})
            writer.writerow({"id": "102", "name": "USB Hub", "price": "24.99", "quantity": "12"})
            writer.writerow({"id": "103", "name": "Monitor Arm", "price": "129.00", "quantity": "3"})

        pipe = DataPipeline(sample_config)
        raw = pipe.extract(csv_path)
        transformed = pipe.transform(raw)
        output = os.path.join(temp_data_dir, "output", "processed.json")
        count = pipe.load(transformed, output)

        assert count == 3
        assert pipe.processed_count == 3
        with open(output) as f:
            data = json.load(f)
        assert data[0]["price"] == 49.99
        assert data[1]["quantity"] == 12

    def test_batch_then_load(self, temp_data_dir, sample_config):
        pipe = DataPipeline({**sample_config, "batch_size": 2})
        records = [
            {"id": i, "name": f"Product {i}", "price": str(i * 10.5)}
            for i in range(1, 6)
        ]
        transformed = pipe.transform(records)
        batches = pipe.process_batch(transformed)
        assert len(batches) == 3  # 5 records / batch_size 2 = 3 batches

        for idx, batch in enumerate(batches):
            out = os.path.join(temp_data_dir, "batches", f"batch_{idx}.json")
            pipe.load(batch, out)
            assert os.path.exists(out)
"""
    with open(f'{PROJECT_DIR}/tests/test_integration.py', 'w') as f:
        f.write(test_integration_content)

    # Create a VSCode settings.json for the workspace (NOT launch.json)
    workspace_settings = {
        "python.defaultInterpreterPath": "/usr/bin/python3",
        "python.testing.pytestEnabled": True,
        "python.testing.pytestArgs": [
            "tests"
        ],
        "editor.formatOnSave": True,
        "files.trimTrailingWhitespace": True,
    }
    with open(f'{VSCODE_DIR}/settings.json', 'w') as f:
        json.dump(workspace_settings, f, indent=4)

    # Create a README for context
    readme_content = """\
# Parallel Tests

Data pipeline project with pytest-xdist for parallel test execution.

## Running Tests

```bash
# Run tests in parallel (default with pytest-xdist)
pytest

# Run tests sequentially
pytest -p no:xdist

# Run only unit tests
pytest tests/test_pipeline.py

# Run integration tests
pytest -m integration
```

## Project Structure

```
parallel-tests/
├── src/
│   ├── __init__.py
│   └── pipeline.py
├── tests/
│   ├── conftest.py
│   ├── test_pipeline.py
│   └── test_integration.py
├── .vscode/
│   └── settings.json
└── pyproject.toml
```
"""
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme_content)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  Files: pyproject.toml, src/pipeline.py, tests/test_pipeline.py, tests/test_integration.py')
    print(f'  .vscode/settings.json (workspace settings, NO launch.json)')

    # GUI-ready: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

"""
Initial Setup: Create a Python package project structure for debugging task
Task ID: vscode_td_089
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_089'
PROJECT_DIR = f'{WORKDIR}/projects/mypackage'

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
    os.makedirs(f'{PROJECT_DIR}/mypackage', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/config', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # --- setup.py ---
    with open(f'{PROJECT_DIR}/setup.py', 'w') as f:
        f.write('''from setuptools import setup, find_packages

setup(
    name="mypackage",
    version="0.3.1",
    description="Data processing pipeline for customer analytics",
    author="Elena Rodriguez",
    author_email="elena.rodriguez@analyticsco.com",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.5.0",
        "pyyaml>=6.0",
        "click>=8.0",
        "sqlalchemy>=2.0",
    ],
    entry_points={
        "console_scripts": [
            "mypackage=mypackage.main:cli",
        ],
    },
    python_requires=">=3.9",
)
''')

    # --- mypackage/__init__.py ---
    with open(f'{PROJECT_DIR}/mypackage/__init__.py', 'w') as f:
        f.write('''"""Customer analytics data processing pipeline."""

__version__ = "0.3.1"
__author__ = "Elena Rodriguez"
''')

    # --- mypackage/main.py ---
    with open(f'{PROJECT_DIR}/mypackage/main.py', 'w') as f:
        f.write('''"""Main entry point for the data processing pipeline."""

import argparse
import os
import sys
import yaml


def load_config(config_path: str) -> dict:
    """Load YAML configuration file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def run_pipeline(config: dict):
    """Execute the data processing pipeline with the given configuration."""
    db_url = config.get("database", {}).get("url", "sqlite:///data.db")
    batch_size = config.get("processing", {}).get("batch_size", 1000)
    output_dir = config.get("output", {}).get("directory", "./output")

    print(f"Connecting to database: {db_url}")
    print(f"Processing with batch size: {batch_size}")
    print(f"Output directory: {output_dir}")

    os.makedirs(output_dir, exist_ok=True)

    # Pipeline stages
    stages = config.get("stages", ["extract", "transform", "load"])
    for stage in stages:
        print(f"Running stage: {stage}")

    print("Pipeline completed successfully.")


def cli():
    """Command-line interface for the pipeline."""
    parser = argparse.ArgumentParser(
        description="Customer Analytics Data Processing Pipeline"
    )
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to YAML configuration file",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate configuration without running pipeline",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging output",
    )

    args = parser.parse_args()
    config = load_config(args.config)

    if args.dry_run:
        print("Configuration validated successfully.")
        print(f"Stages: {config.get('stages', [])}")
        return

    run_pipeline(config)


if __name__ == "__main__":
    cli()
''')

    # --- mypackage/pipeline.py ---
    with open(f'{PROJECT_DIR}/mypackage/pipeline.py', 'w') as f:
        f.write('''"""Core pipeline processing logic."""

from dataclasses import dataclass, field
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class PipelineConfig:
    """Configuration for a pipeline run."""
    source_table: str
    destination_table: str
    batch_size: int = 1000
    max_retries: int = 3
    filters: List[str] = field(default_factory=list)
    dry_run: bool = False


class DataPipeline:
    """Main data processing pipeline."""

    def __init__(self, config: PipelineConfig):
        self.config = config
        self._stages = []

    def add_stage(self, stage_name: str, transform_func=None):
        """Register a processing stage."""
        self._stages.append({
            "name": stage_name,
            "transform": transform_func,
        })
        logger.info(f"Added stage: {stage_name}")

    def execute(self) -> dict:
        """Run all pipeline stages sequentially."""
        results = {"stages_completed": 0, "records_processed": 0}

        for stage in self._stages:
            logger.info(f"Executing stage: {stage['name']}")
            if stage["transform"]:
                stage["transform"]()
            results["stages_completed"] += 1

        return results
''')

    # --- mypackage/models.py ---
    with open(f'{PROJECT_DIR}/mypackage/models.py', 'w') as f:
        f.write('''"""Data models for customer analytics."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Customer:
    customer_id: str
    name: str
    email: str
    signup_date: datetime
    tier: str = "standard"
    lifetime_value: float = 0.0
    region: Optional[str] = None


@dataclass
class Transaction:
    transaction_id: str
    customer_id: str
    amount: float
    timestamp: datetime
    category: str
    status: str = "completed"


@dataclass
class AnalyticsReport:
    report_id: str
    generated_at: datetime
    total_customers: int
    total_revenue: float
    avg_order_value: float
    churn_rate: float
''')

    # --- config/dev.yaml ---
    with open(f'{PROJECT_DIR}/config/dev.yaml', 'w') as f:
        f.write('''# Development configuration for customer analytics pipeline

database:
  url: "sqlite:///dev_data.db"
  pool_size: 5
  echo: true

processing:
  batch_size: 100
  max_workers: 2
  timeout_seconds: 30

output:
  directory: "./output/dev"
  format: "csv"
  include_metadata: true

stages:
  - extract
  - validate
  - transform
  - aggregate
  - load

logging:
  level: "DEBUG"
  file: "logs/pipeline_dev.log"
''')

    # --- config/prod.yaml ---
    with open(f'{PROJECT_DIR}/config/prod.yaml', 'w') as f:
        f.write('''# Production configuration for customer analytics pipeline

database:
  url: "postgresql://analytics:${DB_PASSWORD}@db.analyticsco.internal:5432/customers"
  pool_size: 20
  echo: false

processing:
  batch_size: 5000
  max_workers: 8
  timeout_seconds: 300

output:
  directory: "/data/reports/production"
  format: "parquet"
  include_metadata: true

stages:
  - extract
  - validate
  - transform
  - aggregate
  - load
  - notify

logging:
  level: "WARNING"
  file: "/var/log/analytics/pipeline.log"
''')

    # --- tests/__init__.py ---
    with open(f'{PROJECT_DIR}/tests/__init__.py', 'w') as f:
        f.write('')

    # --- tests/test_pipeline.py ---
    with open(f'{PROJECT_DIR}/tests/test_pipeline.py', 'w') as f:
        f.write('''"""Unit tests for the data processing pipeline."""

import unittest
from mypackage.pipeline import DataPipeline, PipelineConfig


class TestPipeline(unittest.TestCase):

    def setUp(self):
        self.config = PipelineConfig(
            source_table="raw_customers",
            destination_table="processed_customers",
            batch_size=100,
        )
        self.pipeline = DataPipeline(self.config)

    def test_add_stage(self):
        self.pipeline.add_stage("extract")
        self.assertEqual(len(self.pipeline._stages), 1)

    def test_execute_empty_pipeline(self):
        results = self.pipeline.execute()
        self.assertEqual(results["stages_completed"], 0)

    def test_execute_with_stages(self):
        self.pipeline.add_stage("extract")
        self.pipeline.add_stage("transform")
        results = self.pipeline.execute()
        self.assertEqual(results["stages_completed"], 2)


if __name__ == "__main__":
    unittest.main()
''')

    # --- README.md ---
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write('''# mypackage - Customer Analytics Pipeline

A data processing pipeline for customer analytics, supporting extraction,
transformation, and loading of customer transaction data.

## Installation

```bash
pip install -e .
```

## Usage

```bash
mypackage --config config/dev.yaml
```

## Development

Run tests:
```bash
python -m pytest tests/
```
''')

    # --- .gitignore ---
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write('''__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.eggs/
*.egg
output/
logs/
*.db
.env
''')

    # Simulate pip install -e by creating egg-info
    os.makedirs(f'{PROJECT_DIR}/mypackage.egg-info', exist_ok=True)
    with open(f'{PROJECT_DIR}/mypackage.egg-info/PKG-INFO', 'w') as f:
        f.write('''Metadata-Version: 2.1
Name: mypackage
Version: 0.3.1
Summary: Data processing pipeline for customer analytics
Author: Elena Rodriguez
Author-email: elena.rodriguez@analyticsco.com
Requires-Python: >=3.9
''')

    # Ensure NO .vscode/launch.json exists (the task is to create it)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    if os.path.exists(f'{vscode_dir}/launch.json'):
        os.remove(f'{vscode_dir}/launch.json')

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'Project structure:')
    for root, dirs, files in os.walk(PROJECT_DIR):
        # Skip __pycache__
        dirs[:] = [d for d in dirs if d != '__pycache__']
        level = root.replace(PROJECT_DIR, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f'{subindent}{file}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()

"""
Initial Setup: Create a Python project structure without .vscode configuration.
Task ID: vscode_file_037
Domain: vs_code
"""

import os
import shlex
import subprocess
import time
import shutil

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_037'
PROJECT_DIR = f'{WORKDIR}/analytics'


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
    # Remove any existing project directory to ensure clean state
    if os.path.exists(PROJECT_DIR):
        shutil.rmtree(PROJECT_DIR)

    # Create project directory structure
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)

    # Create src/main.py — realistic Python entry point
    main_py = '''#!/usr/bin/env python3
"""
Analytics Pipeline Entry Point

This module serves as the main entry point for the analytics data pipeline.
It orchestrates data loading, processing, and reporting workflows.
"""

import sys
import os
import logging
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_loader import DataLoader

logging.basicConfig(
    level=logging.INFO,
    format=\'%(asctime)s - %(name)s - %(levelname)s - %(message)s\'
)
logger = logging.getLogger(__name__)


def run_pipeline(data_path: str, output_dir: str = None) -> dict:
    """
    Run the full analytics pipeline.

    Args:
        data_path: Path to input data file or directory
        output_dir: Optional output directory for results

    Returns:
        Dictionary with pipeline execution summary
    """
    logger.info(f"Starting analytics pipeline at {datetime.now().isoformat()}")

    loader = DataLoader()
    records = loader.load(data_path)
    logger.info(f"Loaded {len(records)} records from {data_path}")

    summary = {
        "total_records": len(records),
        "source": data_path,
        "timestamp": datetime.now().isoformat(),
        "status": "success"
    }

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        report_path = os.path.join(output_dir, "pipeline_report.txt")
        with open(report_path, "w") as f:
            for key, value in summary.items():
                f.write(f"{key}: {value}\\n")
        logger.info(f"Report written to {report_path}")

    logger.info("Pipeline completed successfully.")
    return summary


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <data_path> [output_dir]")
        sys.exit(1)

    data_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    result = run_pipeline(data_path, output_dir)
    print(f"Pipeline finished: {result['total_records']} records processed.")
'''

    with open(os.path.join(src_dir, 'main.py'), 'w') as f:
        f.write(main_py)

    # Create src/data_loader.py — realistic data loading module
    data_loader_py = '''"""
Data Loader Module

Handles loading and parsing of various data formats for the analytics pipeline.
Supports CSV, JSON, and plain text data sources.
"""

import os
import csv
import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class DataLoader:
    """
    Multi-format data loader supporting CSV, JSON, and text files.

    Attributes:
        encoding: File encoding to use when reading files (default: utf-8)
        max_rows: Maximum number of rows to load (None = unlimited)
    """

    SUPPORTED_FORMATS = [".csv", ".json", ".txt"]

    def __init__(self, encoding: str = "utf-8", max_rows: int = None):
        self.encoding = encoding
        self.max_rows = max_rows

    def load(self, path: str) -> List[Dict[str, Any]]:
        """
        Load data from a file or directory.

        Args:
            path: Path to file or directory containing data files

        Returns:
            List of records as dictionaries
        """
        if os.path.isdir(path):
            return self._load_directory(path)
        return self._load_file(path)

    def _load_directory(self, directory: str) -> List[Dict[str, Any]]:
        """Load all supported files from a directory."""
        records = []
        for filename in sorted(os.listdir(directory)):
            _, ext = os.path.splitext(filename)
            if ext.lower() in self.SUPPORTED_FORMATS:
                filepath = os.path.join(directory, filename)
                records.extend(self._load_file(filepath))
        return records

    def _load_file(self, filepath: str) -> List[Dict[str, Any]]:
        """Load data from a single file based on its extension."""
        _, ext = os.path.splitext(filepath)
        ext = ext.lower()

        if ext == ".csv":
            return self._load_csv(filepath)
        elif ext == ".json":
            return self._load_json(filepath)
        elif ext == ".txt":
            return self._load_text(filepath)
        else:
            logger.warning(f"Unsupported format: {ext} for file {filepath}")
            return []

    def _load_csv(self, filepath: str) -> List[Dict[str, Any]]:
        """Load CSV file into list of dicts."""
        records = []
        with open(filepath, "r", encoding=self.encoding, newline="") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if self.max_rows and i >= self.max_rows:
                    break
                records.append(dict(row))
        logger.debug(f"CSV loaded: {len(records)} rows from {filepath}")
        return records

    def _load_json(self, filepath: str) -> List[Dict[str, Any]]:
        """Load JSON file — supports list or single object."""
        with open(filepath, "r", encoding=self.encoding) as f:
            data = json.load(f)
        if isinstance(data, list):
            records = data if not self.max_rows else data[:self.max_rows]
        else:
            records = [data]
        logger.debug(f"JSON loaded: {len(records)} records from {filepath}")
        return records

    def _load_text(self, filepath: str) -> List[Dict[str, Any]]:
        """Load plain text file — each line becomes a record."""
        records = []
        with open(filepath, "r", encoding=self.encoding) as f:
            for i, line in enumerate(f):
                if self.max_rows and i >= self.max_rows:
                    break
                line = line.rstrip("\\n")
                if line:
                    records.append({"line": i + 1, "content": line})
        logger.debug(f"Text loaded: {len(records)} lines from {filepath}")
        return records
'''

    with open(os.path.join(src_dir, 'data_loader.py'), 'w') as f:
        f.write(data_loader_py)

    # Create requirements.txt — realistic Python project dependencies
    requirements_txt = '''# Analytics Pipeline Dependencies
# Core data processing
pandas>=2.0.0
numpy>=1.24.0

# Data formats
openpyxl>=3.1.0
xlrd>=2.0.1

# Logging and monitoring
colorlog>=6.7.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0

# Type checking
mypy>=1.5.0

# Code formatting
black>=23.7.0
isort>=5.12.0
'''

    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write(requirements_txt)

    # Ensure NO .vscode directory exists (task requires creating it)
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        shutil.rmtree(vscode_dir)

    print(f'Project structure created at: {PROJECT_DIR}')
    print(f'  - src/main.py')
    print(f'  - src/data_loader.py')
    print(f'  - requirements.txt')
    print(f'  - No .vscode/ folder (task requires creating it)')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project folder, DISPLAY=:0')


create_initial()

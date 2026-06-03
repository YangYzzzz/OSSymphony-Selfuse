"""
Initial Setup: Configure VSCode to find Python venv in non-standard location
Task ID: vscode_fix_051
Domain: vscode

Creates:
- A Python project at ~/myproject with realistic files
- A virtual environment at /opt/venvs/myproject (with bin/python stub)
- VSCode user settings with empty python.venvFolders
- Opens VSCode with ~/myproject
"""

import json
import os
import shlex
import subprocess
import stat
import time

HOME = '/home/user'
TASK_ID = 'vscode_fix_051'
PROJECT_DIR = os.path.join(HOME, 'myproject')
VENV_DIR = '/opt/venvs/myproject'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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


def create_project():
    """Create a realistic Python project."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # main.py
    with open(os.path.join(PROJECT_DIR, 'main.py'), 'w') as f:
        f.write('''\
"""
Data Pipeline Manager - Main Entry Point
Orchestrates ETL workflows for the analytics platform.
"""

import os
import sys
from pathlib import Path

from pipeline.extractor import DataExtractor
from pipeline.transformer import DataTransformer
from pipeline.loader import DataLoader
from utils.config import load_config
from utils.logger import setup_logging


def run_pipeline(config_path: str = "config/pipeline.yaml"):
    """Execute the full ETL pipeline."""
    logger = setup_logging("pipeline")
    config = load_config(config_path)

    logger.info("Starting data pipeline run")

    extractor = DataExtractor(config["sources"])
    raw_data = extractor.fetch_all()
    logger.info(f"Extracted {len(raw_data)} records from {len(config['sources'])} sources")

    transformer = DataTransformer(config["transformations"])
    clean_data = transformer.apply(raw_data)
    logger.info(f"Transformed data: {len(clean_data)} records after filtering")

    loader = DataLoader(config["output"])
    loader.write(clean_data)
    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    config_file = sys.argv[1] if len(sys.argv) > 1 else "config/pipeline.yaml"
    run_pipeline(config_file)
''')

    # pipeline package
    pipeline_dir = os.path.join(PROJECT_DIR, 'pipeline')
    os.makedirs(pipeline_dir, exist_ok=True)
    with open(os.path.join(pipeline_dir, '__init__.py'), 'w') as f:
        f.write('"""Pipeline module for ETL operations."""\n')

    with open(os.path.join(pipeline_dir, 'extractor.py'), 'w') as f:
        f.write('''\
"""Data extraction module - connects to various data sources."""

import csv
import json
from typing import Any, Dict, List


class DataExtractor:
    def __init__(self, sources: List[Dict[str, Any]]):
        self.sources = sources

    def fetch_all(self) -> List[Dict]:
        results = []
        for source in self.sources:
            if source["type"] == "csv":
                results.extend(self._read_csv(source["path"]))
            elif source["type"] == "json":
                results.extend(self._read_json(source["path"]))
        return results

    def _read_csv(self, path: str) -> List[Dict]:
        with open(path, "r") as f:
            reader = csv.DictReader(f)
            return list(reader)

    def _read_json(self, path: str) -> List[Dict]:
        with open(path, "r") as f:
            return json.load(f)
''')

    with open(os.path.join(pipeline_dir, 'transformer.py'), 'w') as f:
        f.write('''\
"""Data transformation and cleaning module."""

from typing import Any, Dict, List


class DataTransformer:
    def __init__(self, rules: List[Dict[str, Any]]):
        self.rules = rules

    def apply(self, data: List[Dict]) -> List[Dict]:
        result = data
        for rule in self.rules:
            if rule["action"] == "filter":
                result = [r for r in result if self._matches(r, rule)]
            elif rule["action"] == "rename":
                result = [self._rename_keys(r, rule["mapping"]) for r in result]
        return result

    @staticmethod
    def _matches(record: Dict, rule: Dict) -> bool:
        field = rule["field"]
        return field in record and record[field] is not None

    @staticmethod
    def _rename_keys(record: Dict, mapping: Dict[str, str]) -> Dict:
        return {mapping.get(k, k): v for k, v in record.items()}
''')

    with open(os.path.join(pipeline_dir, 'loader.py'), 'w') as f:
        f.write('''\
"""Data loading module - writes processed data to output destinations."""

import csv
import json
import os
from typing import Any, Dict, List


class DataLoader:
    def __init__(self, config: Dict[str, Any]):
        self.output_dir = config.get("directory", "output")
        self.format = config.get("format", "csv")

    def write(self, data: List[Dict]):
        os.makedirs(self.output_dir, exist_ok=True)
        output_path = os.path.join(self.output_dir, f"results.{self.format}")
        if self.format == "csv":
            self._write_csv(output_path, data)
        elif self.format == "json":
            self._write_json(output_path, data)

    @staticmethod
    def _write_csv(path: str, data: List[Dict]):
        if not data:
            return
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
    def _write_json(path: str, data: List[Dict]):
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
''')

    # utils package
    utils_dir = os.path.join(PROJECT_DIR, 'utils')
    os.makedirs(utils_dir, exist_ok=True)
    with open(os.path.join(utils_dir, '__init__.py'), 'w') as f:
        f.write('"""Utility modules."""\n')

    with open(os.path.join(utils_dir, 'config.py'), 'w') as f:
        f.write('''\
"""Configuration loading utilities."""

import json
import os


def load_config(path: str) -> dict:
    """Load pipeline configuration from a JSON or YAML file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r") as f:
        return json.load(f)
''')

    with open(os.path.join(utils_dir, 'logger.py'), 'w') as f:
        f.write('''\
"""Logging setup for the pipeline."""

import logging
import sys


def setup_logging(name: str, level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")
    )
    logger.addHandler(handler)
    return logger
''')

    # requirements.txt
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write('''\
pandas>=2.0.0
numpy>=1.24.0
requests>=2.28.0
pyyaml>=6.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
pytest>=7.3.0
black>=23.0.0
''')

    # README
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write('''\
# Data Pipeline Manager

ETL pipeline framework for the analytics platform.

## Setup

```bash
source /opt/venvs/myproject/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py config/pipeline.yaml
```
''')

    print(f"Project created at {PROJECT_DIR}")


def create_venv():
    """Create a fake virtual environment at /opt/venvs/myproject."""
    # /opt requires root to create dirs
    def sudo_run(cmd):
        subprocess.run(f"echo 'password' | sudo -S {cmd}", shell=True, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    sudo_run(f'mkdir -p {os.path.join(VENV_DIR, "bin")}')
    sudo_run(f'mkdir -p {os.path.join(VENV_DIR, "lib", "python3.10", "site-packages")}')
    sudo_run('chown -R user:user /opt/venvs')
    bin_dir = os.path.join(VENV_DIR, 'bin')
    lib_dir = os.path.join(VENV_DIR, 'lib', 'python3.10', 'site-packages')

    # Create python executable (symlink to system python)
    python_path = os.path.join(bin_dir, 'python')
    if not os.path.exists(python_path):
        # Find system python
        system_python = '/usr/bin/python3'
        if not os.path.exists(system_python):
            system_python = '/usr/bin/python'
        os.symlink(system_python, python_path)

    python3_path = os.path.join(bin_dir, 'python3')
    if not os.path.exists(python3_path):
        os.symlink(python_path, python3_path)

    # Create activate script
    with open(os.path.join(bin_dir, 'activate'), 'w') as f:
        f.write(f'''\
# This file must be used with "source bin/activate" *from bash*
VIRTUAL_ENV="{VENV_DIR}"
export VIRTUAL_ENV
_OLD_VIRTUAL_PATH="$PATH"
PATH="$VIRTUAL_ENV/bin:$PATH"
export PATH
''')

    # Create pip stub
    pip_path = os.path.join(bin_dir, 'pip')
    with open(pip_path, 'w') as f:
        f.write(f'''\
#!/usr/bin/env python3
import sys
print("pip 23.2.1 from {VENV_DIR}/lib/python3.10/site-packages/pip (python 3.10)")
''')
    os.chmod(pip_path, os.stat(pip_path).st_mode | stat.S_IEXEC)

    # pyvenv.cfg
    with open(os.path.join(VENV_DIR, 'pyvenv.cfg'), 'w') as f:
        f.write('''\
home = /usr/bin
include-system-site-packages = false
version = 3.10.12
''')

    print(f"Virtual environment created at {VENV_DIR}")


def configure_vscode():
    """Set up VSCode user settings with empty python.venvFolders."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings if any
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Set initial state: python.venvFolders is empty, no defaultInterpreterPath
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.formatOnSave": True,
        "workbench.colorTheme": "Default Dark Modern",
        "python.venvFolders": [],
        "python.analysis.autoSearchPaths": True,
        "python.analysis.typeCheckingMode": "basic",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000
    })

    # Ensure python.defaultInterpreterPath is NOT set to the venv
    if "python.defaultInterpreterPath" in settings:
        if "/opt/venvs" in str(settings["python.defaultInterpreterPath"]):
            del settings["python.defaultInterpreterPath"]

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f"VSCode settings configured at {SETTINGS_PATH}")


def main():
    create_project()
    create_venv()
    configure_vscode()

    # Open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: VSCode launched with ~/myproject')


main()

"""
Initial Setup: Turn on breadcrumb navigation in VSCode
Task ID: vscode_stu_054
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
WORKSPACE_DIR = os.path.join(HOME, 'workspace')


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


def load_settings():
    try:
        with open(SETTINGS_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def update_settings(updates: dict):
    settings = load_settings()
    settings.update(updates)
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)


def create_text_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def create_workspace():
    """Create a nested Python project structure."""

    # Top-level main.py
    create_text_file(os.path.join(WORKSPACE_DIR, 'main.py'), '''\
"""
Data Analytics Pipeline - Main Entry Point
"""
from src.pipeline.processor import DataProcessor
from src.pipeline.validators import InputValidator
from src.utils.config import load_config


def main():
    config = load_config("config/settings.yaml")
    validator = InputValidator(config)
    processor = DataProcessor(config)

    raw_data = processor.load_raw_data("data/input/sales_q1_2025.csv")
    validated = validator.validate(raw_data)
    results = processor.transform(validated)
    processor.export(results, "data/output/report.csv")
    print(f"Pipeline complete: {len(results)} records processed.")


if __name__ == "__main__":
    main()
''')

    # src/pipeline/processor.py
    create_text_file(os.path.join(WORKSPACE_DIR, 'src', 'pipeline', 'processor.py'), '''\
"""
Data processing module for the analytics pipeline.
"""
import csv
from datetime import datetime
from typing import List, Dict, Any


class DataProcessor:
    def __init__(self, config: dict):
        self.config = config
        self.batch_size = config.get("batch_size", 500)
        self.output_format = config.get("output_format", "csv")

    def load_raw_data(self, filepath: str) -> List[Dict[str, Any]]:
        records = []
        with open(filepath, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(dict(row))
        return records

    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for record in data:
            transformed = {
                "date": datetime.strptime(record["date"], "%Y-%m-%d"),
                "region": record["region"].strip().title(),
                "revenue": float(record["revenue"]),
                "units_sold": int(record["units_sold"]),
                "unit_price": float(record["revenue"]) / max(int(record["units_sold"]), 1),
            }
            results.append(transformed)
        return results

    def export(self, data: List[Dict[str, Any]], filepath: str):
        if not data:
            return
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
''')

    # src/pipeline/validators.py
    create_text_file(os.path.join(WORKSPACE_DIR, 'src', 'pipeline', 'validators.py'), '''\
"""
Input validation for pipeline data.
"""
from typing import List, Dict, Any


class InputValidator:
    REQUIRED_FIELDS = ["date", "region", "revenue", "units_sold"]

    def __init__(self, config: dict):
        self.strict_mode = config.get("strict_validation", False)

    def validate(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        valid = []
        for i, record in enumerate(records):
            missing = [f for f in self.REQUIRED_FIELDS if f not in record]
            if missing:
                if self.strict_mode:
                    raise ValueError(f"Row {i}: missing fields {missing}")
                continue
            if float(record.get("revenue", 0)) < 0:
                continue
            valid.append(record)
        return valid
''')

    # src/pipeline/__init__.py
    create_text_file(os.path.join(WORKSPACE_DIR, 'src', 'pipeline', '__init__.py'), '')
    create_text_file(os.path.join(WORKSPACE_DIR, 'src', '__init__.py'), '')

    # src/utils/config.py
    create_text_file(os.path.join(WORKSPACE_DIR, 'src', 'utils', 'config.py'), '''\
"""
Configuration loader utility.
"""
import json
import os


def load_config(filepath: str) -> dict:
    """Load configuration from a YAML or JSON file."""
    if not os.path.exists(filepath):
        return _default_config()
    with open(filepath, "r") as f:
        return json.load(f)


def _default_config():
    return {
        "batch_size": 500,
        "output_format": "csv",
        "strict_validation": False,
        "log_level": "INFO",
    }
''')

    create_text_file(os.path.join(WORKSPACE_DIR, 'src', 'utils', '__init__.py'), '')

    print(f"Workspace created at {WORKSPACE_DIR}")


def setup_vscode_settings():
    """Set VSCode settings with breadcrumbs explicitly disabled."""
    update_settings({
        "breadcrumbs.enabled": False,
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.wordWrap": "off",
        "workbench.colorTheme": "Default Dark Modern",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
        "editor.minimap.enabled": True,
    })
    print(f"VSCode settings written to {SETTINGS_PATH} with breadcrumbs.enabled = false")


def main():
    create_workspace()
    setup_vscode_settings()

    # Open VSCode with the workspace folder and a nested file
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    launch_gui(f'code "{WORKSPACE_DIR}/src/pipeline/processor.py"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


main()

"""
Initial Setup: Set up workspace trust settings to restrict untrusted workspaces
Task ID: vscode_lp_094
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_094'
PROJECT_DIR = f'{WORKDIR}/data-pipeline'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
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


def create_project_files():
    """Create a realistic project directory with source files."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Main Python script
    with open(os.path.join(PROJECT_DIR, 'pipeline.py'), 'w') as f:
        f.write('''"""Data Pipeline - ETL workflow for sales analytics."""

import csv
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class DataExtractor:
    """Extracts raw data from CSV sources."""

    def __init__(self, source_dir: str):
        self.source_dir = source_dir
        self.raw_records: List[Dict] = []

    def extract_csv(self, filename: str) -> List[Dict]:
        filepath = os.path.join(self.source_dir, filename)
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            records = list(reader)
        self.raw_records.extend(records)
        return records

    def extract_all(self) -> List[Dict]:
        for fname in os.listdir(self.source_dir):
            if fname.endswith('.csv'):
                self.extract_csv(fname)
        return self.raw_records


class DataTransformer:
    """Transforms and cleans extracted data."""

    def __init__(self, records: List[Dict]):
        self.records = records
        self.transformed: List[Dict] = []

    def clean_nulls(self) -> 'DataTransformer':
        self.records = [r for r in self.records if all(v for v in r.values())]
        return self

    def normalize_dates(self, date_field: str, fmt: str = '%Y-%m-%d') -> 'DataTransformer':
        for record in self.records:
            try:
                dt = datetime.strptime(record[date_field], fmt)
                record[date_field] = dt.isoformat()
            except (ValueError, KeyError):
                pass
        return self

    def compute_metrics(self) -> 'DataTransformer':
        for record in self.records:
            try:
                qty = float(record.get('quantity', 0))
                price = float(record.get('unit_price', 0))
                record['total_revenue'] = round(qty * price, 2)
                record['tax_amount'] = round(qty * price * 0.08, 2)
            except (ValueError, TypeError):
                record['total_revenue'] = 0.0
                record['tax_amount'] = 0.0
        self.transformed = self.records
        return self


class DataLoader:
    """Loads transformed data to output destination."""

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def load_json(self, records: List[Dict], filename: str) -> str:
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(records, f, indent=2)
        return filepath

    def load_summary(self, records: List[Dict], filename: str) -> str:
        total_revenue = sum(r.get('total_revenue', 0) for r in records)
        total_records = len(records)
        summary = {
            'generated_at': datetime.now().isoformat(),
            'total_records': total_records,
            'total_revenue': round(total_revenue, 2),
            'avg_revenue': round(total_revenue / max(total_records, 1), 2),
        }
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2)
        return filepath


def run_pipeline(source_dir: str, output_dir: str):
    """Execute the full ETL pipeline."""
    extractor = DataExtractor(source_dir)
    raw = extractor.extract_all()
    print(f"Extracted {len(raw)} records")

    transformer = DataTransformer(raw)
    transformer.clean_nulls().normalize_dates('date').compute_metrics()
    print(f"Transformed {len(transformer.transformed)} records")

    loader = DataLoader(output_dir)
    loader.load_json(transformer.transformed, 'processed_sales.json')
    loader.load_summary(transformer.transformed, 'summary.json')
    print("Pipeline complete")


if __name__ == '__main__':
    run_pipeline('./data/raw', './data/output')
''')

    # Config file
    with open(os.path.join(PROJECT_DIR, 'config.json'), 'w') as f:
        json.dump({
            "pipeline": {
                "name": "sales-analytics-etl",
                "version": "2.1.0",
                "schedule": "0 6 * * *",
                "source": {
                    "type": "csv",
                    "directory": "./data/raw",
                    "encoding": "utf-8"
                },
                "output": {
                    "type": "json",
                    "directory": "./data/output",
                    "compress": False
                },
                "notifications": {
                    "on_failure": "ops-team@company.com",
                    "on_success": False
                }
            }
        }, f, indent=2)

    # Test file
    with open(os.path.join(PROJECT_DIR, 'test_pipeline.py'), 'w') as f:
        f.write('''"""Unit tests for the data pipeline."""

import unittest
import os
import tempfile
import json
from pipeline import DataExtractor, DataTransformer, DataLoader


class TestDataTransformer(unittest.TestCase):

    def test_clean_nulls_removes_incomplete_records(self):
        records = [
            {"name": "Widget A", "quantity": "10", "unit_price": "5.99"},
            {"name": "", "quantity": "5", "unit_price": "3.49"},
            {"name": "Gadget C", "quantity": "8", "unit_price": "12.00"},
        ]
        transformer = DataTransformer(records)
        transformer.clean_nulls()
        self.assertEqual(len(transformer.records), 2)

    def test_compute_metrics_calculates_revenue(self):
        records = [
            {"quantity": "10", "unit_price": "5.99"},
        ]
        transformer = DataTransformer(records)
        transformer.compute_metrics()
        self.assertAlmostEqual(transformer.transformed[0]["total_revenue"], 59.90, places=2)
        self.assertAlmostEqual(transformer.transformed[0]["tax_amount"], 4.79, places=2)

    def test_compute_metrics_handles_missing_values(self):
        records = [{"quantity": "abc", "unit_price": "5.99"}]
        transformer = DataTransformer(records)
        transformer.compute_metrics()
        self.assertEqual(transformer.transformed[0]["total_revenue"], 0.0)


class TestDataLoader(unittest.TestCase):

    def test_load_json_creates_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            loader = DataLoader(tmpdir)
            records = [{"name": "test", "value": 42}]
            path = loader.load_json(records, "test_output.json")
            self.assertTrue(os.path.exists(path))
            with open(path) as f:
                loaded = json.load(f)
            self.assertEqual(loaded, records)


if __name__ == "__main__":
    unittest.main()
''')

    # Requirements file
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write('''pandas>=2.0.0
numpy>=1.24.0
requests>=2.28.0
python-dateutil>=2.8.2
boto3>=1.26.0
pytest>=7.3.0
''')

    # .vscode/tasks.json (workspace tasks that should be restricted)
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    os.makedirs(vscode_dir, exist_ok=True)
    with open(os.path.join(vscode_dir, 'tasks.json'), 'w') as f:
        json.dump({
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "Run Pipeline",
                    "type": "shell",
                    "command": "python3 pipeline.py",
                    "group": {
                        "kind": "build",
                        "isDefault": True
                    },
                    "problemMatcher": ["$pylint"]
                },
                {
                    "label": "Run Tests",
                    "type": "shell",
                    "command": "python3 -m pytest test_pipeline.py -v",
                    "group": "test"
                }
            ]
        }, f, indent=2)

    # .vscode/launch.json (debug config that should be restricted)
    with open(os.path.join(vscode_dir, 'launch.json'), 'w') as f:
        json.dump({
            "version": "0.2.0",
            "configurations": [
                {
                    "name": "Debug Pipeline",
                    "type": "python",
                    "request": "launch",
                    "program": "${workspaceFolder}/pipeline.py",
                    "console": "integratedTerminal",
                    "justMyCode": True
                }
            ]
        }, f, indent=2)

    # Sample data directory
    data_dir = os.path.join(PROJECT_DIR, 'data', 'raw')
    os.makedirs(data_dir, exist_ok=True)
    with open(os.path.join(data_dir, 'sales_q1_2025.csv'), 'w') as f:
        f.write('''date,product,quantity,unit_price,region
2025-01-05,Ergonomic Keyboard,24,79.99,North America
2025-01-12,USB-C Hub,56,34.50,Europe
2025-01-18,Monitor Stand,18,45.00,North America
2025-02-03,Wireless Mouse,42,29.99,Asia Pacific
2025-02-14,Laptop Sleeve,31,22.50,Europe
2025-02-22,Desk Lamp,15,67.00,North America
2025-03-01,Cable Organizer,88,12.99,Asia Pacific
2025-03-10,Webcam HD,27,89.99,Europe
2025-03-19,Headset Pro,33,149.00,North America
2025-03-28,Docking Station,12,199.99,Asia Pacific
''')

    print(f'Project directory created: {PROJECT_DIR}')


def setup_initial_vscode_settings():
    """Set up minimal VSCode settings - trust enabled but no restrictions configured."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Initial settings: trust is enabled, workspace is trusted, but NO restriction config
    settings = {
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.wordWrap": "on",
        "workbench.colorTheme": "Default Dark Modern",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
        "terminal.integrated.defaultProfile.linux": "bash",
        # Trust is enabled (per task context) but no restrictions configured
        "security.workspace.trust.enabled": True,
    }
    # Do NOT include restriction settings like startupPrompt, banner,
    # task.allowAutomaticTasks, etc. Those are the task completion items.

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'VSCode settings written: {SETTINGS_PATH}')


def main():
    create_project_files()
    setup_initial_vscode_settings()

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()

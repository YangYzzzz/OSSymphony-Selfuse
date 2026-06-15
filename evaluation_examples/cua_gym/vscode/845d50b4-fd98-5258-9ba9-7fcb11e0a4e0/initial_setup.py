"""
Initial Setup: Configure language-specific settings for Python files
Task ID: vscode_we_015
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_015'
WORKSPACE = f'{WORKDIR}/workspace'
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


def create_initial():
    # Create a Python project workspace
    os.makedirs(WORKSPACE, exist_ok=True)

    # Create some realistic Python files
    main_py = '''\
import pandas as pd
from data_processor import DataProcessor
from report_generator import ReportGenerator


def main():
    """Main entry point for the quarterly sales analysis pipeline."""
    processor = DataProcessor(source="quarterly_sales_2025.csv")
    cleaned_data = processor.clean()
    validated_data = processor.validate(cleaned_data)

    report = ReportGenerator(data=validated_data)
    report.generate_summary()
    report.export_pdf("Q1_2025_Sales_Report.pdf")
    print("Report generation complete.")


if __name__ == "__main__":
    main()
'''
    with open(os.path.join(WORKSPACE, 'main.py'), 'w') as f:
        f.write(main_py)

    data_processor_py = '''\
import csv
from datetime import datetime
from typing import List, Dict, Optional


class DataProcessor:
    """Handles data ingestion, cleaning, and validation for sales data."""

    def __init__(self, source: str):
        self.source = source
        self.raw_data: List[Dict] = []
        self.error_log: List[str] = []

    def clean(self) -> List[Dict]:
        """Remove duplicates, fix formatting, handle missing values."""
        cleaned = []
        seen_ids = set()
        for record in self.raw_data:
            record_id = record.get("transaction_id")
            if record_id in seen_ids:
                continue
            seen_ids.add(record_id)
            record["amount"] = float(record.get("amount", 0))
            record["date"] = self._parse_date(record.get("date", ""))
            cleaned.append(record)
        return cleaned

    def validate(self, data: List[Dict]) -> List[Dict]:
        """Validate cleaned data against business rules."""
        valid = []
        for record in data:
            if record["amount"] <= 0:
                self.error_log.append(f"Invalid amount: {record}")
                continue
            if record["date"] is None:
                self.error_log.append(f"Invalid date: {record}")
                continue
            valid.append(record)
        return valid

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d-%b-%Y"):
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return None
'''
    with open(os.path.join(WORKSPACE, 'data_processor.py'), 'w') as f:
        f.write(data_processor_py)

    report_gen_py = '''\
from typing import List, Dict


class ReportGenerator:
    """Generates formatted reports from processed sales data."""

    def __init__(self, data: List[Dict]):
        self.data = data
        self.summary: Dict = {}

    def generate_summary(self) -> Dict:
        """Calculate key metrics for the report."""
        total_sales = sum(r["amount"] for r in self.data)
        avg_sale = total_sales / len(self.data) if self.data else 0
        self.summary = {
            "total_sales": round(total_sales, 2),
            "average_sale": round(avg_sale, 2),
            "transaction_count": len(self.data),
        }
        return self.summary

    def export_pdf(self, filename: str):
        """Export the summary report to PDF format."""
        print(f"Exporting report to {filename}...")
'''
    with open(os.path.join(WORKSPACE, 'report_generator.py'), 'w') as f:
        f.write(report_gen_py)

    # Set up VSCode user settings - initial state WITHOUT the [python] block
    os.makedirs(VSCODE_USER, exist_ok=True)
    settings = {
        "editor.tabSize": 2,
        "editor.formatOnSave": False,
        "workbench.colorTheme": "Default Dark Modern",
        "editor.minimap.enabled": True,
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000
    }
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'Initial settings created: {SETTINGS_PATH}')
    print(f'Workspace created: {WORKSPACE}')

    # Launch VSCode with the workspace
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

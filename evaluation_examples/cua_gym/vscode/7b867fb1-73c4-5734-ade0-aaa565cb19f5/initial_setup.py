"""
Initial Setup: Configure VSCode with Python extension, format on save disabled
Task ID: vscode_stu_043
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_043'

# VSCode config paths
HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")

# Workspace directory with a sample Python file
WORKSPACE_DIR = os.path.join(WORKDIR, "python_project")


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
            content = f.read()
        # Handle JSONC (strip comments)
        import re
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def update_settings(updates: dict):
    settings = load_settings()
    settings.update(updates)
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)


def create_initial():
    # 1. Create a Python workspace with realistic content
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Main Python file with intentionally imperfect formatting
    # (so format-on-save would have something to fix)
    main_py = os.path.join(WORKSPACE_DIR, "data_processor.py")
    with open(main_py, "w") as f:
        f.write('''import os
import sys
import json
from datetime import datetime, timedelta


class DataProcessor:
    """Processes quarterly sales data for reporting."""

    def __init__(self, input_dir, output_dir):
        self.input_dir=input_dir
        self.output_dir=output_dir
        self.records=[]

    def load_csv(self,  filepath):
        """Load a CSV file and return parsed records."""
        results=[]
        with open(filepath,  'r') as f:
            headers=f.readline().strip().split(',')
            for line in f:
                values=line.strip().split(',')
                record=dict(zip(headers,  values))
                results.append(record)
        return results

    def calculate_totals(self,records):
        """Calculate total revenue per region."""
        totals={}
        for record in records:
            region=record.get('region',  'Unknown')
            amount=float(record.get('amount',  0))
            if region not in totals:
                totals[region]=0.0
            totals[region]+=amount
        return totals

    def generate_report(self,totals,  report_date=None):
        """Generate a JSON report from totals."""
        if report_date is None:
            report_date=datetime.now().strftime('%Y-%m-%d')
        report={
            'date': report_date,
            'summary': totals,
            'generated_at': datetime.now().isoformat()
        }
        output_path=os.path.join(self.output_dir,  f'report_{report_date}.json')
        with open(output_path,  'w') as f:
            json.dump(report,  f,  indent=2)
        return output_path


def main():
    processor=DataProcessor('/data/sales',  '/data/reports')
    files=os.listdir(processor.input_dir)
    all_records=[]
    for fname in files:
        if fname.endswith('.csv'):
            filepath=os.path.join(processor.input_dir,  fname)
            records=processor.load_csv(filepath)
            all_records.extend(records)
    totals=processor.calculate_totals(all_records)
    report_path=processor.generate_report(totals)
    print(f"Report generated: {report_path}")


if __name__ == '__main__':
    main()
''')

    # A helper module
    utils_py = os.path.join(WORKSPACE_DIR, "utils.py")
    with open(utils_py, "w") as f:
        f.write('''"""Utility functions for data processing pipeline."""

import hashlib
import logging

logger = logging.getLogger(__name__)


def validate_record(record, required_fields):
    """Check that a record contains all required fields."""
    missing = [f for f in required_fields if f not in record]
    if missing:
        logger.warning(f"Missing fields: {missing}")
        return False
    return True


def compute_checksum(filepath):
    """Compute SHA256 checksum of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()
''')

    # 2. Configure VSCode settings - explicitly disable format on save
    # and do NOT set any Python formatter
    settings = load_settings()

    # Make sure formatOnSave is disabled (or absent)
    settings["editor.formatOnSave"] = False

    # Remove any existing Python formatting provider setting
    settings.pop("python.formatting.provider", None)
    settings.pop("[python]", None)

    # Add some realistic baseline settings
    settings.setdefault("editor.fontSize", 14)
    settings.setdefault("editor.tabSize", 4)
    settings.setdefault("editor.minimap.enabled", True)
    settings.setdefault("workbench.colorTheme", "Default Dark Modern")
    settings.setdefault("files.autoSave", "afterDelay")
    settings.setdefault("files.autoSaveDelay", 1000)

    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)

    print(f"Initial settings written to: {SETTINGS_PATH}")
    print(f"Workspace created at: {WORKSPACE_DIR}")

    # 3. Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()

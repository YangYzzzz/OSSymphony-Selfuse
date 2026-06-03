"""
Initial Setup: Configure Pylance type checking, auto-import, and analysis memory
Task ID: vscode_we_078
Domain: vscode

Creates a Python project workspace and sets VSCode settings with
python.analysis.typeCheckingMode set to "off" (pre-task state).
"""

import json
import os
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")
WORKSPACE_DIR = os.path.join(HOME, "workspace")


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
            import re
            content = f.read()
            content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_settings(settings):
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)


def create_workspace():
    """Create a realistic Python project for the agent to work with."""
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Main application file
    main_py = os.path.join(WORKSPACE_DIR, "main.py")
    with open(main_py, "w") as f:
        f.write('''\
"""Sales Analytics Dashboard - Entry Point"""

from analytics.report_generator import ReportGenerator
from analytics.data_loader import load_quarterly_data


def main():
    data = load_quarterly_data("data/q1_2025.csv")
    generator = ReportGenerator(data)
    summary = generator.generate_summary()
    print(f"Total Revenue: ${summary['total_revenue']:,.2f}")
    print(f"Top Region: {summary['top_region']}")
    generator.export_pdf("reports/q1_summary.pdf")


if __name__ == "__main__":
    main()
''')

    # Analytics package
    analytics_dir = os.path.join(WORKSPACE_DIR, "analytics")
    os.makedirs(analytics_dir, exist_ok=True)

    init_py = os.path.join(analytics_dir, "__init__.py")
    with open(init_py, "w") as f:
        f.write('"""Analytics package for sales data processing."""\n')

    report_gen = os.path.join(analytics_dir, "report_generator.py")
    with open(report_gen, "w") as f:
        f.write('''\
"""Report generation module."""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class SalesRecord:
    region: str
    product: str
    quantity: int
    unit_price: float
    date: str


class ReportGenerator:
    def __init__(self, data: List[SalesRecord]):
        self.data = data
        self._cache: Optional[Dict] = None

    def generate_summary(self) -> Dict:
        total_revenue = sum(r.quantity * r.unit_price for r in self.data)
        by_region = {}
        for record in self.data:
            by_region.setdefault(record.region, 0)
            by_region[record.region] += record.quantity * record.unit_price
        top_region = max(by_region, key=by_region.get)
        return {
            "total_revenue": total_revenue,
            "top_region": top_region,
            "region_breakdown": by_region,
            "record_count": len(self.data),
        }

    def export_pdf(self, output_path: str) -> None:
        summary = self.generate_summary()
        print(f"Exporting report to {output_path}...")
''')

    data_loader = os.path.join(analytics_dir, "data_loader.py")
    with open(data_loader, "w") as f:
        f.write('''\
"""Data loading utilities."""

import csv
from typing import List
from .report_generator import SalesRecord


def load_quarterly_data(filepath: str) -> List[SalesRecord]:
    records = []
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(SalesRecord(
                region=row["region"],
                product=row["product"],
                quantity=int(row["quantity"]),
                unit_price=float(row["unit_price"]),
                date=row["date"],
            ))
    return records
''')

    # Sample data directory
    data_dir = os.path.join(WORKSPACE_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)
    csv_file = os.path.join(data_dir, "q1_2025.csv")
    with open(csv_file, "w") as f:
        f.write("region,product,quantity,unit_price,date\n")
        f.write("North America,Widget Pro,150,29.99,2025-01-15\n")
        f.write("Europe,Widget Pro,85,32.50,2025-01-22\n")
        f.write("Asia Pacific,Gadget X,200,45.00,2025-02-03\n")
        f.write("North America,Gadget X,120,45.00,2025-02-10\n")
        f.write("Europe,Widget Lite,300,12.99,2025-03-01\n")

    # Reports directory
    os.makedirs(os.path.join(WORKSPACE_DIR, "reports"), exist_ok=True)

    print(f"Workspace created: {WORKSPACE_DIR}")


def setup_initial_settings():
    """Set VSCode settings with typeCheckingMode off (pre-task state)."""
    settings = load_settings()

    # Set the initial state: typeCheckingMode is off
    # Do NOT include autoImportCompletions or memory.keepLibraryAst
    settings["python.analysis.typeCheckingMode"] = "off"

    # Some other realistic existing settings
    settings.setdefault("editor.fontSize", 14)
    settings.setdefault("editor.tabSize", 4)
    settings.setdefault("editor.formatOnSave", True)
    settings.setdefault("workbench.colorTheme", "Default Dark Modern")

    save_settings(settings)
    print(f"Settings written: {SETTINGS_PATH}")


def main():
    create_workspace()
    setup_initial_settings()

    # Ensure Pylance is installed
    try:
        result = subprocess.run(
            ["code", "--list-extensions"],
            capture_output=True, text=True, timeout=15
        )
        if "ms-python.vscode-pylance" not in result.stdout.lower():
            subprocess.run(
                ["code", "--install-extension", "ms-python.vscode-pylance"],
                capture_output=True, timeout=60
            )
            print("Installed ms-python.vscode-pylance")
        else:
            print("ms-python.vscode-pylance already installed")
    except Exception as e:
        print(f"Extension check/install note: {e}")

    # Launch VSCode with the workspace
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with workspace and DISPLAY=:0")


main()

"""
Initial Setup: Set up VSCode with a Python project (no pyproject.toml, no pylint config)
Task ID: vscode_stu_070
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_070'
PROJECT_DIR = os.path.join(WORKDIR, 'cs301', 'project')
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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create realistic Python project files
    # main.py - entry point
    with open(os.path.join(PROJECT_DIR, 'main.py'), 'w') as f:
        f.write('''"""CS301 Data Analysis Project - Main Entry Point"""

import sys
from data_processor import DataProcessor
from report_generator import ReportGenerator


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    processor = DataProcessor(input_file)
    cleaned_data = processor.load_and_clean()
    stats = processor.compute_statistics(cleaned_data)

    report = ReportGenerator(stats)
    report.generate_summary()
    report.export_to_csv("output/summary_report.csv")
    print(f"Analysis complete. Processed {len(cleaned_data)} records.")


if __name__ == "__main__":
    main()
''')

    # data_processor.py
    with open(os.path.join(PROJECT_DIR, 'data_processor.py'), 'w') as f:
        f.write('''import csv
import statistics
from typing import List, Dict, Any


class DataProcessor:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.raw_data = []
        self.column_types = {}

    def load_and_clean(self) -> List[Dict[str, Any]]:
        with open(self.filepath, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cleaned_row = {k: v.strip() for k, v in row.items() if v.strip()}
                if cleaned_row:
                    self.raw_data.append(cleaned_row)
        return self.raw_data

    def compute_statistics(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        numeric_columns = self._detect_numeric_columns(data)
        stats = {}
        for col in numeric_columns:
            values = [float(row[col]) for row in data if col in row]
            if values:
                stats[col] = {
                    "mean": statistics.mean(values),
                    "median": statistics.median(values),
                    "stdev": statistics.stdev(values) if len(values) > 1 else 0,
                    "min": min(values),
                    "max": max(values),
                    "count": len(values),
                }
        return stats

    def _detect_numeric_columns(self, data: List[Dict[str, Any]]) -> List[str]:
        if not data:
            return []
        numeric = []
        for key in data[0]:
            try:
                float(data[0][key])
                numeric.append(key)
            except (ValueError, TypeError):
                pass
        return numeric
''')

    # report_generator.py
    with open(os.path.join(PROJECT_DIR, 'report_generator.py'), 'w') as f:
        f.write('''import csv
import os
from typing import Dict, Any


class ReportGenerator:
    def __init__(self, statistics: Dict[str, Any]):
        self.statistics = statistics
        self.summary_lines = []

    def generate_summary(self):
        self.summary_lines.append("=" * 60)
        self.summary_lines.append("STATISTICAL ANALYSIS REPORT")
        self.summary_lines.append("=" * 60)
        for column, stats in self.statistics.items():
            self.summary_lines.append(f"\\nColumn: {column}")
            self.summary_lines.append("-" * 40)
            self.summary_lines.append(f"  Mean:    {stats['mean']:.2f}")
            self.summary_lines.append(f"  Median:  {stats['median']:.2f}")
            self.summary_lines.append(f"  Std Dev: {stats['stdev']:.2f}")
            self.summary_lines.append(f"  Min:     {stats['min']:.2f}")
            self.summary_lines.append(f"  Max:     {stats['max']:.2f}")
            self.summary_lines.append(f"  Count:   {stats['count']}")
        for line in self.summary_lines:
            print(line)

    def export_to_csv(self, output_path: str):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Column", "Mean", "Median", "StdDev", "Min", "Max", "Count"])
            for column, stats in self.statistics.items():
                writer.writerow([
                    column, f"{stats['mean']:.2f}", f"{stats['median']:.2f}",
                    f"{stats['stdev']:.2f}", f"{stats['min']:.2f}",
                    f"{stats['max']:.2f}", stats['count']
                ])
''')

    # tests/test_processor.py
    test_dir = os.path.join(PROJECT_DIR, 'tests')
    os.makedirs(test_dir, exist_ok=True)
    with open(os.path.join(test_dir, '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(test_dir, 'test_processor.py'), 'w') as f:
        f.write('''import unittest
import os
import tempfile
from data_processor import DataProcessor


class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.test_csv = tempfile.NamedTemporaryFile(
            mode='w', suffix='.csv', delete=False
        )
        self.test_csv.write("name,score,grade\\n")
        self.test_csv.write("Alice,92.5,A\\n")
        self.test_csv.write("Bob,78.0,B\\n")
        self.test_csv.write("Charlie,85.3,B+\\n")
        self.test_csv.close()

    def tearDown(self):
        os.unlink(self.test_csv.name)

    def test_load_and_clean(self):
        proc = DataProcessor(self.test_csv.name)
        data = proc.load_and_clean()
        self.assertEqual(len(data), 3)
        self.assertIn("name", data[0])

    def test_compute_statistics(self):
        proc = DataProcessor(self.test_csv.name)
        data = proc.load_and_clean()
        stats = proc.compute_statistics(data)
        self.assertIn("score", stats)
        self.assertAlmostEqual(stats["score"]["mean"], 85.27, places=1)


if __name__ == "__main__":
    unittest.main()
''')

    # requirements.txt
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write('''# CS301 Project Dependencies
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
pytest>=7.3.0
pylint>=3.0.0
''')

    # README.md
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write('''# CS301 Data Analysis Project

A statistical analysis toolkit for processing CSV datasets and generating
summary reports with descriptive statistics.

## Usage

```bash
python main.py data/input.csv
```

## Project Structure

- `main.py` - Entry point
- `data_processor.py` - Data loading and statistical computation
- `report_generator.py` - Report formatting and export
- `tests/` - Unit tests
''')

    # Ensure NO pyproject.toml exists (negative constraint)
    pyproject_path = os.path.join(PROJECT_DIR, 'pyproject.toml')
    if os.path.exists(pyproject_path):
        os.remove(pyproject_path)

    # Ensure VSCode settings do NOT have pylint config
    # Load existing settings and remove any pylint-related keys
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Remove any pylint-related keys
    pylint_keys = [k for k in settings if 'pylint' in k.lower() or 'linting' in k.lower()]
    for k in pylint_keys:
        del settings[k]

    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Files: main.py, data_processor.py, report_generator.py, tests/, requirements.txt, README.md')
    print(f'No pyproject.toml exists (as required)')

    # GUI-ready: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

"""
Initial Setup: Create a Python CLI project structure for documentation workflow task
Task ID: vscode_wf_041
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_041'
PROJECT_DIR = f'{WORKDIR}/project'


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
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # --- src/__init__.py ---
    with open(f'{PROJECT_DIR}/src/__init__.py', 'w') as f:
        f.write('"""DataFlow - A command-line data processing toolkit."""\n\n__version__ = "0.3.1"\n')

    # --- src/cli.py ---
    with open(f'{PROJECT_DIR}/src/cli.py', 'w') as f:
        f.write('''"""Command-line interface for DataFlow."""

import argparse
import sys
from .processor import DataProcessor


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="dataflow",
        description="Process and transform data files from the command line.",
    )
    parser.add_argument("input", help="Path to the input data file (CSV, JSON, or Parquet)")
    parser.add_argument("-o", "--output", help="Output file path", default=None)
    parser.add_argument(
        "-f", "--format",
        choices=["csv", "json", "parquet"],
        default="csv",
        help="Output format (default: csv)",
    )
    parser.add_argument(
        "--filter",
        metavar="EXPR",
        help="Filter expression, e.g. 'age > 30'",
    )
    parser.add_argument(
        "--sort",
        metavar="COLUMN",
        help="Sort output by the given column",
    )
    parser.add_argument(
        "--aggregate",
        nargs=2,
        metavar=("COLUMN", "FUNC"),
        help="Aggregate COLUMN with FUNC (sum, mean, count, min, max)",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    processor = DataProcessor(verbose=args.verbose)

    processor.load(args.input)

    if args.filter:
        processor.apply_filter(args.filter)

    if args.sort:
        processor.sort_by(args.sort)

    if args.aggregate:
        column, func = args.aggregate
        processor.aggregate(column, func)

    output_path = args.output or f"output.{args.format}"
    processor.save(output_path, fmt=args.format)

    if args.verbose:
        print(f"Processed {processor.row_count} rows -> {output_path}")


if __name__ == "__main__":
    main()
''')

    # --- src/processor.py ---
    with open(f'{PROJECT_DIR}/src/processor.py', 'w') as f:
        f.write('''"""Core data processing engine for DataFlow."""

import csv
import json
import os


class DataProcessor:
    """Loads, transforms, and exports tabular data."""

    SUPPORTED_FORMATS = ("csv", "json", "parquet")
    AGGREGATE_FUNCS = ("sum", "mean", "count", "min", "max")

    def __init__(self, verbose=False):
        self._data = []
        self._headers = []
        self._verbose = verbose

    # ---- properties ----
    @property
    def row_count(self):
        return len(self._data)

    @property
    def headers(self):
        return list(self._headers)

    # ---- I/O ----
    def load(self, path):
        ext = os.path.splitext(path)[1].lower()
        if ext == ".csv":
            self._load_csv(path)
        elif ext == ".json":
            self._load_json(path)
        else:
            raise ValueError(f"Unsupported input format: {ext}")
        if self._verbose:
            print(f"Loaded {self.row_count} rows from {path}")

    def _load_csv(self, path):
        with open(path, newline="") as fh:
            reader = csv.DictReader(fh)
            self._headers = reader.fieldnames or []
            self._data = [dict(row) for row in reader]

    def _load_json(self, path):
        with open(path) as fh:
            records = json.load(fh)
        if records:
            self._headers = list(records[0].keys())
        self._data = records

    def save(self, path, fmt="csv"):
        if fmt == "csv":
            self._save_csv(path)
        elif fmt == "json":
            self._save_json(path)
        else:
            raise ValueError(f"Unsupported output format: {fmt}")

    def _save_csv(self, path):
        with open(path, "w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=self._headers)
            writer.writeheader()
            writer.writerows(self._data)

    def _save_json(self, path):
        with open(path, "w") as fh:
            json.dump(self._data, fh, indent=2)

    # ---- transformations ----
    def apply_filter(self, expression):
        """Filter rows by a simple expression like 'age > 30'."""
        parts = expression.split()
        if len(parts) != 3:
            raise ValueError(f"Invalid filter expression: {expression}")
        col, op, val = parts
        self._data = [
            row for row in self._data
            if self._compare(row.get(col, ""), op, val)
        ]

    def sort_by(self, column, descending=False):
        self._data.sort(
            key=lambda row: self._sort_key(row.get(column, "")),
            reverse=descending,
        )

    def aggregate(self, column, func):
        values = [self._to_number(row.get(column, 0)) for row in self._data]
        if func == "sum":
            result = sum(values)
        elif func == "mean":
            result = sum(values) / len(values) if values else 0
        elif func == "count":
            result = len(values)
        elif func == "min":
            result = min(values) if values else 0
        elif func == "max":
            result = max(values) if values else 0
        else:
            raise ValueError(f"Unknown aggregate function: {func}")
        self._data = [{"column": column, "function": func, "result": result}]
        self._headers = ["column", "function", "result"]

    # ---- helpers ----
    @staticmethod
    def _to_number(val):
        try:
            return float(val)
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    def _sort_key(val):
        try:
            return (0, float(val))
        except (ValueError, TypeError):
            return (1, str(val))

    @staticmethod
    def _compare(cell_val, op, ref_val):
        try:
            cell_num = float(cell_val)
            ref_num = float(ref_val)
        except (ValueError, TypeError):
            cell_num, ref_num = str(cell_val), str(ref_val)
        ops = {
            ">": lambda a, b: a > b,
            "<": lambda a, b: a < b,
            ">=": lambda a, b: a >= b,
            "<=": lambda a, b: a <= b,
            "==": lambda a, b: a == b,
            "!=": lambda a, b: a != b,
        }
        return ops.get(op, lambda a, b: False)(cell_num, ref_num)
''')

    # --- tests/__init__.py ---
    with open(f'{PROJECT_DIR}/tests/__init__.py', 'w') as f:
        f.write('')

    # --- tests/test_processor.py ---
    with open(f'{PROJECT_DIR}/tests/test_processor.py', 'w') as f:
        f.write('''"""Tests for the DataProcessor class."""

import json
import os
import tempfile
import unittest

from src.processor import DataProcessor


class TestDataProcessorLoad(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.csv_path = os.path.join(self.tmp, "sample.csv")
        with open(self.csv_path, "w") as f:
            f.write("name,age,salary\\nAlice,30,72000\\nBob,25,65000\\nCarla,35,88000\\n")

    def test_load_csv(self):
        proc = DataProcessor()
        proc.load(self.csv_path)
        self.assertEqual(proc.row_count, 3)
        self.assertEqual(proc.headers, ["name", "age", "salary"])

    def test_filter(self):
        proc = DataProcessor()
        proc.load(self.csv_path)
        proc.apply_filter("age > 28")
        self.assertEqual(proc.row_count, 2)

    def test_sort(self):
        proc = DataProcessor()
        proc.load(self.csv_path)
        proc.sort_by("salary")
        self.assertEqual(proc._data[0]["name"], "Bob")

    def test_aggregate_sum(self):
        proc = DataProcessor()
        proc.load(self.csv_path)
        proc.aggregate("salary", "sum")
        self.assertAlmostEqual(proc._data[0]["result"], 225000.0)


class TestDataProcessorSave(unittest.TestCase):
    def test_save_json(self):
        proc = DataProcessor()
        proc._headers = ["x", "y"]
        proc._data = [{"x": 1, "y": 2}]
        tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        tmp.close()
        proc.save(tmp.name, fmt="json")
        with open(tmp.name) as f:
            loaded = json.load(f)
        self.assertEqual(loaded, [{"x": 1, "y": 2}])
        os.unlink(tmp.name)


if __name__ == "__main__":
    unittest.main()
''')

    # --- setup.py ---
    with open(f'{PROJECT_DIR}/setup.py', 'w') as f:
        f.write('''"""Package setup for DataFlow CLI tool."""

from setuptools import setup, find_packages

setup(
    name="dataflow",
    version="0.3.1",
    description="A command-line data processing toolkit",
    author="DataFlow Team",
    author_email="team@dataflow.dev",
    url="https://github.com/dataflow-team/dataflow",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.5.0",
        "pyarrow>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "dataflow=src.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
    ],
)
''')

    # No README.md or docs/ folder - those are what the agent must create
    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Contents:')
    for root, dirs, files in os.walk(PROJECT_DIR):
        for fname in files:
            rel = os.path.relpath(os.path.join(root, fname), PROJECT_DIR)
            print(f'  {rel}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with ~/project and DISPLAY=:0')


create_initial()

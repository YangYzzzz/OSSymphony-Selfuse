"""
Initial Setup: Create a data-pipeline project with Python files for VSCode task creation
Task ID: vscode_td_010
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_010'
PROJECT_DIR = f'{WORKDIR}/projects/data-pipeline'
SRC_DIR = f'{PROJECT_DIR}/src'
TESTS_DIR = f'{PROJECT_DIR}/tests'


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
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(TESTS_DIR, exist_ok=True)

    # --- src/__init__.py ---
    with open(f'{SRC_DIR}/__init__.py', 'w') as f:
        f.write('"""Data pipeline package."""\n')

    # --- src/extract.py ---
    with open(f'{SRC_DIR}/extract.py', 'w') as f:
        f.write('''"""Extract module - handles data ingestion from various sources."""

import csv
import json
from pathlib import Path
from typing import List, Dict, Any


class CSVExtractor:
    """Extract data from CSV files."""

    def __init__(self, source_path: str, delimiter: str = ","):
        self.source_path = Path(source_path)
        self.delimiter = delimiter

    def extract(self) -> List[Dict[str, Any]]:
        """Read CSV file and return list of dictionaries."""
        records = []
        with open(self.source_path, "r", newline="") as f:
            reader = csv.DictReader(f, delimiter=self.delimiter)
            for row in reader:
                records.append(dict(row))
        return records

    def validate_schema(self, expected_columns: List[str]) -> bool:
        """Check that the CSV has the expected column headers."""
        with open(self.source_path, "r") as f:
            reader = csv.reader(f, delimiter=self.delimiter)
            headers = next(reader, [])
        return all(col in headers for col in expected_columns)


class JSONExtractor:
    """Extract data from JSON files."""

    def __init__(self, source_path: str):
        self.source_path = Path(source_path)

    def extract(self) -> List[Dict[str, Any]]:
        """Read JSON file and return data."""
        with open(self.source_path, "r") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return [data]
''')

    # --- src/transform.py ---
    with open(f'{SRC_DIR}/transform.py', 'w') as f:
        f.write('''"""Transform module - data cleaning and transformation logic."""

from typing import List, Dict, Any, Optional
from datetime import datetime


def clean_whitespace(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Strip leading/trailing whitespace from all string values."""
    cleaned = []
    for record in records:
        cleaned_record = {}
        for key, value in record.items():
            if isinstance(value, str):
                cleaned_record[key.strip()] = value.strip()
            else:
                cleaned_record[key] = value
        cleaned.append(cleaned_record)
    return cleaned


def normalize_dates(records: List[Dict[str, Any]], date_fields: List[str],
                    input_format: str = "%m/%d/%Y",
                    output_format: str = "%Y-%m-%d") -> List[Dict[str, Any]]:
    """Convert date fields to a consistent format."""
    for record in records:
        for field in date_fields:
            if field in record and record[field]:
                try:
                    dt = datetime.strptime(record[field], input_format)
                    record[field] = dt.strftime(output_format)
                except (ValueError, TypeError):
                    pass
    return records


def filter_records(records: List[Dict[str, Any]],
                   field: str, min_value: Optional[float] = None,
                   max_value: Optional[float] = None) -> List[Dict[str, Any]]:
    """Filter records by numeric range on a given field."""
    filtered = []
    for record in records:
        value = float(record.get(field, 0))
        if min_value is not None and value < min_value:
            continue
        if max_value is not None and value > max_value:
            continue
        filtered.append(record)
    return filtered


def add_computed_field(records: List[Dict[str, Any]],
                       new_field: str, source_fields: List[str],
                       operation: str = "sum") -> List[Dict[str, Any]]:
    """Add a computed field based on existing numeric fields."""
    for record in records:
        values = [float(record.get(f, 0)) for f in source_fields]
        if operation == "sum":
            record[new_field] = sum(values)
        elif operation == "avg":
            record[new_field] = sum(values) / len(values) if values else 0
        elif operation == "max":
            record[new_field] = max(values) if values else 0
    return records
''')

    # --- src/load.py ---
    with open(f'{SRC_DIR}/load.py', 'w') as f:
        f.write('''"""Load module - writes transformed data to output destinations."""

import csv
import json
from pathlib import Path
from typing import List, Dict, Any


class CSVLoader:
    """Write data to CSV files."""

    def __init__(self, output_path: str):
        self.output_path = Path(output_path)

    def load(self, records: List[Dict[str, Any]]) -> int:
        """Write records to CSV. Returns number of rows written."""
        if not records:
            return 0
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = list(records[0].keys())
        with open(self.output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
        return len(records)


class JSONLoader:
    """Write data to JSON files."""

    def __init__(self, output_path: str):
        self.output_path = Path(output_path)

    def load(self, records: List[Dict[str, Any]], indent: int = 2) -> int:
        """Write records to JSON. Returns number of records written."""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_path, "w") as f:
            json.dump(records, f, indent=indent)
        return len(records)
''')

    # --- src/pipeline.py ---
    with open(f'{SRC_DIR}/pipeline.py', 'w') as f:
        f.write('''"""Pipeline orchestrator - coordinates extract, transform, load steps."""

from src.extract import CSVExtractor, JSONExtractor
from src.transform import clean_whitespace, normalize_dates, filter_records
from src.load import CSVLoader, JSONLoader


def run_sales_pipeline(input_csv: str, output_json: str) -> dict:
    """Run the sales data pipeline: extract CSV -> transform -> load JSON."""
    extractor = CSVExtractor(input_csv)
    records = extractor.extract()
    records = clean_whitespace(records)
    records = normalize_dates(records, ["sale_date"])
    records = filter_records(records, "amount", min_value=10.0)
    loader = JSONLoader(output_json)
    count = loader.load(records)
    return {"input_records": len(extractor.extract()), "output_records": count}


if __name__ == "__main__":
    result = run_sales_pipeline("data/sales_raw.csv", "output/sales_clean.json")
    print(f"Pipeline complete: {result}")
''')

    # --- tests/__init__.py ---
    with open(f'{TESTS_DIR}/__init__.py', 'w') as f:
        f.write('')

    # --- tests/test_transform.py ---
    with open(f'{TESTS_DIR}/test_transform.py', 'w') as f:
        f.write('''"""Tests for the transform module."""

import unittest
from src.transform import clean_whitespace, normalize_dates, filter_records, add_computed_field


class TestCleanWhitespace(unittest.TestCase):
    def test_strips_string_values(self):
        records = [{"name": "  Alice  ", "city": " Portland "}]
        result = clean_whitespace(records)
        self.assertEqual(result[0]["name"], "Alice")
        self.assertEqual(result[0]["city"], "Portland")

    def test_leaves_non_strings_unchanged(self):
        records = [{"count": 42, "active": True}]
        result = clean_whitespace(records)
        self.assertEqual(result[0]["count"], 42)
        self.assertTrue(result[0]["active"])


class TestNormalizeDates(unittest.TestCase):
    def test_converts_date_format(self):
        records = [{"sale_date": "03/15/2025"}]
        result = normalize_dates(records, ["sale_date"])
        self.assertEqual(result[0]["sale_date"], "2025-03-15")

    def test_handles_invalid_date(self):
        records = [{"sale_date": "not-a-date"}]
        result = normalize_dates(records, ["sale_date"])
        self.assertEqual(result[0]["sale_date"], "not-a-date")


class TestFilterRecords(unittest.TestCase):
    def test_filters_by_min_value(self):
        records = [{"amount": "5"}, {"amount": "15"}, {"amount": "25"}]
        result = filter_records(records, "amount", min_value=10.0)
        self.assertEqual(len(result), 2)


class TestAddComputedField(unittest.TestCase):
    def test_sum_operation(self):
        records = [{"price": "100", "tax": "8.5"}]
        result = add_computed_field(records, "total", ["price", "tax"], "sum")
        self.assertAlmostEqual(result[0]["total"], 108.5)


if __name__ == "__main__":
    unittest.main()
''')

    # --- tests/test_extract.py ---
    with open(f'{TESTS_DIR}/test_extract.py', 'w') as f:
        f.write('''"""Tests for the extract module."""

import unittest
import tempfile
import os
import json
from src.extract import CSVExtractor, JSONExtractor


class TestCSVExtractor(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.csv_path = os.path.join(self.temp_dir, "test.csv")
        with open(self.csv_path, "w") as f:
            f.write("name,amount,date\\nAlice,150.00,2025-01-10\\nBob,75.50,2025-02-20\\n")

    def test_extract_returns_list_of_dicts(self):
        extractor = CSVExtractor(self.csv_path)
        records = extractor.extract()
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["name"], "Alice")

    def test_validate_schema_passes(self):
        extractor = CSVExtractor(self.csv_path)
        self.assertTrue(extractor.validate_schema(["name", "amount"]))


class TestJSONExtractor(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.json_path = os.path.join(self.temp_dir, "test.json")
        with open(self.json_path, "w") as f:
            json.dump([{"id": 1, "value": "test"}], f)

    def test_extract_returns_list(self):
        extractor = JSONExtractor(self.json_path)
        records = extractor.extract()
        self.assertEqual(len(records), 1)


if __name__ == "__main__":
    unittest.main()
''')

    # --- pyproject.toml (makes black happy) ---
    with open(f'{PROJECT_DIR}/pyproject.toml', 'w') as f:
        f.write('''[tool.black]
line-length = 88
target-version = ["py310"]

[project]
name = "data-pipeline"
version = "0.1.0"
description = "ETL pipeline for sales data processing"
requires-python = ">=3.10"
dependencies = []
''')

    # --- README (small, realistic) ---
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write('''# Data Pipeline

ETL pipeline for processing sales data from CSV/JSON sources.

## Structure

- `src/` - Core pipeline modules (extract, transform, load)
- `tests/` - Unit tests

## Usage

```bash
python -m src.pipeline
```
''')

    # Ensure NO .vscode/tasks.json exists (negative constraint)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    tasks_path = f'{vscode_dir}/tasks.json'
    if os.path.exists(tasks_path):
        os.remove(tasks_path)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  src/: extract.py, transform.py, load.py, pipeline.py')
    print(f'  tests/: test_transform.py, test_extract.py')
    print(f'  No .vscode/tasks.json (as required)')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

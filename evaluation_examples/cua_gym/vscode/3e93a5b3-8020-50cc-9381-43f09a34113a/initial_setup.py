"""
Initial Setup: Create a Python project with pyproject.toml for package building.
Task ID: vscode_py_027
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_027'
PROJECT_DIR = f'{WORKDIR}/workspace'
SRC_DIR = f'{PROJECT_DIR}/src/datautils'


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
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # pyproject.toml - realistic Python package config
    pyproject_content = """[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "datautils"
version = "0.3.1"
description = "A collection of lightweight data processing utilities"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.9"
authors = [
    {name = "Priya Sharma", email = "priya.sharma@example.com"},
]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "pandas>=2.0",
    "numpy>=1.24",
]

[project.optional-dependencies]
dev = ["pytest>=7.0", "ruff>=0.1.0"]
"""
    with open(f'{PROJECT_DIR}/pyproject.toml', 'w') as f:
        f.write(pyproject_content)

    # README.md
    readme_content = """# datautils

A collection of lightweight data processing utilities for common ETL tasks.

## Installation

```bash
pip install datautils
```

## Features

- CSV/JSON normalization
- Date parsing with timezone awareness
- Column-level statistics aggregation
- Missing value imputation strategies

## Usage

```python
from datautils import normalize_csv, parse_dates

df = normalize_csv("sales_q1.csv", encoding="auto")
df["order_date"] = parse_dates(df["order_date"], tz="UTC")
```

## License

MIT
"""
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme_content)

    # Package __init__.py
    init_content = '''"""datautils - lightweight data processing utilities."""

__version__ = "0.3.1"

from .normalize import normalize_csv, normalize_json
from .dates import parse_dates
from .stats import column_stats
'''
    with open(f'{SRC_DIR}/__init__.py', 'w') as f:
        f.write(init_content)

    # normalize.py
    normalize_content = '''"""Data normalization utilities."""

import csv
import json
from pathlib import Path
from typing import Optional


def normalize_csv(filepath: str, encoding: Optional[str] = None,
                  delimiter: Optional[str] = None) -> list[dict]:
    """Read a CSV file and return normalized records.

    Args:
        filepath: Path to the CSV file.
        encoding: File encoding. If "auto", tries utf-8 then latin-1.
        delimiter: Column delimiter. Auto-detected if None.

    Returns:
        List of dictionaries, one per row.
    """
    enc = encoding or "utf-8"
    if enc == "auto":
        for try_enc in ("utf-8", "latin-1", "cp1252"):
            try:
                return _read_csv(filepath, try_enc, delimiter)
            except UnicodeDecodeError:
                continue
        raise UnicodeDecodeError("Could not detect encoding")
    return _read_csv(filepath, enc, delimiter)


def _read_csv(filepath: str, encoding: str,
              delimiter: Optional[str]) -> list[dict]:
    with open(filepath, "r", encoding=encoding) as fh:
        if delimiter:
            reader = csv.DictReader(fh, delimiter=delimiter)
        else:
            sample = fh.read(4096)
            fh.seek(0)
            dialect = csv.Sniffer().sniff(sample)
            reader = csv.DictReader(fh, dialect=dialect)
        return [dict(row) for row in reader]


def normalize_json(filepath: str) -> list[dict]:
    """Load a JSON file and flatten nested records."""
    data = json.loads(Path(filepath).read_text())
    if isinstance(data, dict):
        data = [data]
    return [_flatten(record) for record in data]


def _flatten(d: dict, parent_key: str = "", sep: str = ".") -> dict:
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(_flatten(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
'''
    with open(f'{SRC_DIR}/normalize.py', 'w') as f:
        f.write(normalize_content)

    # dates.py
    dates_content = '''"""Date parsing utilities."""

from datetime import datetime, timezone
from typing import Optional


def parse_dates(values: list, fmt: Optional[str] = None,
                tz: Optional[str] = None) -> list[datetime]:
    """Parse a list of date strings into datetime objects.

    Args:
        values: List of date strings.
        fmt: strftime format string. If None, common formats are tried.
        tz: Timezone name (currently only "UTC" supported).

    Returns:
        List of parsed datetime objects.
    """
    results = []
    for val in values:
        dt = _try_parse(str(val).strip(), fmt)
        if tz == "UTC":
            dt = dt.replace(tzinfo=timezone.utc)
        results.append(dt)
    return results


COMMON_FORMATS = [
    "%Y-%m-%d",
    "%Y-%m-%d %H:%M:%S",
    "%m/%d/%Y",
    "%d-%b-%Y",
    "%B %d, %Y",
]


def _try_parse(value: str, fmt: Optional[str] = None) -> datetime:
    if fmt:
        return datetime.strptime(value, fmt)
    for f in COMMON_FORMATS:
        try:
            return datetime.strptime(value, f)
        except ValueError:
            continue
    raise ValueError(f"Could not parse date: {value!r}")
'''
    with open(f'{SRC_DIR}/dates.py', 'w') as f:
        f.write(dates_content)

    # stats.py
    stats_content = '''"""Column-level statistics aggregation."""

from typing import Any


def column_stats(records: list[dict], column: str) -> dict[str, Any]:
    """Compute basic statistics for a numeric column.

    Args:
        records: List of row dictionaries.
        column: Column name to analyze.

    Returns:
        Dictionary with count, sum, mean, min, max.
    """
    values = []
    for row in records:
        val = row.get(column)
        if val is not None:
            try:
                values.append(float(val))
            except (ValueError, TypeError):
                continue

    if not values:
        return {"count": 0, "sum": 0, "mean": None, "min": None, "max": None}

    return {
        "count": len(values),
        "sum": sum(values),
        "mean": sum(values) / len(values),
        "min": min(values),
        "max": max(values),
    }
'''
    with open(f'{SRC_DIR}/stats.py', 'w') as f:
        f.write(stats_content)

    # tests/test_normalize.py
    test_content = '''"""Tests for normalize module."""

import json
import os
import tempfile

from datautils.normalize import normalize_csv, normalize_json


def test_normalize_csv_basic():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("name,age,city\\n")
        f.write("Alice,30,Portland\\n")
        f.write("Bob,25,Seattle\\n")
        path = f.name
    try:
        rows = normalize_csv(path)
        assert len(rows) == 2
        assert rows[0]["name"] == "Alice"
        assert rows[1]["age"] == "25"
    finally:
        os.unlink(path)


def test_normalize_json_flat():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"a": 1, "b": {"c": 2, "d": 3}}, f)
        path = f.name
    try:
        rows = normalize_json(path)
        assert len(rows) == 1
        assert rows[0]["b.c"] == 2
    finally:
        os.unlink(path)
'''
    with open(f'{PROJECT_DIR}/tests/test_normalize.py', 'w') as f:
        f.write(test_content)

    # IMPORTANT: NO .vscode/tasks.json - the task is to create it
    print(f'Initial project created at: {PROJECT_DIR}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

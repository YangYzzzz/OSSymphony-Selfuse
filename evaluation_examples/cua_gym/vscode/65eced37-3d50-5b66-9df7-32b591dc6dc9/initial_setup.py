"""
Initial Setup: Create a Python project with src/ structure but NO analyzer.py
Task ID: vscode_file_057
Domain: vs_code

The agent will use VSCode's Command Palette 'New File' command,
type Python code, and save it as src/analyzer.py.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_057'
PROJECT_DIR = f'{WORKDIR}/data-project'
SRC_DIR = f'{PROJECT_DIR}/src'


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

    # Create src/loader.py — data loading module
    loader_content = '''\
"""
loader.py — Data loading utilities for the data-project pipeline.
"""

import os
import csv
from typing import List, Dict, Any


DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')


def load_csv(filename: str) -> List[Dict[str, Any]]:
    """Load a CSV file from the data directory and return a list of dicts.

    Args:
        filename: Name of the CSV file (without directory prefix).

    Returns:
        List of row dicts with column headers as keys.
    """
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found: {filepath}")

    rows = []
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    return rows


def load_text(filename: str) -> str:
    """Read a plain text file from the data directory.

    Args:
        filename: Name of the text file.

    Returns:
        File contents as a string.
    """
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, encoding='utf-8') as f:
        return f.read()


def list_available_datasets() -> List[str]:
    """Return a sorted list of available data files in the data directory."""
    if not os.path.isdir(DATA_DIR):
        return []
    return sorted(
        f for f in os.listdir(DATA_DIR)
        if os.path.isfile(os.path.join(DATA_DIR, f))
    )
'''

    with open(f'{SRC_DIR}/loader.py', 'w') as f:
        f.write(loader_content)

    # Create src/processor.py — data processing module
    processor_content = '''\
"""
processor.py — Data transformation and processing utilities.
"""

from typing import List, Dict, Any, Optional


def filter_rows(
    data: List[Dict[str, Any]],
    column: str,
    value: Any,
    strict: bool = True,
) -> List[Dict[str, Any]]:
    """Filter a list of dicts by matching a column value.

    Args:
        data: List of row dicts to filter.
        column: Column name to filter on.
        value: Value to match.
        strict: If True use exact match; if False use case-insensitive substring.

    Returns:
        Filtered list of row dicts.
    """
    result = []
    for row in data:
        cell = row.get(column, '')
        if strict:
            if cell == value:
                result.append(row)
        else:
            if str(value).lower() in str(cell).lower():
                result.append(row)
    return result


def compute_statistics(
    data: List[Dict[str, Any]],
    numeric_column: str,
) -> Dict[str, float]:
    """Compute basic descriptive statistics on a numeric column.

    Args:
        data: List of row dicts.
        numeric_column: Name of the column containing numeric values.

    Returns:
        Dict with keys: count, mean, min, max, total.
    """
    values = []
    for row in data:
        try:
            values.append(float(row[numeric_column]))
        except (KeyError, ValueError, TypeError):
            pass

    if not values:
        return {'count': 0, 'mean': 0.0, 'min': 0.0, 'max': 0.0, 'total': 0.0}

    return {
        'count': len(values),
        'mean': sum(values) / len(values),
        'min': min(values),
        'max': max(values),
        'total': sum(values),
    }


def deduplicate(
    data: List[Dict[str, Any]],
    key_column: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Remove duplicate rows.

    Args:
        data: List of row dicts.
        key_column: If provided, deduplicate by this column; otherwise by full row.

    Returns:
        Deduplicated list preserving first occurrence.
    """
    seen = set()
    result = []
    for row in data:
        key = row.get(key_column) if key_column else str(sorted(row.items()))
        if key not in seen:
            seen.add(key)
            result.append(row)
    return result


def rename_columns(
    data: List[Dict[str, Any]],
    mapping: Dict[str, str],
) -> List[Dict[str, Any]]:
    """Rename columns according to a mapping dict.

    Args:
        data: List of row dicts.
        mapping: {old_name: new_name} pairs.

    Returns:
        New list with renamed keys.
    """
    return [
        {mapping.get(k, k): v for k, v in row.items()}
        for row in data
    ]
'''

    with open(f'{SRC_DIR}/processor.py', 'w') as f:
        f.write(processor_content)

    # Create requirements.txt
    requirements_content = '''\
# data-project dependencies
pandas>=1.5.0
numpy>=1.23.0
requests>=2.28.0
python-dotenv>=0.21.0
pytest>=7.2.0
'''

    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write(requirements_content)

    # IMPORTANT: src/analyzer.py must NOT exist in the initial state
    analyzer_path = f'{SRC_DIR}/analyzer.py'
    if os.path.exists(analyzer_path):
        os.remove(analyzer_path)
        print(f'Removed pre-existing {analyzer_path}')

    print(f'Project structure created: {PROJECT_DIR}')
    print(f'  {SRC_DIR}/loader.py')
    print(f'  {SRC_DIR}/processor.py')
    print(f'  {PROJECT_DIR}/requirements.txt')
    print(f'  (src/analyzer.py does NOT exist — agent must create it)')

    # GUI-ready startup: open VSCode with the project folder, no files open
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with data-project folder, DISPLAY=:0')


create_initial()

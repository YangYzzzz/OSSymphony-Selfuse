"""
Initial Setup: Set up Sphinx documentation for a Python project
Task ID: vscode_gf6_083
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_083'
PROJECT_DIR = f'{WORKDIR}/projects/python-sphinx-docs'
SRC_DIR = f'{PROJECT_DIR}/src/mypackage'


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
    # Create project structure
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/.vscode', exist_ok=True)

    # Create src/mypackage/__init__.py
    with open(f'{SRC_DIR}/__init__.py', 'w') as f:
        f.write('"""MyPackage - A sample Python package for documentation demo."""\n\n__version__ = "0.1.0"\n')

    # Create src/mypackage/core.py - 5 public functions WITHOUT docstrings
    with open(f'{SRC_DIR}/core.py', 'w') as f:
        f.write('''"""Core module for MyPackage."""

from typing import List, Dict, Optional


def calculate_statistics(data: List[float]) -> Dict[str, float]:
    if not data:
        return {"mean": 0.0, "median": 0.0, "std_dev": 0.0}
    n = len(data)
    mean = sum(data) / n
    sorted_data = sorted(data)
    if n % 2 == 0:
        median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
    else:
        median = sorted_data[n // 2]
    variance = sum((x - mean) ** 2 for x in data) / n
    std_dev = variance ** 0.5
    return {"mean": round(mean, 4), "median": round(median, 4), "std_dev": round(std_dev, 4)}


def transform_records(records: List[Dict], key_mapping: Dict[str, str]) -> List[Dict]:
    transformed = []
    for record in records:
        new_record = {}
        for old_key, new_key in key_mapping.items():
            if old_key in record:
                new_record[new_key] = record[old_key]
        transformed.append(new_record)
    return transformed


def filter_by_threshold(items: List[Dict], field: str, threshold: float,
                        above: bool = True) -> List[Dict]:
    if above:
        return [item for item in items if item.get(field, 0) >= threshold]
    return [item for item in items if item.get(field, 0) < threshold]


def merge_datasets(primary: List[Dict], secondary: List[Dict],
                   join_key: str) -> List[Dict]:
    secondary_map = {}
    for record in secondary:
        key_val = record.get(join_key)
        if key_val is not None:
            secondary_map[key_val] = record
    merged = []
    for record in primary:
        key_val = record.get(join_key)
        merged_record = dict(record)
        if key_val in secondary_map:
            for k, v in secondary_map[key_val].items():
                if k not in merged_record:
                    merged_record[k] = v
        merged.append(merged_record)
    return merged


def generate_report(title: str, sections: List[Dict[str, str]],
                    include_toc: bool = True) -> str:
    lines = [f"# {title}", ""]
    if include_toc and sections:
        lines.append("## Table of Contents")
        for i, section in enumerate(sections, 1):
            heading = section.get("heading", f"Section {i}")
            lines.append(f"  {i}. {heading}")
        lines.append("")
    for section in sections:
        heading = section.get("heading", "Untitled")
        content = section.get("content", "")
        lines.append(f"## {heading}")
        lines.append(content)
        lines.append("")
    return "\\n".join(lines)
''')

    # Create src/mypackage/utils.py - 3 public functions WITHOUT docstrings
    with open(f'{SRC_DIR}/utils.py', 'w') as f:
        f.write('''"""Utility module for MyPackage."""

import os
import re
from typing import List, Optional, Any
from datetime import datetime


def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def format_timestamp(dt: Optional[datetime] = None,
                     fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    if dt is None:
        dt = datetime.now()
    return dt.strftime(fmt)


def batch_process(items: List[Any], batch_size: int = 10) -> List[List[Any]]:
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")
    return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]
''')

    # Create a basic setup.py
    with open(f'{PROJECT_DIR}/setup.py', 'w') as f:
        f.write('''from setuptools import setup, find_packages

setup(
    name="mypackage",
    version="0.1.0",
    author="Elena Rodriguez",
    author_email="elena.rodriguez@example.com",
    description="A sample Python package for documentation demo",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
)
''')

    # Create a requirements.txt (basic, no sphinx yet)
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write('requests>=2.28.0\npytest>=7.0.0\n')

    # Create venv with basic packages (use --without-pip as ensurepip may not be available)
    venv_path = f'{PROJECT_DIR}/venv'
    pip = f'{venv_path}/bin/pip'
    python_venv = f'{venv_path}/bin/python3'
    if not os.path.exists(venv_path):
        subprocess.run(['python3', '-m', 'venv', '--without-pip', venv_path], check=True)
        # Bootstrap pip
        subprocess.run(['bash', '-c',
                        f'curl -sS https://bootstrap.pypa.io/get-pip.py | {python_venv}'],
                       check=True)
        subprocess.run([pip, 'install', '--quiet', 'requests', 'pytest'], check=True)
        # Install the package itself in development mode
        subprocess.run([pip, 'install', '--quiet', '-e', PROJECT_DIR], check=True)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  src/mypackage/core.py: 5 public functions (no docstrings)')
    print(f'  src/mypackage/utils.py: 3 public functions (no docstrings)')
    print(f'  venv/ with basic packages (no sphinx)')

    # GUI-ready startup: open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

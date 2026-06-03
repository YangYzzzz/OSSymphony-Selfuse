"""
Initial Setup: Configure VSCode to show type stubs for pandas
Task ID: vscode_py_046
Domain: vscode

Creates a Python project with pandas usage and pandas-stubs installed
in a virtual environment. VSCode is open but stubPath is NOT configured,
so Pylance shows incomplete type information.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_046'
PROJECT_DIR = f'{WORKDIR}/workspace'
VSCODE_SETTINGS_DIR = f'{PROJECT_DIR}/.vscode'
VENV_STUBS = f'{PROJECT_DIR}/.venv/lib/python3.10/site-packages/pandas-stubs'

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
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(VSCODE_SETTINGS_DIR, exist_ok=True)

    # Create main.py with realistic pandas usage
    main_py_content = '''"""
Sales Analytics Pipeline
========================
Processes quarterly sales data and generates summary reports.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def load_sales_data() -> pd.DataFrame:
    """Load raw sales data from CSV and perform initial cleaning."""
    np.random.seed(42)
    n_records = 200

    departments = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books"]
    regions = ["North", "South", "East", "West", "Central"]
    sales_reps = [
        "Sarah Chen", "Marcus Johnson", "Priya Patel",
        "James Wilson", "Elena Rodriguez", "David Kim",
        "Rachel Adams", "Omar Hassan", "Lisa Thompson", "Carlos Mendez"
    ]

    start_date = datetime(2025, 1, 1)
    dates = [start_date + timedelta(days=np.random.randint(0, 365)) for _ in range(n_records)]

    df = pd.DataFrame({
        "transaction_id": [f"TXN-{i:05d}" for i in range(1, n_records + 1)],
        "date": dates,
        "sales_rep": np.random.choice(sales_reps, n_records),
        "department": np.random.choice(departments, n_records),
        "region": np.random.choice(regions, n_records),
        "units_sold": np.random.randint(1, 50, n_records),
        "unit_price": np.round(np.random.uniform(9.99, 499.99, n_records), 2),
        "discount_pct": np.random.choice([0, 5, 10, 15, 20], n_records),
    })

    df["revenue"] = df["units_sold"] * df["unit_price"] * (1 - df["discount_pct"] / 100)
    return df


def quarterly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Generate quarterly revenue summary by department."""
    df["quarter"] = df["date"].dt.quarter
    summary = df.groupby(["quarter", "department"]).agg(
        total_revenue=("revenue", "sum"),
        avg_order_value=("revenue", "mean"),
        transaction_count=("transaction_id", "count"),
        unique_reps=("sales_rep", "nunique"),
    ).reset_index()
    return summary


def top_performers(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Identify top N sales representatives by total revenue."""
    perf = df.groupby("sales_rep").agg(
        total_revenue=("revenue", "sum"),
        total_transactions=("transaction_id", "count"),
        avg_discount=("discount_pct", "mean"),
    ).sort_values("total_revenue", ascending=False).head(n)
    return perf


def regional_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze sales performance by region."""
    regional = df.groupby("region").agg(
        revenue=("revenue", "sum"),
        units=("units_sold", "sum"),
        orders=("transaction_id", "count"),
    )
    regional["avg_revenue_per_order"] = regional["revenue"] / regional["orders"]
    regional["avg_units_per_order"] = regional["units"] / regional["orders"]
    return regional.sort_values("revenue", ascending=False)


if __name__ == "__main__":
    sales_df = load_sales_data()
    print(f"Loaded {len(sales_df)} sales records")
    print(f"Date range: {sales_df['date'].min()} to {sales_df['date'].max()}")

    q_summary = quarterly_summary(sales_df)
    print("\\nQuarterly Summary:")
    print(q_summary.to_string(index=False))

    top = top_performers(sales_df)
    print("\\nTop Performers:")
    print(top.to_string())

    regions = regional_analysis(sales_df)
    print("\\nRegional Analysis:")
    print(regions.to_string())
'''
    with open(f'{PROJECT_DIR}/main.py', 'w') as f:
        f.write(main_py_content)

    # Create a helper module
    utils_content = '''"""Utility functions for data processing."""

import pandas as pd
from typing import Optional


def clean_currency(series: pd.Series) -> pd.Series:
    """Remove currency symbols and convert to float."""
    return series.replace(r'[\\$,]', '', regex=True).astype(float)


def date_features(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    """Extract date features from a datetime column."""
    df = df.copy()
    df["year"] = df[date_col].dt.year
    df["month"] = df[date_col].dt.month
    df["day_of_week"] = df[date_col].dt.day_name()
    df["is_weekend"] = df[date_col].dt.dayofweek >= 5
    return df


def filter_by_date_range(
    df: pd.DataFrame,
    start: Optional[str] = None,
    end: Optional[str] = None,
    date_col: str = "date"
) -> pd.DataFrame:
    """Filter DataFrame to a date range."""
    mask = pd.Series([True] * len(df), index=df.index)
    if start:
        mask &= df[date_col] >= pd.Timestamp(start)
    if end:
        mask &= df[date_col] <= pd.Timestamp(end)
    return df[mask]
'''
    with open(f'{PROJECT_DIR}/utils.py', 'w') as f:
        f.write(utils_content)

    # Create requirements.txt
    requirements_content = '''pandas>=2.0.0
numpy>=1.24.0
pandas-stubs>=2.0.0
'''
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write(requirements_content)

    # Create fake virtual environment with pandas-stubs directory
    # This simulates having pandas-stubs installed in the venv
    os.makedirs(VENV_STUBS, exist_ok=True)

    # Create minimal stub files to make it look realistic
    init_stub = '''"""Type stubs for pandas library."""
from pandas.core.frame import DataFrame as DataFrame
from pandas.core.series import Series as Series
from pandas import Timestamp as Timestamp
'''
    with open(f'{VENV_STUBS}/__init__.pyi', 'w') as f:
        f.write(init_stub)

    # Create a core subdirectory with frame stubs
    os.makedirs(f'{VENV_STUBS}/core', exist_ok=True)
    frame_stub = '''"""DataFrame type stubs."""
from typing import Any, Dict, List, Optional, Sequence, Union
import numpy as np

class DataFrame:
    def __init__(self, data: Any = ..., index: Any = ..., columns: Any = ...) -> None: ...
    def groupby(self, by: Union[str, List[str]], **kwargs: Any) -> "DataFrameGroupBy": ...
    def merge(self, right: "DataFrame", on: Optional[str] = ..., how: str = ...) -> "DataFrame": ...
    def sort_values(self, by: Union[str, List[str]], ascending: bool = ...) -> "DataFrame": ...
    def head(self, n: int = ...) -> "DataFrame": ...
    def to_string(self, index: bool = ...) -> str: ...
    def copy(self) -> "DataFrame": ...
    @property
    def dt(self) -> "DatetimeProperties": ...

class DataFrameGroupBy:
    def agg(self, func: Any, **kwargs: Any) -> DataFrame: ...
    def sum(self) -> DataFrame: ...
    def mean(self) -> DataFrame: ...
    def count(self) -> DataFrame: ...
'''
    with open(f'{VENV_STUBS}/core/frame.pyi', 'w') as f:
        f.write(frame_stub)

    with open(f'{VENV_STUBS}/core/__init__.pyi', 'w') as f:
        f.write('')

    # Create venv bin and pyvenv.cfg to make it look like a real venv
    os.makedirs(f'{PROJECT_DIR}/.venv/bin', exist_ok=True)
    pyvenv_cfg = '''home = /usr/bin
include-system-site-packages = false
version = 3.10.12
'''
    with open(f'{PROJECT_DIR}/.venv/pyvenv.cfg', 'w') as f:
        f.write(pyvenv_cfg)

    # Create VSCode settings WITHOUT stubPath (this is what the agent needs to add)
    vscode_settings = {
        "python.defaultInterpreterPath": ".venv/bin/python",
        "python.analysis.autoImportCompletions": True,
        "python.analysis.typeCheckingMode": "basic",
        "editor.fontSize": 14,
        "editor.formatOnSave": True,
        "files.autoSave": "afterDelay"
    }
    with open(f'{VSCODE_SETTINGS_DIR}/settings.json', 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'  main.py: Sales analytics pipeline')
    print(f'  utils.py: Helper functions')
    print(f'  .venv with pandas-stubs at: {VENV_STUBS}')
    print(f'  .vscode/settings.json: NO stubPath configured')

    # Launch VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

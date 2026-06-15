"""
Initial Setup: Configure GitHub Copilot extension settings in VSCode
Task ID: vscode_we_091
Domain: vscode

Initial state: VSCode open with empty user settings. GitHub.copilot extension installed.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_091'

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")


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
    # Ensure VSCode user config directory exists
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Write empty settings (initial state per task context)
    with open(SETTINGS_PATH, "w") as f:
        json.dump({}, f, indent=4)

    print(f"Initial settings created: {SETTINGS_PATH}")
    print(f"Settings content: {{}}")

    # Create a workspace directory with some sample files so VSCode has something to show
    workspace_dir = os.path.join(WORKDIR, "project")
    os.makedirs(workspace_dir, exist_ok=True)

    # Create a sample Python file
    with open(os.path.join(workspace_dir, "main.py"), "w") as f:
        f.write('''"""
Project: Sales Analytics Dashboard
Author: Sarah Chen
Date: 2025-03-15
"""

import pandas as pd
import numpy as np
from datetime import datetime


def load_sales_data(filepath: str) -> pd.DataFrame:
    """Load and validate sales data from CSV."""
    df = pd.read_csv(filepath)
    df["date"] = pd.to_datetime(df["date"])
    df["revenue"] = df["quantity"] * df["unit_price"]
    return df


def calculate_monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales data by month."""
    monthly = df.groupby(df["date"].dt.to_period("M")).agg(
        total_revenue=("revenue", "sum"),
        total_orders=("order_id", "nunique"),
        avg_order_value=("revenue", "mean"),
    )
    return monthly.reset_index()


def get_top_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return top N products by revenue."""
    return (
        df.groupby("product_name")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )


if __name__ == "__main__":
    data = load_sales_data("sales_2025.csv")
    summary = calculate_monthly_summary(data)
    top = get_top_products(data)
    print(summary)
    print(top)
''')

    # Create a sample Markdown file
    with open(os.path.join(workspace_dir, "README.md"), "w") as f:
        f.write("""# Sales Analytics Dashboard

## Overview
This project provides automated sales analytics and reporting.

## Features
- Monthly revenue summaries
- Top product rankings
- Customer segmentation analysis

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Place sales data in `data/` directory
3. Run `python main.py`

## Data Format
The input CSV should contain these columns:
- `date` - Transaction date (YYYY-MM-DD)
- `order_id` - Unique order identifier
- `product_name` - Product name
- `quantity` - Units sold
- `unit_price` - Price per unit
""")

    # Launch VSCode with the project folder
    launch_gui(f'code "{workspace_dir}"', delay_sec=3.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()

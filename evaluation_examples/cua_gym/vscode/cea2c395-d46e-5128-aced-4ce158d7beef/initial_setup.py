"""
Initial Setup: Configure VSCode workspace settings for a Python data science project
Task ID: vscode_we_022
Domain: vscode

Creates a Python data science project directory with realistic files.
The .vscode/ directory does NOT exist yet - the agent must create it.
Opens VSCode with the project folder.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'data-analysis')


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
    os.makedirs(os.path.join(PROJECT_DIR, 'data'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'notebooks'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)

    # Ensure .vscode does NOT exist
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    # Create main analysis script
    with open(os.path.join(PROJECT_DIR, 'src', 'analysis.py'), 'w') as f:
        f.write('''\
"""Sales data analysis pipeline for Q1 2025 regional performance."""

import pandas as pd
import numpy as np
from pathlib import Path


DATA_DIR = Path(__file__).parent.parent / "data"


def load_sales_data(filepath: str) -> pd.DataFrame:
    """Load and clean raw sales CSV data."""
    df = pd.read_csv(filepath)
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["revenue"] = df["quantity"] * df["unit_price"]
    return df


def compute_regional_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales metrics by region."""
    summary = df.groupby("region").agg(
        total_revenue=("revenue", "sum"),
        avg_order_value=("revenue", "mean"),
        order_count=("order_id", "nunique"),
        top_product=("product_name", lambda x: x.mode().iloc[0]),
    ).reset_index()
    return summary.sort_values("total_revenue", ascending=False)


def detect_anomalies(df: pd.DataFrame, threshold: float = 2.5) -> pd.DataFrame:
    """Flag orders with revenue beyond threshold standard deviations."""
    mean_rev = df["revenue"].mean()
    std_rev = df["revenue"].std()
    df["is_anomaly"] = np.abs(df["revenue"] - mean_rev) > threshold * std_rev
    return df[df["is_anomaly"]]


if __name__ == "__main__":
    sales = load_sales_data(DATA_DIR / "q1_sales_2025.csv")
    summary = compute_regional_summary(sales)
    print(summary.to_string(index=False))

    anomalies = detect_anomalies(sales)
    print(f"\\nDetected {len(anomalies)} anomalous orders")
''')

    # Create a utility module
    with open(os.path.join(PROJECT_DIR, 'src', '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(PROJECT_DIR, 'src', 'visualization.py'), 'w') as f:
        f.write('''\
"""Visualization helpers for sales dashboard."""

import matplotlib.pyplot as plt
import seaborn as sns


def plot_revenue_by_region(summary_df, output_path=None):
    """Create a horizontal bar chart of revenue by region."""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=summary_df, x="total_revenue", y="region", ax=ax, palette="viridis")
    ax.set_xlabel("Total Revenue ($)")
    ax.set_ylabel("Region")
    ax.set_title("Q1 2025 Revenue by Region")
    plt.tight_layout()
    if output_path:
        fig.savefig(output_path, dpi=150)
    return fig


def plot_monthly_trend(df, output_path=None):
    """Plot monthly revenue trend with confidence intervals."""
    monthly = df.set_index("order_date").resample("M")["revenue"].agg(["sum", "count"])
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly.index, monthly["sum"], marker="o", linewidth=2)
    ax.fill_between(monthly.index,
                    monthly["sum"] * 0.9,
                    monthly["sum"] * 1.1,
                    alpha=0.2)
    ax.set_title("Monthly Revenue Trend")
    ax.set_ylabel("Revenue ($)")
    plt.tight_layout()
    if output_path:
        fig.savefig(output_path, dpi=150)
    return fig
''')

    # Create a sample Jupyter notebook (as .ipynb JSON)
    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["# Q1 2025 Sales Data Analysis\\n", "\\n", "This notebook explores regional sales patterns and identifies trends."]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import pandas as pd\\n",
                    "import numpy as np\\n",
                    "import matplotlib.pyplot as plt\\n",
                    "import seaborn as sns\\n",
                    "\\n",
                    "sns.set_theme(style='whitegrid')\\n",
                    "pd.set_option('display.max_columns', None)"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Load sales data\\n",
                    "df = pd.read_csv('../data/q1_sales_2025.csv')\\n",
                    "print(f'Loaded {len(df)} records')\\n",
                    "df.head()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## Regional Performance Summary"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "regional = df.groupby('region').agg(\\n",
                    "    total_revenue=('revenue', 'sum'),\\n",
                    "    avg_order=('revenue', 'mean'),\\n",
                    "    num_orders=('order_id', 'nunique')\\n",
                    ")\\n",
                    "regional.sort_values('total_revenue', ascending=False)"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.12"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }
    import json
    with open(os.path.join(PROJECT_DIR, 'notebooks', 'exploration.ipynb'), 'w') as f:
        json.dump(notebook_content, f, indent=1)

    # Create a sample CSV data file
    with open(os.path.join(PROJECT_DIR, 'data', 'q1_sales_2025.csv'), 'w') as f:
        f.write("order_id,order_date,region,product_name,quantity,unit_price\n")
        f.write("ORD-1001,2025-01-05,Northeast,Wireless Keyboard,3,49.99\n")
        f.write("ORD-1002,2025-01-08,Southwest,USB-C Hub,1,79.95\n")
        f.write("ORD-1003,2025-01-12,Midwest,Ergonomic Mouse,2,34.50\n")
        f.write("ORD-1004,2025-01-15,Southeast,Monitor Stand,1,129.00\n")
        f.write("ORD-1005,2025-01-19,Northeast,Laptop Sleeve,4,24.99\n")
        f.write("ORD-1006,2025-01-22,West,Webcam HD,2,89.00\n")
        f.write("ORD-1007,2025-01-28,Midwest,Desk Lamp LED,1,45.00\n")
        f.write("ORD-1008,2025-02-03,Southeast,Noise-Cancel Headphones,1,199.99\n")
        f.write("ORD-1009,2025-02-07,Northeast,Mechanical Keyboard,2,119.99\n")
        f.write("ORD-1010,2025-02-11,West,Portable SSD 1TB,3,109.95\n")
        f.write("ORD-1011,2025-02-14,Southwest,Bluetooth Speaker,2,59.99\n")
        f.write("ORD-1012,2025-02-20,Midwest,Cable Management Kit,5,15.99\n")
        f.write("ORD-1013,2025-02-25,Northeast,Docking Station,1,249.00\n")
        f.write("ORD-1014,2025-03-01,Southeast,Trackpad,1,69.99\n")
        f.write("ORD-1015,2025-03-08,West,Standing Desk Mat,2,39.99\n")

    # Create requirements.txt
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write("pandas>=2.0.0\n")
        f.write("numpy>=1.24.0\n")
        f.write("matplotlib>=3.7.0\n")
        f.write("seaborn>=0.12.0\n")
        f.write("jupyter>=1.0.0\n")
        f.write("scikit-learn>=1.3.0\n")

    # Create README
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write("# Data Analysis Project\n\n")
        f.write("Q1 2025 regional sales performance analysis.\n\n")
        f.write("## Structure\n\n")
        f.write("- `data/` - Raw and processed datasets\n")
        f.write("- `notebooks/` - Jupyter exploration notebooks\n")
        f.write("- `src/` - Python analysis modules\n")

    print(f'Project created at: {PROJECT_DIR}')
    print(f'.vscode directory exists: {os.path.exists(vscode_dir)}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

"""
Initial Setup: Create a monolithic analysis notebook with 14 cells
Task ID: vscode_gf1_086
Domain: vscode (notebook refactoring)
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf1_086'
NOTEBOOKS_DIR = f'{WORKDIR}/notebooks'

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


def make_code_cell(source, execution_count=None):
    """Create a Jupyter notebook code cell."""
    return {
        "cell_type": "code",
        "execution_count": execution_count,
        "metadata": {},
        "outputs": [],
        "source": source if isinstance(source, list) else [source]
    }


def make_markdown_cell(source):
    """Create a Jupyter notebook markdown cell."""
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source if isinstance(source, list) else [source]
    }


def create_notebook(cells):
    """Build a complete Jupyter notebook dict."""
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
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
        "cells": cells
    }


def create_initial():
    os.makedirs(NOTEBOOKS_DIR, exist_ok=True)

    # Build 14 cells: first 8 for data cleaning, last 6 for visualization
    cells = []

    # --- Cell 1: Imports (all combined) ---
    cells.append(make_code_cell([
        "import pandas as pd\n",
        "import numpy as np\n",
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "from datetime import datetime\n",
        "import os"
    ]))

    # --- Cell 2: Markdown header for data cleaning section ---
    cells.append(make_markdown_cell([
        "# Sales Data Analysis\n",
        "\n",
        "This notebook performs end-to-end analysis of quarterly sales data,\n",
        "including data cleaning, transformation, and visualization."
    ]))

    # --- Cell 3: Load raw data ---
    cells.append(make_code_cell([
        "# Load raw sales data\n",
        "raw_data = {\n",
        "    'date': ['2025-01-15', '2025-01-22', '2025-02-03', '2025-02-14',\n",
        "             '2025-03-01', '2025-03-18', None, '2025-04-05',\n",
        "             '2025-04-20', '2025-05-02', '2025-05-15', '2025-06-01'],\n",
        "    'product': ['Widget A', 'Widget B', 'Widget A', 'Widget C',\n",
        "                'Widget B', 'Widget A', 'Widget C', 'Widget B',\n",
        "                'Widget A', 'Widget C', 'Widget B', 'Widget A'],\n",
        "    'region': ['North', 'South', 'East', 'West', 'North', 'South',\n",
        "               'East', 'West', 'North', 'South', 'East', 'West'],\n",
        "    'units_sold': [150, 230, 180, -5, 310, 275, 190, 205, 160, 340, 280, 225],\n",
        "    'unit_price': [29.99, 45.50, 29.99, 67.25, 45.50, 29.99,\n",
        "                   67.25, 45.50, 29.99, 67.25, 45.50, 29.99],\n",
        "    'sales_rep': ['Sarah Chen', 'Marcus Johnson', 'Aisha Patel', 'Carlos Rivera',\n",
        "                  'Sarah Chen', 'Marcus Johnson', 'Aisha Patel', 'Carlos Rivera',\n",
        "                  'Sarah Chen', 'Marcus Johnson', 'Aisha Patel', 'Carlos Rivera']\n",
        "}\n",
        "df = pd.DataFrame(raw_data)\n",
        "print(f'Loaded {len(df)} records')\n",
        "df.head()"
    ]))

    # --- Cell 4: Handle missing values ---
    cells.append(make_code_cell([
        "# Handle missing dates\n",
        "print(f'Missing dates: {df[\"date\"].isna().sum()}')\n",
        "df['date'] = pd.to_datetime(df['date'])\n",
        "df['date'] = df['date'].fillna(pd.Timestamp('2025-03-10'))\n",
        "print(f'After fill: {df[\"date\"].isna().sum()} missing')"
    ]))

    # --- Cell 5: Fix negative values ---
    cells.append(make_code_cell([
        "# Fix negative units_sold (data entry errors)\n",
        "neg_mask = df['units_sold'] < 0\n",
        "print(f'Found {neg_mask.sum()} negative values')\n",
        "df.loc[neg_mask, 'units_sold'] = df.loc[neg_mask, 'units_sold'].abs()\n",
        "print('Negative values corrected to absolute values')"
    ]))

    # --- Cell 6: Calculate derived columns ---
    cells.append(make_code_cell([
        "# Calculate revenue and add month column\n",
        "df['revenue'] = df['units_sold'] * df['unit_price']\n",
        "df['month'] = df['date'].dt.month\n",
        "df['quarter'] = df['date'].dt.quarter\n",
        "print(f'Total revenue: ${df[\"revenue\"].sum():,.2f}')\n",
        "df.head()"
    ]))

    # --- Cell 7: Remove duplicates and validate ---
    cells.append(make_code_cell([
        "# Remove any duplicate entries\n",
        "before_count = len(df)\n",
        "df = df.drop_duplicates(subset=['date', 'product', 'region'])\n",
        "after_count = len(df)\n",
        "print(f'Removed {before_count - after_count} duplicates')\n",
        "print(f'Data shape: {df.shape}')\n",
        "print(f'Date range: {df[\"date\"].min()} to {df[\"date\"].max()}')"
    ]))

    # --- Cell 8: Save cleaned data ---
    cells.append(make_code_cell([
        "# Save cleaned dataset\n",
        "output_path = os.path.join(os.path.dirname(os.path.abspath('__file__')), 'cleaned_sales.csv')\n",
        "df.to_csv(output_path, index=False)\n",
        "print(f'Cleaned data saved to {output_path}')\n",
        "print(f'Final dataset: {len(df)} rows, {len(df.columns)} columns')"
    ]))

    # --- Cell 9: Markdown header for visualization section ---
    cells.append(make_markdown_cell([
        "## Visualization Section\n",
        "\n",
        "Generate charts and graphs from the cleaned sales data."
    ]))

    # --- Cell 10: Revenue by product bar chart ---
    cells.append(make_code_cell([
        "# Revenue by product\n",
        "product_revenue = df.groupby('product')['revenue'].sum().sort_values(ascending=False)\n",
        "fig, ax = plt.subplots(figsize=(10, 6))\n",
        "product_revenue.plot(kind='bar', ax=ax, color=['#2196F3', '#4CAF50', '#FF9800'])\n",
        "ax.set_title('Total Revenue by Product', fontsize=14)\n",
        "ax.set_ylabel('Revenue ($)')\n",
        "ax.set_xlabel('Product')\n",
        "plt.xticks(rotation=45)\n",
        "plt.tight_layout()\n",
        "plt.savefig('revenue_by_product.png', dpi=150)\n",
        "plt.show()"
    ]))

    # --- Cell 11: Monthly sales trend ---
    cells.append(make_code_cell([
        "# Monthly sales trend\n",
        "monthly_sales = df.groupby('month')['revenue'].sum()\n",
        "fig, ax = plt.subplots(figsize=(10, 6))\n",
        "monthly_sales.plot(kind='line', marker='o', ax=ax, color='#E91E63', linewidth=2)\n",
        "ax.set_title('Monthly Revenue Trend', fontsize=14)\n",
        "ax.set_ylabel('Revenue ($)')\n",
        "ax.set_xlabel('Month')\n",
        "ax.grid(True, alpha=0.3)\n",
        "plt.tight_layout()\n",
        "plt.savefig('monthly_trend.png', dpi=150)\n",
        "plt.show()"
    ]))

    # --- Cell 12: Regional distribution pie chart ---
    cells.append(make_code_cell([
        "# Regional distribution\n",
        "region_revenue = df.groupby('region')['revenue'].sum()\n",
        "fig, ax = plt.subplots(figsize=(8, 8))\n",
        "colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']\n",
        "region_revenue.plot(kind='pie', ax=ax, colors=colors, autopct='%1.1f%%',\n",
        "                    startangle=90, fontsize=12)\n",
        "ax.set_title('Revenue by Region', fontsize=14)\n",
        "ax.set_ylabel('')\n",
        "plt.tight_layout()\n",
        "plt.savefig('regional_distribution.png', dpi=150)\n",
        "plt.show()"
    ]))

    # --- Cell 13: Sales rep performance heatmap ---
    cells.append(make_code_cell([
        "# Sales rep performance by product\n",
        "pivot = df.pivot_table(values='revenue', index='sales_rep',\n",
        "                       columns='product', aggfunc='sum', fill_value=0)\n",
        "fig, ax = plt.subplots(figsize=(10, 6))\n",
        "sns.heatmap(pivot, annot=True, fmt=',.0f', cmap='YlOrRd', ax=ax)\n",
        "ax.set_title('Revenue by Sales Rep and Product', fontsize=14)\n",
        "plt.tight_layout()\n",
        "plt.savefig('rep_performance.png', dpi=150)\n",
        "plt.show()"
    ]))

    # --- Cell 14: Summary statistics ---
    cells.append(make_code_cell([
        "# Summary statistics\n",
        "print('=== Sales Analysis Summary ===')\n",
        "print(f'Total Revenue: ${df[\"revenue\"].sum():,.2f}')\n",
        "print(f'Average Order Value: ${df[\"revenue\"].mean():,.2f}')\n",
        "print(f'Top Product: {df.groupby(\"product\")[\"revenue\"].sum().idxmax()}')\n",
        "print(f'Top Region: {df.groupby(\"region\")[\"revenue\"].sum().idxmax()}')\n",
        "print(f'Top Sales Rep: {df.groupby(\"sales_rep\")[\"revenue\"].sum().idxmax()}')\n",
        "print(f'Period: {df[\"date\"].min().strftime(\"%Y-%m-%d\")} to {df[\"date\"].max().strftime(\"%Y-%m-%d\")}')"
    ]))

    # Build and save the notebook
    nb = create_notebook(cells)
    output_path = os.path.join(NOTEBOOKS_DIR, 'analysis.ipynb')
    with open(output_path, 'w') as f:
        json.dump(nb, f, indent=1)
    print(f'Initial notebook created: {output_path}')
    print(f'Total cells: {len(cells)}')

    # Open VSCode with the notebooks folder and the analysis notebook
    launch_gui(f'code "{NOTEBOOKS_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{output_path}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

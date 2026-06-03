"""
Initial Setup: Convert code cell to markdown and markdown cell to code in Jupyter notebook
Task ID: vscode_prod_010
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_prod_010'
PROJECT_DIR = f'{WORKDIR}/projects/data-science'
OUTPUT = f'{PROJECT_DIR}/exploration.ipynb'


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
    os.makedirs(PROJECT_DIR, exist_ok=True)

    notebook = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "from datetime import datetime\n",
                    "\n",
                    "print('Libraries loaded successfully')"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": 2,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Load the quarterly sales dataset\n",
                    "data = {\n",
                    "    'Quarter': ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025'],\n",
                    "    'Revenue': [145200, 162800, 158400, 189600, 172300],\n",
                    "    'Expenses': [98700, 105400, 101200, 118900, 109500],\n",
                    "    'Customers': [342, 389, 371, 425, 398],\n",
                    "    'Region': ['West', 'West', 'East', 'East', 'West']\n",
                    "}\n",
                    "df = pd.DataFrame(data)\n",
                    "df['Profit'] = df['Revenue'] - df['Expenses']\n",
                    "print(f'Dataset loaded: {len(df)} records')"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Data Exploration Summary\n",
                    "# \n",
                    "# This section analyzes the quarterly sales performance\n",
                    "# across different regions. Key metrics include:\n",
                    "# - Revenue trends over the past 5 quarters\n",
                    "# - Expense-to-revenue ratio analysis\n",
                    "# - Customer acquisition rates by region\n",
                    "# \n",
                    "# The analysis below focuses on identifying seasonal\n",
                    "# patterns and regional performance differences."
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "summary_stats = df.describe()\n",
                    "avg_profit_by_region = df.groupby('Region')['Profit'].mean()\n",
                    "growth_rate = (df['Revenue'].iloc[-1] - df['Revenue'].iloc[0]) / df['Revenue'].iloc[0] * 100\n",
                    "print(f'Average profit margin: {df[\"Profit\"].mean():.2f}')\n",
                    "print(f'Revenue growth rate: {growth_rate:.1f}%')"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": 3,
                "metadata": {},
                "outputs": [],
                "source": [
                    "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
                    "\n",
                    "# Revenue vs Expenses bar chart\n",
                    "x = range(len(df))\n",
                    "axes[0].bar(x, df['Revenue'], width=0.4, label='Revenue', color='#2196F3')\n",
                    "axes[0].bar([i + 0.4 for i in x], df['Expenses'], width=0.4, label='Expenses', color='#FF5722')\n",
                    "axes[0].set_title('Revenue vs Expenses by Quarter')\n",
                    "axes[0].set_xticks([i + 0.2 for i in x])\n",
                    "axes[0].set_xticklabels(df['Quarter'], rotation=45)\n",
                    "axes[0].legend()\n",
                    "\n",
                    "# Profit trend line\n",
                    "axes[1].plot(df['Quarter'], df['Profit'], marker='o', color='#4CAF50', linewidth=2)\n",
                    "axes[1].set_title('Profit Trend')\n",
                    "axes[1].tick_params(axis='x', rotation=45)\n",
                    "\n",
                    "plt.tight_layout()\n",
                    "plt.savefig('quarterly_analysis.png', dpi=150)\n",
                    "plt.show()"
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
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbformat_minor": 0,
                "pygments_lexer": "ipython3",
                "version": "3.10.12"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    with open(OUTPUT, 'w') as f:
        json.dump(notebook, f, indent=1)

    print(f'Initial file created: {OUTPUT}')

    # Launch VSCode with the project directory and the notebook file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

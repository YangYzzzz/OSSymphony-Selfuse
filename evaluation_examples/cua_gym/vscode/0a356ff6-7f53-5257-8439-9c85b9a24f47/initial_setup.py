"""
Initial Setup: Create a data-science project with analysis.ipynb, no launch.json
Task ID: vscode_td_087
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_087'
PROJECT_DIR = f'{WORKDIR}/projects/data-science'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'


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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create a realistic Jupyter notebook: analysis.ipynb
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Customer Churn Analysis\n",
                    "\n",
                    "Exploratory data analysis for predicting customer churn in a telecom dataset."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "import seaborn as sns\n",
                    "\n",
                    "sns.set_theme(style='whitegrid')\n",
                    "pd.set_option('display.max_columns', None)"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Generate synthetic telecom churn dataset\n",
                    "np.random.seed(42)\n",
                    "n_customers = 500\n",
                    "\n",
                    "data = {\n",
                    "    'customer_id': [f'CUST-{i:04d}' for i in range(1, n_customers + 1)],\n",
                    "    'tenure_months': np.random.randint(1, 72, n_customers),\n",
                    "    'monthly_charges': np.round(np.random.uniform(20, 110, n_customers), 2),\n",
                    "    'total_charges': np.round(np.random.uniform(100, 8000, n_customers), 2),\n",
                    "    'contract_type': np.random.choice(['Month-to-month', 'One year', 'Two year'], n_customers, p=[0.5, 0.3, 0.2]),\n",
                    "    'internet_service': np.random.choice(['DSL', 'Fiber optic', 'No'], n_customers, p=[0.35, 0.45, 0.2]),\n",
                    "    'churned': np.random.choice([0, 1], n_customers, p=[0.73, 0.27])\n",
                    "}\n",
                    "\n",
                    "df = pd.DataFrame(data)\n",
                    "print(f'Dataset shape: {df.shape}')\n",
                    "df.head(10)"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Churn rate by contract type\n",
                    "churn_by_contract = df.groupby('contract_type')['churned'].mean().sort_values(ascending=False)\n",
                    "print('Churn Rate by Contract Type:')\n",
                    "print(churn_by_contract.to_string())\n",
                    "\n",
                    "fig, ax = plt.subplots(figsize=(8, 5))\n",
                    "churn_by_contract.plot(kind='bar', color=['#e74c3c', '#f39c12', '#2ecc71'], ax=ax)\n",
                    "ax.set_title('Churn Rate by Contract Type')\n",
                    "ax.set_ylabel('Churn Rate')\n",
                    "plt.tight_layout()\n",
                    "plt.savefig('churn_by_contract.png', dpi=150)\n",
                    "plt.show()"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Monthly charges distribution: churned vs retained\n",
                    "fig, ax = plt.subplots(figsize=(8, 5))\n",
                    "df[df['churned'] == 0]['monthly_charges'].hist(alpha=0.6, bins=30, label='Retained', ax=ax)\n",
                    "df[df['churned'] == 1]['monthly_charges'].hist(alpha=0.6, bins=30, label='Churned', ax=ax)\n",
                    "ax.set_title('Monthly Charges Distribution')\n",
                    "ax.set_xlabel('Monthly Charges ($)')\n",
                    "ax.legend()\n",
                    "plt.tight_layout()\n",
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
                "name": "python",
                "version": "3.10.12"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    notebook_path = f'{PROJECT_DIR}/analysis.ipynb'
    with open(notebook_path, 'w') as f:
        json.dump(notebook, f, indent=1)
    print(f'Created notebook: {notebook_path}')

    # Create a requirements.txt for realism
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write("pandas>=2.0\nnumpy>=1.24\nmatplotlib>=3.7\nseaborn>=0.12\nscikit-learn>=1.3\n")
    print(f'Created requirements.txt')

    # Create a small utility module
    os.makedirs(f'{PROJECT_DIR}/utils', exist_ok=True)
    with open(f'{PROJECT_DIR}/utils/__init__.py', 'w') as f:
        f.write("")
    with open(f'{PROJECT_DIR}/utils/preprocessing.py', 'w') as f:
        f.write("""\"\"\"Data preprocessing utilities for churn analysis.\"\"\"
import pandas as pd
import numpy as np


def encode_categorical(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    \"\"\"One-hot encode specified categorical columns.\"\"\"
    return pd.get_dummies(df, columns=columns, drop_first=True)


def scale_numeric(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    \"\"\"Min-max scale specified numeric columns.\"\"\"
    result = df.copy()
    for col in columns:
        min_val = result[col].min()
        max_val = result[col].max()
        if max_val > min_val:
            result[col] = (result[col] - min_val) / (max_val - min_val)
    return result
""")
    print(f'Created utils/preprocessing.py')

    # Ensure NO .vscode/launch.json exists
    launch_json_path = f'{VSCODE_DIR}/launch.json'
    if os.path.exists(launch_json_path):
        os.remove(launch_json_path)
        print(f'Removed existing launch.json')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

"""
Initial Setup: Set up a Python data science project workspace without extensions.json
Task ID: vscode_lp_085
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_085'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'


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
    # Create the project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/data', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/notebooks', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)

    # requirements.txt
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write("""numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
scikit-learn>=1.3.0
jupyter>=1.0.0
scipy>=1.11.0
statsmodels>=0.14.0
""")

    # Main analysis script
    with open(f'{PROJECT_DIR}/src/analysis.py', 'w') as f:
        f.write('''"""
Customer Churn Analysis Pipeline
Analyzes customer behavior data to predict churn probability.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score


def load_data(filepath: str) -> pd.DataFrame:
    """Load and validate the customer dataset."""
    df = pd.read_csv(filepath)
    required_cols = [
        "customer_id", "tenure_months", "monthly_charges",
        "total_charges", "contract_type", "churn"
    ]
    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return df


def preprocess(df: pd.DataFrame) -> tuple:
    """Clean data and prepare features for modeling."""
    df = df.dropna(subset=["total_charges"])
    df["total_charges"] = pd.to_numeric(df["total_charges"], errors="coerce")
    df = df.fillna(df.median(numeric_only=True))

    feature_cols = ["tenure_months", "monthly_charges", "total_charges"]
    X = df[feature_cols]
    y = df["churn"].map({"Yes": 1, "No": 0})
    return train_test_split(X, y, test_size=0.2, random_state=42)


def train_model(X_train, y_train):
    """Train a Random Forest classifier."""
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_split=5,
        random_state=42,
    )
    model.fit(X_train, y_train)
    return model


def evaluate(model, X_test, y_test) -> dict:
    """Evaluate model performance."""
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    report = classification_report(y_test, y_pred, output_dict=True)
    auc = roc_auc_score(y_test, y_proba)
    return {"classification_report": report, "auc_roc": auc}


if __name__ == "__main__":
    df = load_data("../data/customer_churn.csv")
    X_train, X_test, y_train, y_test = preprocess(df)
    model = train_model(X_train, y_train)
    results = evaluate(model, X_test, y_test)
    print(f"AUC-ROC: {results[\'auc_roc\']:.4f}")
''')

    # Data preprocessing utility
    with open(f'{PROJECT_DIR}/src/data_utils.py', 'w') as f:
        f.write('''"""
Data utility functions for the churn analysis project.
"""

import pandas as pd
import numpy as np
from pathlib import Path


def generate_sample_data(n_customers: int = 500, seed: int = 42) -> pd.DataFrame:
    """Generate synthetic customer churn dataset for development."""
    rng = np.random.default_rng(seed)

    tenure = rng.integers(1, 72, size=n_customers)
    monthly = rng.uniform(20, 120, size=n_customers).round(2)
    total = (tenure * monthly * rng.uniform(0.8, 1.1, size=n_customers)).round(2)

    contracts = rng.choice(
        ["Month-to-month", "One year", "Two year"],
        size=n_customers,
        p=[0.5, 0.3, 0.2],
    )

    churn_prob = 0.3 - 0.003 * tenure + 0.001 * monthly
    churn_prob = np.clip(churn_prob, 0.05, 0.7)
    churn = rng.binomial(1, churn_prob)

    return pd.DataFrame({
        "customer_id": [f"CUST-{i:05d}" for i in range(n_customers)],
        "tenure_months": tenure,
        "monthly_charges": monthly,
        "total_charges": total,
        "contract_type": contracts,
        "churn": np.where(churn, "Yes", "No"),
    })


def compute_summary_stats(df: pd.DataFrame) -> dict:
    """Compute summary statistics grouped by churn status."""
    grouped = df.groupby("churn").agg(
        avg_tenure=("tenure_months", "mean"),
        avg_monthly=("monthly_charges", "mean"),
        avg_total=("total_charges", "mean"),
        count=("customer_id", "count"),
    )
    return grouped.to_dict(orient="index")


if __name__ == "__main__":
    data = generate_sample_data()
    data.to_csv("../data/customer_churn.csv", index=False)
    print(f"Generated {len(data)} customer records")
    stats = compute_summary_stats(data)
    for status, metrics in stats.items():
        print(f"  {status}: {metrics}")
''')

    # Visualization module
    with open(f'{PROJECT_DIR}/src/visualize.py', 'w') as f:
        f.write('''"""
Visualization utilities for customer churn analysis.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_churn_distribution(df: pd.DataFrame, output_path: str = None):
    """Plot the distribution of churn vs non-churn customers."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    sns.countplot(data=df, x="churn", ax=axes[0], palette="Set2")
    axes[0].set_title("Churn Distribution")

    sns.boxplot(data=df, x="churn", y="monthly_charges", ax=axes[1], palette="Set2")
    axes[1].set_title("Monthly Charges by Churn Status")

    sns.histplot(data=df, x="tenure_months", hue="churn", ax=axes[2], palette="Set2")
    axes[2].set_title("Tenure Distribution")

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150)
    plt.close()


def plot_correlation_matrix(df: pd.DataFrame, output_path: str = None):
    """Plot correlation heatmap for numeric features."""
    numeric_df = df.select_dtypes(include="number")
    corr = numeric_df.corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, ax=ax)
    ax.set_title("Feature Correlation Matrix")

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150)
    plt.close()
''')

    # README
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write("""# Customer Churn Analysis

A data science project analyzing customer behavior patterns to predict
churn probability using machine learning.

## Project Structure

```
vscode_lp_085/
├── data/              # Raw and processed datasets
├── notebooks/         # Jupyter notebooks for exploration
├── src/               # Source code modules
│   ├── analysis.py    # Main ML pipeline
│   ├── data_utils.py  # Data loading and preprocessing
│   └── visualize.py   # Plotting utilities
└── requirements.txt   # Python dependencies
```

## Setup

```bash
pip install -r requirements.txt
python src/data_utils.py   # Generate sample data
python src/analysis.py     # Run analysis pipeline
```

## Team

- Sarah Chen — Lead Data Scientist
- Marcus Johnson — ML Engineer
- Priya Patel — Data Analyst
""")

    # __init__.py for src package
    with open(f'{PROJECT_DIR}/src/__init__.py', 'w') as f:
        f.write('"""Customer churn analysis package."""\n')

    # .gitignore
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write("""__pycache__/
*.pyc
.ipynb_checkpoints/
data/*.csv
*.egg-info/
dist/
build/
.env
""")

    # Ensure NO .vscode/extensions.json exists
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    extensions_file = f'{vscode_dir}/extensions.json'
    if os.path.exists(extensions_file):
        os.remove(extensions_file)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'.vscode/extensions.json does NOT exist (as required)')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

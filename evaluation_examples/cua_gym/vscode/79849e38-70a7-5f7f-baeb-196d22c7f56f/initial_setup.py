"""
Initial Setup: Jupyter notebook with 7 cells in original order for cell reordering task
Task ID: vscode_rf_009
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rf_009'
PROJECT_DIR = f'{WORKDIR}/projects/ml_pipeline'
OUTPUT = f'{PROJECT_DIR}/pipeline.ipynb'


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


def create_notebook_cell(cell_type, source, execution_count=None):
    """Create a Jupyter notebook cell."""
    cell = {
        "cell_type": cell_type,
        "metadata": {},
        "source": source if isinstance(source, list) else [source],
    }
    if cell_type == "code":
        cell["execution_count"] = execution_count
        cell["outputs"] = []
    return cell


def create_initial():
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Cell 1: Imports
    cell1 = create_notebook_cell("code", [
        "import numpy as np\n",
        "import pandas as pd\n",
        "from sklearn.model_selection import train_test_split\n",
        "from sklearn.ensemble import RandomForestClassifier\n",
        "from sklearn.metrics import accuracy_score, classification_report\n",
        "from sklearn.preprocessing import StandardScaler, LabelEncoder\n",
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "\n",
        "# Set random seed for reproducibility\n",
        "np.random.seed(42)\n",
        "print('Libraries loaded successfully')"
    ], execution_count=1)

    # Cell 2: Model Training
    cell2 = create_notebook_cell("code", [
        "# Model Training\n",
        "X_train, X_test, y_train, y_test = train_test_split(\n",
        "    X_processed, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded\n",
        ")\n",
        "\n",
        "rf_model = RandomForestClassifier(\n",
        "    n_estimators=200,\n",
        "    max_depth=15,\n",
        "    min_samples_split=5,\n",
        "    min_samples_leaf=2,\n",
        "    random_state=42,\n",
        "    n_jobs=-1\n",
        ")\n",
        "\n",
        "rf_model.fit(X_train, y_train)\n",
        "y_pred = rf_model.predict(X_test)\n",
        "print(f'Training complete. Train size: {len(X_train)}, Test size: {len(X_test)}')"
    ], execution_count=2)

    # Cell 3: Data Cleaning (preprocessing)
    cell3 = create_notebook_cell("code", [
        "# Data Cleaning\n",
        "df = pd.read_csv('customer_churn_raw.csv')\n",
        "print(f'Raw dataset shape: {df.shape}')\n",
        "\n",
        "# Remove duplicate entries\n",
        "df = df.drop_duplicates(subset='customer_id', keep='last')\n",
        "\n",
        "# Handle missing values\n",
        "df['monthly_charges'].fillna(df['monthly_charges'].median(), inplace=True)\n",
        "df['total_charges'] = pd.to_numeric(df['total_charges'], errors='coerce')\n",
        "df['total_charges'].fillna(df['total_charges'].median(), inplace=True)\n",
        "\n",
        "# Remove outliers using IQR method\n",
        "for col in ['monthly_charges', 'total_charges', 'tenure_months']:\n",
        "    Q1 = df[col].quantile(0.25)\n",
        "    Q3 = df[col].quantile(0.75)\n",
        "    IQR = Q3 - Q1\n",
        "    df = df[(df[col] >= Q1 - 1.5 * IQR) & (df[col] <= Q3 + 1.5 * IQR)]\n",
        "\n",
        "print(f'Cleaned dataset shape: {df.shape}')"
    ], execution_count=3)

    # Cell 4: Data Normalization (preprocessing)
    cell4 = create_notebook_cell("code", [
        "# Data Normalization\n",
        "scaler = StandardScaler()\n",
        "\n",
        "numeric_cols = ['tenure_months', 'monthly_charges', 'total_charges',\n",
        "                'num_support_tickets', 'avg_session_duration']\n",
        "\n",
        "df[numeric_cols] = scaler.fit_transform(df[numeric_cols])\n",
        "\n",
        "# Encode categorical variables\n",
        "le = LabelEncoder()\n",
        "categorical_cols = ['contract_type', 'payment_method', 'internet_service']\n",
        "for col in categorical_cols:\n",
        "    df[col] = le.fit_transform(df[col].astype(str))\n",
        "\n",
        "print(f'Normalized columns: {numeric_cols}')\n",
        "print(f'Encoded columns: {categorical_cols}')\n",
        "print(df[numeric_cols].describe().round(2))"
    ], execution_count=4)

    # Cell 5: Feature Engineering (preprocessing)
    cell5 = create_notebook_cell("code", [
        "# Feature Engineering\n",
        "df['charge_per_month'] = df['total_charges'] / (df['tenure_months'] + 1)\n",
        "df['support_ratio'] = df['num_support_tickets'] / (df['tenure_months'] + 1)\n",
        "df['engagement_score'] = df['avg_session_duration'] * df['tenure_months']\n",
        "\n",
        "# Create interaction features\n",
        "df['charges_tenure_interaction'] = df['monthly_charges'] * df['tenure_months']\n",
        "df['high_value_customer'] = (df['monthly_charges'] > df['monthly_charges'].quantile(0.75)).astype(int)\n",
        "\n",
        "# Prepare final feature matrix\n",
        "feature_cols = numeric_cols + categorical_cols + [\n",
        "    'charge_per_month', 'support_ratio', 'engagement_score',\n",
        "    'charges_tenure_interaction', 'high_value_customer'\n",
        "]\n",
        "X_processed = df[feature_cols]\n",
        "y_encoded = df['churn_label']\n",
        "\n",
        "print(f'Feature matrix shape: {X_processed.shape}')\n",
        "print(f'Features: {feature_cols}')"
    ], execution_count=5)

    # Cell 6: Evaluation
    cell6 = create_notebook_cell("code", [
        "# Model Evaluation\n",
        "accuracy = accuracy_score(y_test, y_pred)\n",
        "print(f'Model Accuracy: {accuracy:.4f}')\n",
        "print('\\nClassification Report:')\n",
        "print(classification_report(y_test, y_pred, target_names=['No Churn', 'Churn']))\n",
        "\n",
        "# Feature importance analysis\n",
        "feature_importance = pd.DataFrame({\n",
        "    'feature': feature_cols,\n",
        "    'importance': rf_model.feature_importances_\n",
        "}).sort_values('importance', ascending=False)\n",
        "\n",
        "print('\\nTop 5 Important Features:')\n",
        "print(feature_importance.head().to_string(index=False))"
    ], execution_count=6)

    # Cell 7: Visualization
    cell7 = create_notebook_cell("code", [
        "# Visualization\n",
        "fig, axes = plt.subplots(1, 3, figsize=(18, 5))\n",
        "\n",
        "# Feature Importance Bar Plot\n",
        "axes[0].barh(feature_importance['feature'][:10], feature_importance['importance'][:10])\n",
        "axes[0].set_title('Top 10 Feature Importances')\n",
        "axes[0].set_xlabel('Importance')\n",
        "\n",
        "# Confusion Matrix Heatmap\n",
        "from sklearn.metrics import confusion_matrix\n",
        "cm = confusion_matrix(y_test, y_pred)\n",
        "sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[1],\n",
        "            xticklabels=['No Churn', 'Churn'],\n",
        "            yticklabels=['No Churn', 'Churn'])\n",
        "axes[1].set_title('Confusion Matrix')\n",
        "axes[1].set_xlabel('Predicted')\n",
        "axes[1].set_ylabel('Actual')\n",
        "\n",
        "# Prediction Distribution\n",
        "axes[2].hist(rf_model.predict_proba(X_test)[:, 1], bins=30, edgecolor='black', alpha=0.7)\n",
        "axes[2].set_title('Churn Probability Distribution')\n",
        "axes[2].set_xlabel('Predicted Probability')\n",
        "axes[2].set_ylabel('Frequency')\n",
        "\n",
        "plt.tight_layout()\n",
        "plt.savefig('pipeline_results.png', dpi=150, bbox_inches='tight')\n",
        "plt.show()\n",
        "print('Visualization saved to pipeline_results.png')"
    ], execution_count=7)

    # Build the notebook
    notebook = {
        "cells": [cell1, cell2, cell3, cell4, cell5, cell6, cell7],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbformat_minor": 2,
                "pygments_lexer": "ipython3",
                "version": "3.10.12"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }

    with open(OUTPUT, 'w') as f:
        json.dump(notebook, f, indent=1)

    print(f'Initial notebook created: {OUTPUT}')

    # Launch VSCode with the project folder and open the notebook
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

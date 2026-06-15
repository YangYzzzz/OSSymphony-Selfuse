"""
Initial Setup: Create a Python file with 35 lines of imports in 3 logical groups, no region comments.
Task ID: vscode_rf_022
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rf_022'
PROJECT_DIR = f'{WORKDIR}/projects/datascience'
OUTPUT = f'{PROJECT_DIR}/analysis.py'


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

    # Build analysis.py with 35 lines of imports in 3 groups, then code starting at line 37
    lines = []

    # Group 1: Standard Library (lines 1-10)
    lines.append("import os")                        # 1
    lines.append("import sys")                       # 2
    lines.append("import json")                      # 3
    lines.append("import csv")                       # 4
    lines.append("import datetime")                  # 5
    lines.append("import re")                        # 6
    lines.append("import math")                      # 7
    lines.append("import collections")               # 8
    lines.append("import itertools")                 # 9
    lines.append("import functools")                 # 10

    # Blank line separating groups
    lines.append("")                                 # 11

    # Group 2: Third-party packages (lines 12-25)
    lines.append("import numpy as np")               # 12
    lines.append("import pandas as pd")              # 13
    lines.append("import matplotlib.pyplot as plt")  # 14
    lines.append("import seaborn as sns")            # 15
    lines.append("import sklearn")                   # 16
    lines.append("from sklearn.model_selection import train_test_split")  # 17
    lines.append("from sklearn.preprocessing import StandardScaler")      # 18
    lines.append("from sklearn.ensemble import RandomForestClassifier")   # 19
    lines.append("from sklearn.metrics import accuracy_score, f1_score")  # 20
    lines.append("import scipy.stats as stats")      # 21
    lines.append("import statsmodels.api as sm")     # 22
    lines.append("import xgboost as xgb")            # 23
    lines.append("import lightgbm as lgb")           # 24
    lines.append("import plotly.express as px")      # 25

    # Blank line separating groups
    lines.append("")                                 # 26

    # Group 3: Local modules (lines 27-35)
    lines.append("from utils.data_loader import load_dataset, validate_schema")   # 27
    lines.append("from utils.preprocessing import clean_missing, encode_categoricals")  # 28
    lines.append("from utils.feature_engineering import create_interactions")      # 29
    lines.append("from utils.metrics import custom_loss, weighted_f1")            # 30
    lines.append("from config.settings import DB_URI, CACHE_DIR, MODEL_PATH")    # 31
    lines.append("from config.logging_config import setup_logger")               # 32
    lines.append("from pipelines.etl import extract_transform_load")             # 33
    lines.append("from pipelines.model_pipeline import train_evaluate_pipeline") # 34
    lines.append("from visualization.dashboards import render_summary_report")   # 35

    # Blank line before code
    lines.append("")                                 # 36

    # Actual code logic starting at line 37
    lines.append("# ============================================================")  # 37
    lines.append("# Data Science Analysis Pipeline")                                 # 38
    lines.append("# ============================================================")  # 39
    lines.append("")                                                                  # 40
    lines.append("logger = setup_logger(__name__)")                                   # 41
    lines.append("")                                                                  # 42
    lines.append("")                                                                  # 43
    lines.append("def load_and_prepare_data(filepath: str) -> pd.DataFrame:")         # 44
    lines.append('    """Load raw data and apply cleaning pipeline."""')               # 45
    lines.append("    logger.info(f'Loading data from {filepath}')")                  # 46
    lines.append("    raw_df = load_dataset(filepath)")                               # 47
    lines.append("    validated = validate_schema(raw_df)")                           # 48
    lines.append("    cleaned = clean_missing(validated)")                            # 49
    lines.append("    encoded = encode_categoricals(cleaned)")                        # 50
    lines.append("    return encoded")                                                # 51
    lines.append("")                                                                  # 52
    lines.append("")                                                                  # 53
    lines.append("def run_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:")    # 54
    lines.append('    """Generate derived features for model training."""')            # 55
    lines.append("    interactions = create_interactions(df)")                         # 56
    lines.append("    df = pd.concat([df, interactions], axis=1)")                    # 57
    lines.append("    logger.info(f'Feature matrix shape: {df.shape}')")              # 58
    lines.append("    return df")                                                     # 59
    lines.append("")                                                                  # 60
    lines.append("")                                                                  # 61
    lines.append("def train_model(X_train, y_train, X_test, y_test):")                # 62
    lines.append('    """Train and evaluate the ensemble model."""')                   # 63
    lines.append("    scaler = StandardScaler()")                                     # 64
    lines.append("    X_train_scaled = scaler.fit_transform(X_train)")                # 65
    lines.append("    X_test_scaled = scaler.transform(X_test)")                      # 66
    lines.append("")                                                                  # 67
    lines.append("    rf = RandomForestClassifier(n_estimators=200, random_state=42)")  # 68
    lines.append("    rf.fit(X_train_scaled, y_train)")                               # 69
    lines.append("    predictions = rf.predict(X_test_scaled)")                       # 70
    lines.append("")                                                                  # 71
    lines.append("    acc = accuracy_score(y_test, predictions)")                     # 72
    lines.append("    f1 = f1_score(y_test, predictions, average='weighted')")        # 73
    lines.append("    logger.info(f'Accuracy: {acc:.4f}, F1: {f1:.4f}')")             # 74
    lines.append("    return rf, {'accuracy': acc, 'f1': f1}")                        # 75
    lines.append("")                                                                  # 76
    lines.append("")                                                                  # 77
    lines.append("if __name__ == '__main__':")                                        # 78
    lines.append("    data = load_and_prepare_data('data/customer_churn.csv')")       # 79
    lines.append("    features = run_feature_engineering(data)")                      # 80
    lines.append("    X = features.drop('target', axis=1)")                           # 81
    lines.append("    y = features['target']")                                        # 82
    lines.append("    X_train, X_test, y_train, y_test = train_test_split(")          # 83
    lines.append("        X, y, test_size=0.2, random_state=42")                      # 84
    lines.append("    )")                                                             # 85
    lines.append("    model, metrics = train_model(X_train, y_train, X_test, y_test)")  # 86
    lines.append("    render_summary_report(metrics)")                                # 87
    lines.append("    print('Pipeline complete.')")                                   # 88

    content = "\n".join(lines) + "\n"

    with open(OUTPUT, 'w') as f:
        f.write(content)

    print(f'Initial file created: {OUTPUT}')

    # Enable region folding in VSCode settings
    vscode_user_dir = os.path.join(WORKDIR, '.config', 'Code', 'User')
    os.makedirs(vscode_user_dir, exist_ok=True)
    settings_path = os.path.join(vscode_user_dir, 'settings.json')
    try:
        import json as _json
        with open(settings_path, 'r') as f:
            settings = _json.load(f)
    except (FileNotFoundError, ValueError):
        settings = {}
    settings["editor.folding"] = True
    settings["editor.foldingStrategy"] = "auto"
    settings["editor.showFoldingControls"] = "always"
    with open(settings_path, 'w') as f:
        import json as _json
        _json.dump(settings, f, indent=4)

    # Launch VSCode with the project folder and open the file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

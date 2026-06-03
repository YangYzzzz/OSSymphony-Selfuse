"""
Reward Script: Create manual fold regions using '#region' and '#endregion' comments
Task ID: vscode_rf_022
Domain: vscode
Scoring:
  - Component 1 (0.30): '# region Standard Library' / '# endregion' wrapping standard lib imports
  - Component 2 (0.30): '# region Third Party' / '# endregion' wrapping third-party imports
  - Component 3 (0.30): '# region Local Modules' / '# endregion' wrapping local module imports
  - Component 4 (0.10): All original import lines preserved intact
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rf_022'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'datascience', 'analysis.py')

# Known import lines that must be preserved (from initial state)
STANDARD_LIB_IMPORTS = [
    'import os',
    'import sys',
    'import json',
    'import csv',
    'import datetime',
    'import re',
    'import math',
    'import collections',
    'import itertools',
    'import functools',
]

THIRD_PARTY_IMPORTS = [
    'import numpy as np',
    'import pandas as pd',
    'import matplotlib.pyplot as plt',
    'import seaborn as sns',
    'import sklearn',
    'from sklearn.model_selection import train_test_split',
    'from sklearn.preprocessing import StandardScaler',
    'from sklearn.ensemble import RandomForestClassifier',
    'from sklearn.metrics import accuracy_score, f1_score',
    'import scipy.stats as stats',
    'import statsmodels.api as sm',
    'import xgboost as xgb',
    'import lightgbm as lgb',
    'import plotly.express as px',
]

LOCAL_MODULE_IMPORTS = [
    'from utils.data_loader import load_dataset, validate_schema',
    'from utils.preprocessing import clean_missing, encode_categoricals',
    'from utils.feature_engineering import create_interactions',
    'from utils.metrics import custom_loss, weighted_f1',
    'from config.settings import DB_URI, CACHE_DIR, MODEL_PATH',
    'from config.logging_config import setup_logger',
    'from pipelines.etl import extract_transform_load',
    'from pipelines.model_pipeline import train_evaluate_pipeline',
    'from visualization.dashboards import render_summary_report',
]


def find_region_block(lines, region_name):
    """
    Find a region block with the given name.
    Returns (start_idx, end_idx) of the region/endregion comment lines,
    or (None, None) if not found.
    """
    start_idx = None
    end_idx = None
    # Look for '# region <name>' (case-insensitive on 'region')
    for i, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r'^#\s*region\s+' + re.escape(region_name), stripped, re.IGNORECASE):
            start_idx = i
            break

    if start_idx is None:
        return None, None

    # Look for matching '# endregion' after start
    for i in range(start_idx + 1, len(lines)):
        stripped = lines[i].strip()
        if re.match(r'^#\s*endregion', stripped, re.IGNORECASE):
            end_idx = i
            break

    return start_idx, end_idx


def check_imports_in_region(lines, start_idx, end_idx, expected_imports):
    """
    Check that all expected import lines exist between start_idx and end_idx.
    Returns (found_count, total_count).
    """
    if start_idx is None or end_idx is None:
        return 0, len(expected_imports)

    region_content = [lines[i].strip() for i in range(start_idx + 1, end_idx)]
    found = 0
    for imp in expected_imports:
        if imp.strip() in region_content:
            found += 1
    return found, len(expected_imports)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
        lines = content.split('\n')
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: '# region Standard Library' block exists and wraps correct imports (0.30 pts)
    try:
        start, end = find_region_block(lines, 'Standard Library')
        if start is not None and end is not None:
            found, total = check_imports_in_region(lines, start, end, STANDARD_LIB_IMPORTS)
            if found == total:
                print(f"PASS: Component 1 -- '# region Standard Library' block found (lines {start+1}-{end+1}) with all {total} imports (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 1 -- '# region Standard Library' block found but only {found}/{total} imports inside")
        else:
            print(f"FAIL: Component 1 -- '# region Standard Library' block not found (start={start}, end={end})")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: '# region Third Party' block exists and wraps correct imports (0.30 pts)
    try:
        start, end = find_region_block(lines, 'Third Party')
        if start is not None and end is not None:
            found, total = check_imports_in_region(lines, start, end, THIRD_PARTY_IMPORTS)
            if found == total:
                print(f"PASS: Component 2 -- '# region Third Party' block found (lines {start+1}-{end+1}) with all {total} imports (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 -- '# region Third Party' block found but only {found}/{total} imports inside")
        else:
            print(f"FAIL: Component 2 -- '# region Third Party' block not found (start={start}, end={end})")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: '# region Local Modules' block exists and wraps correct imports (0.30 pts)
    try:
        start, end = find_region_block(lines, 'Local Modules')
        if start is not None and end is not None:
            found, total = check_imports_in_region(lines, start, end, LOCAL_MODULE_IMPORTS)
            if found == total:
                print(f"PASS: Component 3 -- '# region Local Modules' block found (lines {start+1}-{end+1}) with all {total} imports (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 -- '# region Local Modules' block found but only {found}/{total} imports inside")
        else:
            print(f"FAIL: Component 3 -- '# region Local Modules' block not found (start={start}, end={end})")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: All original import lines preserved AND regions exist (0.10 pts)
    # This is a compound check: regions must exist (task-introduced change) AND imports must be intact
    try:
        # Gate: at least one region must exist (ensures this only scores task changes)
        has_any_region = any(
            re.match(r'^#\s*region\s+', l.strip(), re.IGNORECASE) for l in lines
        )
        if has_any_region:
            all_imports = STANDARD_LIB_IMPORTS + THIRD_PARTY_IMPORTS + LOCAL_MODULE_IMPORTS
            content_lines = [l.strip() for l in lines]
            missing = []
            for imp in all_imports:
                if imp.strip() not in content_lines:
                    missing.append(imp)
            if len(missing) == 0:
                print(f"PASS: Component 4 -- Regions exist and all {len(all_imports)} original import lines preserved (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 -- {len(missing)} import lines missing: {missing[:3]}...")
        else:
            print(f"FAIL: Component 4 -- No region comments found, cannot score import preservation")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

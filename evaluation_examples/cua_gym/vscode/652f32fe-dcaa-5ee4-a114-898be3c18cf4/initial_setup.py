"""
Initial Setup: Create a Python project with src/main.py that imports third-party libraries.
No .vscode/launch.json should exist.
Task ID: vscode_td_061
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_061'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'library-debug')
SRC_DIR = os.path.join(PROJECT_DIR, 'src')


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
    os.makedirs(SRC_DIR, exist_ok=True)

    # Create src/__init__.py
    with open(os.path.join(SRC_DIR, '__init__.py'), 'w') as f:
        f.write('')

    # Create src/main.py with third-party library imports
    main_py_content = '''"""
Data analysis pipeline for quarterly sales reports.
Processes CSV data, performs statistical analysis, and generates visualizations.
"""

import os
import sys
import json
from datetime import datetime

import requests
import pandas as pd
import numpy as np
from flask import Flask, jsonify


def load_sales_data(filepath: str) -> pd.DataFrame:
    """Load and validate sales data from CSV file."""
    df = pd.read_csv(filepath)
    required_cols = ['date', 'product', 'quantity', 'unit_price', 'region']
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    df['date'] = pd.to_datetime(df['date'])
    df['total'] = df['quantity'] * df['unit_price']
    return df


def compute_regional_summary(df: pd.DataFrame) -> dict:
    """Compute summary statistics by region."""
    summary = {}
    for region in df['region'].unique():
        region_data = df[df['region'] == region]
        summary[region] = {
            'total_revenue': float(region_data['total'].sum()),
            'avg_order_value': float(region_data['total'].mean()),
            'order_count': int(len(region_data)),
            'top_product': region_data.groupby('product')['total'].sum().idxmax(),
        }
    return summary


def fetch_exchange_rates(base_currency: str = 'USD') -> dict:
    """Fetch current exchange rates from external API."""
    url = f"https://api.exchangerate.host/latest?base={base_currency}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json().get('rates', {})


def generate_forecast(historical: np.ndarray, periods: int = 4) -> np.ndarray:
    """Simple moving average forecast for future periods."""
    window = min(len(historical), 4)
    weights = np.ones(window) / window
    smoothed = np.convolve(historical, weights, mode='valid')
    last_avg = smoothed[-1] if len(smoothed) > 0 else historical[-1]
    trend = (smoothed[-1] - smoothed[0]) / len(smoothed) if len(smoothed) > 1 else 0
    forecast = np.array([last_avg + trend * (i + 1) for i in range(periods)])
    return forecast


app = Flask(__name__)


@app.route('/api/summary')
def api_summary():
    """REST endpoint for sales summary data."""
    return jsonify({'status': 'ok', 'message': 'Sales analysis API running'})


if __name__ == '__main__':
    print("Sales Analysis Pipeline v2.1")
    print(f"Started at: {datetime.now().isoformat()}")

    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sales_q4.csv')
    if os.path.exists(data_path):
        df = load_sales_data(data_path)
        summary = compute_regional_summary(df)
        print(json.dumps(summary, indent=2))
    else:
        print(f"Data file not found: {data_path}")
        print("Running in API-only mode...")
        app.run(host='0.0.0.0', port=5050, debug=True)
'''

    with open(os.path.join(SRC_DIR, 'main.py'), 'w') as f:
        f.write(main_py_content)

    # Create a requirements.txt
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write('requests>=2.28.0\npandas>=1.5.0\nnumpy>=1.23.0\nflask>=2.2.0\n')

    # Create a README
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write('# Library Debug Project\n\nQuarterly sales analysis pipeline with REST API.\n\n## Setup\n\n```bash\npip install -r requirements.txt\npython src/main.py\n```\n')

    # Create data directory with a sample CSV
    data_dir = os.path.join(PROJECT_DIR, 'data')
    os.makedirs(data_dir, exist_ok=True)
    with open(os.path.join(data_dir, 'sales_q4.csv'), 'w') as f:
        f.write('date,product,quantity,unit_price,region\n')
        f.write('2025-10-01,Widget A,150,24.99,North\n')
        f.write('2025-10-03,Widget B,85,39.50,South\n')
        f.write('2025-10-07,Widget A,200,24.99,East\n')
        f.write('2025-10-12,Widget C,45,89.00,West\n')
        f.write('2025-10-15,Widget B,120,39.50,North\n')

    # Ensure NO .vscode/launch.json exists
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    launch_json = os.path.join(vscode_dir, 'launch.json')
    if os.path.exists(launch_json):
        os.remove(launch_json)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  src/main.py with third-party imports')
    print(f'  No .vscode/launch.json')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

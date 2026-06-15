"""
Initial Setup: Configure SQLTools extension settings in VSCode User Settings JSON
Task ID: vscode_gf3_004
Domain: vscode

Creates a realistic VSCode settings.json with some pre-existing settings
(but NO sqltools.* settings), then opens VSCode.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_004'

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

    # Load existing settings if any, to merge rather than overwrite
    try:
        with open(SETTINGS_PATH, "r") as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Remove any sqltools.* keys that might already exist (ensure clean initial state)
    keys_to_remove = [k for k in settings if k.startswith("sqltools.")]
    for k in keys_to_remove:
        del settings[k]

    # Add some realistic pre-existing settings (a data engineer's typical config)
    initial_settings = {
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.wordWrap": "on",
        "editor.minimap.enabled": True,
        "editor.formatOnSave": True,
        "editor.renderWhitespace": "boundary",
        "workbench.colorTheme": "Default Dark Modern",
        "workbench.startupEditor": "none",
        "terminal.integrated.fontSize": 13,
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
        "python.analysis.typeCheckingMode": "basic",
        "git.autofetch": True,
        "git.confirmSync": False,
        "explorer.confirmDelete": False,
        "explorer.confirmDragAndDrop": False,
    }

    # Merge: keep existing settings, add our initial ones without overwriting existing
    for k, v in initial_settings.items():
        if k not in settings:
            settings[k] = v

    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)

    print(f"Initial settings.json created at: {SETTINGS_PATH}")
    print(f"Settings keys: {list(settings.keys())}")
    print(f"No sqltools.* keys present: {not any(k.startswith('sqltools.') for k in settings)}")

    # Also create a small workspace project so VSCode has something to open
    project_dir = os.path.join(WORKDIR, "data-pipeline")
    os.makedirs(project_dir, exist_ok=True)

    # Create a sample SQL file that a data engineer would have
    sql_file = os.path.join(project_dir, "queries.sql")
    if not os.path.exists(sql_file):
        with open(sql_file, "w") as f:
            f.write("""-- Daily sales aggregation query
SELECT
  date_trunc('day', order_date) AS sale_date,
  COUNT(DISTINCT customer_id) AS unique_customers,
  COUNT(order_id) AS total_orders,
  SUM(order_total) AS revenue,
  AVG(order_total) AS avg_order_value
FROM sales.orders
WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY 1
ORDER BY 1 DESC;

-- Top products by revenue
SELECT
  p.product_name,
  p.category,
  COUNT(oi.order_item_id) AS units_sold,
  SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM sales.order_items oi
JOIN products.catalog p ON oi.product_id = p.product_id
WHERE oi.created_at >= '2025-01-01'
GROUP BY 1, 2
ORDER BY 4 DESC
LIMIT 20;
""")

    # Create a Python ETL script
    etl_file = os.path.join(project_dir, "etl_pipeline.py")
    if not os.path.exists(etl_file):
        with open(etl_file, "w") as f:
            f.write("""import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://analyst:readonly@db.internal:5432/warehouse"

def extract_daily_metrics():
    engine = create_engine(DATABASE_URL)
    query = open("queries.sql").read().split(";")[0]
    return pd.read_sql(query, engine)

def transform(df):
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    df["revenue_per_customer"] = df["revenue"] / df["unique_customers"]
    return df

def load(df, table_name="analytics.daily_metrics"):
    engine = create_engine(DATABASE_URL)
    df.to_sql(table_name, engine, if_exists="append", index=False)

if __name__ == "__main__":
    raw = extract_daily_metrics()
    cleaned = transform(raw)
    load(cleaned)
    print(f"Loaded {len(cleaned)} rows into daily_metrics")
""")

    print(f"Project directory created: {project_dir}")

    # Launch VSCode with the project folder
    launch_gui(f'code "{project_dir}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()

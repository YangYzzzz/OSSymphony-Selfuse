"""
Initial Setup: Performance investigation workflow in ~/project
Task ID: vscode_wf_055
Domain: vscode (os)
Creates a Python data processing project with main.py and data.csv.
No profiling setup exists. VSCode opens with ~/project.
"""

import os
import shlex
import subprocess
import time
import json
import csv
import random

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
VSCODE_DIR = os.path.join(PROJECT, '.vscode')


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
    os.makedirs(PROJECT, exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # --- main.py: A data processing script that takes ~10 seconds ---
    main_py_content = '''\
"""
Data Processing Pipeline
Reads sales data from CSV, performs aggregation and analysis.
"""

import csv
import time
import statistics
from collections import defaultdict


def load_data(filepath):
    """Load CSV data into list of dicts."""
    data = []
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["amount"] = float(row["amount"])
            row["quantity"] = int(row["quantity"])
            data.append(row)
    return data


def validate_records(data):
    """Validate each record for completeness and correctness."""
    valid = []
    for record in data:
        if record["amount"] > 0 and record["quantity"] > 0:
            # Simulate complex validation logic
            checksum = sum(ord(c) for c in record["product"])
            if checksum % 7 != 0 or True:
                valid.append(record)
    return valid


def aggregate_by_region(data):
    """Group and sum sales by region with nested iteration."""
    regions = defaultdict(lambda: {"total": 0.0, "count": 0, "amounts": []})
    for record in data:
        region = record["region"]
        regions[region]["total"] += record["amount"]
        regions[region]["count"] += 1
        regions[region]["amounts"].append(record["amount"])
    # Compute stats for each region
    for region, info in regions.items():
        info["mean"] = statistics.mean(info["amounts"])
        info["stdev"] = statistics.stdev(info["amounts"]) if len(info["amounts"]) > 1 else 0
        info["median"] = statistics.median(info["amounts"])
    return dict(regions)


def compute_moving_averages(data, window=50):
    """Compute moving averages over the amount field."""
    amounts = [r["amount"] for r in data]
    averages = []
    for i in range(len(amounts)):
        start = max(0, i - window + 1)
        window_slice = amounts[start:i + 1]
        averages.append(sum(window_slice) / len(window_slice))
    return averages


def detect_anomalies(data):
    """Detect anomalous records using z-score approach."""
    amounts = [r["amount"] for r in data]
    mean_val = statistics.mean(amounts)
    stdev_val = statistics.stdev(amounts) if len(amounts) > 1 else 1
    anomalies = []
    for i, record in enumerate(data):
        z_score = abs(record["amount"] - mean_val) / stdev_val
        if z_score > 2.5:
            anomalies.append((i, record, z_score))
    return anomalies


def generate_summary_report(data, regions, anomalies, moving_avgs):
    """Generate a text summary of the analysis."""
    total_sales = sum(r["amount"] for r in data)
    total_quantity = sum(r["quantity"] for r in data)
    report_lines = [
        "=" * 60,
        "SALES DATA ANALYSIS REPORT",
        "=" * 60,
        f"Total Records: {len(data)}",
        f"Total Sales: ${total_sales:,.2f}",
        f"Total Quantity: {total_quantity:,}",
        "",
        "--- Regional Breakdown ---",
    ]
    for region, info in sorted(regions.items()):
        report_lines.append(
            f"  {region}: ${info[\'total\']:,.2f} "
            f"(avg: ${info[\'mean\']:,.2f}, median: ${info[\'median\']:,.2f})"
        )
    report_lines.append(f"\\nAnomalies Detected: {len(anomalies)}")
    report_lines.append(f"Moving Average (last): ${moving_avgs[-1]:,.2f}" if moving_avgs else "")
    return "\\n".join(report_lines)


def main():
    """Main entry point for data processing pipeline."""
    print("Loading data...")
    data = load_data("data.csv")
    print(f"Loaded {len(data)} records")

    print("Validating records...")
    valid_data = validate_records(data)
    print(f"Valid records: {len(valid_data)}")

    print("Aggregating by region...")
    regions = aggregate_by_region(valid_data)

    print("Computing moving averages...")
    moving_avgs = compute_moving_averages(valid_data)

    print("Detecting anomalies...")
    anomalies = detect_anomalies(valid_data)

    print("Generating report...")
    report = generate_summary_report(valid_data, regions, anomalies, moving_avgs)
    print(report)

    # Write results
    with open("analysis_output.txt", "w") as f:
        f.write(report)
    print("\\nAnalysis complete. Results saved to analysis_output.txt")


if __name__ == "__main__":
    main()
'''

    with open(os.path.join(PROJECT, 'main.py'), 'w') as f:
        f.write(main_py_content)

    # --- data.csv: Large CSV with sales data (~5000 rows) ---
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East']
    products = [
        'Widget Pro', 'DataSync 3000', 'CloudBase Plus', 'NetGuard Suite',
        'AnalytiX Dashboard', 'SecureVault', 'StreamLine ERP', 'DevOps Toolkit',
        'SmartReport', 'EdgeConnect'
    ]
    sales_reps = [
        'Sarah Chen', 'Marcus Johnson', 'Priya Patel', 'James O\'Brien',
        'Yuki Tanaka', 'Elena Rodriguez', 'David Kim', 'Aisha Mohammed',
        'Thomas Weber', 'Maria Silva', 'Alex Petrov', 'Sophie Laurent'
    ]

    random.seed(42)
    csv_path = os.path.join(PROJECT, 'data.csv')
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'region', 'product', 'sales_rep', 'amount', 'quantity', 'customer_id'])
        for i in range(5000):
            year = random.choice([2023, 2024, 2025])
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            date_str = f'{year}-{month:02d}-{day:02d}'
            region = random.choice(regions)
            product = random.choice(products)
            rep = random.choice(sales_reps)
            amount = round(random.uniform(150.0, 25000.0), 2)
            quantity = random.randint(1, 100)
            cust_id = f'CUST-{random.randint(1000, 9999)}'
            writer.writerow([date_str, region, product, rep, amount, quantity, cust_id])

    # --- requirements.txt ---
    with open(os.path.join(PROJECT, 'requirements.txt'), 'w') as f:
        f.write("# Data Processing Pipeline Dependencies\n")
        f.write("# Standard library only - no external packages needed\n")

    # --- README.md for the project ---
    with open(os.path.join(PROJECT, 'README.md'), 'w') as f:
        f.write("# Sales Data Processing Pipeline\n\n")
        f.write("A Python data processing pipeline that analyzes sales CSV data.\n\n")
        f.write("## Usage\n\n")
        f.write("```bash\npython main.py\n```\n\n")
        f.write("## Input\n\n")
        f.write("- `data.csv` - Sales records with region, product, amount, quantity fields\n\n")
        f.write("## Output\n\n")
        f.write("- `analysis_output.txt` - Summary report with regional breakdowns and anomaly detection\n")

    # --- .vscode/settings.json (minimal, NO tasks.json or launch.json) ---
    vscode_settings = {
        "python.defaultInterpreterPath": "/usr/bin/python3",
        "editor.fontSize": 14,
        "editor.wordWrap": "on"
    }
    with open(os.path.join(VSCODE_DIR, 'settings.json'), 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    print(f'Initial project created at: {PROJECT}')
    print(f'  main.py: Data processing script')
    print(f'  data.csv: 5000 rows of sales data')
    print(f'  .vscode/settings.json: Minimal editor settings')
    print(f'  NO tasks.json, NO launch.json, NO profile.prof, NO performance_report.md')

    # Launch VSCode with the project
    launch_gui(f'code "{PROJECT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

"""
Initial Setup: VSCode open with analysis.py containing data processing code.
Task ID: vscode_stu_079
Domain: vs-code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_079'
OUTPUT = f'{WORKDIR}/analysis.py'


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
    # Create analysis.py with realistic data processing code
    # Lines 15-25 will contain a block that processes a list
    content = '''\
import csv
import os
import statistics
from datetime import datetime


def load_sales_data(filepath):
    """Load sales records from a CSV file."""
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)


def analyze_quarterly_report(records):
    filtered = []
    running_total = 0.0
    for record in records:
        amount = float(record["amount"])
        if amount > 100.0:
            tax = amount * 0.08
            net = amount - tax
            running_total += net
            record["net_amount"] = round(net, 2)
            record["tax"] = round(tax, 2)
            record["running_total"] = round(running_total, 2)
            filtered.append(record)
    avg_net = running_total / len(filtered) if filtered else 0.0

    summary = {
        "total_records": len(filtered),
        "running_total": round(running_total, 2),
        "average_net": round(avg_net, 2),
        "generated_at": datetime.now().isoformat(),
    }
    return filtered, summary


def write_report(output_path, filtered, summary):
    """Write the analysis results to a text report."""
    with open(output_path, "w") as f:
        f.write("Quarterly Sales Analysis Report\\n")
        f.write("=" * 40 + "\\n\\n")
        f.write(f"Total qualifying records: {summary['total_records']}\\n")
        f.write(f"Running total (net): ${summary['running_total']:,.2f}\\n")
        f.write(f"Average net amount: ${summary['average_net']:,.2f}\\n")
        f.write(f"Report generated: {summary['generated_at']}\\n\\n")
        for rec in filtered:
            f.write(f"  {rec.get('date', 'N/A')} | "
                    f"${rec['net_amount']:>10,.2f} | "
                    f"Tax: ${rec['tax']:>8,.2f}\\n")


if __name__ == "__main__":
    data_file = os.path.join(os.path.dirname(__file__), "sales_q3.csv")
    if os.path.exists(data_file):
        records = load_sales_data(data_file)
        results, summary = analyze_quarterly_report(records)
        write_report("quarterly_report.txt", results, summary)
        print(f"Report written with {summary['total_records']} records.")
    else:
        print(f"Data file not found: {data_file}")
'''

    os.makedirs(WORKDIR, exist_ok=True)
    with open(OUTPUT, 'w') as f:
        f.write(content)
    print(f'Initial file created: {OUTPUT}')

    # Ensure Python extension is installed
    try:
        subprocess.run(['code', '--install-extension', 'ms-python.python'],
                       capture_output=True, text=True, timeout=30)
        print('Python extension installed/verified.')
    except Exception as e:
        print(f'Extension install note: {e}')

    # Launch VSCode with the file
    launch_gui(f'code "{OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with analysis.py on DISPLAY=:0')


create_initial()

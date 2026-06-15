"""
Initial Setup: Enable trim trailing whitespace on save in VSCode
Task ID: vscode_we_008
Domain: vscode

Creates a Python file with trailing whitespace and ensures VSCode
user settings are empty. Launches VSCode with the file open.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_008'
OUTPUT = f'{WORKDIR}/{TASK_ID}.py'

VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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
    # 1. Create a Python file with intentional trailing whitespace
    # (trailing spaces marked with visible comment for clarity in source,
    #  but actual trailing spaces are present on each marked line)
    lines = [
        "#!/usr/bin/env python3",
        '"""',
        "Quarterly Sales Report Generator   ",
        "Generates PDF reports from sales data.   ",
        '"""',
        "",
        "import csv   ",
        "import os",
        "from datetime import datetime   ",
        "",
        "",
        "REGIONS = [   ",
        '    "North America",   ',
        '    "Europe",',
        '    "Asia Pacific",   ',
        '    "Latin America",',
        "]",
        "",
        "",
        "def load_sales_data(filepath):   ",
        '    """Load sales records from a CSV file."""   ',
        "    records = []   ",
        '    with open(filepath, "r") as f:',
        "        reader = csv.DictReader(f)   ",
        "        for row in reader:",
        '            records.append({   ',
        '                "region": row["region"],',
        '                "product": row["product"],   ',
        '                "revenue": float(row["revenue"]),',
        '                "units_sold": int(row["units_sold"]),   ',
        "            })",
        "    return records   ",
        "",
        "",
        "def calculate_totals(records):   ",
        '    """Calculate revenue totals by region."""',
        "    totals = {}   ",
        "    for record in records:",
        '        region = record["region"]   ',
        "        if region not in totals:",
        "            totals[region] = 0.0   ",
        '        totals[region] += record["revenue"]',
        "    return totals   ",
        "",
        "",
        "def generate_report(totals, output_path):   ",
        '    """Write a summary report to disk."""   ',
        '    with open(output_path, "w") as f:',
        '        f.write("Quarterly Sales Summary\\n")   ',
        '        f.write("=" * 40 + "\\n")   ',
        '        f.write(f"Generated: {datetime.now().strftime(\'%Y-%m-%d\')}\\n\\n")',
        "        for region in REGIONS:   ",
        "            revenue = totals.get(region, 0.0)",
        '            f.write(f"  {region}: ${revenue:,.2f}\\n")   ',
        '        f.write("\\n")   ',
        '        grand_total = sum(totals.values())',
        '        f.write(f"  Grand Total: ${grand_total:,.2f}\\n")   ',
        "",
        "",
        'if __name__ == "__main__":   ',
        '    data = load_sales_data("sales_q4_2025.csv")   ',
        "    totals = calculate_totals(data)",
        '    generate_report(totals, "report_q4_2025.txt")   ',
        '    print("Report generated successfully.")   ',
        "",
    ]
    content = "\n".join(lines) + "\n"

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, 'w') as f:
        f.write(content)
    print(f'Initial file created: {OUTPUT}')

    # 2. Ensure VSCode user settings are empty
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)
    print(f'VSCode settings reset to empty: {SETTINGS_PATH}')

    # 3. Launch VSCode with the file open
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

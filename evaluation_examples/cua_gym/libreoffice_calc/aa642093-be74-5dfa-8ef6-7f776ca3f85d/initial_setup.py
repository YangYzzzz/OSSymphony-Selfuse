"""
Initial Setup: Install CSV Rainbow VSCode extension and write CSV filtering Python script
Task ID: osworld_multi_apps_vscode_ext_script_014
Domain: vs-code / multi-apps

Initial state:
  - ~/Desktop/sales_data.csv exists with columns: date, product, revenue, units
  - The CSV Rainbow extension (mechatroner.rainbow-csv) is NOT installed
  - VSCode is open to the Desktop folder
"""

import csv
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_vscode_ext_script_014'
SALES_CSV = f'{WORKDIR}/sales_data.csv'


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


def ensure_rainbow_csv_not_installed():
    """Uninstall mechatroner.rainbow-csv if it happens to be installed."""
    result = subprocess.run(
        ["code", "--list-extensions"],
        capture_output=True, text=True
    )
    if "mechatroner.rainbow-csv" in result.stdout.lower():
        subprocess.run(
            ["code", "--uninstall-extension", "mechatroner.rainbow-csv"],
            capture_output=True, text=True
        )
        time.sleep(1.0)
        print("Uninstalled mechatroner.rainbow-csv (was present)")
    else:
        print("mechatroner.rainbow-csv is not installed — OK")


def create_sales_csv():
    """Create a realistic sales_data.csv with mix of high/low revenue rows."""
    os.makedirs(WORKDIR, exist_ok=True)

    rows = [
        # date, product, revenue, units
        ["2025-01-05", "Laptop Pro 15",      15999.00, 12],
        ["2025-01-08", "USB-C Hub",            3450.50, 98],
        ["2025-01-12", "Mechanical Keyboard",  8750.00, 45],
        ["2025-01-15", "4K Monitor 27in",     21300.00, 18],
        ["2025-01-20", "Webcam HD 1080p",      4200.75, 120],
        ["2025-01-22", "Noise-Cancel Headset", 9800.00, 35],
        ["2025-02-03", "SSD 1TB External",    12450.00, 55],
        ["2025-02-06", "Ergonomic Chair",      5600.00, 14],
        ["2025-02-10", "Tablet 10in",         18750.00, 22],
        ["2025-02-14", "Smart Speaker",        2300.90, 75],
        ["2025-02-18", "Gaming Mouse",         6100.25, 88],
        ["2025-02-21", "Portable Projector",  11000.00, 10],
        ["2025-03-01", "Docking Station",      7800.00, 32],
        ["2025-03-05", "Ultrawide Monitor",   22500.00, 15],
        ["2025-03-09", "Wireless Charger",     1950.60, 200],
        ["2025-03-12", "Action Camera 4K",    13200.00, 28],
        ["2025-03-17", "Bluetooth Earbuds",    4850.00, 145],
        ["2025-03-20", "NAS Storage 8TB",     16400.00, 8],
        ["2025-03-25", "Drawing Tablet",       9350.00, 19],
        ["2025-03-28", "Mini PC i7",          10500.00, 11],
    ]

    with open(SALES_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["date", "product", "revenue", "units"])
        writer.writerows(rows)

    print(f"Created sales CSV: {SALES_CSV} ({len(rows)} data rows)")


def create_initial():
    # 1. Ensure CSV Rainbow extension is NOT installed
    ensure_rainbow_csv_not_installed()

    # 2. Create the sales_data.csv file on Desktop
    create_sales_csv()

    # 3. Open VSCode with the Desktop folder (GUI-ready)
    launch_gui(f'code "{WORKDIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with Desktop folder (DISPLAY=:0)')


create_initial()

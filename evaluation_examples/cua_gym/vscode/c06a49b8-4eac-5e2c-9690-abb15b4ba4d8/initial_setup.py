"""
Initial Setup: Jupyter notebook workflow in ~/project
Task ID: vscode_wf_058
Domain: vscode

Creates:
- ~/project/data/sales.csv with realistic sales data
- VSCode opened with ~/project folder
- No Jupyter extension, no notebook, no Jupyter settings, no tasks.json
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_058'
PROJECT_DIR = os.path.join(WORKDIR, 'project')
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
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


def create_sales_csv():
    """Create a realistic sales CSV dataset."""
    os.makedirs(DATA_DIR, exist_ok=True)
    csv_path = os.path.join(DATA_DIR, 'sales.csv')

    lines = [
        'Date,Product,Category,Region,Units,UnitPrice,Revenue',
        '2025-01-05,Ergonomic Keyboard,Electronics,North,42,89.99,3779.58',
        '2025-01-08,Standing Desk,Furniture,West,15,549.00,8235.00',
        '2025-01-12,Wireless Mouse,Electronics,South,78,34.99,2729.22',
        '2025-01-15,Monitor Arm,Accessories,East,31,79.99,2479.69',
        '2025-01-19,USB-C Hub,Electronics,North,56,49.99,2799.44',
        '2025-01-23,Desk Lamp,Accessories,West,44,62.50,2750.00',
        '2025-01-27,Laptop Stand,Accessories,South,27,39.99,1079.73',
        '2025-02-02,Mechanical Keyboard,Electronics,East,63,129.99,8189.37',
        '2025-02-06,Office Chair,Furniture,North,9,899.00,8091.00',
        '2025-02-10,Webcam HD,Electronics,West,51,74.99,3824.49',
        '2025-02-14,Cable Management Kit,Accessories,South,88,19.99,1759.12',
        '2025-02-18,Noise Cancelling Headphones,Electronics,East,22,249.99,5499.78',
        '2025-02-22,Whiteboard,Furniture,North,17,189.00,3213.00',
        '2025-02-26,Desk Organizer,Accessories,West,65,24.99,1624.35',
        '2025-03-02,Portable Charger,Electronics,South,39,59.99,2339.61',
        '2025-03-06,Filing Cabinet,Furniture,East,8,349.00,2792.00',
        '2025-03-10,Mouse Pad XL,Accessories,North,92,15.99,1471.08',
        '2025-03-14,Bluetooth Speaker,Electronics,West,33,89.99,2969.67',
        '2025-03-18,Adjustable Footrest,Furniture,South,19,69.99,1329.81',
        '2025-03-22,Screen Protector,Accessories,East,110,12.99,1428.90',
        '2025-03-26,Docking Station,Electronics,North,14,199.99,2799.86',
        '2025-03-30,Ergonomic Wrist Rest,Accessories,West,57,22.99,1310.43',
        '2025-04-03,Smart Power Strip,Electronics,South,41,44.99,1844.59',
        '2025-04-07,Bookshelf,Furniture,East,6,279.00,1674.00',
    ]

    with open(csv_path, 'w') as f:
        f.write('\n'.join(lines) + '\n')

    print(f'Created sales CSV: {csv_path}')


def ensure_clean_state():
    """Make sure no Jupyter extension, notebook, or Jupyter settings exist."""
    # Remove any existing notebook
    notebook_path = os.path.join(PROJECT_DIR, 'data_analysis.ipynb')
    if os.path.exists(notebook_path):
        os.remove(notebook_path)

    # Remove tasks.json if it exists
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    tasks_path = os.path.join(vscode_dir, 'tasks.json')
    if os.path.exists(tasks_path):
        os.remove(tasks_path)

    # Ensure no Jupyter-related settings
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
            # Remove any jupyter-related keys
            keys_to_remove = [k for k in settings if 'jupyter' in k.lower() or 'notebook' in k.lower()]
            for k in keys_to_remove:
                del settings[k]
            with open(SETTINGS_PATH, 'w') as f:
                json.dump(settings, f, indent=4)
        except (json.JSONDecodeError, FileNotFoundError):
            pass

    # Uninstall Jupyter extension if present (ignore errors)
    try:
        subprocess.run(['code', '--uninstall-extension', 'ms-toolsai.jupyter'],
                       capture_output=True, timeout=30)
    except Exception:
        pass

    print('Clean state ensured: no Jupyter extension, notebook, or settings')


def create_initial():
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

    create_sales_csv()
    ensure_clean_state()

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with ~/project and DISPLAY=:0')


create_initial()

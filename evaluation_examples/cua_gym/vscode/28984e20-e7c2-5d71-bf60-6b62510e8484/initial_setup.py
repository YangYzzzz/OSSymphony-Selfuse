"""
Initial Setup: Rust data processor project scaffold
Task ID: vscode_gf4_030
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_030'
PROJECT_DIR = f'{WORKDIR}/projects/rust-data-processor'

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
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/data', exist_ok=True)

    # --- Cargo.toml: bare minimum ---
    cargo_toml = """\
[package]
name = "rust-data-processor"
version = "0.1.0"
edition = "2021"
"""
    with open(f'{PROJECT_DIR}/Cargo.toml', 'w') as f:
        f.write(cargo_toml)
    print(f'Created {PROJECT_DIR}/Cargo.toml')

    # --- src/main.rs: minimal ---
    main_rs = """\
fn main() {}
"""
    with open(f'{PROJECT_DIR}/src/main.rs', 'w') as f:
        f.write(main_rs)
    print(f'Created {PROJECT_DIR}/src/main.rs')

    # --- data/records.csv: 20 rows of realistic data ---
    csv_content = """\
id,name,value,category
1,Quantum Analytics Platform,4523.75,technology
2,Emerald Supply Chain,1892.40,logistics
3,Solar Panel Efficiency Study,7841.20,energy
4,Urban Farming Initiative,3215.60,agriculture
5,Neural Network Optimizer,9102.35,technology
6,Pacific Trade Routes,2764.80,logistics
7,Wind Turbine Maintenance,5438.90,energy
8,Organic Harvest Tracker,1547.25,agriculture
9,Cloud Migration Toolkit,6789.10,technology
10,Continental Freight Audit,4321.55,logistics
11,Geothermal Mapping Project,8956.70,energy
12,Precision Irrigation System,2103.45,agriculture
13,Blockchain Ledger Sync,7234.85,technology
14,Harbor Logistics Dashboard,3890.20,logistics
15,Battery Storage Analysis,6127.30,energy
16,Crop Yield Forecaster,1678.95,agriculture
17,API Gateway Monitor,5543.60,technology
18,Rail Network Optimizer,4012.75,logistics
19,Hydrogen Fuel Cell Test,9387.40,energy
20,Vertical Farm Controller,2856.15,agriculture
"""
    with open(f'{PROJECT_DIR}/data/records.csv', 'w') as f:
        f.write(csv_content)
    print(f'Created {PROJECT_DIR}/data/records.csv')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    # Also open Cargo.toml specifically
    launch_gui(f'code "{PROJECT_DIR}/Cargo.toml"', delay_sec=1.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()

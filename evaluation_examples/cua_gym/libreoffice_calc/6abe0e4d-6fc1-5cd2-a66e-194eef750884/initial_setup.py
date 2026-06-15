"""
Initial Setup: Set up a Rust development environment in ~/project
Task ID: vscode_wf_046
Domain: libreoffice_calc (VSCode workflow)
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_046'
PROJECT_DIR = f'{WORKDIR}/project'
VSCODE_USER = f'{WORKDIR}/.config/Code/User'
SETTINGS_PATH = f'{VSCODE_USER}/settings.json'


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
    # Step 1: Install Rust toolchain
    print("Installing Rust toolchain...")
    result = subprocess.run(
        ["sh", "-c", "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y"],
        capture_output=True, text=True, timeout=300
    )
    print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
    if result.returncode != 0:
        print(f"Rustup stderr: {result.stderr[-500:]}")

    # Source the cargo env for this process
    cargo_bin = f'{WORKDIR}/.cargo/bin'
    os.environ['PATH'] = f'{cargo_bin}:{os.environ["PATH"]}'

    # Verify installation
    verify = subprocess.run(["rustc", "--version"], capture_output=True, text=True)
    print(f"Rust version: {verify.stdout.strip()}")
    verify2 = subprocess.run(["cargo", "--version"], capture_output=True, text=True)
    print(f"Cargo version: {verify2.stdout.strip()}")

    # Step 2: Create empty ~/project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f"Created project directory: {PROJECT_DIR}")

    # Step 3: Ensure VSCode settings are minimal (no rust-analyzer config)
    # Keep existing trust settings, do NOT add any rust-analyzer settings
    try:
        with open(SETTINGS_PATH, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Remove any rust-analyzer settings if they exist
    keys_to_remove = [k for k in settings if k.startswith('rust-analyzer')]
    for k in keys_to_remove:
        del settings[k]

    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f"Settings cleaned: {SETTINGS_PATH}")

    # Step 4: Ensure no .vscode/launch.json in project
    launch_json_dir = os.path.join(PROJECT_DIR, '.vscode')
    launch_json_path = os.path.join(launch_json_dir, 'launch.json')
    if os.path.exists(launch_json_path):
        os.remove(launch_json_path)

    # Step 5: Uninstall rust-analyzer extension if installed
    subprocess.run(["code", "--uninstall-extension", "rust-lang.rust-analyzer"],
                   capture_output=True, text=True)
    print("Ensured rust-analyzer extension is not installed")

    # Step 6: Launch VSCode with the empty project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

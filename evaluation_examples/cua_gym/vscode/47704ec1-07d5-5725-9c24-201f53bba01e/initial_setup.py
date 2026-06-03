"""
Initial Setup: Configure remote development workspace settings
Task ID: vscode_we_040
Domain: vscode

Initial state: VSCode open with Remote-SSH extension installed, empty user settings.
"""

import json
import os
import shlex
import subprocess
import time

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
    # Ensure VSCode config directory exists
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Write empty settings (initial state has no remote SSH config)
    with open(SETTINGS_PATH, "w") as f:
        json.dump({}, f, indent=4)

    print(f"Initial settings.json created at {SETTINGS_PATH} (empty)")

    # Install Remote-SSH extension if not already installed
    try:
        result = subprocess.run(
            ["code", "--list-extensions"],
            capture_output=True, text=True, timeout=30
        )
        if "ms-vscode-remote.remote-ssh" not in result.stdout:
            print("Installing Remote-SSH extension...")
            subprocess.run(
                ["code", "--install-extension", "ms-vscode-remote.remote-ssh"],
                capture_output=True, text=True, timeout=120
            )
            print("Remote-SSH extension installed.")
        else:
            print("Remote-SSH extension already installed.")
    except Exception as e:
        print(f"Extension check/install note: {e}")

    # Create a workspace directory with some sample files for realistic context
    workspace_dir = os.path.join(HOME, "remote-project")
    os.makedirs(workspace_dir, exist_ok=True)

    # Create a sample Python file
    sample_py = os.path.join(workspace_dir, "main.py")
    with open(sample_py, "w") as f:
        f.write('''"""Remote Development Sample Project"""

import os
import sys


def connect_to_server(host: str, port: int = 22):
    """Establish SSH connection to remote development server."""
    print(f"Connecting to {host}:{port}...")
    # Placeholder for remote connection logic
    return {"host": host, "port": port, "status": "connected"}


def run_remote_analysis(connection, data_path: str):
    """Run data analysis on remote machine."""
    print(f"Running analysis on {data_path}...")
    results = {
        "records_processed": 15420,
        "errors": 0,
        "output_path": "/remote/output/results.csv"
    }
    return results


if __name__ == "__main__":
    conn = connect_to_server("dev-server.company.internal")
    results = run_remote_analysis(conn, "/data/quarterly_report")
    print(f"Analysis complete: {results['records_processed']} records processed")
''')

    # Create a requirements file
    requirements = os.path.join(workspace_dir, "requirements.txt")
    with open(requirements, "w") as f:
        f.write("""numpy==1.26.4
pandas==2.2.1
scikit-learn==1.4.1
matplotlib==3.8.3
jupyter==1.0.0
paramiko==3.4.0
""")

    # Create a README
    readme = os.path.join(workspace_dir, "README.md")
    with open(readme, "w") as f:
        f.write("""# Remote Development Project

This project runs data analysis pipelines on remote Linux servers via SSH.

## Setup
1. Configure VSCode Remote-SSH settings
2. Connect to the development server
3. Run analysis scripts
""")

    print(f"Workspace created at {workspace_dir}")

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{workspace_dir}"', delay_sec=3.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()

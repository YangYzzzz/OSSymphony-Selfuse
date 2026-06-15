"""
Initial Setup: VSCode open with no Docker extension installed
Task ID: vscode_ext_008
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ext_008'

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

def ensure_docker_ext_not_installed():
    """Make sure the Docker extension is not installed."""
    ext_id = "ms-azuretools.vscode-docker"
    try:
        result = subprocess.run(
            ["code", "--list-extensions"],
            capture_output=True,
            text=True,
            timeout=30
        )
        installed = result.stdout.strip().lower()
        if ext_id.lower() in installed:
            print(f"Docker extension found — uninstalling...")
            subprocess.run(
                ["code", "--uninstall-extension", ext_id],
                capture_output=True,
                text=True,
                timeout=60
            )
            print(f"Uninstalled {ext_id}")
        else:
            print(f"Docker extension not installed — initial state is correct")
    except FileNotFoundError:
        print("Warning: 'code' CLI not found in PATH, skipping extension check")
    except subprocess.TimeoutExpired:
        print("Warning: code CLI timed out")

def create_workspace():
    """Create a simple workspace folder for the agent to work in."""
    workspace_dir = os.path.join(WORKDIR, 'workspace')
    os.makedirs(workspace_dir, exist_ok=True)
    # Create a simple placeholder file
    readme_path = os.path.join(workspace_dir, 'README.md')
    if not os.path.exists(readme_path):
        with open(readme_path, 'w') as f:
            f.write("# My Project\n\nThis project uses Docker for containerization.\n")
    print(f"Workspace created: {workspace_dir}")
    return workspace_dir

def setup_initial():
    # Ensure Docker extension is NOT installed
    ensure_docker_ext_not_installed()

    # Create a simple workspace
    workspace_dir = create_workspace()

    # Open VSCode with the workspace so the Extensions panel is accessible
    launch_gui(f'code "{workspace_dir}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

setup_initial()

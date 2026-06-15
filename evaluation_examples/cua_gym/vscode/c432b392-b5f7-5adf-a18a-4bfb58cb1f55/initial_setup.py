"""
Initial Setup: Set default terminal shell to zsh with login shell arguments
Task ID: vscode_rrt_070
Domain: vscode

Initial state: VSCode open with default settings (no custom terminal profiles).
Zsh is installed at /usr/bin/zsh but no terminal profile configured.
"""

import json
import os
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")
WORKSPACE_DIR = os.path.join(HOME, "workspace")

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

def install_zsh():
    """Ensure zsh is installed at /usr/bin/zsh."""
    result = subprocess.run(["which", "zsh"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Installing zsh...")
        # sudo password is 'user' on this VM
        subprocess.run(
            "echo 'password' | sudo -S apt-get update -qq",
            shell=True, check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            "echo 'password' | sudo -S apt-get install -y -qq zsh",
            shell=True, check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        print("Zsh installed successfully.")
    else:
        print("Zsh already installed.")

def setup_initial_settings():
    """Write VSCode settings with NO terminal customization (initial state)."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings and preserve them
    settings = {}
    try:
        with open(SETTINGS_PATH, "r") as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    # Ensure NO terminal profile settings exist (remove if present)
    settings.pop("terminal.integrated.defaultProfile.linux", None)
    settings.pop("terminal.integrated.profiles.linux", None)

    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)
    print(f"Settings written to {SETTINGS_PATH}")

def create_workspace():
    """Create a simple workspace directory with a sample file."""
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
    sample_file = os.path.join(WORKSPACE_DIR, "main.py")
    if not os.path.exists(sample_file):
        with open(sample_file, "w") as f:
            f.write('#!/usr/bin/env python3\n')
            f.write('"""Project entry point."""\n\n')
            f.write('import sys\n')
            f.write('import os\n\n\n')
            f.write('def main():\n')
            f.write('    """Run the application."""\n')
            f.write('    print("Application started")\n')
            f.write('    print(f"Python version: {sys.version}")\n')
            f.write('    print(f"Working directory: {os.getcwd()}")\n')
            f.write('    return 0\n\n\n')
            f.write('if __name__ == "__main__":\n')
            f.write('    sys.exit(main())\n')
    print(f"Workspace created at {WORKSPACE_DIR}")

def main():
    # 1. Install zsh so it's available at /usr/bin/zsh
    install_zsh()

    # 2. Set up initial VSCode settings (no terminal customization)
    setup_initial_settings()

    # 3. Create workspace with sample files
    create_workspace()

    # 4. Launch VSCode with the workspace
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")

main()

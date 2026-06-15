"""
Initial Setup: Change VSCode icon theme to 'material-icon-theme' and set product icon theme to 'fluent-icons'
Task ID: vscode_we_021
Domain: vscode
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
    # Ensure VSCode user config directory exists
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Write empty settings (default icon themes - no icon theme or product icon theme set)
    settings = {}
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)

    print(f"Initial settings created: {SETTINGS_PATH}")

    # Create a simple workspace folder so VSCode has something to open
    workspace_dir = os.path.join(HOME, "workspace")
    os.makedirs(workspace_dir, exist_ok=True)

    # Create a sample file in the workspace
    sample_file = os.path.join(workspace_dir, "README.md")
    with open(sample_file, "w") as f:
        f.write("# Project Workspace\n\nThis is a sample project workspace.\n")

    # Create a few more files to make the workspace realistic
    src_dir = os.path.join(workspace_dir, "src")
    os.makedirs(src_dir, exist_ok=True)

    with open(os.path.join(src_dir, "main.py"), "w") as f:
        f.write('''"""Main application entry point."""

import os
import sys


def main():
    """Run the application."""
    print("Hello, World!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
''')

    with open(os.path.join(src_dir, "utils.py"), "w") as f:
        f.write('''"""Utility functions for the application."""


def format_currency(amount: float) -> str:
    """Format a number as USD currency."""
    return f"${amount:,.2f}"


def calculate_tax(amount: float, rate: float = 0.08) -> float:
    """Calculate tax on a given amount."""
    return round(amount * rate, 2)
''')

    print(f"Workspace created: {workspace_dir}")

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{workspace_dir}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()

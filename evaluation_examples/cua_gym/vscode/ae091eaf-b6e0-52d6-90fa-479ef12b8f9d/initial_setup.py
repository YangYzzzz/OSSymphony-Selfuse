"""
Initial Setup: Configure terminal profiles in VSCode
Task ID: vscode_wf_026
Domain: vscode

Creates a VSCode environment with basic settings but NO terminal profile
configuration. The agent must add terminal profiles and set the default.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_026'
HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")
PROJECT_DIR = os.path.join(HOME, "project")


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
    # Create project directory that the "Project Shell" profile will reference
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create a small project structure for realism
    readme_path = os.path.join(PROJECT_DIR, "README.md")
    if not os.path.exists(readme_path):
        with open(readme_path, "w") as f:
            f.write("# Data Pipeline Project\n\n")
            f.write("Automated ETL pipeline for quarterly sales reporting.\n\n")
            f.write("## Setup\n\n")
            f.write("1. Install dependencies: `pip install -r requirements.txt`\n")
            f.write("2. Configure environment variables\n")
            f.write("3. Run `python main.py`\n")

    main_py_path = os.path.join(PROJECT_DIR, "main.py")
    if not os.path.exists(main_py_path):
        with open(main_py_path, "w") as f:
            f.write('#!/usr/bin/env python3\n')
            f.write('"""Main entry point for the data pipeline."""\n\n')
            f.write('import os\n')
            f.write('import sys\n\n\n')
            f.write('def main():\n')
            f.write('    env = os.getenv("PROJECT_ENV", "production")\n')
            f.write('    print(f"Running in {env} mode")\n\n\n')
            f.write('if __name__ == "__main__":\n')
            f.write('    main()\n')

    # Write VSCode settings with basic config but NO terminal profiles
    os.makedirs(VSCODE_USER, exist_ok=True)
    settings = {
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.wordWrap": "on",
        "editor.minimap.enabled": True,
        "workbench.colorTheme": "Default Dark Modern",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
        "editor.formatOnSave": False,
        "window.zoomLevel": 0
    }
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)
    print(f"Settings written to: {SETTINGS_PATH}")

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()

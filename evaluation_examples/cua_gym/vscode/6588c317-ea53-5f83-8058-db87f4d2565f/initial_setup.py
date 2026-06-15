"""
Initial Setup: Customize diff editor settings in VSCode
Task ID: vscode_we_049
Domain: vscode

Initial state: VSCode open with empty user settings (no diffEditor.* keys).
"""

import json
import os
import shlex
import subprocess
import time

HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')

# Create a simple workspace with some files so VSCode has something to show
WORKSPACE = os.path.join(HOME, 'workspace')


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
    # Ensure workspace directory exists with some realistic content
    os.makedirs(WORKSPACE, exist_ok=True)

    # Create a sample project file so the workspace is not empty
    readme_path = os.path.join(WORKSPACE, 'README.md')
    with open(readme_path, 'w') as f:
        f.write('# Data Processing Pipeline\n\n')
        f.write('This project contains utilities for batch data processing.\n\n')
        f.write('## Setup\n\n')
        f.write('1. Install dependencies: `pip install -r requirements.txt`\n')
        f.write('2. Configure settings in `config.yaml`\n')
        f.write('3. Run the pipeline: `python main.py`\n')

    main_py_path = os.path.join(WORKSPACE, 'main.py')
    with open(main_py_path, 'w') as f:
        f.write('"""Data processing pipeline entry point."""\n\n')
        f.write('import argparse\nimport sys\n\n\n')
        f.write('def parse_args():\n')
        f.write('    parser = argparse.ArgumentParser(description="Run data pipeline")\n')
        f.write('    parser.add_argument("--input", type=str, required=True)\n')
        f.write('    parser.add_argument("--output", type=str, default="output/")\n')
        f.write('    parser.add_argument("--verbose", action="store_true")\n')
        f.write('    return parser.parse_args()\n\n\n')
        f.write('def main():\n')
        f.write('    args = parse_args()\n')
        f.write('    print(f"Processing {args.input} -> {args.output}")\n\n\n')
        f.write('if __name__ == "__main__":\n')
        f.write('    main()\n')

    # Ensure VSCode User config directory exists
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Write empty settings (no diffEditor.* keys)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)

    print(f'Settings file created: {SETTINGS_PATH}')
    print(f'Workspace created: {WORKSPACE}')

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

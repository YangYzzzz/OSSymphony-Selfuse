"""
Initial Setup: Set up VSCode with default settings for accessibility configuration task.
Task ID: vscode_we_041
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_041'
HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")

# Create a workspace folder with some sample files so VSCode has something to show
WORKSPACE = os.path.join(WORKDIR, "workspace")
os.makedirs(WORKSPACE, exist_ok=True)

# Create a realistic sample project
sample_files = {
    "README.md": """# Accessibility Demo Project

This project demonstrates accessible coding practices.

## Getting Started

1. Open this folder in VSCode
2. Configure your editor settings for accessibility
3. Start coding!
""",
    "main.py": """#!/usr/bin/env python3
\"\"\"Main entry point for the accessibility demo application.\"\"\"

import sys
from utils.config import load_config
from utils.display import render_output


def main():
    \"\"\"Run the main application loop.\"\"\"
    config = load_config("config.json")
    print(f"Application started with theme: {config.get('theme', 'default')}")

    data = [
        {"name": "Screen Reader Mode", "enabled": False},
        {"name": "High Contrast", "enabled": False},
        {"name": "Large Cursor", "enabled": False},
        {"name": "Line Spacing", "enabled": False},
    ]

    for feature in data:
        status = "ON" if feature["enabled"] else "OFF"
        print(f"  {feature['name']}: {status}")

    render_output(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
""",
    "config.json": """{
    "theme": "default",
    "language": "en",
    "version": "1.0.0",
    "features": {
        "accessibility": false,
        "highContrast": false
    }
}
""",
}

for filename, content in sample_files.items():
    filepath = os.path.join(WORKSPACE, filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write(content)

# Create utils subdirectory
utils_dir = os.path.join(WORKSPACE, "utils")
os.makedirs(utils_dir, exist_ok=True)

with open(os.path.join(utils_dir, "__init__.py"), "w") as f:
    f.write("")

with open(os.path.join(utils_dir, "config.py"), "w") as f:
    f.write("""\"\"\"Configuration loading utilities.\"\"\"
import json
import os


def load_config(path: str) -> dict:
    \"\"\"Load configuration from a JSON file.\"\"\"
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)
""")

with open(os.path.join(utils_dir, "display.py"), "w") as f:
    f.write("""\"\"\"Display rendering utilities.\"\"\"


def render_output(data: list) -> None:
    \"\"\"Render accessibility feature status to console.\"\"\"
    print("\\n--- Accessibility Features ---")
    for item in data:
        marker = "[x]" if item.get("enabled") else "[ ]"
        print(f"  {marker} {item['name']}")
    print("--- End ---\\n")
""")

# Ensure VSCode settings directory exists with empty settings
os.makedirs(VSCODE_USER, exist_ok=True)
with open(SETTINGS_PATH, "w") as f:
    json.dump({}, f, indent=4)

print(f"Initial workspace created: {WORKSPACE}")
print(f"VSCode settings reset to empty: {SETTINGS_PATH}")


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


# Launch VSCode with the workspace folder
launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
print("GUI_READY: launched VSCode with DISPLAY=:0")

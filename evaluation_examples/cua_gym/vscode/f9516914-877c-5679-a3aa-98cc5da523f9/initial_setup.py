"""
Initial Setup: Set up VSCode with empty keybindings.json
Task ID: vscode_rrt_085
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
KEYBINDINGS_PATH = os.path.join(VSCODE_USER, "keybindings.json")
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


def create_initial():
    # Ensure VSCode user config directory exists
    os.makedirs(VSCODE_USER, exist_ok=True)
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Create empty keybindings.json (empty array)
    with open(KEYBINDINGS_PATH, "w") as f:
        json.dump([], f, indent=4)
    print(f"Created empty keybindings.json at {KEYBINDINGS_PATH}")

    # Ensure settings.json exists with default editor word wrap setting
    # so Alt+Z works in editor by default
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r") as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Make sure editor word wrap toggle works (default behavior)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)
    print(f"Settings at {SETTINGS_PATH}")

    # Create a sample file with long lines to demonstrate the need for terminal word wrap
    sample_file = os.path.join(WORKSPACE_DIR, "long_output.sh")
    with open(sample_file, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("# Script that produces long output lines in terminal\n")
        f.write('echo "This is a very long line of output that would require horizontal scrolling in the terminal without word wrap enabled. It demonstrates why having Alt+Z to toggle terminal word wrap would be useful, just like the editor already supports Alt+Z for toggling word wrap in text files."\n')
        f.write('echo "Another long line: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."\n')
        f.write('echo "Server log entry [2026-04-02T10:15:32.456Z] INFO RequestHandler - Processing incoming request from client 192.168.1.105 with headers Accept:application/json, Content-Type:text/html, Authorization:Bearer eyJhbGciOiJIUzI1NiJ9 for endpoint /api/v2/users/profile/settings"\n')
    os.chmod(sample_file, 0o755)
    print(f"Created sample script at {sample_file}")

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()

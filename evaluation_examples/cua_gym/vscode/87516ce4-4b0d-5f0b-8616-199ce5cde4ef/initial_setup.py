"""
Initial Setup: Configure VSCode editor settings for JS development
Task ID: vscode_gf5_002
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_002'

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

    # Create a minimal settings.json — does NOT contain any of the task target settings
    minimal_settings = {
        "workbench.colorTheme": "Default Dark Modern",
        "editor.minimap.enabled": True,
        "editor.renderWhitespace": "selection",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000
    }

    with open(SETTINGS_PATH, "w") as f:
        json.dump(minimal_settings, f, indent=4)
    print(f"Initial settings.json created at {SETTINGS_PATH}")

    # Create a sample JS workspace so the task context makes sense
    workspace_dir = os.path.join(WORKDIR, "js-project")
    os.makedirs(workspace_dir, exist_ok=True)

    # Create a sample JavaScript file
    js_content = '''// utils.js - Utility functions for the web app

function formatCurrency(amount, currency = "USD") {
    return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: currency,
    }).format(amount);
}

function debounce(func, delay = 300) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

function generateId(prefix = "id") {
    return `${prefix}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

module.exports = { formatCurrency, debounce, generateId };
'''
    js_path = os.path.join(workspace_dir, "utils.js")
    with open(js_path, "w") as f:
        f.write(js_content)
    print(f"Sample JS file created at {js_path}")

    # Install Prettier extension (task says it should be installed)
    try:
        subprocess.run(
            ["code", "--install-extension", "esbenp.prettier-vscode", "--force"],
            capture_output=True, text=True, timeout=60
        )
        print("Prettier extension installed")
    except Exception as e:
        print(f"Extension install note: {e}")

    # Open VSCode with the JS project folder
    launch_gui(f'code "{workspace_dir}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with js-project folder with DISPLAY=:0")


create_initial()

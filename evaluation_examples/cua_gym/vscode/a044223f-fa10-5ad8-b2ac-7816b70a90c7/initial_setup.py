"""
Initial Setup: Configure Git settings in VSCode User Settings JSON
Task ID: vscode_gf2_022
Domain: vs_code

Creates a realistic VSCode settings.json with editor preferences but
NO Git settings — those are what the agent must add.
Opens VSCode to the User Settings JSON.
"""

import json
import os
import shlex
import subprocess
import time

VSCODE_USER = os.path.join(os.path.expanduser("~"), ".config", "Code", "User")
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
    # Ensure the VSCode User config directory exists
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Realistic base settings — editor preferences only, NO git settings
    settings = {
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.wordWrap": "on",
        "editor.minimap.enabled": True,
        "editor.renderWhitespace": "selection",
        "editor.bracketPairColorization.enabled": True,
        "editor.formatOnSave": False,
        "editor.suggestSelection": "first",
        "workbench.colorTheme": "Default Dark Modern",
        "workbench.startupEditor": "welcomePage",
        "workbench.iconTheme": "vs-seti",
        "terminal.integrated.fontSize": 13,
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
        "explorer.confirmDelete": False,
        "explorer.confirmDragAndDrop": False,
        "debug.console.fontSize": 13,
        "window.zoomLevel": 0,
    }

    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)

    print(f"Initial settings.json created at: {SETTINGS_PATH}")
    print(f"Settings keys: {list(settings.keys())}")
    print("No git.* keys present — agent must add them.")

    # Launch VSCode
    launch_gui('code "/home/user"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()

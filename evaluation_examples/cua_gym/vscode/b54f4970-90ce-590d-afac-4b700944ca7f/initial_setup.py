"""
Initial Setup: Disable auto-closing brackets for Markdown files only
Task ID: vscode_code_051
Domain: vs_code
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'  # VM path — all scripts run on the VM
TASK_ID = 'vscode_code_051'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
WORKSPACE_DIR = os.path.join(WORKDIR, 'workspace')


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
    # Create VSCode user settings directory if it doesn't exist
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Write initial settings.json — global auto-closing brackets always on,
    # NO language-specific overrides (that's what the agent needs to add)
    settings = {
        "editor.autoClosingBrackets": "always",
        "editor.autoClosingQuotes": "always"
    }

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'Initial settings.json created: {SETTINGS_PATH}')
    print(f'Contents: {json.dumps(settings, indent=4)}')

    # Create a workspace directory with some sample files for context
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Create a sample Markdown file showing the annoyance context
    readme_path = os.path.join(WORKSPACE_DIR, 'README.md')
    if not os.path.exists(readme_path):
        with open(readme_path, 'w') as f:
            f.write("""# Project Notes

## Overview

This document tracks project progress and decisions. It includes
parenthetical comments (like this one) and various prose annotations.

## Status

- Feature A: Complete (merged on 2025-01-15)
- Feature B: In progress (blocked by API changes)
- Feature C: Planned (target Q2 2025)

## Notes

When writing documentation, auto-closing brackets can be annoying.
For example, typing ( in prose adds ) automatically which interrupts
the natural writing flow.

## References

See docs/api-guide.md for API documentation.
See docs/setup.md for environment setup instructions.
""")

    # Create a sample JavaScript file to show JS still uses auto-close
    src_dir = os.path.join(WORKSPACE_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)
    main_js_path = os.path.join(src_dir, 'main.js')
    if not os.path.exists(main_js_path):
        with open(main_js_path, 'w') as f:
            f.write("""// Main application entry point

function greet(name) {
    return `Hello, ${name}!`;
}

function processItems(items) {
    return items.filter(item => item.active).map(item => ({
        id: item.id,
        label: item.name,
        value: item.data
    }));
}

module.exports = { greet, processItems };
""")

    print(f'Workspace created: {WORKSPACE_DIR}')

    # GUI-ready startup: open VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

"""
Initial Setup: Configure editor for Markdown writing
Task ID: vscode_we_043
Domain: vscode

Sets up VSCode with basic settings (editor.wordWrap: off) and ensures
the Markdown All in One extension is installed. Opens VSCode.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_043'

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
    # Ensure VSCode config directory exists
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Create a simple markdown file for context
    workspace_dir = os.path.join(WORKDIR, "workspace")
    os.makedirs(workspace_dir, exist_ok=True)

    md_file = os.path.join(workspace_dir, "notes.md")
    with open(md_file, "w") as f:
        f.write("""# Project Notes

## Overview

This document contains notes about the current project status and upcoming milestones.

### Q2 2025 Goals

- Complete the API redesign for the user authentication module
- Migrate the legacy database to PostgreSQL 16
- Implement real-time notification system using WebSockets
- Conduct performance benchmarks on the new caching layer

### Team Updates

The engineering team has grown to 12 members this quarter. Sarah Chen joined as the new backend lead, bringing extensive experience with distributed systems. Marcus Johnson transitioned to the DevOps role, focusing on CI/CD pipeline improvements.

### Architecture Decisions

We decided to adopt a microservices architecture for the payment processing module. This allows independent scaling and deployment of critical financial operations. The message queue will use RabbitMQ for inter-service communication, with Redis serving as the session cache.

### Known Issues

1. Memory leak in the image processing service when handling TIFF files larger than 50MB
2. Intermittent timeout errors on the search API during peak hours (>1000 concurrent users)
3. CSS rendering inconsistency in the dashboard on Safari 17.2

### References

- [Architecture RFC](https://internal.docs/rfc/2025-003)
- [Performance Baseline Report](https://metrics.internal/q1-2025)
- [Team Roster](https://hr.internal/engineering/roster)
""")

    # Write initial settings - only editor.wordWrap: off, NO markdown-specific settings
    settings = {
        "editor.wordWrap": "off"
    }
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)
    print(f"Settings written to {SETTINGS_PATH}")

    # Install Markdown All in One extension
    try:
        result = subprocess.run(
            ["code", "--install-extension", "yzhang.markdown-all-in-one", "--force"],
            capture_output=True, text=True, timeout=60
        )
        print(f"Extension install: {result.stdout.strip()}")
        if result.returncode != 0:
            print(f"Extension install stderr: {result.stderr.strip()}")
    except Exception as e:
        print(f"Extension install error: {e}")

    # Launch VSCode with workspace
    launch_gui(f'code "{workspace_dir}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()

"""
Initial Setup: Set up file associations in VSCode
Task ID: vscode_we_027
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

    # Write empty settings (no files.associations)
    settings = {}
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)

    print(f"Initial settings created: {SETTINGS_PATH}")

    # Also create a small workspace with sample files so the task feels realistic
    workspace_dir = os.path.join(HOME, "project")
    os.makedirs(workspace_dir, exist_ok=True)

    # Create sample files with relevant extensions
    sample_files = {
        "app.env": "DATABASE_URL=postgres://localhost:5432/mydb\nSECRET_KEY=abc123\nDEBUG=true\n",
        "README.mdx": "# Project Docs\n\nimport { Component } from './Component'\n\n<Component />\n\nThis is an MDX file mixing markdown and JSX.\n",
        "schema.prisma": 'datasource db {\n  provider = "postgresql"\n  url      = env("DATABASE_URL")\n}\n\nmodel User {\n  id    Int     @id @default(autoincrement())\n  email String  @unique\n  name  String?\n}\n',
        "index.js": "const express = require('express');\nconst app = express();\n\napp.get('/', (req, res) => {\n  res.send('Hello World');\n});\n\napp.listen(3000);\n",
    }

    for filename, content in sample_files.items():
        filepath = os.path.join(workspace_dir, filename)
        with open(filepath, "w") as f:
            f.write(content)
        print(f"Created: {filepath}")

    # Launch VSCode with the project folder
    launch_gui(f'code "{workspace_dir}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()

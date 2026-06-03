"""
Initial Setup: Configure VSCode with Python workspace but no codeActionsOnSave
Task ID: vscode_stu_093
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_093'
HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")
WORKSPACE_DIR = os.path.join(WORKDIR, "python_project")


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
    # 1. Create a realistic Python project workspace
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Create a main Python file with some imports (to make organize imports relevant)
    main_py = os.path.join(WORKSPACE_DIR, "main.py")
    with open(main_py, "w") as f:
        f.write("""import sys
import os
from datetime import datetime
import json
from pathlib import Path
import re

def analyze_logs(log_dir: str) -> dict:
    \"\"\"Analyze log files in the given directory and return statistics.\"\"\"
    results = {
        "total_files": 0,
        "total_lines": 0,
        "error_count": 0,
        "warning_count": 0,
        "analyzed_at": datetime.now().isoformat(),
    }

    log_path = Path(log_dir)
    if not log_path.exists():
        return results

    for log_file in log_path.glob("*.log"):
        results["total_files"] += 1
        with open(log_file, "r") as fh:
            for line in fh:
                results["total_lines"] += 1
                if re.search(r"\\bERROR\\b", line):
                    results["error_count"] += 1
                elif re.search(r"\\bWARNING\\b", line):
                    results["warning_count"] += 1

    return results


def export_report(stats: dict, output_path: str):
    \"\"\"Export analysis report as JSON.\"\"\"
    with open(output_path, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"Report saved to {output_path}")


if __name__ == "__main__":
    log_directory = sys.argv[1] if len(sys.argv) > 1 else "/var/log/app"
    report = analyze_logs(log_directory)
    export_report(report, os.path.join(os.getcwd(), "report.json"))
""")

    # Create a utils module
    utils_py = os.path.join(WORKSPACE_DIR, "utils.py")
    with open(utils_py, "w") as f:
        f.write("""import hashlib
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


def compute_checksum(file_path: str) -> str:
    \"\"\"Compute SHA256 checksum of a file.\"\"\"
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def filter_items(items: List[dict], key: str, value: Optional[str] = None) -> List[dict]:
    \"\"\"Filter list of dicts by key existence or key-value match.\"\"\"
    if value is None:
        return [item for item in items if key in item]
    return [item for item in items if item.get(key) == value]
""")

    # 2. Set up VSCode settings WITHOUT codeActionsOnSave
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    try:
        with open(SETTINGS_PATH, "r") as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Remove any codeActionsOnSave if it exists (ensure clean initial state)
    settings.pop("editor.codeActionsOnSave", None)

    # Add some baseline settings that a Python dev might have
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.insertSpaces": True,
        "editor.wordWrap": "off",
        "python.analysis.typeCheckingMode": "basic",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
        "workbench.colorTheme": "Default Dark Modern",
    })

    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)

    print(f"Settings written to: {SETTINGS_PATH}")
    print(f"Workspace created at: {WORKSPACE_DIR}")

    # 3. Launch VSCode with the project folder
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()

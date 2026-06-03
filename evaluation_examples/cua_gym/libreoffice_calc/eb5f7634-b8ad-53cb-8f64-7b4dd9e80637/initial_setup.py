"""
Initial Setup: Create VSCode environment without custom Python snippets
Task ID: vscode_py_031
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_031'
HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SNIPPETS_DIR = os.path.join(VSCODE_USER, "snippets")
SNIPPET_FILE = os.path.join(SNIPPETS_DIR, "python.json")

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
    # Ensure the snippets directory exists but python.json does NOT exist
    os.makedirs(SNIPPETS_DIR, exist_ok=True)

    # Remove python.json if it exists (ensure clean initial state)
    if os.path.exists(SNIPPET_FILE):
        os.remove(SNIPPET_FILE)
        print(f"Removed existing {SNIPPET_FILE}")

    # Create a sample Python workspace file so the user has something to work with
    workspace_dir = os.path.join(WORKDIR, "workspace")
    os.makedirs(workspace_dir, exist_ok=True)

    sample_py = os.path.join(workspace_dir, "main.py")
    with open(sample_py, "w") as f:
        f.write("""import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_data(data):
    \"\"\"Process incoming data records.\"\"\"
    results = []
    for item in data:
        results.append(item * 2)
    return results

if __name__ == "__main__":
    sample_data = [1, 2, 3, 4, 5]
    output = process_data(sample_data)
    logger.info("Processed %d items", len(output))
    print(output)
""")
    print(f"Created sample Python file: {sample_py}")

    # Verify initial state: no python.json snippet file
    assert not os.path.exists(SNIPPET_FILE), f"ERROR: {SNIPPET_FILE} should not exist!"
    print(f"Verified: {SNIPPET_FILE} does not exist (correct initial state)")

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{workspace_dir}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")

create_initial()

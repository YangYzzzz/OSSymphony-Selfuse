"""
Initial Setup: Outdent lines 12-18 in nested.py
Task ID: vscode_edit_021
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_021'
DESKTOP = f'{WORKDIR}/Desktop'
OUTPUT = f'{DESKTOP}/nested.py'


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
    os.makedirs(DESKTOP, exist_ok=True)

    # 40-line Python file where lines 12-18 are over-indented (8 spaces instead of 4).
    # The task asks the agent to outdent lines 12-18 by one level (remove 4 spaces each).
    lines = [
        "# nested.py - Data processing utilities",          # line 1
        "# Author: Alex Rivera",                             # line 2
        "# Version: 2.1.0",                                  # line 3
        "",                                                  # line 4
        "import os",                                         # line 5
        "import sys",                                        # line 6
        "from typing import List, Optional",                 # line 7
        "",                                                  # line 8
        "",                                                  # line 9
        "def init_workspace(base_path: str) -> dict:",       # line 10
        '    """Initialize workspace directories and return status."""',  # line 11
        "        config = {}",                               # line 12 - OVER-INDENTED: 8 spaces (should be 4)
        '        config["base"] = base_path',                # line 13 - OVER-INDENTED: 8 spaces (should be 4)
        '        config["logs"] = os.path.join(base_path, "logs")',  # line 14 - OVER-INDENTED
        '        config["cache"] = os.path.join(base_path, "cache")',  # line 15 - OVER-INDENTED
        '        config["output"] = os.path.join(base_path, "output")',  # line 16 - OVER-INDENTED
        '        config["version"] = "2.1.0"',              # line 17 - OVER-INDENTED: 8 spaces (should be 4)
        "        return config",                             # line 18 - OVER-INDENTED: 8 spaces (should be 4)
        "",                                                  # line 19
        "",                                                  # line 20
        "def ensure_dirs(config: dict) -> bool:",            # line 21
        '    """Create all directories defined in config."""',  # line 22
        "    created = []",                                  # line 23
        "    for key, path in config.items():",              # line 24
        '        if key == "version":',                      # line 25
        "            continue",                              # line 26
        "        if not os.path.exists(path):",              # line 27
        "            os.makedirs(path, exist_ok=True)",      # line 28
        "            created.append(path)",                  # line 29
        "    return len(created) > 0",                       # line 30
        "",                                                  # line 31
        "",                                                  # line 32
        "def get_file_list(directory: str, ext: Optional[str] = None) -> List[str]:",  # line 33
        '    """Return list of files in directory, optionally filtered by extension."""',  # line 34
        "    if not os.path.isdir(directory):",              # line 35
        "        return []",                                 # line 36
        "    files = os.listdir(directory)",                 # line 37
        "    if ext:",                                       # line 38
        "        files = [f for f in files if f.endswith(ext)]",  # line 39
        "    return sorted(files)",                          # line 40
    ]

    content = "\n".join(lines) + "\n"

    with open(OUTPUT, 'w') as f:
        f.write(content)
    print(f'Initial file created: {OUTPUT}')

    # Verify line count and indentation
    with open(OUTPUT) as f:
        file_lines = f.readlines()
    print(f'Line count: {len(file_lines)} (expected 40)')
    for i in range(11, 18):
        spaces = len(file_lines[i]) - len(file_lines[i].lstrip())
        print(f'  Line {i+1}: {spaces} leading spaces (expected 8)')

    # GUI-ready startup: open the file in VSCode
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

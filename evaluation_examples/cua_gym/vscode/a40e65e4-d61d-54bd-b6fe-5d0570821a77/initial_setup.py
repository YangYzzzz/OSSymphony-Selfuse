"""
Initial Setup: Create Python user snippet task
Task ID: vscode_code_018
Domain: vs_code

Prepares an initial VM state where:
- VSCode is installed and ready
- A workspace folder exists with a sample Python file
- No Python snippets exist (python.json absent from snippets dir)
- VSCode is launched open to the workspace
"""

import os
import json
import shlex
import subprocess
import time

HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SNIPPETS_DIR = os.path.join(VSCODE_USER, 'snippets')
PYTHON_SNIPPET_PATH = os.path.join(SNIPPETS_DIR, 'python.json')
WORKSPACE_DIR = os.path.join(HOME, 'workspace')


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # 1. Ensure the snippets directory exists but remove any existing python.json
    os.makedirs(SNIPPETS_DIR, exist_ok=True)
    if os.path.exists(PYTHON_SNIPPET_PATH):
        os.remove(PYTHON_SNIPPET_PATH)
        print(f'Removed existing snippet file: {PYTHON_SNIPPET_PATH}')
    else:
        print(f'No existing python.json snippet found (correct initial state).')

    # 2. Create a workspace folder with a realistic sample Python file
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    sample_py = os.path.join(WORKSPACE_DIR, 'data_processor.py')
    sample_content = '''\
"""
Data processing utilities for sales analytics.
"""
from typing import List, Optional


def calculate_revenue(sales: List[float], discount_rate: float = 0.0) -> float:
    """Calculate total revenue after applying discount."""
    total = sum(sales)
    return total * (1.0 - discount_rate)


def filter_by_threshold(values: List[float], threshold: float) -> List[float]:
    """Return only values above the given threshold."""
    return [v for v in values if v > threshold]


# TODO: Add a Customer class with __init__ method below

'''
    with open(sample_py, 'w') as f:
        f.write(sample_content)
    print(f'Created sample Python file: {sample_py}')

    # 3. Ensure VSCode settings file exists (so VSCode opens cleanly)
    settings_path = os.path.join(VSCODE_USER, 'settings.json')
    os.makedirs(VSCODE_USER, exist_ok=True)
    if not os.path.exists(settings_path):
        with open(settings_path, 'w') as f:
            json.dump({
                "editor.fontSize": 14,
                "editor.tabSize": 4,
                "editor.insertSpaces": True,
                "files.autoSave": "onFocusChange"
            }, f, indent=4)
        print(f'Created default VSCode settings: {settings_path}')

    # 4. Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

    print('Initial setup complete.')
    print(f'  Snippets dir exists: {os.path.isdir(SNIPPETS_DIR)}')
    print(f'  python.json absent: {not os.path.exists(PYTHON_SNIPPET_PATH)}')
    print(f'  Workspace dir: {WORKSPACE_DIR}')


create_initial()

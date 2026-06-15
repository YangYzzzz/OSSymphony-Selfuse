"""
Reward Script: Set up Python project with venv, pylint, and VSCode linter config
Task ID: vscode_wf_011
Domain: vscode (libreoffice_calc label but actually vscode workflow)
Scoring:
  Component 1: venv directory exists at ~/project/venv/ (0.25 pts)
  Component 2: pylint is installed in the venv (0.30 pts)
  Component 3: settings.json has python.defaultInterpreterPath pointing to venv python (0.25 pts)
  Component 4: settings.json has python.linting.pylintEnabled = true (0.20 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'project')
VENV_DIR = os.path.join(PROJECT_DIR, 'venv')
SETTINGS_PATH = os.path.join(PROJECT_DIR, '.vscode', 'settings.json')
TASK_ID = 'vscode_wf_011'


def load_settings(path):
    """Load settings.json, handling JSONC (comments)."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments for JSONC compatibility
        cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(cleaned)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARN: Could not load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: venv directory exists at ~/project/venv/ (0.25 points)
    # The venv must be a valid Python virtual environment (has bin/python and pyvenv.cfg)
    try:
        venv_python = os.path.join(VENV_DIR, 'bin', 'python')
        pyvenv_cfg = os.path.join(VENV_DIR, 'pyvenv.cfg')
        if os.path.isdir(VENV_DIR) and os.path.isfile(venv_python) and os.path.isfile(pyvenv_cfg):
            print(f"PASS: Component 1 — venv exists at {VENV_DIR} with bin/python and pyvenv.cfg (0.25 pts)")
            total_score += 0.25
        else:
            missing = []
            if not os.path.isdir(VENV_DIR):
                missing.append("venv dir missing")
            if not os.path.isfile(venv_python):
                missing.append("bin/python missing")
            if not os.path.isfile(pyvenv_cfg):
                missing.append("pyvenv.cfg missing")
            print(f"FAIL: Component 1 — venv not a valid virtual environment: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: pylint is installed in the venv (0.30 points)
    # Check that the pylint package directory exists in venv site-packages
    try:
        venv_lib = os.path.join(VENV_DIR, 'lib')
        pylint_dirs = []
        if os.path.isdir(venv_lib):
            for pydir in os.listdir(venv_lib):
                site_pkgs = os.path.join(venv_lib, pydir, 'site-packages')
                if os.path.isdir(site_pkgs):
                    pylint_dirs = [
                        item for item in os.listdir(site_pkgs)
                        if item.lower().startswith('pylint')
                        and os.path.isdir(os.path.join(site_pkgs, item))
                    ]
                if len(pylint_dirs) > 0:
                    break

        if len(pylint_dirs) > 0:
            print(f"PASS: Component 2 — pylint is installed in venv site-packages (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — pylint not found in venv site-packages")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: settings.json has python.defaultInterpreterPath pointing to venv (0.25 points)
    try:
        settings = load_settings(SETTINGS_PATH)
        if settings is None:
            print(f"FAIL: Component 3 — settings.json could not be loaded")
        else:
            interpreter_path = settings.get('python.defaultInterpreterPath', None)
            if interpreter_path is not None:
                # Accept various forms: "./venv/bin/python", "venv/bin/python",
                # "/home/user/project/venv/bin/python", etc.
                normalized = interpreter_path.strip()
                valid_paths = [
                    './venv/bin/python',
                    'venv/bin/python',
                    '/home/user/project/venv/bin/python',
                    './venv/bin/python3',
                    'venv/bin/python3',
                    '/home/user/project/venv/bin/python3',
                ]
                if normalized in valid_paths or 'venv/bin/python' in normalized:
                    print(f"PASS: Component 3 — python.defaultInterpreterPath = '{interpreter_path}' (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 3 — python.defaultInterpreterPath = '{interpreter_path}' does not point to venv python")
            else:
                print(f"FAIL: Component 3 — python.defaultInterpreterPath not set in settings.json")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: settings.json has python.linting.pylintEnabled = true (0.20 points)
    try:
        settings = load_settings(SETTINGS_PATH)
        if settings is None:
            print(f"FAIL: Component 4 — settings.json could not be loaded")
        else:
            pylint_enabled = settings.get('python.linting.pylintEnabled', None)
            if pylint_enabled is True:
                print(f"PASS: Component 4 — python.linting.pylintEnabled = true (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — python.linting.pylintEnabled = {pylint_enabled} (expected true)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

"""
Reward Script: Python venv setup with flask/requests and VSCode interpreter selection
Task ID: vscode_stu_062
Domain: vscode
Scoring:
  Component 1: venv directory exists at ~/cs301/webapp/venv with valid structure (0.25)
  Component 2: Flask package installed in venv (0.25)
  Component 3: Requests package installed in venv (0.25)
  Component 4: VSCode Python interpreter set to venv python3 (0.25)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_062'
PROJECT_DIR = os.path.join(WORKDIR, 'cs301', 'webapp')
VENV_DIR = os.path.join(PROJECT_DIR, 'venv')
VENV_PYTHON = os.path.join(VENV_DIR, 'bin', 'python3')
VSCODE_GLOBAL_SETTINGS = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')
VSCODE_WS_SETTINGS = os.path.join(PROJECT_DIR, '.vscode', 'settings.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: venv directory exists with valid structure (0.25 points)
    # The venv must have bin/python3 and pyvenv.cfg — a real venv, not just an empty dir.
    # This FAILS on initial_env (no venv dir) and PASSES on golden_env.
    try:
        has_python = os.path.isfile(VENV_PYTHON)
        has_pyvenv_cfg = os.path.isfile(os.path.join(VENV_DIR, 'pyvenv.cfg'))
        if has_python and has_pyvenv_cfg:
            print(f"PASS: Component 1 - venv exists with python3 and pyvenv.cfg (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 - venv structure incomplete. python3={has_python}, pyvenv.cfg={has_pyvenv_cfg}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Flask installed in venv (0.25 points)
    # Check if flask is importable from the venv's site-packages.
    # This FAILS on initial_env (no venv) and PASSES on golden_env.
    try:
        flask_found = False
        site_packages_base = os.path.join(VENV_DIR, 'lib')
        if os.path.isdir(site_packages_base):
            # Walk lib/pythonX.Y/site-packages looking for flask
            for direntry in os.listdir(site_packages_base):
                sp = os.path.join(site_packages_base, direntry, 'site-packages')
                if os.path.isdir(sp):
                    # Check for flask directory or Flask*.dist-info
                    entries = os.listdir(sp)
                    for entry in entries:
                        if entry.lower() == 'flask' and os.path.isdir(os.path.join(sp, entry)):
                            flask_found = True
                            break
                        if entry.lower().startswith('flask') and 'dist-info' in entry.lower():
                            flask_found = True
                            break
                if flask_found:
                    break

        if flask_found:
            print(f"PASS: Component 2 - Flask is installed in venv (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 - Flask not found in venv site-packages")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Requests installed in venv (0.25 points)
    # Check if requests is importable from the venv's site-packages.
    # This FAILS on initial_env (no venv) and PASSES on golden_env.
    try:
        requests_found = False
        site_packages_base = os.path.join(VENV_DIR, 'lib')
        if os.path.isdir(site_packages_base):
            for direntry in os.listdir(site_packages_base):
                sp = os.path.join(site_packages_base, direntry, 'site-packages')
                if os.path.isdir(sp):
                    entries = os.listdir(sp)
                    for entry in entries:
                        if entry.lower() == 'requests' and os.path.isdir(os.path.join(sp, entry)):
                            requests_found = True
                            break
                        if entry.lower().startswith('requests') and 'dist-info' in entry.lower():
                            requests_found = True
                            break
                if requests_found:
                    break

        if requests_found:
            print(f"PASS: Component 3 - Requests is installed in venv (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 - Requests not found in venv site-packages")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: VSCode Python interpreter set to venv python3 (0.25 points)
    # Check both global settings and workspace settings (.vscode/settings.json).
    # The interpreter path should point to the venv python3.
    # This FAILS on initial_env (no such setting) and PASSES on golden_env.
    try:
        interpreter_set = False
        expected_path = '/home/user/cs301/webapp/venv/bin/python3'

        # Check workspace-level settings first (preferred)
        if os.path.isfile(VSCODE_WS_SETTINGS):
            with open(VSCODE_WS_SETTINGS, 'r') as f:
                content = f.read()
                # Strip JSONC comments
                content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
                ws_settings = json.loads(content)
            ws_interp = ws_settings.get('python.defaultInterpreterPath', '')
            if ws_interp == expected_path:
                interpreter_set = True

        # Also check global settings
        if not interpreter_set and os.path.isfile(VSCODE_GLOBAL_SETTINGS):
            with open(VSCODE_GLOBAL_SETTINGS, 'r') as f:
                content = f.read()
                content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
                global_settings = json.loads(content)
            global_interp = global_settings.get('python.defaultInterpreterPath', '')
            if global_interp == expected_path:
                interpreter_set = True

        if interpreter_set:
            print(f"PASS: Component 4 - VSCode interpreter set to {expected_path} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 - VSCode interpreter not set to {expected_path}")
            # Print what was found for debugging
            if os.path.isfile(VSCODE_WS_SETTINGS):
                with open(VSCODE_WS_SETTINGS, 'r') as f:
                    print(f"  Workspace settings: {f.read().strip()}")
            if os.path.isfile(VSCODE_GLOBAL_SETTINGS):
                with open(VSCODE_GLOBAL_SETTINGS, 'r') as f:
                    print(f"  Global settings: {f.read().strip()}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

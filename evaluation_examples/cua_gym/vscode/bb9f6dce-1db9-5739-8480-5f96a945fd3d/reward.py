"""
Reward Script: Configure Python virtual environment and select as workspace interpreter
Task ID: vscode_lp_016
Domain: vscode
Scoring:
  Component 1 (0.3): .venv directory exists with valid pyvenv.cfg
  Component 2 (0.3): .venv/bin/python symlink exists and resolves to a Python executable
  Component 3 (0.4): VSCode workspace settings configure .venv interpreter path
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'newapp')
VENV_DIR = os.path.join(PROJECT_DIR, '.venv')
VSCODE_SETTINGS = os.path.join(PROJECT_DIR, '.vscode', 'settings.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: .venv directory exists with valid pyvenv.cfg (0.3 points)
    # This checks that a virtual environment was actually created (not just a directory)
    try:
        pyvenv_cfg_path = os.path.join(VENV_DIR, 'pyvenv.cfg')
        if os.path.isdir(VENV_DIR) and os.path.isfile(pyvenv_cfg_path):
            # Verify pyvenv.cfg has expected content (home key pointing to a Python installation)
            with open(pyvenv_cfg_path, 'r') as f:
                cfg_content = f.read()
            if 'home' in cfg_content and 'version' in cfg_content:
                print(f"PASS: Component 1 -- .venv exists with valid pyvenv.cfg (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 -- pyvenv.cfg exists but missing 'home' or 'version' keys. Content: {cfg_content[:200]}")
        else:
            print(f"FAIL: Component 1 -- .venv dir exists: {os.path.isdir(VENV_DIR)}, pyvenv.cfg exists: {os.path.isfile(pyvenv_cfg_path) if os.path.isdir(VENV_DIR) else 'N/A'}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: .venv/bin/python exists and is a valid Python symlink/executable (0.3 points)
    # This ensures the venv has a usable Python interpreter
    try:
        python_path = os.path.join(VENV_DIR, 'bin', 'python')
        if os.path.exists(python_path):
            # Check it's either a symlink to a python binary or an executable
            is_executable = os.access(python_path, os.X_OK) or os.path.islink(python_path)
            if is_executable:
                # Resolve the symlink to verify it points to a real python
                resolved = os.path.realpath(python_path)
                if 'python' in os.path.basename(resolved).lower():
                    print(f"PASS: Component 2 -- .venv/bin/python exists and resolves to {resolved} (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 -- .venv/bin/python resolves to {resolved}, which doesn't appear to be a Python executable")
            else:
                print(f"FAIL: Component 2 -- .venv/bin/python exists but is not executable/symlink")
        else:
            print(f"FAIL: Component 2 -- .venv/bin/python does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: VSCode workspace settings configure .venv as interpreter (0.4 points)
    # This verifies the user selected the venv as the workspace interpreter in VSCode
    try:
        if os.path.isfile(VSCODE_SETTINGS):
            with open(VSCODE_SETTINGS, 'r') as f:
                content = f.read()
            # Strip JSONC comments if present
            clean_content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            settings = json.loads(clean_content)

            # Check for python interpreter path setting
            # VSCode uses python.defaultInterpreterPath or python.pythonPath (deprecated)
            interpreter_path = settings.get('python.defaultInterpreterPath', settings.get('python.pythonPath', ''))

            if interpreter_path:
                # The interpreter path should reference the .venv in the project
                # Accept various valid forms:
                #   /home/user/projects/newapp/.venv/bin/python
                #   .venv/bin/python
                #   ${workspaceFolder}/.venv/bin/python
                venv_patterns = [
                    '.venv/bin/python',
                    '.venv\\bin\\python',
                    os.path.join(PROJECT_DIR, '.venv', 'bin', 'python'),
                ]
                matched = any(pattern in interpreter_path for pattern in venv_patterns)
                # Also check for ${workspaceFolder} variable
                if not matched and '${workspaceFolder}' in interpreter_path:
                    expanded = interpreter_path.replace('${workspaceFolder}', PROJECT_DIR)
                    matched = '.venv/bin/python' in expanded or '.venv\\bin\\python' in expanded

                if matched:
                    print(f"PASS: Component 3 -- VSCode interpreter set to '{interpreter_path}' (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 3 -- Interpreter path '{interpreter_path}' does not reference .venv")
            else:
                print(f"FAIL: Component 3 -- No python.defaultInterpreterPath or python.pythonPath found in workspace settings. Keys: {list(settings.keys())}")
        else:
            print(f"FAIL: Component 3 -- {VSCODE_SETTINGS} does not exist")
    except json.JSONDecodeError as e:
        print(f"ERROR: Component 3 -- Invalid JSON in workspace settings: {e}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

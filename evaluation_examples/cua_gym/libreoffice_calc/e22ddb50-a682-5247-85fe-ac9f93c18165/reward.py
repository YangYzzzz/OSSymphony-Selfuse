"""
Reward Script: Python development environment setup with pyenv
Task ID: os_gf5_021
Domain: os
Scoring:
  Component 1: pyenv installed at ~/.pyenv (0.20)
  Component 2: Python 3.11.7 installed and set as global (0.25)
  Component 3: pyenv configured in .bashrc (0.15)
  Component 4: virtualenv at ~/projects/ml-project/.venv using 3.11.7 (0.25)
  Component 5: VS Code settings.json with venv interpreter path (0.15)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'os_gf5_021'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: pyenv installed at ~/.pyenv with executable (0.20 points)
    try:
        pyenv_root = os.path.join(WORKDIR, '.pyenv')
        pyenv_bin = os.path.join(pyenv_root, 'bin', 'pyenv')
        if os.path.isdir(pyenv_root) and os.path.isfile(pyenv_bin):
            # Verify it's actually a functional pyenv by checking it has key subdirs
            has_libexec = os.path.isdir(os.path.join(pyenv_root, 'libexec'))
            has_plugins = os.path.isdir(os.path.join(pyenv_root, 'plugins'))
            if has_libexec and has_plugins:
                print(f"PASS: Component 1 — pyenv installed at {pyenv_root} with functional structure (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 — pyenv dir exists but missing key subdirs (libexec={has_libexec}, plugins={has_plugins})")
        else:
            print(f"FAIL: Component 1 — pyenv not found at {pyenv_root} or bin/pyenv missing")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Python 3.11.7 installed via pyenv AND set as global (0.25 points)
    try:
        python_dir = os.path.join(WORKDIR, '.pyenv', 'versions', '3.11.7')
        python_bin = os.path.join(python_dir, 'bin', 'python3.11')
        version_file = os.path.join(WORKDIR, '.pyenv', 'version')

        python_installed = os.path.isdir(python_dir) and os.path.isfile(python_bin)
        global_set = False
        if os.path.isfile(version_file):
            version_content = open(version_file).read().strip()
            global_set = version_content == '3.11.7'

        if python_installed and global_set:
            print(f"PASS: Component 2 — Python 3.11.7 installed and set as global (0.25 pts)")
            total_score += 0.25
        elif python_installed and not global_set:
            # Partial: installed but not set as global
            print(f"FAIL: Component 2 — Python 3.11.7 installed but not set as global (version file: {version_content if os.path.isfile(version_file) else 'missing'})")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 — Python 3.11.7 not installed at {python_dir}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: pyenv configured in .bashrc (0.15 points)
    try:
        bashrc_path = os.path.join(WORKDIR, '.bashrc')
        if os.path.isfile(bashrc_path):
            bashrc_content = open(bashrc_path).read()
            has_pyenv_root = 'PYENV_ROOT' in bashrc_content
            has_pyenv_path = '.pyenv' in bashrc_content and 'PATH' in bashrc_content
            has_pyenv_init = 'pyenv init' in bashrc_content

            if has_pyenv_root and has_pyenv_init:
                print(f"PASS: Component 3 — pyenv configured in .bashrc (PYENV_ROOT + init) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — .bashrc missing pyenv config (PYENV_ROOT={has_pyenv_root}, init={has_pyenv_init})")
        else:
            print(f"FAIL: Component 3 — .bashrc not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: virtualenv at ~/projects/ml-project/.venv using Python 3.11.7 (0.25 points)
    try:
        venv_dir = os.path.join(WORKDIR, 'projects', 'ml-project', '.venv')
        pyvenv_cfg = os.path.join(venv_dir, 'pyvenv.cfg')
        venv_python = os.path.join(venv_dir, 'bin', 'python')

        if os.path.isdir(venv_dir) and os.path.isfile(pyvenv_cfg) and os.path.isfile(venv_python):
            cfg_content = open(pyvenv_cfg).read()
            # Check that the venv is based on Python 3.11.7
            uses_3117 = '3.11.7' in cfg_content
            if uses_3117:
                print(f"PASS: Component 4 — virtualenv at .venv uses Python 3.11.7 (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 — virtualenv exists but does not use Python 3.11.7. Config: {cfg_content[:200]}")
        else:
            print(f"FAIL: Component 4 — virtualenv not found at {venv_dir} (dir={os.path.isdir(venv_dir)}, cfg={os.path.isfile(pyvenv_cfg) if os.path.isdir(venv_dir) else 'N/A'})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: VS Code settings.json with venv interpreter path (0.15 points)
    try:
        vscode_settings = os.path.join(WORKDIR, 'projects', 'ml-project', '.vscode', 'settings.json')
        if os.path.isfile(vscode_settings):
            with open(vscode_settings) as f:
                settings = json.load(f)

            # Check that python interpreter path points to the venv
            interpreter_path = settings.get('python.defaultInterpreterPath', '')
            expected_venv_path = '/home/user/projects/ml-project/.venv'
            if expected_venv_path in interpreter_path and 'python' in interpreter_path.lower():
                print(f"PASS: Component 5 — VS Code settings point to venv interpreter: {interpreter_path} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — python.defaultInterpreterPath is '{interpreter_path}', expected path containing {expected_venv_path}")
        else:
            print(f"FAIL: Component 5 — VS Code settings.json not found at {vscode_settings}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

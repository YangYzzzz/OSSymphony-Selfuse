"""
Reward Script: Initialize Python venv, install flask/flask-sqlalchemy, create requirements.txt,
               and set python.defaultInterpreterPath in VSCode settings.
Task ID: vscode_gf4_001
Domain: vscode
Scoring:
  Component 1 (0.25): venv directory is a valid Python virtual environment
  Component 2 (0.20): Flask is installed in the venv
  Component 3 (0.20): Flask-SQLAlchemy is installed in the venv
  Component 4 (0.20): requirements.txt contains flask and flask-sqlalchemy
  Component 5 (0.15): VSCode settings.json has python.defaultInterpreterPath -> venv
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_001'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'flask-api')
VENV_DIR = os.path.join(PROJECT_DIR, 'venv')
REQ_FILE = os.path.join(PROJECT_DIR, 'requirements.txt')
SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: venv directory is a valid Python virtual environment (0.25 points)
    # A valid venv has pyvenv.cfg and bin/python
    try:
        pyvenv_cfg = os.path.join(VENV_DIR, 'pyvenv.cfg')
        venv_python = os.path.join(VENV_DIR, 'bin', 'python')
        if os.path.isdir(VENV_DIR) and os.path.isfile(pyvenv_cfg) and os.path.isfile(venv_python):
            print(f"PASS: Component 1 — venv is a valid Python virtual environment (0.25 pts)")
            total_score += 0.25
        else:
            missing = []
            if not os.path.isdir(VENV_DIR):
                missing.append("venv dir missing")
            if not os.path.isfile(pyvenv_cfg):
                missing.append("pyvenv.cfg missing")
            if not os.path.isfile(venv_python):
                missing.append("bin/python missing")
            print(f"FAIL: Component 1 — invalid venv: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Flask is installed in the venv (0.20 points)
    # Check by looking for flask in the venv site-packages
    try:
        venv_lib = os.path.join(VENV_DIR, 'lib')
        flask_found = False
        if os.path.isdir(venv_lib):
            for pyver in os.listdir(venv_lib):
                sp = os.path.join(venv_lib, pyver, 'site-packages', 'flask')
                if os.path.isdir(sp):
                    flask_found = True
                    break
        if flask_found:
            print(f"PASS: Component 2 — Flask is installed in venv site-packages (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Flask not found in venv site-packages")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Flask-SQLAlchemy is installed in the venv (0.20 points)
    try:
        venv_lib = os.path.join(VENV_DIR, 'lib')
        fsa_found = False
        if os.path.isdir(venv_lib):
            for pyver in os.listdir(venv_lib):
                sp = os.path.join(venv_lib, pyver, 'site-packages', 'flask_sqlalchemy')
                if os.path.isdir(sp):
                    fsa_found = True
                    break
        if fsa_found:
            print(f"PASS: Component 3 — Flask-SQLAlchemy is installed in venv site-packages (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Flask-SQLAlchemy not found in venv site-packages")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: requirements.txt exists and contains flask and flask-sqlalchemy (0.20 points)
    try:
        if os.path.isfile(REQ_FILE):
            with open(REQ_FILE, 'r') as f:
                content = f.read().lower()
            # Check for flask and flask-sqlalchemy entries (case-insensitive)
            has_flask = bool(re.search(r'^flask[=><!~\s]', content, re.MULTILINE) or
                            re.search(r'^flask$', content, re.MULTILINE))
            has_fsa = bool(re.search(r'^flask[-_]sqlalchemy[=><!~\s]', content, re.MULTILINE) or
                          re.search(r'^flask[-_]sqlalchemy$', content, re.MULTILINE))
            if has_flask and has_fsa:
                print(f"PASS: Component 4 — requirements.txt contains flask and flask-sqlalchemy (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — requirements.txt missing: flask={has_flask}, flask-sqlalchemy={has_fsa}")
        else:
            print(f"FAIL: Component 4 — requirements.txt does not exist")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: VSCode settings.json has python.defaultInterpreterPath pointing to venv (0.15 points)
    try:
        if os.path.isfile(SETTINGS_PATH):
            with open(SETTINGS_PATH, 'r') as f:
                raw = f.read()
            # Strip JSONC comments
            cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
            settings = json.loads(cleaned)
            interpreter = settings.get('python.defaultInterpreterPath', '')
            # Accept both ~/projects/... and /home/user/projects/... forms
            # The key thing is it points to the venv python binary
            if interpreter and ('flask-api/venv/bin/python' in interpreter or
                                'flask-api/venv/bin/python3' in interpreter):
                print(f"PASS: Component 5 — python.defaultInterpreterPath = '{interpreter}' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — python.defaultInterpreterPath = '{interpreter}', expected path to venv python")
        else:
            print(f"FAIL: Component 5 — settings.json not found at {SETTINGS_PATH}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

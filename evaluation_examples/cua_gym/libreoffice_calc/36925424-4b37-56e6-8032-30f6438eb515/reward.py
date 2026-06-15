"""
Reward Script: Set up VSCode for Docker development
Task ID: osworld_multi_apps_vscode_ext_script_013
Domain: vscode / os (multi-app)
Scoring:
  Component 1 (0.4): Docker extension ms-azuretools.vscode-docker is installed
                      (extension directory and/or extensions.json entry present)
  Component 2 (0.3): Dockerfile exists at ~/Desktop/myapp/Dockerfile
  Component 3 (0.3): Dockerfile content is valid — uses python:3.11 base, COPYs
                      requirements.txt and app.py, runs pip install, exposes port 5000,
                      CMD runs app.py
Total: 1.0
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_ext_script_013'

DOCKERFILE_PATH = os.path.join(WORKDIR, 'Desktop', 'myapp', 'Dockerfile')
VSCODE_EXTENSIONS_DIR = os.path.join(WORKDIR, '.vscode', 'extensions')
EXTENSIONS_JSON_PATH = os.path.join(VSCODE_EXTENSIONS_DIR, 'extensions.json')
DOCKER_EXT_ID = 'ms-azuretools.vscode-docker'


def docker_ext_dir_present():
    """Check if Docker extension directory exists in ~/.vscode/extensions/."""
    if not os.path.isdir(VSCODE_EXTENSIONS_DIR):
        return False
    for entry in os.listdir(VSCODE_EXTENSIONS_DIR):
        if entry.lower().startswith('ms-azuretools.vscode-docker'):
            return entry
    return None


def docker_ext_in_json():
    """Check if Docker extension entry exists in extensions.json."""
    if not os.path.isfile(EXTENSIONS_JSON_PATH):
        return None
    try:
        with open(EXTENSIONS_JSON_PATH, 'r') as f:
            ext_data = json.load(f)
        if isinstance(ext_data, list):
            for ext in ext_data:
                ext_id = ext.get('identifier', {}).get('id', '') or ext.get('id', '')
                if DOCKER_EXT_ID.lower() in ext_id.lower():
                    return ext_id
    except (json.JSONDecodeError, KeyError, TypeError):
        pass
    return None


def verify_dockerfile_content(path):
    """
    Parse Dockerfile and verify all required instructions are present.
    Returns a dict of check_name -> bool.
    """
    with open(path, 'r') as f:
        content = f.read()

    return {
        'python3.11_base': bool(re.search(r'FROM\s+python:3\.11', content, re.IGNORECASE)),
        'copy_requirements': bool(re.search(r'COPY\s+requirements\.txt', content, re.IGNORECASE)),
        'copy_apppy': bool(re.search(r'COPY\s+app\.py', content, re.IGNORECASE)),
        'pip_install': bool(re.search(r'RUN\s+pip\s+install', content, re.IGNORECASE)),
        'port_or_cmd': bool(
            re.search(r'EXPOSE\s+5000', content, re.IGNORECASE) or
            re.search(r'CMD\s*.*app\.py', content, re.IGNORECASE)
        ),
    }


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Docker extension ms-azuretools.vscode-docker is installed (0.4 points)
    # The extension directory should exist in ~/.vscode/extensions/
    # and/or extensions.json should contain the extension entry
    try:
        ext_dir = docker_ext_dir_present()
        ext_json = docker_ext_in_json()

        if ext_dir:
            print(f"PASS: Docker extension directory found: {ext_dir}")
        else:
            print(f"INFO: Docker extension directory not found in {VSCODE_EXTENSIONS_DIR}")

        if ext_json:
            print(f"PASS: Docker extension found in extensions.json: {ext_json}")
        else:
            print(f"INFO: Docker extension not found in extensions.json")

        if ext_dir or ext_json:
            print(f"PASS: Component 1 — Docker extension installed (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Docker extension ms-azuretools.vscode-docker NOT found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Dockerfile exists at ~/Desktop/myapp/Dockerfile (0.3 points)
    try:
        if os.path.isfile(DOCKERFILE_PATH):
            print(f"PASS: Component 2 — Dockerfile exists at {DOCKERFILE_PATH} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Dockerfile NOT found at {DOCKERFILE_PATH}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Dockerfile content is valid Flask app Dockerfile (0.3 points)
    # Must: use python:3.11 as base, COPY requirements.txt, COPY app.py,
    #        run pip install, EXPOSE 5000 or CMD runs app.py
    try:
        if not os.path.isfile(DOCKERFILE_PATH):
            print(f"FAIL: Component 3 — Dockerfile not found, cannot verify content")
        else:
            checks = verify_dockerfile_content(DOCKERFILE_PATH)
            passed = sum(1 for v in checks.values() if v)
            total_checks = len(checks)

            print(f"Component 3 checks ({passed}/{total_checks}):")
            for check_name, result in checks.items():
                status = "PASS" if result else "FAIL"
                print(f"  {status}: {check_name}")

            if passed == total_checks:
                print(f"PASS: Component 3 — Dockerfile content fully valid (0.3 pts)")
                total_score += 0.3
            elif passed >= 3:
                # Partial credit proportional to checks passed
                partial = round(0.3 * passed / total_checks, 2)
                print(f"PARTIAL: Component 3 — {passed}/{total_checks} checks pass ({partial} pts)")
                if passed >= 3:
                    total_score += partial
            else:
                print(f"FAIL: Component 3 — Dockerfile content invalid ({passed}/{total_checks} checks pass)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

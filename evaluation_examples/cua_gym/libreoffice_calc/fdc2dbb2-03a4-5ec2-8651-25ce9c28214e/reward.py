"""
Reward Script: Clone scikit-learn, install dependencies, install in editable mode
Task ID: osworld_multi_apps_vscode_env_setup_006
Domain: os (environment setup)
Scoring:
  Component 1: scikit-learn repo cloned to /home/user/scikit-learn with correct remote (0.3)
  Component 2: Cython installed (was missing on initial_env)             (0.2)
  Component 3: scikit-learn installed in editable mode                   (0.3)
  Component 4: 'import sklearn' succeeds (package importable)            (0.2)
  Total: 1.0

Notes:
  - numpy and scipy were ALREADY present on initial_env, so they are NOT scored
    (scoring them would give >0 on initial_env, violating the contract)
  - Cython was NOT present on initial_env, so it IS scored
  - The editable install (.pth file) was NOT present on initial_env, so it IS scored
  - The 'import sklearn' check was failing on initial_env, so it IS scored
"""

import os
import subprocess
import importlib

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_env_setup_006'
REPO_PATH = '/home/user/scikit-learn'
SITE_PACKAGES_PATH = '/home/user/.local/lib/python3.10/site-packages'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Repository cloned to /home/user/scikit-learn with correct remote (0.3 points)
    # This FAILS on initial_env (no directory) → PASSES on golden_env (directory present with correct remote)
    try:
        if not os.path.isdir(REPO_PATH):
            print(f"FAIL: Component 1 — /home/user/scikit-learn directory does not exist")
        elif not os.path.isdir(os.path.join(REPO_PATH, '.git')):
            print(f"FAIL: Component 1 — /home/user/scikit-learn exists but is not a git repository")
        else:
            # Check the git remote URL
            result = subprocess.run(
                ['git', '-C', REPO_PATH, 'remote', 'get-url', 'origin'],
                capture_output=True, text=True
            )
            remote_url = result.stdout.strip()
            expected_url = 'https://github.com/scikit-learn/scikit-learn'
            if result.returncode == 0 and expected_url in remote_url:
                print(f"PASS: Component 1 — scikit-learn repo cloned at {REPO_PATH}, remote: {remote_url} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — git remote URL mismatch: expected {expected_url}, got '{remote_url}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Cython installed (0.2 points)
    # Cython was NOT installed on initial_env → MUST be installed on golden_env
    try:
        result = subprocess.run(
            ['pip', 'show', 'cython'],
            capture_output=True, text=True
        )
        if result.returncode == 0 and 'Name: Cython' in result.stdout:
            import re
            version_match = re.search(r'Version:\s*(\S+)', result.stdout)
            version = version_match.group(1) if version_match else 'unknown'
            print(f"PASS: Component 2 — Cython installed (version: {version}) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — Cython not installed. pip show returned: {result.stdout.strip()} | {result.stderr.strip()}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: scikit-learn installed in editable mode (0.3 points)
    # The editable .pth file was NOT present on initial_env → MUST be present on golden_env
    try:
        # Check for the editable install marker: scikit-learn-editable.pth in site-packages
        editable_pth = os.path.join(SITE_PACKAGES_PATH, 'scikit-learn-editable.pth')
        editable_loader = os.path.join(SITE_PACKAGES_PATH, '_scikit_learn_editable_loader.py')

        if os.path.isfile(editable_pth):
            pth_content = open(editable_pth).read().strip()
            print(f"PASS: Component 3 — scikit-learn editable install found ({editable_pth}, content: {pth_content}) (0.3 pts)")
            total_score += 0.3
        elif os.path.isfile(editable_loader):
            print(f"PASS: Component 3 — scikit-learn editable loader found ({editable_loader}) (0.3 pts)")
            total_score += 0.3
        else:
            # Fallback: check dist-info for editable marker (direct_url.json)
            dist_info_path = os.path.join(SITE_PACKAGES_PATH, 'scikit_learn-1.6.1.dist-info')
            direct_url_file = os.path.join(dist_info_path, 'direct_url.json')
            if os.path.isfile(direct_url_file):
                import json
                with open(direct_url_file) as f:
                    direct_url = json.load(f)
                if direct_url.get('dir_info', {}).get('editable', False):
                    print(f"PASS: Component 3 — scikit-learn editable install confirmed via direct_url.json (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 3 — scikit-learn installed but NOT in editable mode. direct_url.json: {direct_url}")
            else:
                print(f"FAIL: Component 3 — No editable install markers found in {SITE_PACKAGES_PATH}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: sklearn can be imported successfully (0.2 points)
    # import sklearn FAILS on initial_env (ModuleNotFoundError) → PASSES on golden_env
    try:
        result = subprocess.run(
            ['python3', '-c', 'import sklearn; print(sklearn.__version__)'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            version = result.stdout.strip().split('\n')[-1]
            print(f"PASS: Component 4 — 'import sklearn' succeeded, version: {version} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — 'import sklearn' failed: {result.stderr.strip()}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

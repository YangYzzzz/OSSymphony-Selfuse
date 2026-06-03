"""
Reward Script: Clone requests library, create venv, install editable, verify import
Task ID: osworld_multi_apps_vscode_env_setup_002
Domain: os (terminal/dev-environment setup)
Scoring:
  Component 1 (0.3): /home/user/requests exists as a git repo with psf/requests origin
  Component 2 (0.3): Virtual environment exists at /home/user/requests/venv
  Component 3 (0.4): requests is installed in editable mode AND can be imported via venv python
"""

import os
import sys

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_env_setup_002'

REQUESTS_DIR = os.path.join(WORKDIR, 'requests')
VENV_DIR = os.path.join(REQUESTS_DIR, 'venv')
VENV_PYTHON = os.path.join(VENV_DIR, 'bin', 'python')
VENV_SITE_PACKAGES_BASE = os.path.join(VENV_DIR, 'lib')


def find_site_packages():
    """Find site-packages directory inside the venv."""
    if not os.path.isdir(VENV_SITE_PACKAGES_BASE):
        return None
    for entry in os.listdir(VENV_SITE_PACKAGES_BASE):
        candidate = os.path.join(VENV_SITE_PACKAGES_BASE, entry, 'site-packages')
        if os.path.isdir(candidate):
            return candidate
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: /home/user/requests exists as a git repository with
    #              origin pointing to https://github.com/psf/requests (0.3 points)
    # This FAILS on initial (no requests dir) and PASSES on golden (cloned repo)
    try:
        git_config_path = os.path.join(REQUESTS_DIR, '.git', 'config')
        if not os.path.isdir(REQUESTS_DIR):
            print(f"FAIL: Component 1 — /home/user/requests directory does not exist")
        elif not os.path.isdir(os.path.join(REQUESTS_DIR, '.git')):
            print(f"FAIL: Component 1 — /home/user/requests is not a git repository")
        elif not os.path.isfile(git_config_path):
            print(f"FAIL: Component 1 — .git/config not found")
        else:
            with open(git_config_path, 'r') as f:
                git_config = f.read()
            # Check that origin points to psf/requests on github
            if 'github.com/psf/requests' in git_config or 'github.com:psf/requests' in git_config:
                print(f"PASS: Component 1 — git repo cloned with psf/requests origin (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — .git/config does not reference psf/requests. Content snippet: {git_config[:200]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Virtual environment exists at /home/user/requests/venv (0.3 points)
    # This FAILS on initial (no requests dir at all) and PASSES on golden (venv created)
    try:
        pyvenv_cfg = os.path.join(VENV_DIR, 'pyvenv.cfg')
        venv_python_exists = os.path.isfile(VENV_PYTHON)
        pyvenv_cfg_exists = os.path.isfile(pyvenv_cfg)

        venv_valid = (
            os.path.isdir(VENV_DIR)
            and venv_python_exists
            and pyvenv_cfg_exists
        )
        if not os.path.isdir(VENV_DIR):
            print(f"FAIL: Component 2 — venv directory not found at {VENV_DIR}")
        elif not venv_python_exists:
            print(f"FAIL: Component 2 — venv/bin/python not found at {VENV_PYTHON}")
        elif not pyvenv_cfg_exists:
            print(f"FAIL: Component 2 — pyvenv.cfg not found at {pyvenv_cfg}")
        if venv_valid:
            print(f"PASS: Component 2 — venv exists at {VENV_DIR} with python binary (0.3 pts)")
            total_score += 0.3
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: requests is installed in editable mode AND importable via venv python (0.4 points)
    # Editable install marker: __editable__.requests-*.pth file in site-packages
    # This FAILS on initial (no venv) and PASSES on golden (editable install done)
    try:
        site_packages = find_site_packages()
        if site_packages is None:
            print(f"FAIL: Component 3 — could not find site-packages in venv")
        else:
            # Check for editable install pth file
            editable_pth = None
            dist_info = None
            for fname in os.listdir(site_packages):
                if fname.startswith('__editable__.requests') and fname.endswith('.pth'):
                    editable_pth = fname
                if 'requests' in fname and fname.endswith('.dist-info'):
                    dist_info = fname

            if editable_pth is None:
                print(f"FAIL: Component 3 — no __editable__.requests*.pth found in site-packages ({site_packages})")
                print(f"       site-packages contents: {os.listdir(site_packages)}")
            else:
                # Verify the pth file points back into the repo's src directory
                pth_path = os.path.join(site_packages, editable_pth)
                with open(pth_path, 'r') as f:
                    pth_content = f.read().strip()

                # pth should reference the src dir inside the project
                if REQUESTS_DIR in pth_content or 'requests' in pth_content.lower():
                    # Also verify the venv python can actually import requests
                    # We do this by checking that requests source files exist at the pth path
                    src_path = pth_content.strip()
                    requests_pkg_path = os.path.join(src_path, 'requests', '__init__.py')
                    if os.path.isfile(requests_pkg_path):
                        print(f"PASS: Component 3 — editable install found ({editable_pth}), "
                              f"source at {src_path}, import should succeed (0.4 pts)")
                        total_score += 0.4
                    else:
                        # pth might point directly to the requests package
                        alt_init = os.path.join(src_path, '__init__.py')
                        if os.path.isfile(alt_init):
                            print(f"PASS: Component 3 — editable install found ({editable_pth}), "
                                  f"source at {src_path} (0.4 pts)")
                            total_score += 0.4
                        else:
                            print(f"FAIL: Component 3 — editable pth found but source path "
                                  f"'{src_path}' does not contain requests package")
                else:
                    print(f"FAIL: Component 3 — editable pth file does not reference requests repo. "
                          f"Content: {pth_content}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()

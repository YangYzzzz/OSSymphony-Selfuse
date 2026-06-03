"""
Reward Script: Set up numpy project environment
Task ID: osworld_multi_apps_vscode_env_setup_003
Domain: vscode / multi_apps (OS-level environment setup)
Scoring:
  Component 1: /home/user/numpy exists as a git repo cloned from https://github.com/numpy/numpy (0.5 pts)
  Component 2: Build dependencies cython, meson-python, build are installed/importable (0.5 pts)
  Total: 1.0

Note: 'import numpy' is a precondition (present in both initial and golden envs) and is NOT scored.
It is used only as a sanity gate if needed.
"""

import os
import importlib.util

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_env_setup_003'
NUMPY_REPO_DIR = os.path.join(WORKDIR, 'numpy')
EXPECTED_REMOTE = 'https://github.com/numpy/numpy'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: /home/user/numpy exists as a valid git repository
    # cloned from https://github.com/numpy/numpy (0.5 points)
    # This FAILS on initial_env (no /home/user/numpy) and PASSES on golden_env
    try:
        # Check directory exists
        if not os.path.isdir(NUMPY_REPO_DIR):
            print(f"FAIL: Component 1 — /home/user/numpy directory does not exist")
        else:
            # Check it is a git repository
            git_dir = os.path.join(NUMPY_REPO_DIR, '.git')
            if not os.path.isdir(git_dir):
                print(f"FAIL: Component 1 — /home/user/numpy exists but is not a git repository (no .git dir)")
            else:
                # Check remote URL points to numpy/numpy
                git_config_path = os.path.join(git_dir, 'config')
                remote_ok = False
                try:
                    with open(git_config_path, 'r') as f:
                        config_content = f.read()
                    # Accept either full URL or github.com/numpy/numpy substring
                    remote_ok = (EXPECTED_REMOTE in config_content or
                                 'github.com/numpy/numpy' in config_content)
                except Exception as read_err:
                    print(f"WARN: Could not read git config: {read_err}")

                if remote_ok:
                    # Also verify some key numpy repo files exist (basic integrity)
                    key_files = ['README.md', 'meson.build', 'pyproject.toml']
                    found_files = [f for f in key_files if os.path.isfile(os.path.join(NUMPY_REPO_DIR, f))]
                    if len(found_files) >= 2:
                        print(f"PASS: Component 1 — /home/user/numpy is a valid git repo cloned from {EXPECTED_REMOTE} "
                              f"(found key files: {found_files}) (0.5 pts)")
                        total_score += 0.5
                    else:
                        print(f"FAIL: Component 1 — git repo found but missing expected numpy files "
                              f"(found: {found_files}, expected at least 2 of {key_files})")
                else:
                    print(f"FAIL: Component 1 — /home/user/numpy is a git repo but remote does not point to "
                          f"{EXPECTED_REMOTE}. Check .git/config for actual remote URL.")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Build dependencies (cython, meson-python, build) are installed
    # This FAILS on initial_env (none installed) and PASSES on golden_env (all installed)
    # We check using importlib.util.find_spec which works without subprocess
    try:
        deps_status = {}

        # Check Cython
        cython_spec = importlib.util.find_spec('cython')
        deps_status['cython'] = cython_spec is not None

        # Check meson-python (imports as 'mesonpy')
        mesonpy_spec = importlib.util.find_spec('mesonpy')
        deps_status['meson-python (mesonpy)'] = mesonpy_spec is not None

        # Check build
        build_spec = importlib.util.find_spec('build')
        deps_status['build'] = build_spec is not None

        installed = [name for name, present in deps_status.items() if present]
        missing = [name for name, present in deps_status.items() if not present]

        if len(missing) == 0:
            print(f"PASS: Component 2 — All 3 build dependencies installed: "
                  f"cython, meson-python, build (0.5 pts)")
            total_score += 0.5
        elif len(installed) > 0:
            # Partial credit not awarded here — all 3 must be present
            print(f"FAIL: Component 2 — Only {len(installed)}/3 build dependencies installed. "
                  f"Installed: {installed}. Missing: {missing}")
        else:
            print(f"FAIL: Component 2 — None of the required build dependencies are installed: "
                  f"cython, meson-python, build")

    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

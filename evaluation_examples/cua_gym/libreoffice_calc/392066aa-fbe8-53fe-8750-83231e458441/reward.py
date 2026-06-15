"""
Reward Script: Clone PyTorch from source, install requirements.txt dependencies, verify 'import torch' succeeds.
Task ID: osworld_multi_apps_vscode_env_setup_013
Domain: os / multi_apps_vscode_env_setup
Scoring:
  - Component 1: /home/user/pytorch exists and is a git repository (0.3 pts)
  - Component 2: Git remote origin matches https://github.com/pytorch/pytorch (0.2 pts)
  - Component 3: requirements.txt dependencies installed (filelock, fsspec, networkx) (0.2 pts)
  - Component 4: 'import torch' succeeds without error (0.3 pts)
  Total: 1.0
"""

import os
import sys

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_env_setup_013'
PYTORCH_DIR = '/home/user/pytorch'

def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: /home/user/pytorch exists and is a git repository (0.3 points)
    # This FAILS on initial_env (no pytorch dir) and PASSES on golden_env (cloned)
    try:
        git_dir = os.path.join(PYTORCH_DIR, '.git')
        if os.path.isdir(PYTORCH_DIR) and os.path.isdir(git_dir):
            print(f"PASS: Component 1 — /home/user/pytorch exists and is a git repository (0.3 pts)")
            total_score += 0.3
        else:
            if not os.path.isdir(PYTORCH_DIR):
                print(f"FAIL: Component 1 — /home/user/pytorch directory does not exist")
            else:
                print(f"FAIL: Component 1 — /home/user/pytorch exists but is not a git repository (no .git dir)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Git remote origin matches https://github.com/pytorch/pytorch (0.2 points)
    # This FAILS on initial_env (no pytorch dir) and PASSES on golden_env (correct remote)
    try:
        git_config_path = os.path.join(PYTORCH_DIR, '.git', 'config')
        if not os.path.isfile(git_config_path):
            print(f"FAIL: Component 2 — .git/config not found, cannot verify remote")
        else:
            with open(git_config_path, 'r') as f:
                git_config = f.read()
            expected_remote = 'https://github.com/pytorch/pytorch'
            if expected_remote in git_config:
                print(f"PASS: Component 2 — Git remote origin matches {expected_remote} (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — Expected remote {expected_remote} not found in .git/config")
                print(f"  git config content snippet: {git_config[:300]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Key requirements.txt dependencies installed (0.2 points)
    # Check packages that are unique to the golden_env (not present in initial_env):
    # filelock, fsspec, networkx — these were absent from initial_env pip list
    # This FAILS on initial_env and PASSES on golden_env
    try:
        import importlib.util
        # filelock is NOT in initial_env, IS in golden_env
        # fsspec is NOT in initial_env, IS in golden_env
        # networkx is NOT in initial_env, IS in golden_env
        required_packages = ['filelock', 'fsspec', 'networkx']
        missing = []
        for pkg in required_packages:
            spec = importlib.util.find_spec(pkg)
            if spec is None:
                missing.append(pkg)
        if not missing:
            print(f"PASS: Component 3 — Required packages installed: {required_packages} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Missing packages from requirements.txt: {missing}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 'import torch' succeeds without error (0.3 points)
    # This FAILS on initial_env (torch not installed) and PASSES on golden_env (torch installed)
    try:
        import importlib.util
        torch_spec = importlib.util.find_spec('torch')
        if torch_spec is not None:
            # Actually try importing to confirm it works
            import torch
            print(f"PASS: Component 4 — 'import torch' succeeded (version: {torch.__version__}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 4 — 'torch' module not found; 'import torch' would fail")
    except ImportError as e:
        print(f"FAIL: Component 4 — 'import torch' failed with ImportError: {e}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

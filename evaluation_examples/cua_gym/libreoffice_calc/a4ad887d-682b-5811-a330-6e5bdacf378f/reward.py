"""
Reward Script: Clone huggingface/transformers, install editable with torch, confirm pipeline import
Task ID: osworld_multi_apps_vscode_env_setup_004
Domain: os (git + pip + python)
Scoring:
  Component 1 (0.35): /home/user/transformers exists as a git clone of huggingface/transformers
  Component 2 (0.35): transformers is installed in editable mode from /home/user/transformers
  Component 3 (0.15): torch is installed (dist-info present in user site-packages)
  Component 4 (0.15): 'from transformers import pipeline' succeeds (pipeline is importable)
"""

import os
import json
import glob

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_env_setup_004'

# Expected paths
TRANSFORMERS_CLONE_PATH = '/home/user/transformers'
TRANSFORMERS_GIT_CONFIG = '/home/user/transformers/.git/config'
EXPECTED_REMOTE_URL = 'https://github.com/huggingface/transformers'
USER_SITE_PACKAGES = '/home/user/.local/lib/python3.10/site-packages'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: /home/user/transformers exists as a git clone of huggingface/transformers (0.35 points)
    # Verified by checking directory existence + reading .git/config for the correct remote URL.
    # This FAILS on initial_env (no transformers dir) and PASSES on golden_env.
    try:
        clone_exists = os.path.isdir(TRANSFORMERS_CLONE_PATH)
        git_dir_exists = os.path.isdir(os.path.join(TRANSFORMERS_CLONE_PATH, '.git'))
        if not clone_exists:
            print(f"FAIL: Component 1 — /home/user/transformers directory does not exist")
        elif not git_dir_exists:
            print(f"FAIL: Component 1 — /home/user/transformers is not a git repository (no .git dir)")
        else:
            # Read .git/config to verify the remote URL
            with open(TRANSFORMERS_GIT_CONFIG, 'r') as f:
                git_config_content = f.read()
            if EXPECTED_REMOTE_URL in git_config_content:
                print(f"PASS: Component 1 — /home/user/transformers is a git clone of {EXPECTED_REMOTE_URL} (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 — .git/config does not reference {EXPECTED_REMOTE_URL}")
                print(f"  Actual .git/config content:\n{git_config_content}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: transformers is installed in editable mode from /home/user/transformers (0.35 points)
    # Verified by reading direct_url.json from the dist-info directory.
    # Editable install produces: {"dir_info": {"editable": true}, "url": "file:///home/user/transformers"}
    # This FAILS on initial_env (no dist-info) and PASSES on golden_env.
    try:
        dist_info_pattern = os.path.join(USER_SITE_PACKAGES, 'transformers-*.dist-info')
        dist_info_dirs = glob.glob(dist_info_pattern)
        if not dist_info_dirs:
            print(f"FAIL: Component 2 — No transformers dist-info found in {USER_SITE_PACKAGES}")
        else:
            dist_info_dir = dist_info_dirs[0]
            direct_url_path = os.path.join(dist_info_dir, 'direct_url.json')
            if not os.path.isfile(direct_url_path):
                print(f"FAIL: Component 2 — direct_url.json not found in {dist_info_dir} (not an editable install)")
            else:
                with open(direct_url_path, 'r') as f:
                    direct_url_data = json.load(f)
                is_editable = (
                    isinstance(direct_url_data.get('dir_info'), dict)
                    and direct_url_data['dir_info'].get('editable') is True
                )
                points_to_clone = direct_url_data.get('url', '') == f'file://{TRANSFORMERS_CLONE_PATH}'
                if is_editable and points_to_clone:
                    print(f"PASS: Component 2 — transformers installed in editable mode from {TRANSFORMERS_CLONE_PATH} (0.35 pts)")
                    total_score += 0.35
                elif is_editable:
                    print(f"FAIL: Component 2 — editable install found but does NOT point to {TRANSFORMERS_CLONE_PATH}")
                    print(f"  Actual url: {direct_url_data.get('url', 'N/A')}")
                else:
                    print(f"FAIL: Component 2 — transformers dist-info found but NOT installed in editable mode")
                    print(f"  direct_url.json content: {direct_url_data}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: torch is installed (dist-info present in user site-packages) (0.15 points)
    # Verified by checking for torch*.dist-info directory in site-packages.
    # This FAILS on initial_env (no torch) and PASSES on golden_env.
    try:
        torch_dist_info_pattern = os.path.join(USER_SITE_PACKAGES, 'torch-*.dist-info')
        torch_dist_info_dirs = glob.glob(torch_dist_info_pattern)
        if torch_dist_info_dirs:
            torch_dist_info = os.path.basename(torch_dist_info_dirs[0])
            print(f"PASS: Component 3 — torch is installed ({torch_dist_info}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — torch dist-info not found in {USER_SITE_PACKAGES}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 'from transformers import pipeline' succeeds (0.15 points)
    # Verified by directly importing transformers and checking that pipeline is accessible.
    # Since this reward script runs ON the VM, we can directly import the module.
    # This FAILS on initial_env (ModuleNotFoundError) and PASSES on golden_env.
    try:
        import importlib
        # Attempt to import the transformers package
        transformers_mod = importlib.import_module('transformers')
        # Check that 'pipeline' is accessible from the module
        if hasattr(transformers_mod, 'pipeline') and callable(transformers_mod.pipeline):
            print(f"PASS: Component 4 — 'from transformers import pipeline' succeeds; pipeline is callable (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — transformers module imported but 'pipeline' is not a callable attribute")
    except ImportError as e:
        print(f"FAIL: Component 4 — ImportError when importing transformers: {e}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()

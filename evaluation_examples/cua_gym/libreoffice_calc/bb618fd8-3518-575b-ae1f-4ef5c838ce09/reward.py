"""
Reward Script: Edit .pre-commit-config.yaml to add black hook and set default_language_version
Task ID: osworld_multi_apps_vscode_config_edit_012
Domain: vs-code / os (YAML config editing)
Scoring:
  Component 1: black repo block added to repos list (0.4 pts)
  Component 2: black repo has correct rev (24.3.0) and hook id (black) (0.3 pts)
  Component 3: default_language_version.python set to python3.12 (0.3 pts)
  Total: 1.0
"""

import os
import yaml

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_config_edit_012'
YAML_PATH = '/home/user/Code/myrepo/.pre-commit-config.yaml'


def verify_task(yaml_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Add 'black' hook entry and set default_language_version.python = python3.12
    in .pre-commit-config.yaml

    Expected golden state:
      default_language_version:
        python: python3.12
      repos:
        - repo: https://github.com/PyCQA/flake8
          ...
        - repo: https://github.com/psf/black
          rev: 24.3.0
          hooks:
            - id: black
    """
    total_score = 0.0

    # Load and parse the YAML file
    try:
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        if data is None:
            print("CRITICAL: YAML file is empty or invalid")
            print("REWARD: 0.0")
            return 0.0
    except FileNotFoundError:
        print(f"CRITICAL: Cannot find file {yaml_path}")
        print("REWARD: 0.0")
        return 0.0
    except yaml.YAMLError as e:
        print(f"CRITICAL: YAML parse error in {yaml_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract repos list (precondition gate)
    repos = data.get('repos', [])
    if not isinstance(repos, list):
        print("CRITICAL: 'repos' is not a list — malformed YAML structure")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: black repo block is present in repos (0.4 pts)
    # This FAILS on initial_env (no black repo) and PASSES on golden_env
    try:
        black_repo = None
        for repo_entry in repos:
            if isinstance(repo_entry, dict) and repo_entry.get('repo') == 'https://github.com/psf/black':
                black_repo = repo_entry
                break

        if black_repo is not None:
            print(f"PASS: Component 1 — black repo block found (repo: https://github.com/psf/black) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — black repo block not found in repos list. Expected entry with repo: https://github.com/psf/black")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: black repo has correct rev (24.3.0) and hook id (black) (0.3 pts)
    # This FAILS on initial_env (black_repo is None) and PASSES on golden_env
    try:
        if black_repo is not None:
            rev_correct = black_repo.get('rev') == '24.3.0'
            hooks = black_repo.get('hooks', [])
            hook_ids = [h.get('id') for h in hooks if isinstance(h, dict)]
            hooks_correct = 'black' in hook_ids

            if rev_correct and hooks_correct:
                print(f"PASS: Component 2 — black repo has rev=24.3.0 and hooks=[{{id: black}}] (0.3 pts)")
                total_score += 0.3
            else:
                if not rev_correct:
                    print(f"FAIL: Component 2 — black repo rev is '{black_repo.get('rev')}', expected '24.3.0'")
                if not hooks_correct:
                    print(f"FAIL: Component 2 — black repo hooks do not contain id='black', found: {hook_ids}")
        else:
            print(f"FAIL: Component 2 — skipped (black repo not found in repos)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: default_language_version.python is set to python3.12 (0.3 pts)
    # This FAILS on initial_env (key not present) and PASSES on golden_env
    try:
        dlv = data.get('default_language_version')
        if isinstance(dlv, dict):
            python_version = dlv.get('python')
            if python_version == 'python3.12':
                print(f"PASS: Component 3 — default_language_version.python = python3.12 (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — default_language_version.python = '{python_version}', expected 'python3.12'")
        else:
            print(f"FAIL: Component 3 — 'default_language_version' key missing or not a dict (found: {dlv})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: verify canonical task artifact on this VM
if not os.path.exists(YAML_PATH):
    print(f"File not found: {YAML_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(YAML_PATH)

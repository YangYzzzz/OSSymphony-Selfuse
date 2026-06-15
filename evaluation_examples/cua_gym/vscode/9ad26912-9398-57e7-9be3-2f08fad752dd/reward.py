"""
Reward Script: Create .devcontainer/devcontainer.json with Python 3.11 image
Task ID: vscode_rrt_011
Domain: vscode
Scoring:
  Component 1 — devcontainer.json is valid JSON in .devcontainer/ (0.2 pts)
  Component 2 — image field matches mcr.microsoft.com/devcontainers/python:3.11 (0.4 pts)
  Component 3 — name field is 'Python 3.11 Dev' (0.4 pts)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_011'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'ml-pipeline')
DEVCONTAINER_PATH = os.path.join(PROJECT_DIR, '.devcontainer', 'devcontainer.json')

EXPECTED_IMAGE = 'mcr.microsoft.com/devcontainers/python:3.11'
EXPECTED_NAME = 'Python 3.11 Dev'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: project directory exists
    if not os.path.isdir(PROJECT_DIR):
        print(f"CRITICAL: Project directory not found: {PROJECT_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: .devcontainer/devcontainer.json exists and is valid JSON (0.2 pts)
    # This file does NOT exist in initial_env, so this checks a task-introduced change.
    config = None
    try:
        if not os.path.isfile(DEVCONTAINER_PATH):
            print(f"FAIL: Component 1 — devcontainer.json not found at {DEVCONTAINER_PATH}")
        else:
            with open(DEVCONTAINER_PATH, 'r') as f:
                config = json.load(f)
            if isinstance(config, dict):
                print(f"PASS: Component 1 — devcontainer.json exists and is valid JSON (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 — devcontainer.json is not a JSON object, got {type(config).__name__}")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 1 — devcontainer.json is not valid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If we couldn't load the config, remaining checks will fail
    if config is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: image field matches expected value (0.4 pts)
    try:
        actual_image = config.get('image', None)
        if actual_image is not None and str(actual_image).strip() == EXPECTED_IMAGE:
            print(f"PASS: Component 2 — image is '{actual_image}' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — expected image '{EXPECTED_IMAGE}', found '{actual_image}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: name field matches expected value (0.4 pts)
    try:
        actual_name = config.get('name', None)
        if actual_name is not None and str(actual_name).strip() == EXPECTED_NAME:
            print(f"PASS: Component 3 — name is '{actual_name}' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 3 — expected name '{EXPECTED_NAME}', found '{actual_name}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()

"""
Reward Script: Configure Dev Container with multiple features
Task ID: vscode_rrt_030
Domain: vs_code
Scoring:
  - Component 1: name field is "CI Tools Dev" (0.15 pts)
  - Component 2: image field is correct Ubuntu base image (0.25 pts)
  - Component 3: features contains git:1 (0.2 pts)
  - Component 4: features contains docker-in-docker:2 (0.2 pts)
  - Component 5: features contains github-cli:1 (0.2 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_030'
DEVCONTAINER_PATH = os.path.join(WORKDIR, 'projects', 'ci-tools', '.devcontainer', 'devcontainer.json')

# Expected feature keys (prefix-match to allow version flexibility)
EXPECTED_FEATURES = {
    'ghcr.io/devcontainers/features/git:1': 0.2,
    'ghcr.io/devcontainers/features/docker-in-docker:2': 0.2,
    'ghcr.io/devcontainers/features/github-cli:1': 0.2,
}


def load_jsonc(path):
    """Load a JSON or JSONC file (strip // comments)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: devcontainer.json must exist and be valid JSON
    if not os.path.exists(DEVCONTAINER_PATH):
        print(f"CRITICAL: devcontainer.json not found at {DEVCONTAINER_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        config = load_jsonc(DEVCONTAINER_PATH)
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse devcontainer.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not isinstance(config, dict):
        print(f"CRITICAL: devcontainer.json root is not a JSON object")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: name field is "CI Tools Dev" (0.15 points)
    try:
        name_val = config.get('name', None)
        if isinstance(name_val, str) and name_val.strip() == 'CI Tools Dev':
            print(f"PASS: Component 1 — name is '{name_val}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — expected name 'CI Tools Dev', found: {name_val!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: image field is correct Ubuntu base image (0.25 points)
    try:
        image_val = config.get('image', None)
        expected_image = 'mcr.microsoft.com/devcontainers/base:ubuntu'
        if isinstance(image_val, str) and image_val.strip() == expected_image:
            print(f"PASS: Component 2 — image is '{image_val}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — expected image '{expected_image}', found: {image_val!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Components 3-5: features contain the required devcontainer features
    try:
        features = config.get('features', {})
        if not isinstance(features, dict):
            print(f"FAIL: 'features' field is not a dict, found: {type(features).__name__}")
        else:
            comp_num = 3
            for feature_key, points in EXPECTED_FEATURES.items():
                if feature_key in features:
                    print(f"PASS: Component {comp_num} — feature '{feature_key}' present ({points} pts)")
                    total_score += points
                else:
                    print(f"FAIL: Component {comp_num} — feature '{feature_key}' not found in features")
                comp_num += 1
    except Exception as e:
        print(f"ERROR: Features check — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

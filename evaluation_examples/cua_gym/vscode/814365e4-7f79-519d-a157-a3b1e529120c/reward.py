"""
Reward Script: Configure a devcontainer for a Python project
Task ID: vscode_gf3_034
Domain: vscode
Scoring:
  - Component 1: devcontainer.json exists and is valid JSON (0.1 pts)
  - Component 2: name is "Python API Dev" (0.2 pts)
  - Component 3: image is "mcr.microsoft.com/devcontainers/python:3.11" (0.2 pts)
  - Component 4: all 4 required extensions present (0.3 pts)
  - Component 5: postCreateCommand is "pip install -r requirements.txt" (0.2 pts)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_034'
DEVCONTAINER_PATH = os.path.join(WORKDIR, 'projects', 'python-api', '.devcontainer', 'devcontainer.json')

REQUIRED_EXTENSIONS = [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-toolsai.jupyter",
    "mtxr.sqltools",
]


def verify_task():
    """
    Verify devcontainer.json creation with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: devcontainer.json exists and is valid JSON (0.1 points)
    try:
        if not os.path.exists(DEVCONTAINER_PATH):
            print(f"FAIL: Component 1 — devcontainer.json not found at {DEVCONTAINER_PATH}")
            print("REWARD: 0.0")
            return 0.0

        with open(DEVCONTAINER_PATH, 'r') as f:
            config = json.load(f)

        if isinstance(config, dict):
            print(f"PASS: Component 1 — devcontainer.json exists and is valid JSON (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — devcontainer.json is not a JSON object")
            print("REWARD: 0.0")
            return 0.0
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 1 — devcontainer.json is not valid JSON: {e}")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: name is "Python API Dev" (0.2 points)
    try:
        name = config.get("name", "")
        if name == "Python API Dev":
            print(f"PASS: Component 2 — name is 'Python API Dev' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — expected name 'Python API Dev', found '{name}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: image is correct Python 3.11 devcontainer image (0.2 points)
    try:
        image = config.get("image", "")
        expected_image = "mcr.microsoft.com/devcontainers/python:3.11"
        if image == expected_image:
            print(f"PASS: Component 3 — image is '{expected_image}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — expected image '{expected_image}', found '{image}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: all 4 required VSCode extensions are present (0.3 points)
    try:
        # Extensions can be at customizations.vscode.extensions or at top-level extensions
        extensions = []
        customizations = config.get("customizations", {})
        if isinstance(customizations, dict):
            vscode_config = customizations.get("vscode", {})
            if isinstance(vscode_config, dict):
                extensions = vscode_config.get("extensions", [])

        # Also check top-level extensions as fallback
        if not extensions:
            extensions = config.get("extensions", [])

        if not isinstance(extensions, list):
            extensions = []

        # Normalize to lowercase for comparison
        extensions_lower = [ext.lower() for ext in extensions]
        found_count = 0
        for req_ext in REQUIRED_EXTENSIONS:
            if req_ext.lower() in extensions_lower:
                found_count += 1
                print(f"  Found extension: {req_ext}")
            else:
                print(f"  Missing extension: {req_ext}")

        if found_count == len(REQUIRED_EXTENSIONS):
            print(f"PASS: Component 4 — all {len(REQUIRED_EXTENSIONS)} extensions present (0.3 pts)")
            total_score += 0.3
        elif found_count > 0:
            # Partial credit: proportional to how many extensions are present
            partial = round(0.3 * (found_count / len(REQUIRED_EXTENSIONS)), 2)
            print(f"PARTIAL: Component 4 — {found_count}/{len(REQUIRED_EXTENSIONS)} extensions present ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — no required extensions found in {extensions}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: postCreateCommand is "pip install -r requirements.txt" (0.2 points)
    try:
        post_cmd = config.get("postCreateCommand", "")
        expected_cmd = "pip install -r requirements.txt"
        if isinstance(post_cmd, str) and post_cmd.strip() == expected_cmd:
            print(f"PASS: Component 5 — postCreateCommand is '{expected_cmd}' (0.2 pts)")
            total_score += 0.2
        elif isinstance(post_cmd, list):
            # Some devcontainer configs use list form
            joined = " ".join(post_cmd).strip()
            if joined == expected_cmd:
                print(f"PASS: Component 5 — postCreateCommand (list form) matches (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 5 — expected postCreateCommand '{expected_cmd}', found list: {post_cmd}")
        else:
            print(f"FAIL: Component 5 — expected postCreateCommand '{expected_cmd}', found '{post_cmd}'")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()

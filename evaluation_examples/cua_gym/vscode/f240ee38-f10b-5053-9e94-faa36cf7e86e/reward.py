"""
Reward Script: Configure Dev Container with Dockerfile
Task ID: vscode_rrt_019
Domain: vscode
Scoring:
  Component 1 (0.2): .devcontainer/Dockerfile exists
  Component 2 (0.2): Dockerfile uses FROM python:3.11
  Component 3 (0.2): Dockerfile installs requests via pip
  Component 4 (0.2): devcontainer.json has build.dockerfile = "Dockerfile"
  Component 5 (0.2): devcontainer.json name is "Python Scraper Dev"
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_019'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'scraper')
DEVCONTAINER_DIR = os.path.join(PROJECT_DIR, '.devcontainer')
DOCKERFILE_PATH = os.path.join(DEVCONTAINER_DIR, 'Dockerfile')
DEVCONTAINER_JSON_PATH = os.path.join(DEVCONTAINER_DIR, 'devcontainer.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: .devcontainer/Dockerfile exists (0.2 points)
    # This FAILS on initial (no .devcontainer dir) -> PASSES on golden
    try:
        if os.path.isfile(DOCKERFILE_PATH):
            print(f"PASS: Component 1 — Dockerfile exists at {DOCKERFILE_PATH} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Dockerfile not found at {DOCKERFILE_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Read Dockerfile content for subsequent checks
    dockerfile_content = ""
    try:
        if os.path.isfile(DOCKERFILE_PATH):
            with open(DOCKERFILE_PATH, "r") as f:
                dockerfile_content = f.read()
    except Exception as e:
        print(f"WARN: Could not read Dockerfile: {e}")

    # Component 2: Dockerfile contains FROM python:3.11 (0.2 points)
    try:
        # Match FROM python:3.11 (possibly with -slim or other variants, but base must be python:3.11)
        if re.search(r'FROM\s+python:3\.11', dockerfile_content, re.IGNORECASE):
            print(f"PASS: Component 2 — Dockerfile has FROM python:3.11 (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — Dockerfile missing FROM python:3.11. Content: {dockerfile_content[:200]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Dockerfile installs requests library via pip (0.2 points)
    try:
        # Match RUN pip install ... requests (requests must appear in a pip install line)
        if re.search(r'RUN\s+.*pip\s+install\s+.*requests', dockerfile_content, re.IGNORECASE):
            print(f"PASS: Component 3 — Dockerfile installs requests via pip (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Dockerfile missing pip install requests. Content: {dockerfile_content[:200]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Read devcontainer.json for subsequent checks
    devcontainer_config = None
    try:
        if os.path.isfile(DEVCONTAINER_JSON_PATH):
            with open(DEVCONTAINER_JSON_PATH, "r") as f:
                content = f.read()
            # Strip JSONC comments if present
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            devcontainer_config = json.loads(content_clean)
    except Exception as e:
        print(f"WARN: Could not parse devcontainer.json: {e}")

    # Component 4: devcontainer.json has build.dockerfile referencing "Dockerfile" (0.2 points)
    try:
        if devcontainer_config is not None:
            build_section = devcontainer_config.get("build", {})
            dockerfile_ref = build_section.get("dockerfile", "")
            if dockerfile_ref.lower() == "dockerfile":
                print(f"PASS: Component 4 — devcontainer.json build.dockerfile = '{dockerfile_ref}' (0.2 pts)")
                total_score += 0.2
            else:
                # Also check for top-level "dockerFile" key (alternative schema)
                alt_ref = devcontainer_config.get("dockerFile", "")
                if alt_ref.lower() == "dockerfile":
                    print(f"PASS: Component 4 — devcontainer.json dockerFile = '{alt_ref}' (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 4 — build.dockerfile is '{dockerfile_ref}', expected 'Dockerfile'")
        else:
            print(f"FAIL: Component 4 — devcontainer.json not found or invalid JSON")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: devcontainer.json name is "Python Scraper Dev" (0.2 points)
    try:
        if devcontainer_config is not None:
            name_val = devcontainer_config.get("name", "")
            if name_val == "Python Scraper Dev":
                print(f"PASS: Component 5 — devcontainer.json name = '{name_val}' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 5 — devcontainer.json name is '{name_val}', expected 'Python Scraper Dev'")
        else:
            print(f"FAIL: Component 5 — devcontainer.json not found or invalid JSON")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

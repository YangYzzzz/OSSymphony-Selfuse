"""
Reward Script: Set up file associations in VSCode
Task ID: vscode_we_027
Domain: vscode
Scoring:
  Component 1: files.associations key exists with at least one entry (0.1 pts)
  Component 2: *.env -> shellscript (0.3 pts)
  Component 3: *.mdx -> markdown (0.3 pts)
  Component 4: *.prisma -> prisma (0.3 pts)
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")
TASK_ID = "vscode_we_027"


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip single-line comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("CRITICAL: settings.json not found or invalid")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: files.associations key exists with content (0.1 points)
    try:
        associations = settings.get("files.associations")
        if isinstance(associations, dict) and len(associations) > 0:
            print(f"PASS: Component 1 — files.associations exists with {len(associations)} entries (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — files.associations missing or empty, found: {associations}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: *.env -> shellscript (0.3 points)
    try:
        associations = settings.get("files.associations", {})
        env_val = associations.get("*.env")
        if env_val is not None and str(env_val).lower() == "shellscript":
            print(f"PASS: Component 2 — *.env mapped to '{env_val}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — expected *.env -> 'shellscript', found: {env_val}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: *.mdx -> markdown (0.3 points)
    try:
        associations = settings.get("files.associations", {})
        mdx_val = associations.get("*.mdx")
        if mdx_val is not None and str(mdx_val).lower() == "markdown":
            print(f"PASS: Component 3 — *.mdx mapped to '{mdx_val}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — expected *.mdx -> 'markdown', found: {mdx_val}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: *.prisma -> prisma (0.3 points)
    try:
        associations = settings.get("files.associations", {})
        prisma_val = associations.get("*.prisma")
        if prisma_val is not None and str(prisma_val).lower() == "prisma":
            print(f"PASS: Component 4 — *.prisma mapped to '{prisma_val}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 4 — expected *.prisma -> 'prisma', found: {prisma_val}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

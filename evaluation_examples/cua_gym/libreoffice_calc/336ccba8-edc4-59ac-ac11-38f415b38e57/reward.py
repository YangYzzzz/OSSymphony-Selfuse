"""
Reward Script: Configure VSCode to associate .env files with 'properties' language mode
Task ID: vscode_lp_020
Domain: vscode (settings.json verification)
Scoring:
  - Component 1 (0.5): files.associations key exists with .env mapping
  - Component 2 (0.3): .env maps specifically to "properties"
  - Component 3 (0.2): No extra associations that would conflict
"""

import os
import json
import re

HOME = '/home/user'
SETTINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'settings.json')


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify that VSCode settings.json contains files.associations mapping
    .env to properties language mode.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("CRITICAL: settings.json not found or invalid")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: files.associations key exists and contains .env entry (0.5 points)
    # This checks the structural change: the associations key with .env must be present
    try:
        associations = settings.get("files.associations", {})
        if isinstance(associations, dict) and ".env" in associations:
            print(f"PASS: Component 1 — files.associations contains .env entry (value: {associations['.env']}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — files.associations missing or no .env key. Current associations: {associations}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: .env maps to exactly "properties" (0.3 points)
    # This verifies the correct value — the language mode must be "properties"
    try:
        associations = settings.get("files.associations", {})
        if isinstance(associations, dict):
            env_value = associations.get(".env", None)
            if env_value is not None and str(env_value).strip().lower() == "properties":
                print(f"PASS: Component 2 — .env maps to 'properties' (exact: '{env_value}') (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — .env maps to '{env_value}', expected 'properties'")
        else:
            print(f"FAIL: Component 2 — files.associations is not a dict")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The setting is properly structured as a top-level key (0.2 points)
    # Verify files.associations is at the correct JSON nesting level and the value
    # is exactly "properties" (case-sensitive, as VSCode language IDs are case-sensitive)
    try:
        associations = settings.get("files.associations", {})
        if isinstance(associations, dict):
            env_value = associations.get(".env", None)
            if env_value == "properties":
                print(f"PASS: Component 3 — Exact case-sensitive match: .env -> 'properties' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Case-sensitive check failed. Value: '{env_value}', expected exactly 'properties'")
        else:
            print(f"FAIL: Component 3 — files.associations is not a dict")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

"""
Reward Script: Configure workspace Python formatters (Black for .py, autopep8 for migrations)
Task ID: vscode_py_077
Domain: vscode
Scoring:
  - Component 1 (0.4): [python] language-specific setting uses Black formatter
  - Component 2 (0.4): [python:**/migrations/*.py] uses autopep8 formatter
  - Component 3 (0.2): Both configs coexist correctly in same settings file
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_077'

# Possible locations for workspace settings
WORKSPACE_SETTINGS = os.path.join(WORKDIR, TASK_ID, '.vscode', 'settings.json')
GLOBAL_SETTINGS = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments), stripping // comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (// ...) but not inside strings
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip trailing commas before } or ]
    content = re.sub(r',\s*([}\]])', r'\1', content)
    return json.loads(content)


def find_settings():
    """Find and load workspace or global settings that contain python formatter config."""
    # Try workspace settings first (most likely location)
    for path in [WORKSPACE_SETTINGS, GLOBAL_SETTINGS]:
        if os.path.exists(path):
            try:
                data = load_jsonc(path)
                # Check if this file has any language-specific python settings
                if any(k.startswith('[python') for k in data):
                    return data, path
            except Exception:
                continue

    # If no file has python-specific settings, still return whatever we can find
    for path in [WORKSPACE_SETTINGS, GLOBAL_SETTINGS]:
        if os.path.exists(path):
            try:
                return load_jsonc(path), path
            except Exception:
                continue

    return None, None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings, settings_path = find_settings()
    if settings is None:
        print(f"CRITICAL: No settings.json found at {WORKSPACE_SETTINGS} or {GLOBAL_SETTINGS}")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Using settings from {settings_path}")

    # Component 1: [python] block has Black formatter (0.4 points)
    # This checks that regular Python files use Black as the default formatter.
    # In initial_env, there is NO [python] language-specific override, so this FAILS.
    try:
        python_block = settings.get("[python]", None)
        if python_block is not None and isinstance(python_block, dict):
            formatter = python_block.get("editor.defaultFormatter", "")
            if formatter == "ms-python.black-formatter":
                print(f"PASS: Component 1 — [python] uses Black formatter (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — [python] formatter is '{formatter}', expected 'ms-python.black-formatter'")
        else:
            print(f"FAIL: Component 1 — No [python] language-specific block found in settings")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Migration files use autopep8 formatter (0.4 points)
    # This checks that migration .py files get autopep8. In initial_env, there is
    # NO migration-specific override, so this FAILS.
    try:
        # Look for any key that targets migration files specifically
        migration_formatter = None
        migration_key = None
        for key in settings:
            # Accept various patterns that target migration files:
            # [python:**/migrations/*.py], [python:**/migrations/*.py], etc.
            if 'migration' in key.lower() and key.startswith('['):
                block = settings[key]
                if isinstance(block, dict):
                    migration_formatter = block.get("editor.defaultFormatter", "")
                    migration_key = key
                    break

        if migration_formatter is not None:
            if migration_formatter == "ms-python.autopep8":
                print(f"PASS: Component 2 — {migration_key} uses autopep8 formatter (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — {migration_key} formatter is '{migration_formatter}', expected 'ms-python.autopep8'")
        else:
            print(f"FAIL: Component 2 — No migration-specific formatter override found in settings")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Both formatter configs coexist in the same settings file (0.2 points)
    # This is a compound check: BOTH [python] Black AND migration autopep8 must be present.
    # Only awards points if both Component 1 and 2 individually passed.
    try:
        has_python_black = (
            isinstance(settings.get("[python]"), dict)
            and settings["[python]"].get("editor.defaultFormatter") == "ms-python.black-formatter"
        )
        has_migration_autopep8 = any(
            'migration' in k.lower() and k.startswith('[')
            and isinstance(settings[k], dict)
            and settings[k].get("editor.defaultFormatter") == "ms-python.autopep8"
            for k in settings
        )
        if has_python_black and has_migration_autopep8:
            print(f"PASS: Component 3 — Both formatter configs coexist correctly (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Missing one or both formatter configs (python_black={has_python_black}, migration_autopep8={has_migration_autopep8})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()

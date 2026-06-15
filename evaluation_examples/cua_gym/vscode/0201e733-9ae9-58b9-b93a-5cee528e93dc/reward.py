"""
Reward Script: Fix Prettier config resolution in VSCode
Task ID: vscode_fix_053
Domain: vscode
Scoring:
  Component 1 (0.6): prettier.configPath no longer points to non-existent path
  Component 2 (0.4): Prettier can actually resolve a valid .prettierrc with singleQuote: true
"""

import os
import json
import re

HOME = '/home/user'
SETTINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'settings.json')
PRETTIERRC_PATH = os.path.join(HOME, 'monorepo', '.prettierrc')
TASK_ID = 'vscode_fix_053'


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
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify that Prettier config resolution is fixed.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load settings
    settings = load_settings()
    if settings is None:
        print("CRITICAL: settings.json not found or invalid")
        print("REWARD: 0.0")
        return 0.0

    config_path_value = settings.get('prettier.configPath', None)

    # Component 1: prettier.configPath no longer points to a non-existent path (0.6 points)
    # In the initial state, prettier.configPath = "/home/user/monorepo/configs/.prettierrc"
    # which does not exist. The fix is to either remove the key or set it to a valid path.
    try:
        if config_path_value is None:
            # Key removed entirely — Prettier auto-resolves from parent dirs. This is correct.
            print(f"PASS: Component 1 — prettier.configPath removed from settings (0.6 pts)")
            total_score += 0.6
        elif config_path_value == '':
            # Empty string — effectively removed
            print(f"PASS: Component 1 — prettier.configPath set to empty string (0.6 pts)")
            total_score += 0.6
        elif os.path.exists(config_path_value):
            # Points to an existing file — acceptable fix
            print(f"PASS: Component 1 — prettier.configPath points to existing file: {config_path_value} (0.6 pts)")
            total_score += 0.6
        else:
            # Still points to a non-existent path — NOT fixed
            print(f"FAIL: Component 1 — prettier.configPath still points to non-existent: {config_path_value}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Prettier can resolve a valid config with singleQuote: true (0.4 points)
    # If configPath is set, the file it points to must contain singleQuote: true.
    # If configPath is absent/empty, the monorepo/.prettierrc must exist with singleQuote: true
    # (so Prettier can auto-resolve it).
    try:
        if config_path_value and config_path_value != '' and os.path.exists(config_path_value):
            # configPath points to a real file — check its contents
            target_path = config_path_value
        else:
            # configPath absent or empty — Prettier auto-resolves from parent dirs
            # The .prettierrc at monorepo root should be resolvable
            target_path = PRETTIERRC_PATH

        if config_path_value and config_path_value != '' and not os.path.exists(config_path_value):
            # configPath still broken — Prettier cannot resolve any config
            print(f"FAIL: Component 2 — prettier.configPath points to non-existent file, config unresolvable")
        elif os.path.exists(target_path):
            with open(target_path, 'r') as f:
                rc_content = f.read()
            # Try JSON parse
            try:
                rc_data = json.loads(rc_content)
                if rc_data.get('singleQuote') is True:
                    print(f"PASS: Component 2 — {target_path} has singleQuote: true (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 2 — {target_path} does not have singleQuote: true, found: {rc_data.get('singleQuote')}")
            except json.JSONDecodeError:
                # Try YAML-like format (key: value)
                if 'singleQuote' in rc_content and 'true' in rc_content:
                    print(f"PASS: Component 2 — {target_path} contains singleQuote: true (YAML format) (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 2 — {target_path} does not contain singleQuote: true")
        else:
            print(f"FAIL: Component 2 — No resolvable .prettierrc found at {target_path}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

"""
Reward Script: Configure pyrightconfig.json for basic type checking and exclude migrations
Task ID: vscode_fix_057
Domain: vscode
Scoring:
  Component 1 (0.35): pyrightconfig.json exists with typeCheckingMode "basic"
  Component 2 (0.30): pyrightconfig.json excludes **/migrations
  Component 3 (0.35): VSCode settings typeCheckingMode changed from "strict" to "basic"
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_057'

# Paths to check
PYRIGHT_CONFIG = os.path.join(WORKDIR, 'django-project', 'pyrightconfig.json')
VSCODE_USER_SETTINGS = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')
VSCODE_WORKSPACE_SETTINGS = os.path.join(WORKDIR, 'django-project', '.vscode', 'settings.json')


def load_jsonc(path):
    """Load a JSON file, stripping // comments (JSONC support)."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        # Strip trailing commas before } or ]
        content = re.sub(r',\s*([}\]])', r'\1', content)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
        print(f"  Could not load {path}: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: pyrightconfig.json exists with typeCheckingMode "basic" (0.35 points)
    try:
        config = load_jsonc(PYRIGHT_CONFIG)
        if config is not None:
            mode = config.get('typeCheckingMode', None)
            if mode == 'basic':
                print(f"PASS: Component 1 — pyrightconfig.json has typeCheckingMode='basic' (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 — pyrightconfig.json typeCheckingMode is '{mode}', expected 'basic'")
        else:
            print(f"FAIL: Component 1 — pyrightconfig.json not found or not valid JSON at {PYRIGHT_CONFIG}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: pyrightconfig.json excludes **/migrations (0.30 points)
    try:
        config = load_jsonc(PYRIGHT_CONFIG)
        if config is not None:
            excludes = config.get('exclude', [])
            if isinstance(excludes, list):
                # Check for migrations exclusion pattern — accept common variants
                migrations_excluded = any(
                    'migrations' in entry
                    for entry in excludes
                )
                if migrations_excluded:
                    print(f"PASS: Component 2 — pyrightconfig.json excludes migrations: {excludes} (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"FAIL: Component 2 — pyrightconfig.json exclude list does not contain migrations pattern: {excludes}")
            else:
                print(f"FAIL: Component 2 — pyrightconfig.json 'exclude' is not a list: {type(excludes)}")
        else:
            print(f"FAIL: Component 2 — pyrightconfig.json not found or not valid JSON")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: VSCode settings typeCheckingMode is "basic" (not "strict") (0.35 points)
    # Check both user settings and workspace settings; either location counts
    try:
        type_check_mode = None
        # Check user-level settings
        user_settings = load_jsonc(VSCODE_USER_SETTINGS)
        if user_settings is not None:
            type_check_mode = user_settings.get('python.analysis.typeCheckingMode', None)

        # Also check workspace-level settings (overrides user settings in VSCode)
        ws_settings = load_jsonc(VSCODE_WORKSPACE_SETTINGS)
        if ws_settings is not None:
            ws_mode = ws_settings.get('python.analysis.typeCheckingMode', None)
            if ws_mode is not None:
                type_check_mode = ws_mode  # workspace overrides user

        if type_check_mode == 'basic':
            print(f"PASS: Component 3 — VSCode typeCheckingMode is 'basic' (0.35 pts)")
            total_score += 0.35
        elif type_check_mode == 'strict':
            print(f"FAIL: Component 3 — VSCode typeCheckingMode is still 'strict'")
        else:
            # If the setting was removed entirely, that's also acceptable since
            # pyrightconfig.json now controls it. But only if pyrightconfig.json exists.
            if total_score >= 0.35:
                # pyrightconfig.json has basic mode, and the strict setting is gone
                print(f"PASS: Component 3 — typeCheckingMode 'strict' removed from VSCode settings, "
                      f"pyrightconfig.json controls mode (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 3 — typeCheckingMode is '{type_check_mode}', expected 'basic'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

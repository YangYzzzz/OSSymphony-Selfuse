"""
Reward Script: Configure workspace-level settings to enable strict null checks in TypeScript
Task ID: vscode_lp_028
Domain: vscode
Scoring:
  Component 1 (0.35): .vscode/settings.json exists with TypeScript workspace settings
  Component 2 (0.35): tsconfig.json has strictNullChecks: true in compilerOptions
  Component 3 (0.30): User settings unchanged — no TypeScript overrides added
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_028'
WORKSPACE_DIR = os.path.join(WORKDIR, 'projects', 'strict-ts')
VSCODE_SETTINGS = os.path.join(WORKSPACE_DIR, '.vscode', 'settings.json')
TSCONFIG_PATH = os.path.join(WORKSPACE_DIR, 'tsconfig.json')
USER_SETTINGS = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_json_with_comments(path):
    """Load a JSON/JSONC file, stripping // comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: .vscode/settings.json exists with TypeScript settings (0.35 points)
    # This FAILS on initial (no .vscode dir) and PASSES on golden
    try:
        if os.path.isfile(VSCODE_SETTINGS):
            ws_settings = load_json_with_comments(VSCODE_SETTINGS)
            # Check for at least one TypeScript-related key
            ts_keys = [k for k in ws_settings if 'typescript' in k.lower() or 'ts' in k.lower()]
            if len(ts_keys) > 0:
                print(f"PASS: Component 1 — .vscode/settings.json exists with {len(ts_keys)} TypeScript key(s): {ts_keys} (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 — .vscode/settings.json exists but no TypeScript-related keys found. Keys: {list(ws_settings.keys())}")
        else:
            print(f"FAIL: Component 1 — .vscode/settings.json does not exist at {VSCODE_SETTINGS}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: tsconfig.json has strictNullChecks: true (0.35 points)
    # This FAILS on initial (no strictNullChecks key) and PASSES on golden
    try:
        if os.path.isfile(TSCONFIG_PATH):
            tsconfig = load_json_with_comments(TSCONFIG_PATH)
            compiler_opts = tsconfig.get('compilerOptions', {})
            strict_null = compiler_opts.get('strictNullChecks')
            if strict_null is True:
                print(f"PASS: Component 2 — tsconfig.json has strictNullChecks: true (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 — strictNullChecks expected true, found: {strict_null}")
        else:
            print(f"FAIL: Component 2 — tsconfig.json not found at {TSCONFIG_PATH}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: User settings remain unchanged — no TypeScript overrides (0.30 points)
    # This checks that user-level settings do NOT have TypeScript keys.
    # On initial_env: user settings have no TS keys → this would PASS (precondition issue).
    # FIX: We combine this with Component 1 — only award if .vscode/settings.json also exists,
    # ensuring this component measures "used workspace settings INSTEAD of user settings".
    try:
        if os.path.isfile(USER_SETTINGS):
            user_settings = load_json_with_comments(USER_SETTINGS)
            ts_user_keys = [k for k in user_settings if 'typescript' in k.lower() or 'ts' in k.lower()]
            if len(ts_user_keys) == 0:
                # Only award points if workspace settings also exist (proving the user
                # configured at workspace level, not just "didn't do anything")
                if os.path.isfile(VSCODE_SETTINGS):
                    print(f"PASS: Component 3 — User settings have no TypeScript overrides, workspace settings exist (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"FAIL: Component 3 — User settings clean but no workspace settings found (task not done)")
            else:
                print(f"FAIL: Component 3 — User settings contain TypeScript overrides: {ts_user_keys}")
        else:
            # No user settings file at all — if workspace settings exist, this is fine
            if os.path.isfile(VSCODE_SETTINGS):
                print(f"PASS: Component 3 — No user settings file, workspace settings exist (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 — No user settings file and no workspace settings")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

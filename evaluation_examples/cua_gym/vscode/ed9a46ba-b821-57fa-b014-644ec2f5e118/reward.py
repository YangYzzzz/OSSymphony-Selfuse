"""
Reward Script: Configure VSCode TypeScript to use workspace version
Task ID: vscode_web_086
Domain: vscode
Scoring:
  Component 1 (0.5): typescript.tsdk key exists in workspace .vscode/settings.json
  Component 2 (0.3): typescript.tsdk value points to node_modules/typescript/lib
  Component 3 (0.2): The referenced TypeScript lib directory actually exists on disk
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_086'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'react-ts-app')
WORKSPACE_SETTINGS_PATH = os.path.join(PROJECT_DIR, '.vscode', 'settings.json')
GLOBAL_SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_jsonc(path):
    """Load a JSON or JSONC file (strips // comments)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC format used by VSCode)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load workspace settings — this is where typescript.tsdk should be set
    ws_settings = None
    try:
        ws_settings = load_jsonc(WORKSPACE_SETTINGS_PATH)
        print(f"INFO: Loaded workspace settings from {WORKSPACE_SETTINGS_PATH}")
    except FileNotFoundError:
        print(f"INFO: Workspace settings not found at {WORKSPACE_SETTINGS_PATH}")
    except (json.JSONDecodeError, Exception) as e:
        print(f"ERROR: Could not parse workspace settings: {e}")

    # Also check global settings as alternative location
    global_settings = None
    try:
        global_settings = load_jsonc(GLOBAL_SETTINGS_PATH)
        print(f"INFO: Loaded global settings from {GLOBAL_SETTINGS_PATH}")
    except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
        print(f"INFO: Could not load global settings: {e}")

    # Determine which settings contain typescript.tsdk
    tsdk_value = None
    tsdk_source = None
    if ws_settings and 'typescript.tsdk' in ws_settings:
        tsdk_value = ws_settings['typescript.tsdk']
        tsdk_source = 'workspace'
    elif global_settings and 'typescript.tsdk' in global_settings:
        tsdk_value = global_settings['typescript.tsdk']
        tsdk_source = 'global'

    # Component 1: typescript.tsdk key exists in settings (0.5 points)
    # This is the PRIMARY task change — setting tsdk to use workspace TS version
    try:
        if tsdk_value is not None:
            print(f"PASS: Component 1 — typescript.tsdk found in {tsdk_source} settings: '{tsdk_value}' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — typescript.tsdk not found in workspace or global settings")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: typescript.tsdk value correctly references the TypeScript lib directory (0.3 points)
    # Valid values: "node_modules/typescript/lib" (relative) or absolute path ending in typescript/lib
    try:
        if tsdk_value is not None:
            normalized = tsdk_value.replace('\\', '/').rstrip('/')
            # Accept relative or absolute paths pointing to typescript/lib
            if normalized.endswith('typescript/lib') or normalized.endswith('typescript/lib/'):
                print(f"PASS: Component 2 — typescript.tsdk correctly points to typescript/lib: '{tsdk_value}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — typescript.tsdk value '{tsdk_value}' does not point to typescript/lib")
        else:
            print(f"FAIL: Component 2 — typescript.tsdk not set, cannot verify value")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The TypeScript lib directory actually exists on disk (0.2 points)
    # This validates that the workspace TS is actually installed
    try:
        if tsdk_value is not None:
            # Resolve the path: if relative, resolve against the project dir
            if os.path.isabs(tsdk_value):
                resolved_path = tsdk_value
            else:
                resolved_path = os.path.join(PROJECT_DIR, tsdk_value)

            # Check the directory exists and contains typescript.js (the key TS lib file)
            if os.path.isdir(resolved_path):
                ts_js = os.path.join(resolved_path, 'typescript.js')
                tsserver_js = os.path.join(resolved_path, 'tsserver.js')
                if os.path.isfile(ts_js) or os.path.isfile(tsserver_js):
                    print(f"PASS: Component 3 — TypeScript lib directory exists at '{resolved_path}' with TS files (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 3 — Directory exists at '{resolved_path}' but missing typescript.js/tsserver.js")
            else:
                print(f"FAIL: Component 3 — TypeScript lib directory not found at '{resolved_path}'")
        else:
            print(f"FAIL: Component 3 — typescript.tsdk not set, cannot verify lib directory")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()

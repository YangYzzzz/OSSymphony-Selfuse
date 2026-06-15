"""
Reward Script: Disable 'Bracket Pair Colorizer' extension globally in VSCode
Task ID: vscode_ext_006
Domain: vs_code

Scoring Rubric:
  Component 1: Extension metadata has 'disabled: true' in extensions.json (0.6 pts)
  Component 2: Extension directory still exists (not uninstalled) AND disabled flag is set (0.4 pts)
  Total: 1.0

Key insight: VSCode stores per-extension disable state in
  /home/user/.vscode/extensions/extensions.json
  When an extension is globally disabled, {"disabled": true} appears in its "metadata" object.
  On the initial_env this flag is absent (extension is enabled).
  On the golden_env this flag is present and set to True (extension is disabled).
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_ext_006'
EXTENSION_ID = 'coenraads.bracket-pair-colorizer-2'
EXTENSIONS_JSON = '/home/user/.vscode/extensions/extensions.json'
EXTENSION_DIR = '/home/user/.vscode/extensions/coenraads.bracket-pair-colorizer-2-0.2.4'


def verify_task():
    """
    Verify that the Bracket Pair Colorizer extension is disabled globally
    but still installed (not uninstalled).
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: extensions.json must exist and be parseable
    if not os.path.exists(EXTENSIONS_JSON):
        print(f"CRITICAL: extensions.json not found at {EXTENSIONS_JSON}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(EXTENSIONS_JSON, 'r') as f:
            extensions_data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"CRITICAL: Cannot parse extensions.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the Bracket Pair Colorizer entry
    ext_entry = None
    for entry in extensions_data:
        identifier = entry.get('identifier', {})
        if identifier.get('id', '').lower() == EXTENSION_ID.lower():
            ext_entry = entry
            break

    if ext_entry is None:
        print(f"FAIL: Extension '{EXTENSION_ID}' not found in extensions.json — may have been uninstalled")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Extension metadata has 'disabled: true' (0.6 points)
    # This is the primary signal that the task was completed.
    # On initial_env: metadata does NOT contain 'disabled' key (extension is enabled).
    # On golden_env: metadata contains {"disabled": true} (extension is globally disabled).
    try:
        metadata = ext_entry.get('metadata', {})
        disabled_flag = metadata.get('disabled', None)

        if disabled_flag is True:
            print(f"PASS: Component 1 — Extension metadata has 'disabled: true' (0.6 pts)")
            total_score += 0.6
        elif disabled_flag is False:
            print(f"FAIL: Component 1 — Extension metadata has 'disabled: false' (explicitly enabled)")
        elif disabled_flag is None:
            print(f"FAIL: Component 1 — Extension metadata has no 'disabled' key (extension is enabled by default)")
        else:
            print(f"FAIL: Component 1 — Unexpected 'disabled' value: {disabled_flag!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check disabled flag: {e}")

    # Component 2: Extension directory still exists AND disabled is confirmed (0.4 points)
    # This verifies the extension was DISABLED (not uninstalled) — both conditions must hold.
    # On initial_env: directory exists but disabled is NOT set, so this compound check FAILS.
    # On golden_env: directory exists AND disabled IS set, so this compound check PASSES.
    try:
        dir_exists = os.path.isdir(EXTENSION_DIR)
        disabled_confirmed = (ext_entry.get('metadata', {}).get('disabled', None) is True)

        if dir_exists and disabled_confirmed:
            print(f"PASS: Component 2 — Extension directory exists AND is disabled (not uninstalled) (0.4 pts)")
            total_score += 0.4
        elif not dir_exists:
            print(f"FAIL: Component 2 — Extension directory not found at {EXTENSION_DIR} — extension may have been uninstalled")
        elif not disabled_confirmed:
            print(f"FAIL: Component 2 — Extension directory exists but 'disabled: true' is not set in metadata")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.1f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

"""
FINAL REWARD SCRIPT - SUCCESS
Task: I accidentally disabled ESLint while tweaking my settings, and now my React project isn’t showing any linting errors. Could you help me re-enable the “ESLint” extension?
Generated: 2025-09-11 13:44:16
Status: success
Model: azure-o3
Total Steps: 8
"""

import json
import pathlib
import re


def verify_task():
    """Reward script to verify that the ESLint extension is re-enabled in VS Code.

    Scoring (progressive):
        • 0.2 – ESLint extension (dbaeumer.vscode-eslint) is installed under ~/.vscode/extensions
        • 0.8 – ESLint is enabled in VS Code user settings (eslint.enable is True or undefined)
    Returns a float between 0.0 and 1.0 and prints detailed verification output.
    """
    total_score = 0.0
    weight_extension_installed = 0.2
    weight_eslint_enabled = 0.8

    home = pathlib.Path.home()

    # -----------------------------
    # 1. Verify extension installed
    # -----------------------------
    ext_root = home / '.vscode' / 'extensions'
    eslint_ext_dirs = []
    if ext_root.exists() and ext_root.is_dir():
        for p in ext_root.iterdir():
            if re.match(r'dbaeumer\\.vscode-eslint-.*', p.name):
                eslint_ext_dirs.append(p)

    if eslint_ext_dirs:
        print(f"✓ ESLint extension installed (found {len(eslint_ext_dirs)} director(ies))  (+{weight_extension_installed})")
        total_score += weight_extension_installed
    else:
        print("✗ ESLint extension NOT found in ~/.vscode/extensions  (+0.0)")

    # -------------------------------------
    # 2. Verify ESLint is enabled in VSCode
    # -------------------------------------
    user_settings_path = home / '.config' / 'Code' / 'User' / 'settings.json'
    if user_settings_path.exists():
        try:
            with open(user_settings_path, 'r', encoding='utf-8') as f:
                settings_data = json.load(f)
            eslint_enable_value = settings_data.get('eslint.enable', None)

            # If the key is absent OR True → treated as enabled.
            if eslint_enable_value is False:
                print("✗ 'eslint.enable' is explicitly set to false in user settings (-0.0)")
            else:
                state_str = 'true' if eslint_enable_value else 'not set'
                print(f"✓ 'eslint.enable' is {state_str} (treated as enabled)  (+{weight_eslint_enabled})")
                total_score += weight_eslint_enabled
        except json.JSONDecodeError as e:
            print(f"✗ Failed to parse settings.json: {e}  (+0.0)")
    else:
        print("✗ settings.json not found; cannot verify ESLint enablement  (+0.0)")

    # -----------------------------
    # Final score & output
    # -----------------------------
    final_score = round(min(total_score, 1.0), 2)  # round for neatness
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task()

"""
Reward Script: VSCode ESLint setup with auto-fix on save
Task ID: vscode_gf2_021
Domain: vscode
Scoring:
  Component 1 (0.30): ESLint extension installed
  Component 2 (0.30): eslint.run set to "onSave" in settings.json
  Component 3 (0.25): editor.codeActionsOnSave contains source.fixAll.eslint = true
  Component 4 (0.15): ESLint config file exists in project directory
"""

import os
import json
import re

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")
PROJECT_DIR = "/home/user/projects/web-app"


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARNING: Could not load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: ESLint extension installed (0.30 points)
    # The task requires installing 'ESLint' extension by Microsoft (dbaeumer.vscode-eslint)
    try:
        ext_list_output = os.popen("code --list-extensions 2>/dev/null").read()
        extensions = [e.strip().lower() for e in ext_list_output.strip().split("\n") if e.strip()]
        if "dbaeumer.vscode-eslint" in extensions:
            print(f"PASS: Component 1 — ESLint extension installed (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — ESLint extension not found. Installed: {extensions}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: eslint.run set to "onSave" (0.30 points)
    # Task requires setting eslint.run to "onSave" in User Settings JSON
    try:
        settings = load_settings()
        if settings is None:
            print(f"FAIL: Component 2 — settings.json not found or invalid")
        else:
            eslint_run = settings.get("eslint.run")
            if eslint_run == "onSave":
                print(f"PASS: Component 2 — eslint.run = 'onSave' (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 — eslint.run = {eslint_run!r}, expected 'onSave'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: editor.codeActionsOnSave has source.fixAll.eslint (0.25 points)
    # Task requires adding source.fixAll.eslint to editor.codeActionsOnSave
    try:
        settings = load_settings()
        if settings is None:
            print(f"FAIL: Component 3 — settings.json not found or invalid")
        else:
            code_actions = settings.get("editor.codeActionsOnSave", {})
            if isinstance(code_actions, dict):
                eslint_fix = code_actions.get("source.fixAll.eslint")
                # Accept True, "always", "explicit" as valid truthy values
                if eslint_fix is True or eslint_fix == "always" or eslint_fix == "explicit":
                    print(f"PASS: Component 3 — source.fixAll.eslint = {eslint_fix!r} (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 3 — source.fixAll.eslint = {eslint_fix!r}, expected true/always/explicit")
            else:
                print(f"FAIL: Component 3 — editor.codeActionsOnSave is not a dict: {type(code_actions)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: ESLint config file exists in project (0.15 points)
    # Task requires running npm init @eslint/config which creates a config file
    try:
        eslint_config_patterns = [
            "eslint.config.js",
            "eslint.config.mjs",
            "eslint.config.cjs",
            ".eslintrc.js",
            ".eslintrc.cjs",
            ".eslintrc.json",
            ".eslintrc.yml",
            ".eslintrc.yaml",
            ".eslintrc",
        ]
        config_found = None
        for pattern in eslint_config_patterns:
            config_path = os.path.join(PROJECT_DIR, pattern)
            if os.path.exists(config_path):
                config_found = pattern
                break

        if config_found:
            # Verify the config file has actual content (not empty)
            config_path = os.path.join(PROJECT_DIR, config_found)
            file_size = os.path.getsize(config_path)
            if file_size > 10:
                print(f"PASS: Component 4 — ESLint config '{config_found}' found ({file_size} bytes) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — ESLint config '{config_found}' exists but too small ({file_size} bytes)")
        else:
            print(f"FAIL: Component 4 — No ESLint config file found in {PROJECT_DIR}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

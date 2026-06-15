"""
Reward Script: Install ESLint extension, create .eslintrc.json with rules, configure auto-fix on save
Task ID: vscode_wf_015
Domain: vscode
Scoring:
  Component 1 (0.25) - ESLint extension installed
  Component 2 (0.15) - .eslintrc.json exists and is valid JSON
  Component 3 (0.35) - .eslintrc.json has correct rules
  Component 4 (0.25) - VSCode settings has codeActionsOnSave for ESLint
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_015'

ESLINTRC_PATH = os.path.join(WORKDIR, 'project', '.eslintrc.json')
SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_json_file(path):
    """Load a JSON file, handling JSONC (JSON with Comments) used by VSCode."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (VSCode settings may have them)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip trailing commas before } or ]
    content = re.sub(r',\s*([}\]])', r'\1', content)
    return json.loads(content)


def is_subset(expected, actual):
    """Check that expected is a subset of actual (recursive for dicts)."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        return expected == actual
    return expected == actual


def check_extension_installed(ext_id):
    """Check if a VSCode extension is installed by scanning the extensions directory."""
    extensions_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
    # Also check snap-based and flatpak-based locations
    possible_dirs = [
        extensions_dir,
        os.path.join(WORKDIR, '.vscode-server', 'extensions'),
    ]
    for d in possible_dirs:
        if os.path.isdir(d):
            for entry in os.listdir(d):
                if entry.lower().startswith(ext_id.lower()):
                    return True

    # Fallback: try `code --list-extensions` via os.popen
    try:
        result = os.popen('code --list-extensions 2>/dev/null').read()
        if ext_id.lower() in result.lower():
            return True
    except Exception:
        pass

    return False


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: ESLint extension installed (0.25 points)
    try:
        ext_installed = check_extension_installed('dbaeumer.vscode-eslint')
        if ext_installed:
            print(f"PASS: Component 1 - ESLint extension 'dbaeumer.vscode-eslint' is installed (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 - ESLint extension 'dbaeumer.vscode-eslint' is NOT installed")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: .eslintrc.json exists and is valid JSON (0.15 points)
    eslintrc = None
    try:
        if os.path.isfile(ESLINTRC_PATH):
            eslintrc = load_json_file(ESLINTRC_PATH)
            if isinstance(eslintrc, dict):
                print(f"PASS: Component 2 - .eslintrc.json exists and is valid JSON (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 - .eslintrc.json is not a JSON object")
        else:
            print(f"FAIL: Component 2 - .eslintrc.json does not exist at {ESLINTRC_PATH}")
    except (json.JSONDecodeError, Exception) as e:
        print(f"FAIL: Component 2 - .eslintrc.json is not valid JSON: {e}")

    # Component 3: .eslintrc.json has correct rules (0.35 points)
    # Expected rules:
    #   no-unused-vars: "error"
    #   semi: ["error", "always"]
    #   quotes: ["warn", "single"]
    try:
        if eslintrc is not None and 'rules' in eslintrc:
            rules = eslintrc['rules']
            rule_score = 0.0
            max_per_rule = 0.35 / 3.0  # ~0.1167 per rule

            # Check no-unused-vars
            nuv = rules.get('no-unused-vars')
            if nuv == 'error' or nuv == 2:
                print(f"  PASS: no-unused-vars = {nuv}")
                rule_score += max_per_rule
            else:
                print(f"  FAIL: no-unused-vars expected 'error', found {nuv}")

            # Check semi
            semi = rules.get('semi')
            if (isinstance(semi, list) and len(semi) >= 2
                    and (semi[0] == 'error' or semi[0] == 2)
                    and semi[1] == 'always'):
                print(f"  PASS: semi = {semi}")
                rule_score += max_per_rule
            else:
                print(f"  FAIL: semi expected ['error', 'always'], found {semi}")

            # Check quotes
            quotes = rules.get('quotes')
            if (isinstance(quotes, list) and len(quotes) >= 2
                    and (quotes[0] == 'warn' or quotes[0] == 1)
                    and quotes[1] == 'single'):
                print(f"  PASS: quotes = {quotes}")
                rule_score += max_per_rule
            else:
                print(f"  FAIL: quotes expected ['warn', 'single'], found {quotes}")

            # Round to avoid floating point issues
            rule_score = round(rule_score, 4)
            if rule_score > 0:
                print(f"PASS: Component 3 - ESLint rules verified ({rule_score:.4f} pts)")
                total_score += rule_score
            else:
                print(f"FAIL: Component 3 - No ESLint rules match expected values")
        else:
            print(f"FAIL: Component 3 - .eslintrc.json missing or has no 'rules' key")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: VSCode settings has codeActionsOnSave for ESLint (0.25 points)
    try:
        if os.path.isfile(SETTINGS_PATH):
            settings = load_json_file(SETTINGS_PATH)
            expected = {"editor.codeActionsOnSave": {"source.fixAll.eslint": True}}
            if is_subset(expected, settings):
                print(f"PASS: Component 4 - settings.json has editor.codeActionsOnSave.source.fixAll.eslint = true (0.25 pts)")
                total_score += 0.25
            else:
                # Check what we actually found
                caos = settings.get('editor.codeActionsOnSave', {})
                print(f"FAIL: Component 4 - editor.codeActionsOnSave = {caos}, expected source.fixAll.eslint: true")
        else:
            print(f"FAIL: Component 4 - settings.json not found at {SETTINGS_PATH}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

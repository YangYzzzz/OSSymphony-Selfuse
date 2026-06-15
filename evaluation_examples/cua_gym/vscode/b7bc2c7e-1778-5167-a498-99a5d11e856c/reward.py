"""
Reward Script: Set default formatters for JSON, HTML, JavaScript, and CSS in VSCode
Task ID: vscode_code_013
Domain: vs_code
Scoring:
  Component 1: JSON default formatter set to vscode.json-language-features (0.25)
  Component 2: HTML default formatter set to vscode.html-language-features (0.25)
  Component 3: JavaScript default formatter set to vscode.typescript-language-features (0.25)
  Component 4: CSS default formatter set to vscode.css-language-features (0.25)
  Total: 1.0
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_013'
SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_settings(path):
    """Load settings.json, stripping JSONC comments if present."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments (JSONC support)
        content_stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_stripped)
    except FileNotFoundError:
        print(f"CRITICAL: settings.json not found at {path}")
        return None
    except json.JSONDecodeError as e:
        print(f"CRITICAL: Cannot parse settings.json: {e}")
        return None


def verify_task():
    """
    Verify that default formatters for JSON, HTML, JavaScript, and CSS have been configured
    in VSCode user settings. Each formatter is an independently scored component.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load settings.json - precondition gate
    settings = load_settings(SETTINGS_PATH)
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    # Component 1: JSON default formatter set to vscode.json-language-features (0.25 points)
    # This must be absent on initial_env and present on golden_env
    try:
        json_formatter = settings.get('[json]', {}).get('editor.defaultFormatter')
        expected_json_formatter = 'vscode.json-language-features'
        if json_formatter == expected_json_formatter:
            print(f"PASS: Component 1 - JSON default formatter is '{json_formatter}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 - JSON default formatter expected '{expected_json_formatter}', found: '{json_formatter}'")
    except Exception as e:
        print(f"ERROR: Component 1 - Could not check JSON formatter: {e}")

    # Component 2: HTML default formatter set to vscode.html-language-features (0.25 points)
    try:
        html_formatter = settings.get('[html]', {}).get('editor.defaultFormatter')
        expected_html_formatter = 'vscode.html-language-features'
        if html_formatter == expected_html_formatter:
            print(f"PASS: Component 2 - HTML default formatter is '{html_formatter}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 - HTML default formatter expected '{expected_html_formatter}', found: '{html_formatter}'")
    except Exception as e:
        print(f"ERROR: Component 2 - Could not check HTML formatter: {e}")

    # Component 3: JavaScript default formatter set to vscode.typescript-language-features (0.25 points)
    try:
        js_formatter = settings.get('[javascript]', {}).get('editor.defaultFormatter')
        expected_js_formatter = 'vscode.typescript-language-features'
        if js_formatter == expected_js_formatter:
            print(f"PASS: Component 3 - JavaScript default formatter is '{js_formatter}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 - JavaScript default formatter expected '{expected_js_formatter}', found: '{js_formatter}'")
    except Exception as e:
        print(f"ERROR: Component 3 - Could not check JavaScript formatter: {e}")

    # Component 4: CSS default formatter set to vscode.css-language-features (0.25 points)
    try:
        css_formatter = settings.get('[css]', {}).get('editor.defaultFormatter')
        expected_css_formatter = 'vscode.css-language-features'
        if css_formatter == expected_css_formatter:
            print(f"PASS: Component 4 - CSS default formatter is '{css_formatter}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 - CSS default formatter expected '{expected_css_formatter}', found: '{css_formatter}'")
    except Exception as e:
        print(f"ERROR: Component 4 - Could not check CSS formatter: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: verify task
if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()

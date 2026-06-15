"""
Reward Script: Multi-root workspace folder-specific settings
Task ID: vscode_lp_077
Domain: vscode
Scoring:
  Component 1 (0.25): API folder has editor.tabSize=4 and insertSpaces=true
  Component 2 (0.25): API folder has Black formatter settings for Python
  Component 3 (0.25): Frontend folder has editor.tabSize=2 and insertSpaces=true
  Component 4 (0.25): Frontend folder has Prettier formatter settings for JavaScript
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_077'

API_SETTINGS = os.path.join(WORKDIR, 'projects', 'api', '.vscode', 'settings.json')
FRONTEND_SETTINGS = os.path.join(WORKDIR, 'projects', 'frontend', '.vscode', 'settings.json')


def load_jsonc(path):
    """Load a JSON/JSONC file, stripping // comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def _is_subset(expected, actual):
    """Check that expected is a subset of actual (recursive dict containment)."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and _is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        return expected == actual
    return expected == actual


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: API folder has editor.tabSize=4 and insertSpaces=true (0.25 points)
    # This checks that .vscode/settings.json exists in api/ with correct tab settings.
    # Initial env has NO .vscode/settings.json, so this will FAIL on initial (correct).
    try:
        api_settings = load_jsonc(API_SETTINGS)
        tab_size_ok = api_settings.get('editor.tabSize') == 4
        insert_spaces_ok = api_settings.get('editor.insertSpaces') is True
        if tab_size_ok and insert_spaces_ok:
            print(f"PASS: Component 1 - API tabSize=4, insertSpaces=true (0.25 pts)")
            total_score += 0.25
        elif tab_size_ok:
            print(f"PARTIAL: Component 1 - API tabSize=4 correct but insertSpaces missing/wrong (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - API tabSize={api_settings.get('editor.tabSize')}, expected 4")
    except FileNotFoundError:
        print(f"FAIL: Component 1 - {API_SETTINGS} not found")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: API folder has Black formatter for Python (0.25 points)
    # Checks that the default formatter references Black (ms-python.black-formatter).
    # Initial env has no settings file, so FAIL on initial (correct).
    try:
        api_settings = load_jsonc(API_SETTINGS)
        # Check for Black formatter - could be at top level or in [python] section
        top_formatter = str(api_settings.get('editor.defaultFormatter', '')).lower()
        python_section = api_settings.get('[python]', {})
        python_formatter = str(python_section.get('editor.defaultFormatter', '')).lower()

        has_black_top = 'black' in top_formatter
        has_black_python = 'black' in python_formatter
        has_black_legacy = str(api_settings.get('python.formatting.provider', '')).lower() == 'black'

        if has_black_top or has_black_python:
            print(f"PASS: Component 2 - API has Black formatter configured (0.25 pts)")
            total_score += 0.25
        elif has_black_legacy:
            print(f"PASS: Component 2 - API has Black via legacy python.formatting.provider (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 - API formatter: top={top_formatter}, python={python_formatter}")
    except FileNotFoundError:
        print(f"FAIL: Component 2 - {API_SETTINGS} not found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Frontend folder has editor.tabSize=2 and insertSpaces=true (0.25 points)
    # Initial env has NO .vscode/settings.json in frontend/, so FAIL on initial (correct).
    try:
        fe_settings = load_jsonc(FRONTEND_SETTINGS)
        tab_size_ok = fe_settings.get('editor.tabSize') == 2
        insert_spaces_ok = fe_settings.get('editor.insertSpaces') is True
        if tab_size_ok and insert_spaces_ok:
            print(f"PASS: Component 3 - Frontend tabSize=2, insertSpaces=true (0.25 pts)")
            total_score += 0.25
        elif tab_size_ok:
            print(f"PARTIAL: Component 3 - Frontend tabSize=2 correct but insertSpaces missing/wrong (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 - Frontend tabSize={fe_settings.get('editor.tabSize')}, expected 2")
    except FileNotFoundError:
        print(f"FAIL: Component 3 - {FRONTEND_SETTINGS} not found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Frontend folder has Prettier formatter for JavaScript (0.25 points)
    # Checks for Prettier (esbenp.prettier-vscode) as formatter.
    # Initial env has no settings file, so FAIL on initial (correct).
    try:
        fe_settings = load_jsonc(FRONTEND_SETTINGS)
        # Check for Prettier - could be at top level or in [javascript] section
        top_formatter = str(fe_settings.get('editor.defaultFormatter', '')).lower()
        js_section = fe_settings.get('[javascript]', {})
        js_formatter = str(js_section.get('editor.defaultFormatter', '')).lower()
        jsx_section = fe_settings.get('[javascriptreact]', {})
        jsx_formatter = str(jsx_section.get('editor.defaultFormatter', '')).lower()

        has_prettier_top = 'prettier' in top_formatter
        has_prettier_js = 'prettier' in js_formatter
        has_prettier_jsx = 'prettier' in jsx_formatter

        if has_prettier_top or has_prettier_js:
            print(f"PASS: Component 4 - Frontend has Prettier formatter configured (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 - Frontend formatter: top={top_formatter}, js={js_formatter}")
    except FileNotFoundError:
        print(f"FAIL: Component 4 - {FRONTEND_SETTINGS} not found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

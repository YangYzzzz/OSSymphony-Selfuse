"""
Reward Script: Verify comprehensive .vscode/settings.json for polyglot project
Task ID: vscode_wf_057
Domain: vs_code
Scoring:
  - Component 1 (0.20): Language-specific sections [python], [javascript], [html], [css] exist
  - Component 2 (0.20): Python settings (Black, 4-space tabs, 120 ruler, formatOnSave)
  - Component 3 (0.20): JavaScript settings (Prettier, 2-space tabs, 80 ruler, semicolons, formatOnSave)
  - Component 4 (0.10): HTML settings (auto-closing tags, 2-space tabs, formatOnSave)
  - Component 5 (0.10): files.associations (*.jinja -> html)
  - Component 6 (0.10): files.exclude (__pycache__, node_modules, .pytest_cache)
  - Component 7 (0.10): search.exclude configured
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_057'

SETTINGS_PATH = os.path.join(WORKDIR, 'project', '.vscode', 'settings.json')


def load_settings(path):
    """Load settings.json, handling JSONC comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip JSONC comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must exist and be valid JSON
    try:
        settings = load_settings(SETTINGS_PATH)
    except FileNotFoundError:
        print(f"CRITICAL: File not found: {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse settings.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: settings must not be empty (initial state is {})
    if not settings:
        print("FAIL: settings.json is empty (no configuration)")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Language-specific sections exist (0.20 points)
    # All four language sections must be present: [python], [javascript], [html], [css]
    try:
        required_sections = ['[python]', '[javascript]', '[html]', '[css]']
        found_sections = [s for s in required_sections if s in settings]
        missing_sections = [s for s in required_sections if s not in settings]

        if len(found_sections) == 4:
            print(f"PASS: Component 1 — All 4 language sections present: {found_sections} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Missing sections: {missing_sections}, found: {found_sections}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Python settings correct (0.20 points)
    # Black formatter, tabSize 4, ruler 120, formatOnSave true
    try:
        py_settings = settings.get('[python]', {})
        py_checks = 0
        py_total = 4

        # Check Black formatter
        formatter = py_settings.get('editor.defaultFormatter', '')
        if 'black' in str(formatter).lower():
            py_checks += 1
        else:
            print(f"  DETAIL: Python formatter expected 'black', found: {formatter}")

        # Check tabSize 4
        if py_settings.get('editor.tabSize') == 4:
            py_checks += 1
        else:
            print(f"  DETAIL: Python tabSize expected 4, found: {py_settings.get('editor.tabSize')}")

        # Check ruler 120
        rulers = py_settings.get('editor.rulers', [])
        if isinstance(rulers, list) and 120 in rulers:
            py_checks += 1
        else:
            print(f"  DETAIL: Python rulers expected [120], found: {rulers}")

        # Check formatOnSave
        if py_settings.get('editor.formatOnSave') is True:
            py_checks += 1
        else:
            print(f"  DETAIL: Python formatOnSave expected true, found: {py_settings.get('editor.formatOnSave')}")

        if py_checks == py_total:
            print(f"PASS: Component 2 — Python settings all correct ({py_checks}/{py_total}) (0.20 pts)")
            total_score += 0.20
        elif py_checks > 0:
            partial = round(0.20 * py_checks / py_total, 2)
            print(f"PARTIAL: Component 2 — Python settings {py_checks}/{py_total} correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Python settings 0/{py_total} correct")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: JavaScript settings correct (0.20 points)
    # Prettier formatter, tabSize 2, ruler 80, semicolons, formatOnSave
    try:
        js_settings = settings.get('[javascript]', {})
        js_checks = 0
        js_total = 5

        # Check Prettier formatter
        formatter = js_settings.get('editor.defaultFormatter', '')
        if 'prettier' in str(formatter).lower():
            js_checks += 1
        else:
            print(f"  DETAIL: JS formatter expected 'prettier', found: {formatter}")

        # Check tabSize 2
        if js_settings.get('editor.tabSize') == 2:
            js_checks += 1
        else:
            print(f"  DETAIL: JS tabSize expected 2, found: {js_settings.get('editor.tabSize')}")

        # Check ruler 80
        rulers = js_settings.get('editor.rulers', [])
        if isinstance(rulers, list) and 80 in rulers:
            js_checks += 1
        else:
            print(f"  DETAIL: JS rulers expected [80], found: {rulers}")

        # Check semicolons setting exists
        # Could be at javascript.format.semicolons or editor.formatOnSave
        semicolons_val = js_settings.get('javascript.format.semicolons', '')
        if semicolons_val in ('insert', 'remove'):
            js_checks += 1
        else:
            # Also check top-level
            top_semi = settings.get('javascript.format.semicolons', '')
            if top_semi in ('insert', 'remove'):
                js_checks += 1
            else:
                print(f"  DETAIL: JS semicolons setting not found or invalid: {semicolons_val}")

        # Check formatOnSave
        if js_settings.get('editor.formatOnSave') is True:
            js_checks += 1
        else:
            print(f"  DETAIL: JS formatOnSave expected true, found: {js_settings.get('editor.formatOnSave')}")

        if js_checks == js_total:
            print(f"PASS: Component 3 — JavaScript settings all correct ({js_checks}/{js_total}) (0.20 pts)")
            total_score += 0.20
        elif js_checks > 0:
            partial = round(0.20 * js_checks / js_total, 2)
            print(f"PARTIAL: Component 3 — JavaScript settings {js_checks}/{js_total} correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — JavaScript settings 0/{js_total} correct")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: HTML settings correct (0.10 points)
    # Auto-closing tags, tabSize 2, formatOnSave
    try:
        html_settings = settings.get('[html]', {})
        html_checks = 0
        html_total = 3

        # Check auto-closing tags
        auto_close = html_settings.get('html.autoClosingTags')
        if auto_close is True:
            html_checks += 1
        else:
            # Also check top-level setting
            if settings.get('html.autoClosingTags') is True:
                html_checks += 1
            else:
                print(f"  DETAIL: HTML autoClosingTags expected true, found: {auto_close}")

        # Check tabSize 2
        if html_settings.get('editor.tabSize') == 2:
            html_checks += 1
        else:
            print(f"  DETAIL: HTML tabSize expected 2, found: {html_settings.get('editor.tabSize')}")

        # Check formatOnSave
        if html_settings.get('editor.formatOnSave') is True:
            html_checks += 1
        else:
            print(f"  DETAIL: HTML formatOnSave expected true, found: {html_settings.get('editor.formatOnSave')}")

        if html_checks == html_total:
            print(f"PASS: Component 4 — HTML settings all correct ({html_checks}/{html_total}) (0.10 pts)")
            total_score += 0.10
        elif html_checks > 0:
            partial = round(0.10 * html_checks / html_total, 2)
            print(f"PARTIAL: Component 4 — HTML settings {html_checks}/{html_total} correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — HTML settings 0/{html_total} correct")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: files.associations configured (0.10 points)
    # *.jinja -> html
    try:
        assoc = settings.get('files.associations', {})
        if isinstance(assoc, dict) and assoc.get('*.jinja') == 'html':
            print(f"PASS: Component 5 — files.associations has *.jinja -> html (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — files.associations missing *.jinja -> html, found: {assoc}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: files.exclude patterns (0.10 points)
    # Must hide __pycache__, node_modules, .pytest_cache
    try:
        exclude = settings.get('files.exclude', {})
        required_patterns = ['**/__pycache__', '**/node_modules', '**/.pytest_cache']
        found = 0
        for pattern in required_patterns:
            if isinstance(exclude, dict) and exclude.get(pattern) is True:
                found += 1
            else:
                print(f"  DETAIL: files.exclude missing pattern: {pattern}")

        if found == len(required_patterns):
            print(f"PASS: Component 6 — files.exclude has all 3 required patterns (0.10 pts)")
            total_score += 0.10
        elif found > 0:
            partial = round(0.10 * found / len(required_patterns), 2)
            print(f"PARTIAL: Component 6 — files.exclude {found}/{len(required_patterns)} patterns ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 6 — files.exclude has 0/{len(required_patterns)} required patterns")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: search.exclude configured (0.10 points)
    # Must have at least __pycache__ and node_modules excluded from search
    try:
        search_exclude = settings.get('search.exclude', {})
        required_search = ['**/__pycache__', '**/node_modules']
        found = 0
        for pattern in required_search:
            if isinstance(search_exclude, dict) and search_exclude.get(pattern) is True:
                found += 1
            else:
                print(f"  DETAIL: search.exclude missing pattern: {pattern}")

        if found == len(required_search):
            print(f"PASS: Component 7 — search.exclude has required patterns (0.10 pts)")
            total_score += 0.10
        elif found > 0:
            partial = round(0.10 * found / len(required_search), 2)
            print(f"PARTIAL: Component 7 — search.exclude {found}/{len(required_search)} patterns ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 7 — search.exclude has 0/{len(required_search)} required patterns")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()

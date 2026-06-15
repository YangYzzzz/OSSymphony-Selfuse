"""
Reward Script: Set up .editorconfig file in project root
Task ID: vscode_lp_075
Domain: vscode
Scoring:
  Component 1 (0.15): .editorconfig exists with root = true
  Component 2 (0.35): [*] section has indent_style=space, indent_size=4, end_of_line=lf, charset=utf-8
  Component 3 (0.15): [*.py] section with indent_size=4
  Component 4 (0.20): [*.{js,ts}] section with indent_size=2
  Component 5 (0.15): [*.{yml,yaml}] section with indent_size=2
"""

import os
import configparser
import io

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_075'
EDITORCONFIG_PATH = os.path.join(WORKDIR, 'workspace', '.editorconfig')


def parse_editorconfig(file_path):
    """
    Parse .editorconfig file into a dict of sections.
    EditorConfig files are INI-like but section headers can contain
    glob patterns like [*.{js,ts}]. We use configparser with raw mode.
    """
    with open(file_path, 'r') as f:
        content = f.read()

    # configparser needs a default section or we handle it manually
    # EditorConfig has lines before any section (like root = true)
    # and section headers with glob patterns

    sections = {}
    current_section = '__preamble__'
    sections[current_section] = {}

    for line in content.splitlines():
        stripped = line.strip()
        # Skip empty lines and comments
        if not stripped or stripped.startswith('#') or stripped.startswith(';'):
            continue
        # Section header
        if stripped.startswith('[') and stripped.endswith(']'):
            current_section = stripped[1:-1].strip()
            sections[current_section] = {}
            continue
        # Key = value
        if '=' in stripped:
            key, _, value = stripped.partition('=')
            sections[current_section][key.strip().lower()] = value.strip().lower()

    return sections


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(EDITORCONFIG_PATH):
        print(f"CRITICAL: .editorconfig not found at {EDITORCONFIG_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        sections = parse_editorconfig(EDITORCONFIG_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse .editorconfig: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: .editorconfig exists with root = true (0.15 points)
    try:
        preamble = sections.get('__preamble__', {})
        if preamble.get('root') == 'true':
            print(f"PASS: Component 1 — root = true found in preamble (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — root = true not found. Preamble: {preamble}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: [*] section has default settings (0.35 points)
    # indent_style=space, indent_size=4, end_of_line=lf, charset=utf-8
    try:
        star_section = sections.get('*', {})
        expected_defaults = {
            'indent_style': 'space',
            'indent_size': '4',
            'end_of_line': 'lf',
            'charset': 'utf-8',
        }
        matches = 0
        for key, expected_val in expected_defaults.items():
            actual_val = star_section.get(key)
            if actual_val == expected_val:
                matches += 1
            else:
                print(f"  DETAIL: [*] {key} expected '{expected_val}', found '{actual_val}'")

        if matches == 4:
            print(f"PASS: Component 2 — [*] section has all 4 default settings (0.35 pts)")
            total_score += 0.35
        elif matches >= 2:
            partial = round(0.35 * (matches / 4), 2)
            print(f"PARTIAL: Component 2 — [*] section has {matches}/4 settings ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — [*] section missing or incomplete ({matches}/4)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: [*.py] section with indent_size=4 (0.15 points)
    try:
        py_section = sections.get('*.py', {})
        if py_section.get('indent_size') == '4':
            print(f"PASS: Component 3 — [*.py] indent_size = 4 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — [*.py] indent_size expected '4', found '{py_section.get('indent_size')}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: [*.{js,ts}] section with indent_size=2 (0.20 points)
    try:
        # Look for a section matching JS/TS files
        js_section = None
        for sec_name, sec_data in sections.items():
            # Accept various forms: *.{js,ts}, *.js, etc.
            sec_lower = sec_name.lower()
            if ('js' in sec_lower and 'ts' in sec_lower) or sec_lower == '*.js':
                js_section = sec_data
                break
        if js_section and js_section.get('indent_size') == '2':
            print(f"PASS: Component 4 — [*.{{js,ts}}] indent_size = 2 (0.20 pts)")
            total_score += 0.20
        else:
            found_val = js_section.get('indent_size') if js_section else None
            print(f"FAIL: Component 4 — JS/TS section indent_size expected '2', found '{found_val}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: [*.{yml,yaml}] section with indent_size=2 (0.15 points)
    try:
        yaml_section = None
        for sec_name, sec_data in sections.items():
            sec_lower = sec_name.lower()
            if ('yml' in sec_lower or 'yaml' in sec_lower) and sec_lower != '*':
                yaml_section = sec_data
                break
        if yaml_section and yaml_section.get('indent_size') == '2':
            print(f"PASS: Component 5 — [*.{{yml,yaml}}] indent_size = 2 (0.15 pts)")
            total_score += 0.15
        else:
            found_val = yaml_section.get('indent_size') if yaml_section else None
            print(f"FAIL: Component 5 — YAML section indent_size expected '2', found '{found_val}'")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(EDITORCONFIG_PATH):
    print(f"File not found: {EDITORCONFIG_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()

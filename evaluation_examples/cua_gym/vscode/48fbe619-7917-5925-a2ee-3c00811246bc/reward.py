"""
Reward Script: EditorConfig setup for ~/project
Task ID: vscode_wf_029
Domain: vscode
Scoring:
  Component 1: EditorConfig extension installed (0.20)
  Component 2: .editorconfig exists with root=true (0.15)
  Component 3: [*] section — trim_trailing_whitespace + insert_final_newline (0.20)
  Component 4: [*.{js,ts}] section — indent_style=space, indent_size=2 (0.25)
  Component 5: [*.py] section — indent_style=space, indent_size=4 (0.20)
"""

import os
import re
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_029'
EDITORCONFIG_PATH = os.path.join(WORKDIR, 'project', '.editorconfig')


def parse_editorconfig(content):
    """
    Parse .editorconfig content into a dict of sections.
    Returns: { section_header: { key: value, ... }, ... }
    e.g. { '[*]': {'trim_trailing_whitespace': 'true', ...}, ... }
    """
    sections = {}
    current_section = None
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#') or line.startswith(';'):
            continue
        # Check for section header like [*] or [*.py]
        section_match = re.match(r'^\[(.+)\]$', line)
        if section_match:
            current_section = section_match.group(1).strip()
            sections[current_section] = {}
            continue
        # Check for key=value
        if '=' in line and current_section is not None:
            key, _, value = line.partition('=')
            sections[current_section][key.strip().lower()] = value.strip().lower()
    return sections


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: EditorConfig extension installed (0.20 points)
    # Check by scanning the extensions directory on disk for editorconfig.editorconfig-*
    try:
        ext_dir = os.path.join(os.path.expanduser('~'), '.vscode', 'extensions')
        installed = os.listdir(ext_dir) if os.path.isdir(ext_dir) else []
        matching = [e for e in installed if e.lower().startswith('editorconfig.editorconfig-')]
        if len(matching) > 0:
            print(f"PASS: Component 1 -- EditorConfig extension installed: {matching[0]} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 -- EditorConfig extension not found in {ext_dir}. Contents: {installed}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Precondition: .editorconfig file must exist
    if not os.path.exists(EDITORCONFIG_PATH):
        print(f"FAIL: .editorconfig not found at {EDITORCONFIG_PATH}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    try:
        with open(EDITORCONFIG_PATH, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR: Cannot read .editorconfig: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    sections = parse_editorconfig(content)

    # Component 2: root=true is set (0.15 points)
    # root=true appears before any section or sometimes in a pseudo top-level
    try:
        has_root_true = bool(re.search(r'^\s*root\s*=\s*true\s*$', content, re.MULTILINE | re.IGNORECASE))
        if has_root_true:
            print("PASS: Component 2 -- root=true present in .editorconfig (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 2 -- root=true not found in .editorconfig")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: [*] section with trim_trailing_whitespace=true and insert_final_newline=true (0.20 points)
    try:
        star_section = sections.get('*', {})
        has_trim = star_section.get('trim_trailing_whitespace') == 'true'
        has_newline = star_section.get('insert_final_newline') == 'true'
        if has_trim and has_newline:
            print("PASS: Component 3 -- [*] has trim_trailing_whitespace=true and insert_final_newline=true (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 -- [*] section: trim_trailing_whitespace={star_section.get('trim_trailing_whitespace')}, insert_final_newline={star_section.get('insert_final_newline')}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: [*.{js,ts}] section with indent_style=space, indent_size=2 (0.25 points)
    try:
        # Find JS/TS section - could be [*.{js,ts}] or [*.js] etc.
        js_ts_section = None
        for key in sections:
            key_lower = key.lower()
            # Match patterns like *.{js,ts} or *.{ts,js}
            if 'js' in key_lower and 'ts' in key_lower:
                js_ts_section = sections[key]
                break
        if js_ts_section is None:
            print("FAIL: Component 4 -- No [*.{js,ts}] section found")
        else:
            has_style = js_ts_section.get('indent_style') == 'space'
            has_size = js_ts_section.get('indent_size') == '2'
            if has_style and has_size:
                print("PASS: Component 4 -- [*.{js,ts}] has indent_style=space, indent_size=2 (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 -- [*.{{js,ts}}] indent_style={js_ts_section.get('indent_style')}, indent_size={js_ts_section.get('indent_size')}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: [*.py] section with indent_style=space, indent_size=4 (0.20 points)
    try:
        py_section = None
        for key in sections:
            if key.lower() == '*.py':
                py_section = sections[key]
                break
        if py_section is None:
            print("FAIL: Component 5 -- No [*.py] section found")
        else:
            has_style = py_section.get('indent_style') == 'space'
            has_size = py_section.get('indent_size') == '4'
            if has_style and has_size:
                print("PASS: Component 5 -- [*.py] has indent_style=space, indent_size=4 (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 5 -- [*.py] indent_style={py_section.get('indent_style')}, indent_size={py_section.get('indent_size')}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

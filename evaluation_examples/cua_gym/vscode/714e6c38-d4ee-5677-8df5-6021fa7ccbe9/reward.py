"""
Reward Script: Create .editorconfig with specific indentation rules
Task ID: vscode_ops_054
Domain: vscode
Scoring:
  - Component 1 (0.15): File exists and root = true
  - Component 2 (0.15): Global end_of_line = lf
  - Component 3 (0.15): Global charset = utf-8
  - Component 4 (0.10): Global indent_style = space
  - Component 5 (0.225): YAML/JSON section with indent_size = 2
  - Component 6 (0.225): Python/Shell section with indent_size = 4
"""

import os
import configparser
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_054'
EDITORCONFIG_PATH = os.path.join(WORKDIR, 'infra', '.editorconfig')


def parse_editorconfig(file_path):
    """
    Parse an .editorconfig file into a dict of sections.
    .editorconfig uses INI-like format but with glob patterns as section names.
    Returns dict: section_pattern -> dict of key-value pairs.
    The 'root' key outside any section is returned under '__preamble__'.
    """
    sections = {'__preamble__': {}}
    current_section = '__preamble__'

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#') or line.startswith(';'):
                continue
            # Section header
            section_match = re.match(r'^\[(.+)\]$', line)
            if section_match:
                current_section = section_match.group(1).strip()
                if current_section not in sections:
                    sections[current_section] = {}
                continue
            # Key = value
            if '=' in line:
                key, value = line.split('=', 1)
                sections[current_section][key.strip().lower()] = value.strip().lower()

    return sections


def verify_task():
    """
    Verify .editorconfig creation with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(EDITORCONFIG_PATH):
        print(f"CRITICAL: .editorconfig not found at {EDITORCONFIG_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Parse the file
    try:
        sections = parse_editorconfig(EDITORCONFIG_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse .editorconfig: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: root = true in preamble (0.15 points)
    try:
        preamble = sections.get('__preamble__', {})
        if preamble.get('root') == 'true':
            print(f"PASS: Component 1 — root = true found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — expected root = true, found: {preamble.get('root')}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Find the global [*] section
    global_section = sections.get('*', {})

    # Component 2: end_of_line = lf in global section (0.15 points)
    try:
        eol = global_section.get('end_of_line')
        if eol == 'lf':
            print(f"PASS: Component 2 — end_of_line = lf (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — expected end_of_line = lf, found: {eol}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: charset = utf-8 in global section (0.15 points)
    try:
        charset = global_section.get('charset')
        if charset == 'utf-8':
            print(f"PASS: Component 3 — charset = utf-8 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — expected charset = utf-8, found: {charset}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: indent_style = space in global section (0.10 points)
    try:
        indent_style = global_section.get('indent_style')
        if indent_style == 'space':
            print(f"PASS: Component 4 — indent_style = space in global (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — expected indent_style = space, found: {indent_style}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: YAML/JSON section with indent_size = 2 (0.225 points)
    # Look for a section matching yml/yaml/json patterns
    try:
        yaml_json_section = None
        for key in sections:
            # Match sections like *.{yml,yaml,json} or similar patterns
            if key != '__preamble__' and key != '*':
                key_lower = key.lower()
                if ('yml' in key_lower or 'yaml' in key_lower) and 'json' in key_lower:
                    yaml_json_section = sections[key]
                    break

        if yaml_json_section is None:
            print(f"FAIL: Component 5 — No YAML/JSON section found")
        else:
            indent_size = yaml_json_section.get('indent_size')
            indent_style_yj = yaml_json_section.get('indent_style', global_section.get('indent_style'))
            if indent_size == '2' and indent_style_yj == 'space':
                print(f"PASS: Component 5 — YAML/JSON indent_size = 2, indent_style = space (0.225 pts)")
                total_score += 0.225
            elif indent_size == '2':
                print(f"PARTIAL: Component 5 — indent_size correct but indent_style = {indent_style_yj} (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 5 — expected indent_size = 2, found: {indent_size}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Python/Shell section with indent_size = 4 (0.225 points)
    try:
        py_sh_section = None
        for key in sections:
            if key != '__preamble__' and key != '*':
                key_lower = key.lower()
                if 'py' in key_lower and 'sh' in key_lower:
                    py_sh_section = sections[key]
                    break

        if py_sh_section is None:
            print(f"FAIL: Component 6 — No Python/Shell section found")
        else:
            indent_size = py_sh_section.get('indent_size')
            indent_style_ps = py_sh_section.get('indent_style', global_section.get('indent_style'))
            if indent_size == '4' and indent_style_ps == 'space':
                print(f"PASS: Component 6 — Python/Shell indent_size = 4, indent_style = space (0.225 pts)")
                total_score += 0.225
            elif indent_size == '4':
                print(f"PARTIAL: Component 6 — indent_size correct but indent_style = {indent_style_ps} (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 6 — expected indent_size = 4, found: {indent_size}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()

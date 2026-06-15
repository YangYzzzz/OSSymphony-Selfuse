"""
Reward Script: Create .editorconfig in web-project root
Task ID: vscode_file_062
Domain: vs_code
Scoring:
  - Component 1: root = true directive present (0.2 pts)
  - Component 2: charset = utf-8 in [*] section (0.2 pts)
  - Component 3: end_of_line = lf in [*] section (0.2 pts)
  - Component 4: indent_style = space in [*] section (0.2 pts)
  - Component 5: indent_size = 2 in [*] section (0.2 pts)
  Total: 1.0

The task requires creating /home/user/web-project/.editorconfig with:
  root = true
  [*]
  charset = utf-8
  end_of_line = lf
  indent_style = space
  indent_size = 2
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_062'

EDITORCONFIG_PATH = os.path.join(WORKDIR, 'web-project', '.editorconfig')


def parse_editorconfig(content):
    """
    Parse .editorconfig content into a dict of sections.
    Returns: dict like {'root': 'true', '*': {'charset': 'utf-8', ...}}
    """
    result = {}
    current_section = None

    for line in content.splitlines():
        # Strip whitespace and ignore comments/empty lines
        stripped = line.strip()
        if not stripped or stripped.startswith('#') or stripped.startswith(';'):
            continue

        # Section header
        section_match = re.match(r'^\[(.+)\]$', stripped)
        if section_match:
            current_section = section_match.group(1)
            if current_section not in result:
                result[current_section] = {}
            continue

        # Key-value pair
        kv_match = re.match(r'^(\w+)\s*=\s*(.+)$', stripped)
        if kv_match:
            key = kv_match.group(1).lower().strip()
            value = kv_match.group(2).strip().lower()
            if current_section is None:
                # Global (before any section)
                result[key] = value
            else:
                result[current_section][key] = value

    return result


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Checks that .editorconfig was created with the required content.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist to score anything
    if not os.path.exists(file_path):
        print(f"FAIL: .editorconfig not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"INFO: .editorconfig found at {file_path}")
        print(f"INFO: Content:\n{content}")
    except Exception as e:
        print(f"CRITICAL: Cannot read .editorconfig: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse the .editorconfig
    try:
        parsed = parse_editorconfig(content)
        print(f"INFO: Parsed config: {parsed}")
    except Exception as e:
        print(f"ERROR: Failed to parse .editorconfig: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: root = true (0.2 points)
    # This verifies the file was set up as the root editorconfig
    try:
        root_val = parsed.get('root', None)
        if root_val is not None and root_val.strip().lower() == 'true':
            print(f"PASS: Component 1 — root = true found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — expected root = true, found: {root_val}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Get the [*] section (applies to all files)
    star_section = parsed.get('*', {})

    # Component 2: charset = utf-8 (0.2 points)
    try:
        charset_val = star_section.get('charset', None)
        if charset_val is not None and charset_val.strip().lower() == 'utf-8':
            print(f"PASS: Component 2 — charset = utf-8 found in [*] section (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — expected charset = utf-8 in [*], found: {charset_val}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: end_of_line = lf (0.2 points)
    try:
        eol_val = star_section.get('end_of_line', None)
        if eol_val is not None and eol_val.strip().lower() == 'lf':
            print(f"PASS: Component 3 — end_of_line = lf found in [*] section (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — expected end_of_line = lf in [*], found: {eol_val}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: indent_style = space (0.2 points)
    try:
        indent_style_val = star_section.get('indent_style', None)
        if indent_style_val is not None and indent_style_val.strip().lower() == 'space':
            print(f"PASS: Component 4 — indent_style = space found in [*] section (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — expected indent_style = space in [*], found: {indent_style_val}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: indent_size = 2 (0.2 points)
    try:
        indent_size_val = star_section.get('indent_size', None)
        # Compare as string (parsed values are stored as strings)
        if indent_size_val is not None and str(indent_size_val).strip() == '2':
            print(f"PASS: Component 5 — indent_size = 2 found in [*] section (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 5 — expected indent_size = 2 in [*], found: {indent_size_val}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = EDITORCONFIG_PATH
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

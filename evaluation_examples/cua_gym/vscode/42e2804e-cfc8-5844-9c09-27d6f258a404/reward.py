"""
Reward Script: Fix .editorconfig indent_style conflict with VSCode settings
Task ID: vscode_fix_083
Domain: vscode
Scoring:
  Component 1 (0.6): indent_style = space in [*] section of .editorconfig
  Component 2 (0.4): indent_style = tab NOT present in [*] section (old conflict removed)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_083'
EDITORCONFIG_PATH = os.path.join(WORKDIR, 'project', '.editorconfig')


def parse_editorconfig_section(content, section_name='*'):
    """
    Parse an .editorconfig file and return the key-value pairs for a given section.
    Returns a dict of {key: value} for the specified section.
    """
    result = {}
    in_section = False
    section_pattern = re.compile(r'^\[' + re.escape(section_name) + r'\]\s*$')

    for line in content.splitlines():
        stripped = line.strip()
        # Skip comments and blank lines
        if not stripped or stripped.startswith('#') or stripped.startswith(';'):
            continue
        # Check for section header
        if stripped.startswith('['):
            in_section = bool(section_pattern.match(stripped))
            continue
        # If we're in the target section, parse key=value
        if in_section and '=' in stripped:
            key, _, value = stripped.partition('=')
            result[key.strip().lower()] = value.strip().lower()

    return result


def verify_task():
    """
    Verify that the .editorconfig indent_style conflict has been resolved.
    The fix should change indent_style from 'tab' to 'space' in the [*] section.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: .editorconfig file must exist
    if not os.path.isfile(EDITORCONFIG_PATH):
        print(f"CRITICAL: .editorconfig not found at {EDITORCONFIG_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(EDITORCONFIG_PATH, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read .editorconfig: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse the [*] section
    try:
        star_section = parse_editorconfig_section(content, '*')
        print(f"INFO: [*] section keys: {star_section}")
    except Exception as e:
        print(f"CRITICAL: Cannot parse .editorconfig: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: indent_style is set to 'space' in [*] section (0.6 points)
    # This FAILS on initial_env (indent_style = tab) and PASSES on golden_env (indent_style = space)
    try:
        indent_style = star_section.get('indent_style', None)
        if indent_style == 'space':
            print(f"PASS: Component 1 — indent_style = 'space' in [*] section (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — expected indent_style='space' in [*], found: '{indent_style}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: indent_style = tab is NOT present in [*] section (0.4 points)
    # This FAILS on initial_env (indent_style = tab is present) and PASSES on golden_env (tab replaced by space)
    try:
        indent_style = star_section.get('indent_style', None)
        if indent_style is not None and indent_style != 'tab':
            print(f"PASS: Component 2 — indent_style is '{indent_style}', not 'tab' — conflict resolved (0.4 pts)")
            total_score += 0.4
        elif indent_style == 'tab':
            print(f"FAIL: Component 2 — indent_style is still 'tab', conflict NOT resolved")
        else:
            print(f"FAIL: Component 2 — indent_style key not found in [*] section")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

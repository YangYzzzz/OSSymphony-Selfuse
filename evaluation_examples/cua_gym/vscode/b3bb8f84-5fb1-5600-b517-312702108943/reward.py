"""
Reward Script: Toggle line comments on CSS dark theme rules
Task ID: vscode_code_032
Domain: vs_code
Scoring:
  Component 1: .dark-theme selector line is commented out (0.5 pts)
  Component 2: All 5 CSS property lines inside dark-theme block are commented out AND
               light theme (:root) is still active (0.5 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_032'
FILE_PATH = f'{WORKDIR}/web/theme.css'


def is_line_commented(stripped_line):
    """Return True if the given stripped line starts with a CSS line comment marker."""
    return stripped_line.startswith('//') or stripped_line.startswith('/*')


def get_content_under_comment(stripped_line):
    """Strip leading comment markers to get the actual content."""
    if stripped_line.startswith('//'):
        return stripped_line[2:].strip()
    if stripped_line.startswith('/*') and stripped_line.endswith('*/'):
        return stripped_line[2:-2].strip()
    return stripped_line


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    The task is to comment out the entire .dark-theme CSS block (lines 9-15)
    while leaving the :root (light theme) block unchanged.
    VSCode Ctrl+/ produces '//' style line comments in CSS files.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Read the file content
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        lines = content.splitlines()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: verify file is not empty and has expected structure
    if len(lines) < 10:
        print(f"FAIL: File too short ({len(lines)} lines), expected at least 15 lines")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: The .dark-theme selector line is commented out (0.5 points)
    # In the golden file, the .dark-theme { line should start with '//' or be wrapped in /* */
    # This FAILS on initial (selector is active) and PASSES on golden (selector is commented)
    try:
        comp1_result = "not_found"  # possible values: "not_found", "commented", "active"
        for line in lines:
            stripped = line.strip()
            if '.dark-theme' in stripped:
                if is_line_commented(stripped):
                    comp1_result = "commented"
                else:
                    comp1_result = "active"
                break

        if comp1_result == "commented":
            for line in lines:
                if '.dark-theme' in line.strip():
                    print(f"PASS: Component 1 - .dark-theme selector is commented out: '{line.strip()}' (0.5 pts)")
                    break
            total_score += 0.5
        elif comp1_result == "active":
            for line in lines:
                if '.dark-theme' in line.strip():
                    print(f"FAIL: Component 1 - .dark-theme selector is NOT commented out: '{line.strip()}'")
                    break
        else:
            print("FAIL: Component 1 - .dark-theme selector line not found in file")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: All 5 CSS property lines inside the dark-theme block are commented out,
    # AND the light theme (:root) section is still active/unchanged (0.5 points)
    # Expected dark-theme properties with their golden values (unique to dark theme):
    expected_dark_props_values = [
        '--bg-color: #1a1a2e',                 # dark theme bg (distinct from light #ffffff)
        '--text-color: #e0e0e0',               # dark theme text (distinct from light #333333)
        '--accent-color: #4da6ff',             # dark theme accent (distinct from light #0066cc)
        '--border-color: #333355',             # dark theme only property
        '--shadow-color: rgba(0, 0, 0, 0.3)', # dark theme only property
    ]
    # Expected light-theme properties (must remain active in :root block)
    expected_light_props = [
        '--bg-color: #ffffff',
        '--text-color: #333333',
        '--accent-color: #0066cc',
    ]
    try:
        # Find the start of the .dark-theme block (selector line, whether commented or not)
        dark_start_idx = None
        for i, line in enumerate(lines):
            stripped = line.strip()
            if '.dark-theme' in stripped:
                dark_start_idx = i
                break

        if dark_start_idx is None:
            print("FAIL: Component 2 - .dark-theme block not found")
        else:
            # Collect all lines from dark_start_idx until closing }
            dark_block_lines = []
            for j in range(dark_start_idx, len(lines)):
                dark_block_lines.append(lines[j])
                # Check if this line contains the closing brace (possibly commented)
                raw = get_content_under_comment(lines[j].strip())
                if raw == '}':
                    break

            # Check each expected property in the dark block is commented out
            props_commented = []
            props_issues = []

            for expected_prop in expected_dark_props_values:
                prop_status = "missing"
                for line in dark_block_lines:
                    stripped = line.strip()
                    # Strip comment markers to see the actual content
                    content_part = get_content_under_comment(stripped)

                    # IMPORTANT: Check comment status FIRST, then check if property is present
                    if is_line_commented(stripped) and expected_prop in content_part:
                        # Property found UNDER a comment marker - it IS commented out
                        prop_status = "commented"
                        break
                    elif not is_line_commented(stripped) and expected_prop in stripped:
                        # Property found WITHOUT a comment marker - it is ACTIVE (not commented)
                        prop_status = "active"
                        break

                if prop_status == "commented":
                    props_commented.append(expected_prop.split(':')[0])
                elif prop_status == "active":
                    props_issues.append(expected_prop.split(':')[0] + ' [ACTIVE - not commented]')
                else:
                    props_issues.append(expected_prop.split(':')[0] + ' [MISSING]')

            all_dark_props_commented = (len(props_commented) == len(expected_dark_props_values)
                                        and len(props_issues) == 0)

            # Verify light theme :root is still active and unchanged
            root_start_idx = None
            for i, line in enumerate(lines):
                stripped = line.strip()
                if ':root' in stripped and not is_line_commented(stripped):
                    root_start_idx = i
                    break

            light_props_ok = False
            if root_start_idx is not None:
                root_block_lines = []
                for j in range(root_start_idx, len(lines)):
                    root_block_lines.append(lines[j])
                    if lines[j].strip() == '}':
                        break

                light_count = 0
                for expected_prop in expected_light_props:
                    for line in root_block_lines:
                        stripped = line.strip()
                        if expected_prop in stripped and not is_line_commented(stripped):
                            light_count += 1
                            break
                light_props_ok = (light_count == len(expected_light_props))

            # Both conditions must hold for Component 2
            if all_dark_props_commented and light_props_ok:
                print(f"PASS: Component 2 - All {len(expected_dark_props_values)} dark-theme properties commented out AND light theme remains active (0.5 pts)")
                total_score += 0.5
            elif all_dark_props_commented and not light_props_ok:
                print(f"FAIL: Component 2 - Dark props commented but light theme (:root) was modified or missing")
            elif not all_dark_props_commented and light_props_ok:
                print(f"FAIL: Component 2 - {len(props_commented)}/{len(expected_dark_props_values)} dark properties commented, light theme OK")
                print(f"  Commented: {props_commented}")
                print(f"  Issues: {props_issues}")
            else:
                print(f"FAIL: Component 2 - {len(props_commented)}/{len(expected_dark_props_values)} dark properties commented, light theme also modified")
                print(f"  Dark prop issues: {props_issues}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

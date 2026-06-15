"""
Reward Script: Re-indent entire HTML file to fix inconsistent indentation
Task ID: vscode_edit_061
Domain: vs_code
Scoring:
  Component 1: No tab characters remain in file (0.3 pts)
  Component 2: All indented lines use multiples of 4 spaces, no mixed indentation (0.4 pts)
  Component 3: Top-level HTML nesting is correct - root elements at 0, direct children at 4 spaces (0.3 pts)

  Note: Content preservation is a precondition gate (fails early if key content missing), not a scoring component.
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_061'
FILE_PATH = '/home/user/Desktop/messy.html'


def verify_task(file_path):
    """
    Verify that messy.html has been re-indented with consistent 4-space indentation.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the file — precondition gate
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            lines = content.splitlines()
        print(f"INFO: Loaded {file_path} — {len(lines)} lines")
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: file must not be empty
    if not content.strip():
        print("CRITICAL: File is empty")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: HTML content must be preserved (text content only, not formatting)
    # If key content is gone, file may have been corrupted — return 0.0 as a gate
    key_markers = [
        "Online Bookstore - Featured Titles",
        "The Midnight Library",
        "by Matt Haig",
        "Educated",
        "Categories",
    ]
    for marker in key_markers:
        if marker not in content:
            print(f"CRITICAL GATE: Key content '{marker}' missing — file may be corrupted")
            print("REWARD: 0.0")
            return 0.0
    print(f"INFO: Content gate passed — all key HTML content markers present")

    # Component 1: No tab characters remain in the file (0.3 points)
    # Initial file has tabs from inconsistent indentation; after proper re-indentation
    # with spaces, all tab characters must be eliminated
    try:
        tab_lines = [i + 1 for i, line in enumerate(lines) if '\t' in line]
        if len(tab_lines) == 0:
            print(f"PASS: Component 1 — No tab characters found in file (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Found {len(tab_lines)} lines with tab characters: lines {tab_lines[:5]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All indented lines use multiples of 4 spaces only (0.4 points)
    # Initial file has 2-space, 6-space, and mixed tab+space indentation.
    # After re-indentation, every indented line's leading whitespace count
    # must be a multiple of 4 (4, 8, 12, 16, 20...) — no 2-space, 3-space, 6-space, etc.
    try:
        non_multiple_lines = []
        for i, line in enumerate(lines, 1):
            if not line.strip():
                # Skip blank lines
                continue
            # Check leading spaces (after Component 1 ensures no tabs remain)
            leading = len(line) - len(line.lstrip(' '))
            if leading > 0 and leading % 4 != 0:
                non_multiple_lines.append((i, leading, line[:40]))

        if len(non_multiple_lines) == 0:
            print(f"PASS: Component 2 — All indented lines use multiples of 4 spaces (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — {len(non_multiple_lines)} lines with non-4-multiple indentation:")
            for lineno, indent, snippet in non_multiple_lines[:5]:
                print(f"  Line {lineno}: {indent} spaces — '{snippet}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Top-level HTML nesting uses correct indentation depth (0.3 points)
    # After proper re-indentation, the structural HTML elements must be at correct depths:
    # - <!DOCTYPE html> and <html>, <head>, <body> tags at indent level 0
    # - Direct children of <head>: <meta>, <title>, <link> at indent level 4
    # - Direct children of <body>: <header>, <main>, <footer> at indent level 4
    # In the initial file, these are at wrong levels (e.g., header at 0, meta at 2)
    try:
        nesting_issues = []

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped:
                continue
            leading = len(line) - len(line.lstrip(' '))

            # Root-level tags must be at indent 0
            if re.match(r'^<(!DOCTYPE|html|head|body)[\s>]', stripped, re.IGNORECASE):
                if leading != 0:
                    nesting_issues.append(f"Line {i}: '{stripped[:30]}' at indent {leading}, expected 0")

            # Direct head children must be at indent 4
            elif re.match(r'^<(meta|title|link)\b', stripped, re.IGNORECASE):
                if leading != 4:
                    nesting_issues.append(f"Line {i}: '{stripped[:30]}' at indent {leading}, expected 4")

            # Direct body children (semantic block elements) must be at indent 4
            elif re.match(r'^<(header|main|footer|/header|/main|/footer)\b', stripped, re.IGNORECASE):
                if leading != 4:
                    nesting_issues.append(f"Line {i}: '{stripped[:30]}' at indent {leading}, expected 4")

        if len(nesting_issues) == 0:
            print(f"PASS: Component 3 — Top-level HTML nesting is correct (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — {len(nesting_issues)} nesting issues found:")
            for issue in nesting_issues[:5]:
                print(f"  {issue}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

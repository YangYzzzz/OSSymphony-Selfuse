"""
Reward Script: Use Save All in VSCode to save three currently open files with unsaved changes.
Task ID: vscode_edit_057
Domain: vs_code
Scoring:
  Component 1: ~/Desktop/file1.py contains the 'retry' function (unsaved change saved)  — 0.35 pts
  Component 2: ~/Desktop/file2.js contains the 'buildPieChart' function (unsaved change saved) — 0.35 pts
  Component 3: ~/Desktop/file3.html contains the '<nav>' navigation element (unsaved change saved) — 0.30 pts
  Total: 1.0

Verification strategy:
  The task asks the agent to use VSCode's "Save All" command to commit unsaved editor changes to
  disk for all three files. Each file had specific new content in the editor buffer that had not
  been written to disk yet (evidenced by the unsaved indicator dot on each tab).

  The golden env shows the expected saved state: each file contains content additions that were
  present in the editor but absent on disk in the initial env. We verify by checking for the
  presence of these unique golden markers in the on-disk files.

  Markers that distinguish saved (golden) from unsaved (initial):
    file1.py : presence of 'def retry(' — the retry helper function added to the editor
    file2.js : presence of 'buildPieChart' — the pie-chart builder function added to the editor
    file3.html: presence of '<nav>' — the navigation bar block added to the editor

  These markers are absent in the initial_env on-disk files and present in the golden_env
  on-disk files, making them valid task-change signals.
"""

import os

WORKDIR = '/home/user/Desktop'

FILE1 = os.path.join(WORKDIR, 'file1.py')
FILE2 = os.path.join(WORKDIR, 'file2.js')
FILE3 = os.path.join(WORKDIR, 'file3.html')


def verify_task():
    """
    Verify that all three files were saved via Save All.
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Precondition gate: all three files must exist on disk
    for path in [FILE1, FILE2, FILE3]:
        if not os.path.exists(path):
            print(f"CRITICAL: Required file not found: {path}")
            print("REWARD: 0.0")
            return 0.0

    # Component 1: file1.py contains the 'retry' helper function (0.35 points)
    # The editor had an unsaved addition of a 'retry' utility function and type hints.
    # After Save All, this function must appear in the on-disk file.
    try:
        with open(FILE1, 'r', encoding='utf-8') as f:
            content_py = f.read()
        if 'def retry(' in content_py:
            print(f"PASS: Component 1 — file1.py contains 'def retry(' function (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — file1.py does not contain 'def retry('; Save All may not have been used.")
    except Exception as e:
        print(f"ERROR: Component 1 — could not read file1.py: {e}")

    # Component 2: file2.js contains the 'buildPieChart' function (0.35 points)
    # The editor had an unsaved addition of a buildPieChart builder function.
    # After Save All, this function must appear in the on-disk file.
    try:
        with open(FILE2, 'r', encoding='utf-8') as f:
            content_js = f.read()
        if 'buildPieChart' in content_js:
            print(f"PASS: Component 2 — file2.js contains 'buildPieChart' function (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — file2.js does not contain 'buildPieChart'; Save All may not have been used.")
    except Exception as e:
        print(f"ERROR: Component 2 — could not read file2.js: {e}")

    # Component 3: file3.html contains the '<nav>' navigation element (0.30 points)
    # The editor had an unsaved addition of a <nav> navigation block.
    # After Save All, this element must appear in the on-disk file.
    try:
        with open(FILE3, 'r', encoding='utf-8') as f:
            content_html = f.read()
        if '<nav>' in content_html:
            print(f"PASS: Component 3 — file3.html contains '<nav>' element (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — file3.html does not contain '<nav>'; Save All may not have been used.")
    except Exception as e:
        print(f"ERROR: Component 3 — could not read file3.html: {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

"""
Reward Script: Export PDF bookmarks to text file with hierarchy
Task ID: pdf_mbc_036
Domain: pdf
Scoring:
  Component 1 (0.2): bookmarks_list.txt exists
  Component 2 (0.4): All 6 bookmark names present
  Component 3 (0.4): Correct indentation hierarchy
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_036'

# Expected bookmarks from the PDF TOC (level, title)
EXPECTED_BOOKMARKS = [
    (1, 'Introduction'),
    (1, 'Getting Started'),
    (2, 'Installation'),
    (2, 'Configuration'),
    (1, 'Advanced Usage'),
    (1, 'FAQ'),
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: bookmarks_list.txt exists and is non-empty (0.2 points)
    try:
        if os.path.exists(file_path):
            content = open(file_path, 'r').read()
            if len(content.strip()) > 0:
                print(f"PASS: Component 1 — bookmarks_list.txt exists and is non-empty ({len(content)} bytes) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 — bookmarks_list.txt exists but is empty")
        else:
            print(f"FAIL: Component 1 — bookmarks_list.txt not found at {file_path}")
            # If file doesn't exist, nothing else to check
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Parse the file into lines for further checks
    try:
        content = open(file_path, 'r').read()
        lines = [line for line in content.split('\n') if line.strip()]
    except Exception as e:
        print(f"ERROR: Could not read file for further checks: {e}")
        lines = []

    # Component 2: All 6 bookmark names are present in the file (0.4 points)
    # Each bookmark name found earns partial credit
    try:
        expected_names = [title for _, title in EXPECTED_BOOKMARKS]
        found_count = 0
        for name in expected_names:
            # Check if the bookmark name appears in any line (stripped)
            if any(name == line.strip() for line in lines):
                found_count += 1
            else:
                print(f"FAIL: Component 2 — bookmark '{name}' not found in file")

        if found_count == len(expected_names):
            print(f"PASS: Component 2 — all {found_count}/{len(expected_names)} bookmark names present (0.4 pts)")
            total_score += 0.4
        elif found_count > 0:
            partial = 0.4 * (found_count / len(expected_names))
            print(f"PARTIAL: Component 2 — {found_count}/{len(expected_names)} bookmark names present ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — no expected bookmark names found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct indentation hierarchy (0.4 points)
    # Level 1 bookmarks should have no leading whitespace
    # Level 2 bookmarks should be indented (at least 1 space/tab)
    try:
        hierarchy_correct = 0
        total_checks = len(EXPECTED_BOOKMARKS)

        for level, name in EXPECTED_BOOKMARKS:
            # Find the line containing this bookmark name
            matching_line = None
            for line in lines:
                if line.strip() == name:
                    matching_line = line
                    break

            if matching_line is None:
                print(f"FAIL: Component 3 — cannot check hierarchy for '{name}' (not found)")
                continue

            # Check indentation
            leading_spaces = len(matching_line) - len(matching_line.lstrip())

            if level == 1 and leading_spaces == 0:
                # Top-level: should NOT be indented
                hierarchy_correct += 1
            elif level == 2 and leading_spaces > 0:
                # Sub-level: should be indented
                hierarchy_correct += 1
            else:
                expected_indent = "no indentation" if level == 1 else "some indentation"
                print(f"FAIL: Component 3 — '{name}' has {leading_spaces} spaces, expected {expected_indent}")

        if hierarchy_correct == total_checks:
            print(f"PASS: Component 3 — all {hierarchy_correct}/{total_checks} hierarchy checks correct (0.4 pts)")
            total_score += 0.4
        elif hierarchy_correct > 0:
            partial = 0.4 * (hierarchy_correct / total_checks)
            print(f"PARTIAL: Component 3 — {hierarchy_correct}/{total_checks} hierarchy checks correct ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — no hierarchy checks passed")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/Documents/bookmarks_list.txt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

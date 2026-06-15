"""
FINAL REWARD SCRIPT - SUCCESS
Task: I'm updating /home/user/projects/backup.py and need to shift the indentation of lines 14-21 one tab to the right—what’s the quickest way to do that in VS Code?
Generated: 2025-09-11 19:53:55
Status: success
Model: azure-o3
Total Steps: 19
"""

import re
from pathlib import Path

"""
Reward Script: verify_backup_indentation.py

This script verifies the completion of the VS Code task:
“Shift the indentation of lines 14-21 in /home/user/projects/backup.py one tab to the right.”

Scoring Logic (progressive, 0.0 – 1.0):
• 0.1 point for every target line (14-21) that now starts with at least TWO leading TABs (max 0.8).
• +0.2 bonus if ALL target lines start with EXACTLY two leading TABs (perfect shift).
  → Maximum possible score = 1.0.

The script prints diagnostic information for every checked line, then outputs
“REWARD: X.X”.  It returns the same float value.
"""

TARGET_FILE = Path('/home/user/projects/backup.py')
START_LINE = 14  # inclusive (1-based)
END_LINE   = 21  # inclusive (1-based)


def count_leading_tabs(line: str) -> int:
    """Return the number of leading TAB characters in *line*."""
    match = re.match(r'^(\t*)', line)
    return len(match.group(1)) if match else 0


def verify_task() -> float:
    print(f"Checking task completion for {TARGET_FILE} …")

    # 1 – File existence check (natural condition, but needed for further tests)
    if not TARGET_FILE.exists():
        print("✗ Target Python file does not exist – task incomplete.")
        print("REWARD: 0.0")
        return 0.0

    # 2 – Load file and basic sanity
    lines = TARGET_FILE.read_text().splitlines()
    total_lines = len(lines)
    print(f"File loaded: {total_lines} total lines")

    if total_lines < END_LINE:
        print(f"✗ File has fewer than {END_LINE} lines – cannot verify target range.")
        print("REWARD: 0.0")
        return 0.0

    # 3 – Evaluate indentation for each target line
    atleast_two = 0  # lines with ≥2 tabs
    exact_two   = 0  # lines with exactly 2 tabs

    for idx in range(START_LINE - 1, END_LINE):  # convert to 0-based
        line_no   = idx + 1
        line      = lines[idx]
        tab_count = count_leading_tabs(line)
        preview   = line.replace('\t', '<TAB>')[:60]
        print(f"Line {line_no:>2}: tabs={tab_count} | {preview!r}")

        if tab_count >= 2:
            atleast_two += 1
        if tab_count == 2:
            exact_two += 1

    target_total = END_LINE - START_LINE + 1  # expected 8 lines

    # 4 – Progressive scoring
    score = atleast_two * 0.1  # up to 0.8

    # Bonus for perfect execution (all lines shifted to exactly two tabs)
    if atleast_two == target_total and exact_two == target_total:
        print("✓ All target lines have exactly TWO leading tabs – perfect shift.")
        score += 0.2
    elif atleast_two == target_total:
        print("✓ All target lines have at least TWO leading tabs – extra indentation confirmed.")
    else:
        print(f"Partial success: {atleast_two}/{target_total} lines shifted by at least one additional tab.")

    final_score = round(min(score, 1.0), 2)
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification when run directly
if __name__ == "__main__":
    verify_task()

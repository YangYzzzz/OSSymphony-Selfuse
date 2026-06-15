"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m cleaning up my Python script at /home/user/scripts/data_cleaner.py, and the code block on lines 15–25 is indented one level too deep—could you move those lines back by a single tab?
Generated: 2025-09-11 12:19:33
Status: success
Model: azure-o3
Total Steps: 11
"""

import os
import sys
from typing import List


def _indentation_in_spaces(line: str) -> int:
    """Return the indentation of *line* in **spaces** (tab = 4 spaces)."""
    spaces = 0
    for ch in line:
        if ch == "\t":
            spaces += 4
        elif ch == " ":
            spaces += 1
        else:
            break
    return spaces


def verify_indentation(file_path: str) -> float:
    """Progressively verify that lines 15–25 are dedented by one level.

    Scoring (progressive):
      • 0.5 – all non-blank lines in 15-25 share the same indent.
      • 0.5 – that indent equals the indent of the nearest preceding
        non-blank line (i.e. the block now aligns with surrounding code).

    Prints diagnostics and final score as:  REWARD: <score>
    """
    MAX_SCORE = 1.0
    score = 0.0

    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines: List[str] = f.readlines()

    start_idx, end_idx = 14, 25  # zero-based; covers lines 15-25 inclusive

    # Gather indentation for each non-blank line in the target block
    indents: List[int] = []
    for i in range(start_idx, min(end_idx, len(lines))):
        text = lines[i]
        if text.strip():  # non-blank
            indents.append(_indentation_in_spaces(text))

    if not indents:
        print("✗ No non-blank lines between lines 15-25; cannot verify.")
        print("REWARD: 0.0")
        return 0.0

    # Criterion 1 – internal consistency ---------------------------------
    if min(indents) == max(indents):
        print("✓ All lines in the target block share the same indentation level.")
        score += 0.5
    else:
        print("✗ Inconsistent indentation within the target block:", indents)

    # Determine reference indentation from the preceding code -------------
    reference_indent = 0
    for i in range(start_idx - 1, -1, -1):   # search upward
        if lines[i].strip():
            reference_indent = _indentation_in_spaces(lines[i])
            break

    block_indent = min(indents)
    print(f"Reference indent (preceding code): {reference_indent} spaces")
    print(f"Target block indent             : {block_indent} spaces")

    # Criterion 2 – correct alignment -------------------------------------
    if block_indent == reference_indent and min(indents) == max(indents):
        print("✓ Target block is perfectly aligned with surrounding code.")
        score += 0.5
    else:
        print("✗ Target block is not aligned with surrounding code.")

    final_score = min(score, MAX_SCORE)
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    default_path = "/home/user/scripts/data_cleaner.py"
    path = sys.argv[1] if len(sys.argv) > 1 else default_path
    verify_indentation(path)

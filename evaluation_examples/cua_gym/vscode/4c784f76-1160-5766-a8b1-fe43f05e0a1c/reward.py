"""
FINAL REWARD SCRIPT - SUCCESS
Task: While cleaning up /home/user/portfolio/style.css, I noticed the first five lines sit too far left—could you shift their indent three spaces to the right so they align with the rest of the file?
Generated: 2025-09-11 14:45:02
Status: success
Model: azure-o3
Total Steps: 15
"""

import os
import re
import sys

# Reward script for verifying indentation fix in /home/user/portfolio/style.css
# ---------------------------------------------------------------------------
# Scoring rules
#   • 5 lines to verify (lines 1-5 of the file)
#   • 0.2 points per line that starts with EXACTLY three spaces and then a non-space
#   • Total score ∈ [0.0, 1.0]
# ---------------------------------------------------------------------------

MAX_SCORE = 1.0
LINES_TO_CHECK = 5
SCORE_PER_LINE = MAX_SCORE / LINES_TO_CHECK  # 0.2 each

# Regex: ^   (exactly three spaces) followed by a non-space character OR end-of-line
PATTERN = re.compile(r"^ {3}(\S|$)")

def verify_task(file_path: str = "/home/user/portfolio/style.css") -> float:
    """Verify that the first five lines of the CSS file start with exactly
    three spaces followed by a non-space character.

    Returns a float between 0.0 and 1.0 with progressive scoring.
    """

    print(f"Checking CSS indentation for: {file_path}")

    # 0 points if the target file is missing (natural prerequisite – no credit)
    if not os.path.isfile(file_path):
        print(f"✗ File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Read the first five lines (pad with "" if file shorter)
    first_lines = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as fh:
        for _ in range(LINES_TO_CHECK):
            first_lines.append(fh.readline())

    print(">>> Evaluating indentation of first five lines (expecting exactly 3 leading spaces)")

    correct = 0
    for idx, line in enumerate(first_lines, start=1):
        if line == "":
            print(f"  Line {idx}: <missing> ✗ (file shorter than {LINES_TO_CHECK} lines)")
            continue

        # Diagnostic ‑ count leading spaces
        stripped = line.rstrip("\n")
        leading_spaces = len(stripped) - len(stripped.lstrip(" "))

        if PATTERN.match(line):
            correct += 1
            print(f"  Line {idx}: ✓ Correct ({leading_spaces} spaces) -> {repr(stripped)}")
        else:
            print(f"  Line {idx}: ✗ Incorrect ({leading_spaces} spaces) -> {repr(stripped)}")

    # Progressive score
    total_score = round(correct * SCORE_PER_LINE, 2)
    print(f"Total correctly indented lines: {correct}/{LINES_TO_CHECK}")
    print(f"REWARD: {total_score}")
    return total_score

# ---------------------------------------------------------------------------
# Execute verification when run as a script
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    verify_task()


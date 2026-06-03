"""
FINAL REWARD SCRIPT - SUCCESS
Task: I'm tidying up /home/user/project/main.py; can you help me add two extra spaces of indentation to lines 11 through 17 so they line up with the rest of the block?
Generated: 2025-09-11 19:51:36
Status: success
Model: azure-o3
Total Steps: 16
"""

import sys
from pathlib import Path


def _leading_space_count(line: str) -> int:
    """Return the indentation width of a line in *spaces*.
    Tabs are treated as 4 spaces so mixed-indent files are handled reasonably."""
    count = 0
    for ch in line:
        if ch == " ":
            count += 1
        elif ch == "\t":
            count += 4  # treat tab as 4 spaces
        else:
            break
    return count


def verify_task(target_file: str = "/home/user/project/main.py") -> float:
    """Progressively verify that lines 11-17 have the same indentation as the
    surrounding block (i.e. two extra spaces were added).

    Scoring:
        – 1.0  all relevant lines correctly indented
        – 0.x  proportion of correctly indented lines (progressive)
        – 0.0  file missing / unreadable / not enough lines / no relevant lines
    """
    print(f"Checking indentation for: {target_file}")

    path = Path(target_file)
    if not path.is_file():
        print("✗ Target file not found.")
        print("REWARD: 0.0")
        return 0.0

    try:
        lines = path.read_text().splitlines()
    except Exception as exc:
        print(f"✗ Could not read file: {exc}")
        print("REWARD: 0.0")
        return 0.0

    # We need at least 18 lines to perform the required checks (since we may use
    # line 18+ as reference if needed)
    if len(lines) < 18:
        print("✗ File has fewer than 18 lines – cannot verify.")
        print("REWARD: 0.0")
        return 0.0

    # ------------------------------------------------------------------
    # 1. Determine what the *correct* indentation should be.
    #    Prefer the last non-blank line BEFORE line 11 (index 10). If nothing
    #    suitable is found, fall back to the first non-blank line AFTER line 17.
    # ------------------------------------------------------------------
    reference_indent = None

    # Search backwards from line 10 to line 0.
    for idx in range(10, -1, -1):
        if lines[idx].strip():  # non-blank
            reference_indent = _leading_space_count(lines[idx])
            print(f"Reference indentation obtained from line {idx + 1}: {reference_indent} spaces (backwards search)")
            break

    # If still unknown, look forwards starting from line 18 (index 17)
    if reference_indent is None:
        for idx in range(17, len(lines)):
            if lines[idx].strip():
                reference_indent = _leading_space_count(lines[idx])
                print(f"Reference indentation obtained from line {idx + 1}: {reference_indent} spaces (forward search)")
                break

    if reference_indent is None:
        # File is blank?  Should not happen if earlier length check passed, but be safe.
        print("✗ Unable to determine reference indentation – no non-blank lines found.")
        print("REWARD: 0.0")
        return 0.0

    # ------------------------------------------------------------------
    # 2. Evaluate lines 11-17 (indexes 10-16)
    # ------------------------------------------------------------------
    correct = 0
    checked = 0
    for idx in range(10, 17):
        if idx >= len(lines):
            break  # safety
        content = lines[idx]
        if not content.strip():
            # Ignore completely blank lines when checking indentation alignment
            continue

        checked += 1
        current_indent = _leading_space_count(content)
        if current_indent == reference_indent:
            print(f"✓ Line {idx + 1:>2} indentation correct ({current_indent} spaces)")
            correct += 1
        else:
            print(f"✗ Line {idx + 1:>2} indentation incorrect – {current_indent} vs expected {reference_indent}")

    if checked == 0:
        # No substantive lines to evaluate – treat as failure (score 0)
        print("✗ No relevant code lines between lines 11 and 17 to verify.")
        print("REWARD: 0.0")
        return 0.0

    # ------------------------------------------------------------------
    # 3. Progressive scoring – proportion of correctly indented lines.
    # ------------------------------------------------------------------
    score = round(correct / checked, 2)  # keep two decimals as required

    print(f"Indentation correctness: {correct}/{checked} lines")
    print(f"REWARD: {score}")
    return score


if __name__ == "__main__":
    # Allow an optional path from the command line for easier manual testing
    target = sys.argv[1] if len(sys.argv) > 1 else "/home/user/project/main.py"
    verify_task(target)

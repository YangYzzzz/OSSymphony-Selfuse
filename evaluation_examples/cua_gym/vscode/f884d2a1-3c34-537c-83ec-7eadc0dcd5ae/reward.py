"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m converting a JavaScript helper file to Python, and I need to replace every instance of `console.log` with `print` in /home/user/workspace/utils.js—what’s the quickest way to do this in VS Code?
Generated: 2025-09-11 12:32:14
Status: success
Model: azure-o3
Total Steps: 13
"""

import re
import pathlib
import sys

"""
Reward Verification Script
=========================
Task: Replace every instance of `console.log` with `print` inside
      /home/user/workspace/utils.js using VS Code (or any method).

Scoring (progressive):
  • 0.6 — All `console.log` occurrences have been removed/replaced
  • 0.4 — At least one valid Python-style `print(` statement is present
Total possible: 1.0

The script first checks that the target file exists, then reads its
contents and performs two independent, data-driven verifications:
  1. Search (case-insensitive) for any form of "console.log" that may
     contain arbitrary whitespace around the dot (e.g., "console . log").
  2. Search for the token `print(` (not part of a longer identifier)
     to confirm replacements actually occurred.

No points are awarded for natural conditions such as file existence or
load success—they are merely prerequisites.  Partial credit is granted
only when a requirement is genuinely satisfied.
"""

FILE_PATH = "/home/user/workspace/utils.js"

# ---------------------------------------------------------------------------
# Verification helpers
# ---------------------------------------------------------------------------

def has_no_console_log(text: str) -> bool:
    """Return True if no `console.log` occurrences remain."""
    pattern = re.compile(r"console\s*\.\s*log", re.IGNORECASE)
    return not pattern.search(text)


def count_print_statements(text: str) -> int:
    """Return the number of standalone `print(` statements."""
    pattern = re.compile(r"(?<![\w\.])print\s*\(")  # negative look-behind → not preceded by word char or dot
    # We purposely keep the pattern simple and permissive; it is enough
    # to detect replacements without over-engineering Python parsing.
    matches = re.findall(r"(?<![\w\.])print\s*\(", text)
    return len(matches)


# ---------------------------------------------------------------------------
# Main verification routine
# ---------------------------------------------------------------------------

def verify_console_to_print(file_path: str = FILE_PATH) -> float:
    max_score = 1.0
    score = 0.0

    target = pathlib.Path(file_path)
    print(f"Checking file: {target}")

    # ---------- Requirement 0: File existence (no points, but mandatory) ----------
    if not target.exists():
        print("✗ File does not exist – cannot verify task.")
        print("REWARD: 0.0")
        return 0.0

    try:
        text = target.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        print(f"✗ Unable to read file: {exc}")
        print("REWARD: 0.0")
        return 0.0

    # ---------- Requirement 1: No console.log left (0.6) ----------
    if has_no_console_log(text):
        print("✓ All 'console.log' occurrences have been removed/replaced.")
        score += 0.6
    else:
        # Count remaining occurrences for helpful output
        remaining = re.findall(r"console\s*\.\s*log", text, re.IGNORECASE)
        print(f"✗ Found {len(remaining)} remaining 'console.log' occurrence(s).")

    # ---------- Requirement 2: print statements present (0.4) ----------
    prints_found = count_print_statements(text)
    if prints_found > 0:
        print(f"✓ Found {prints_found} 'print(' statement(s).")
        # Only award if no console.log left – we want proper replacements
        if score >= 0.6:
            score += 0.4
    else:
        print("✗ No 'print(' statements detected.")

    # Clamp & output final score
    score = min(score, max_score)
    print(f"Total Score: {score}/{max_score}")
    print(f"REWARD: {score}")
    return score


# ---------------------------------------------------------------------------
# Script entry-point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Exit code mirrors success (0) or failure (non-zero) but is not
    # strictly required; primary evaluation uses printed REWARD value.
    final_reward = verify_console_to_print()
    sys.exit(0 if final_reward == 1.0 else 1)


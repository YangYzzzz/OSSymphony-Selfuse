"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m tidying up the UI guide—could you go into /home/user/docs/components.md and replace every instance of the word “button” with “btn”?
Generated: 2025-09-11 19:17:14
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
import re
from pathlib import Path

"""
Reward Verification Script
Task: Ensure every instance of the word "button" in /home/user/docs/components.md has been
replaced with "btn".
Scoring (progressive):
    0.7  – No standalone occurrences of the word "button" remain (case-insensitive)
    0.3  – At least one standalone occurrence of the word "btn" exists (case-sensitive)
    1.0  – Both of the above conditions are satisfied
The script prints detailed diagnostics and finishes with a single line:
    REWARD: <score>
Exactly 1.0 is printed only when the task is fully completed.
"""

FILE_PATH = "/home/user/docs/components.md"

# Weights for partial credit
WEIGHT_NO_BUTTON = 0.7   # No more "button"
WEIGHT_HAS_BTN   = 0.3   # At least one "btn"


def verify_replacement(file_path: str) -> float:
    """Verify that 'button'→'btn' replacement task is completed."""
    total_score = 0.0
    max_score   = 1.0

    print(f"Checking file: {file_path}\n")

    # 1. Prerequisite – file must exist and be readable (no points awarded for existence)
    if not os.path.isfile(file_path):
        print("✗ File does not exist – task failed.")
        print("REWARD: 0.0")
        return 0.0

    try:
        content = Path(file_path).read_text(encoding="utf-8")
        print("✓ File loaded successfully (prerequisite, no points)\n")
    except Exception as e:
        print(f"✗ Unable to read file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # 2. Check absence of standalone word 'button' (case-insensitive)
    button_pattern = re.compile(r"\bbutton\b", re.IGNORECASE)
    button_matches = button_pattern.findall(content)
    if not button_matches:
        print("✓ No standalone 'button' word found (0.7 points)")
        total_score += WEIGHT_NO_BUTTON
    else:
        print(f"✗ Found {len(button_matches)} occurrence(s) of 'button' – should all be replaced (0 points)")

    # 3. Check presence of standalone word 'btn' (case-sensitive)
    btn_pattern = re.compile(r"\bbtn\b")
    btn_matches = btn_pattern.findall(content)
    if btn_matches:
        print(f"✓ Found {len(btn_matches)} occurrence(s) of 'btn' (0.3 points)")
        total_score += WEIGHT_HAS_BTN
    else:
        print("✗ No standalone 'btn' word found – replacements missing (0 points)")

    # 4. Final score
    final_score = min(total_score, max_score)
    print(f"\nTotal score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_replacement(FILE_PATH)


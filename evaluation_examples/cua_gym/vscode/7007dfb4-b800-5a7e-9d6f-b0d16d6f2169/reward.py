"""
Reward Script: Convert all single-quoted strings to double-quoted strings in config.py
Task ID: vscode_edit_055
Domain: vs_code
Scoring:
  Component 1: All 12 string values use double quotes (0.7 pts)
  Component 2: No single-quoted strings remain (0.2 pts)
  Component 3: String content is preserved exactly (0.1 pts)
"""

import os
import re

WORKDIR = '/home/user/Desktop'
TASK_ID = 'vscode_edit_055'
FILE_PATH = os.path.join(WORKDIR, 'config.py')

# The 12 expected string values after conversion (double-quoted)
EXPECTED_DOUBLE_QUOTED = [
    '"localhost"',
    '"mydb"',
    '"admin"',
    '"securepass123"',
    '"MyWebApp"',
    '"django-insecure-k9x2p"',
    '"INFO"',
    '"/var/log/mywebapp/app.log"',
    '"memcached"',
    '"smtp.example.com"',
    '"/static/"',
    '"UTC"',
]

# The 12 original single-quoted strings that should NO LONGER appear
ORIGINAL_SINGLE_QUOTED = [
    "'localhost'",
    "'mydb'",
    "'admin'",
    "'securepass123'",
    "'MyWebApp'",
    "'django-insecure-k9x2p'",
    "'INFO'",
    "'/var/log/mywebapp/app.log'",
    "'memcached'",
    "'smtp.example.com'",
    "'/static/'",
    "'UTC'",
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load file content — if missing, return 0
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        print(f"INFO: Loaded file {file_path} ({len(content)} bytes)")
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All 12 double-quoted versions are present in the file (0.7 points)
    # Each string contributes 0.7/12 ≈ 0.0583 pts — we award full 0.7 only if all 12 pass
    try:
        found_double = 0
        for dq_str in EXPECTED_DOUBLE_QUOTED:
            if dq_str in content:
                found_double += 1
            else:
                print(f"FAIL: Component 1 — double-quoted string not found: {dq_str}")

        if found_double == 12:
            print(f"PASS: Component 1 — all 12 double-quoted strings are present (0.7 pts)")
            total_score += 0.7
        elif found_double > 0:
            partial = round(0.7 * found_double / 12, 4)
            print(f"PARTIAL: Component 1 — {found_double}/12 double-quoted strings found ({partial} pts)")
            total_score += partial
        else:
            print("FAIL: Component 1 — no double-quoted strings found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: None of the 12 original single-quoted strings remain in the file (0.2 points)
    # This checks that the conversion actually happened — no leftover single-quoted strings
    try:
        remaining_single = 0
        for sq_str in ORIGINAL_SINGLE_QUOTED:
            if sq_str in content:
                remaining_single += 1
                print(f"FAIL: Component 2 — original single-quoted string still present: {sq_str}")

        if remaining_single == 0:
            print(f"PASS: Component 2 — no original single-quoted strings remain (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — {remaining_single} single-quoted strings still present")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: String content preserved exactly — count double-quoted strings in file matches 12 (0.1 points)
    # Verifies no strings were corrupted, dropped, or duplicated by the regex replacement
    try:
        # Count all double-quoted string tokens in assignment context (value = "...")
        # Pattern: = "..." where content has no embedded double quotes
        double_quoted_assignments = re.findall(r'=\s*"([^"]*)"', content)
        # We expect exactly 12 such assignments in the golden file
        if len(double_quoted_assignments) == 12:
            print(f"PASS: Component 3 — exactly 12 double-quoted string assignments found (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 3 — expected 12 double-quoted string assignments, found {len(double_quoted_assignments)}: {double_quoted_assignments}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {round(total_score, 4)}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: test against the canonical artifact path on the VM
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

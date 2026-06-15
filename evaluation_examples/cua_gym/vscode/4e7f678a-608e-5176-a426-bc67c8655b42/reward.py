"""
FINAL REWARD SCRIPT - SUCCESS
Task: I'm tidying up my Flask app’s config file—please replace every instance of the word “database” with “db” in /home/user/app/config.py.
Generated: 2025-09-11 13:05:44
Status: success
Model: azure-o3
Total Steps: 10
"""

import re
import pathlib
import sys


def verify_task() -> float:
    """
    Reward script for Task:
      "Replace every instance of the word “database” with “db” in
       /home/user/app/config.py"

    Scoring (progressive):
      • 0.7 –  The word "database" (case-insensitive, whole-word) no longer
                appears anywhere in the file.
      • 0.3 –  At least one whole-word occurrence of "db" is present *and*
                "database" is fully removed.
      • 0.2 –  "db" appears but some "database" tokens still remain (partial
                credit).

    The script prints detailed diagnostics and returns a float in [0.0, 1.0].
    """

    CONFIG_PATH = pathlib.Path("/home/user/app/config.py")
    MAX_SCORE = 1.0
    score = 0.0

    print(f"Verifying file at: {CONFIG_PATH}")

    # 1. Ensure the config file exists
    if not CONFIG_PATH.exists():
        print("✗ config.py not found. Task not completed.")
        print("REWARD: 0.0")
        return 0.0  # Cannot evaluate further without the file

    # 2. Read file content safely
    try:
        content = CONFIG_PATH.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"✗ Failed to read config.py: {e}")
        print("REWARD: 0.0")
        return 0.0

    # 3. Check for any remaining occurrences of the word "database"
    database_pattern = re.compile(r"\bdatabase\b", re.IGNORECASE)
    remaining_database = database_pattern.findall(content)
    num_database = len(remaining_database)

    if num_database == 0:
        print("✓ All instances of the word 'database' have been removed (0.7 points)")
        score += 0.7
    else:
        print(f"✗ Found {num_database} remaining occurrence(s) of 'database' (0 points)")

    # 4. Verify that the replacement word "db" appears at least once (whole-word)
    db_pattern = re.compile(r"\bdb\b", re.IGNORECASE)
    num_db = len(db_pattern.findall(content))

    if num_db > 0:
        if num_database == 0:
            # Perfect replacement scenario
            print(f"✓ Found {num_db} occurrence(s) of the word 'db' (0.3 points)")
            score += 0.3
        else:
            # Some replacements done but not all
            print(f"✓ Found {num_db} occurrence(s) of 'db', but 'database' still present (0.2 points)")
            score += 0.2
    else:
        print("✗ No standalone 'db' word found (0 points)")

    # 5. Final scoring
    final_score = min(score, MAX_SCORE)
    print(f"Total Score: {final_score}/{MAX_SCORE}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task()


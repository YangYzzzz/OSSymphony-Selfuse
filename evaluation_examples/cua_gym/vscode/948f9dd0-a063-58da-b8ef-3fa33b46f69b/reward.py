"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m about to define our database structure and need a clean starting point—could you create a new file named ‘schema.sql’ inside /home/user/database/scripts for me?
Generated: 2025-09-11 13:28:55
Status: success
Model: azure-o3
Total Steps: 4
"""

import pathlib

def verify_task():
    """Verify completion of the task:
    Create a new file named `schema.sql` inside `/home/user/database/scripts`.

    Scoring logic (progressive):
    1. Directory `/home/user/database/scripts` exists  -> 0.3 points
    2. File `schema.sql` exists inside that directory   -> +0.7 points

    Full completion (1.0) is awarded only when the file exists at the
    exact required path. The directory‐only state earns partial credit.
    """

    target_dir = pathlib.Path("/home/user/database/scripts")
    target_file = target_dir / "schema.sql"

    total_score = 0.0

    # Check the required directory exists (shows some progress)
    if target_dir.exists() and target_dir.is_dir():
        print(f"✓ Directory exists: {target_dir} (+0.3)")
        total_score += 0.3
    else:
        print(f"✗ Directory not found: {target_dir}")
        print("REWARD: 0.0")
        return 0.0  # Cannot score further if directory itself is missing

    # Check the required file exists
    if target_file.exists() and target_file.is_file():
        print(f"✓ File exists: {target_file} (+0.7)")
        total_score += 0.7
        # Optional informational output (does not affect score)
        try:
            print(f"File size: {target_file.stat().st_size} bytes (info)")
        except Exception as e:
            print(f"Could not read file size: {e}")
    else:
        print(f"✗ File not found: {target_file}")

    # Cap at 1.0
    total_score = min(total_score, 1.0)

    print(f"REWARD: {total_score}")
    return total_score


if __name__ == "__main__":
    verify_task()


"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m setting up an automated deployment workflow for my web app—could you help me create a new shell script named ‘deploy.sh’ inside /home/user/scripts so I can start adding my deployment commands?
Generated: 2025-09-11 13:11:42
Status: success
Model: azure-o3
Total Steps: 1
"""

import os
import stat

def verify_task():
    """
    Verification script for the task:
    "Create a new shell script named ‘deploy.sh’ inside /home/user/scripts so
    the user can start adding deployment commands."

    Scoring criteria (progressive):
    1. File exists                      -> 0.70 points
    2. File starts with a valid shebang -> 0.15 points
    3. File is executable               -> 0.15 points
    Total                               -> 1.00 points
    """

    print("Checking task completion for creation of deploy.sh in /home/user/scripts ...")

    total_score = 0.0           # Progressive score accumulator
    max_score   = 1.0           # Maximum score

    dir_path  = "/home/user/scripts"
    file_path = os.path.join(dir_path, "deploy.sh")

    # ------------------------------------------------------------------
    # Requirement 1 : File existence (0.70 points)
    # ------------------------------------------------------------------
    if os.path.isfile(file_path):
        print(f"✓ Found file: {file_path} (0.7 points)")
        total_score += 0.70
    else:
        print(f"✗ Missing file: {file_path} (0 points)")
        # If the file doesn't exist, the later checks would naturally fail

    # ------------------------------------------------------------------
    # Requirement 2 : Valid shebang (0.15 points)
    # ------------------------------------------------------------------
    shebang_ok = False
    if os.path.isfile(file_path):
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as fh:
                first_line = fh.readline().strip()
                valid_shells = ("bash", "sh", "zsh", "ksh")
                if first_line.startswith("#!") and any(shell in first_line for shell in valid_shells):
                    shebang_ok = True
        except Exception as e:
            print(f"Error reading file for shebang check: {e}")

    if shebang_ok:
        print("✓ Valid shebang detected (0.15 points)")
        total_score += 0.15
    elif os.path.isfile(file_path):
        print("✗ No valid shebang found (0 points)")

    # ------------------------------------------------------------------
    # Requirement 3 : Executable permissions (0.15 points)
    # ------------------------------------------------------------------
    executable_ok = False
    if os.path.isfile(file_path):
        executable_ok = os.access(file_path, os.X_OK)

    if executable_ok:
        print("✓ File has executable permissions (0.15 points)")
        total_score += 0.15
    elif os.path.isfile(file_path):
        print("✗ File is not executable (0 points)")

    # ------------------------------------------------------------------
    # Final scoring output
    # ------------------------------------------------------------------
    final_score = min(total_score, max_score)
    print(f"Total score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score

if __name__ == "__main__":
    verify_task()

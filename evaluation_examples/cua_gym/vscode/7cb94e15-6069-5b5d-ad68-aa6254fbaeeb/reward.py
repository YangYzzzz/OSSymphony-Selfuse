"""
Reward Script: Delete temp.js, debug.js, and test_scratch.py from project root
Task ID: vscode_file_056
Domain: vs_code
Scoring:
  Component 1: temp.js is deleted from project root (0.34 points)
  Component 2: debug.js is deleted from project root (0.33 points)
  Component 3: test_scratch.py is deleted from project root (0.33 points)
  Gate: Other files (package.json, requirements.txt, src/app.js, src/main.py) remain intact
Total: 1.0
"""

import os

WORKDIR = '/home/user/project'
TASK_ID = 'vscode_file_056'

def verify_task(project_dir):
    """
    Verify task completion: three temp files deleted, other files intact.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: verify that the project directory exists
    if not os.path.isdir(project_dir):
        print(f"CRITICAL: Project directory not found: {project_dir}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: other files must remain intact
    # These are files that should NOT have been deleted
    preserved_files = [
        os.path.join(project_dir, 'package.json'),
        os.path.join(project_dir, 'requirements.txt'),
        os.path.join(project_dir, 'src', 'app.js'),
        os.path.join(project_dir, 'src', 'main.py'),
    ]
    for pf in preserved_files:
        if not os.path.exists(pf):
            print(f"GATE FAIL: Preserved file missing: {pf}")
            print("REWARD: 0.0")
            return 0.0
    print("GATE PASS: All preserved files (package.json, requirements.txt, src/app.js, src/main.py) are intact")

    # Component 1: temp.js is deleted (0.34 points)
    # This file should NOT exist in the golden state
    try:
        temp_js_path = os.path.join(project_dir, 'temp.js')
        if not os.path.exists(temp_js_path):
            print(f"PASS: Component 1 — temp.js has been deleted (0.34 pts)")
            total_score += 0.34
        else:
            print(f"FAIL: Component 1 — temp.js still exists at {temp_js_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: debug.js is deleted (0.33 points)
    # This file should NOT exist in the golden state
    try:
        debug_js_path = os.path.join(project_dir, 'debug.js')
        if not os.path.exists(debug_js_path):
            print(f"PASS: Component 2 — debug.js has been deleted (0.33 pts)")
            total_score += 0.33
        else:
            print(f"FAIL: Component 2 — debug.js still exists at {debug_js_path}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: test_scratch.py is deleted (0.33 points)
    # This file should NOT exist in the golden state
    try:
        test_scratch_path = os.path.join(project_dir, 'test_scratch.py')
        if not os.path.exists(test_scratch_path):
            print(f"PASS: Component 3 — test_scratch.py has been deleted (0.33 pts)")
            total_score += 0.33
        else:
            print(f"FAIL: Component 3 — test_scratch.py still exists at {test_scratch_path}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical project directory path
project_dir = WORKDIR
if not os.path.isdir(project_dir):
    print(f"Project directory not found: {project_dir}")
    print("REWARD: 0.0")
else:
    verify_task(project_dir)

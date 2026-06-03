"""
Reward Script: Comprehensive .gitignore setup for VSCode workspace
Task ID: vscode_lp_092
Domain: vscode (file-based)
Scoring:
  - Component 1 (0.25): Python patterns present
  - Component 2 (0.25): Node.js patterns present
  - Component 3 (0.25): IDE patterns present
  - Component 4 (0.25): OS patterns present
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_092'
GITIGNORE_PATH = os.path.join(WORKDIR, TASK_ID, '.gitignore')


def verify_task(file_path):
    """
    Verify .gitignore task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be readable
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        lines = [line.strip() for line in content.splitlines()]
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Helper: check if a pattern exists in .gitignore lines
    # Matches exact line or line without trailing slash
    def has_pattern(pattern):
        """Check if pattern is present in gitignore lines (case-sensitive)."""
        for line in lines:
            # Skip comments and empty lines
            if line.startswith('#') or not line:
                continue
            if line == pattern or line == pattern.rstrip('/'):
                return True
        return False

    # Component 1: Python patterns (0.25 points)
    # Required: __pycache__/, *.pyc, *.pyo, .env, venv/, .pytest_cache/
    # These are NOT in the initial .gitignore (which only has *.log and tmp/)
    try:
        python_patterns = ['__pycache__/', '*.pyc', '*.pyo', '.env', 'venv/', '.pytest_cache/']
        python_found = sum(1 for p in python_patterns if has_pattern(p))
        python_total = len(python_patterns)
        if python_found >= 4:
            print(f"PASS: Component 1 — Python patterns ({python_found}/{python_total} found) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Python patterns ({python_found}/{python_total} found, need >= 4)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Node.js patterns (0.25 points)
    # Required: node_modules/, dist/, build/, .npm
    # These are NOT in the initial .gitignore
    try:
        nodejs_patterns = ['node_modules/', 'dist/', 'build/', '.npm']
        nodejs_found = sum(1 for p in nodejs_patterns if has_pattern(p))
        nodejs_total = len(nodejs_patterns)
        if nodejs_found >= 3:
            print(f"PASS: Component 2 — Node.js patterns ({nodejs_found}/{nodejs_total} found) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Node.js patterns ({nodejs_found}/{nodejs_total} found, need >= 3)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: IDE patterns (0.25 points)
    # Required: .vscode/, .idea/, *.swp
    # These are NOT in the initial .gitignore
    try:
        ide_patterns = ['.vscode/', '.idea/', '*.swp']
        ide_found = sum(1 for p in ide_patterns if has_pattern(p))
        ide_total = len(ide_patterns)
        if ide_found >= 2:
            print(f"PASS: Component 3 — IDE patterns ({ide_found}/{ide_total} found) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — IDE patterns ({ide_found}/{ide_total} found, need >= 2)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: OS patterns (0.25 points)
    # Required: .DS_Store, Thumbs.db
    # These are NOT in the initial .gitignore
    try:
        os_patterns = ['.DS_Store', 'Thumbs.db']
        os_found = sum(1 for p in os_patterns if has_pattern(p))
        os_total = len(os_patterns)
        if os_found >= 1:
            print(f"PASS: Component 4 — OS patterns ({os_found}/{os_total} found) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — OS patterns ({os_found}/{os_total} found, need >= 1)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(GITIGNORE_PATH):
    print(f"File not found: {GITIGNORE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(GITIGNORE_PATH)

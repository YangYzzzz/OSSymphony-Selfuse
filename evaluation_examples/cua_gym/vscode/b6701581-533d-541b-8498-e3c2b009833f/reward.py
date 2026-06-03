"""
Reward Script: Move the entire components/ folder from the project root into the src/ directory.
Task ID: vscode_file_063
Domain: vs_code
Scoring:
  Component 1: src/components/ folder exists with all 3 files (Button.jsx, Modal.jsx, Header.jsx) — 0.5 pts
  Component 2: Root-level components/ folder no longer exists — 0.3 pts
  Component 3: File content of moved files is preserved (Button.jsx content intact) — 0.2 pts
Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_063'
PROJECT_ROOT = '/home/user/react-project'

EXPECTED_FILES = ['Button.jsx', 'Modal.jsx', 'Header.jsx']
SRC_COMPONENTS_DIR = os.path.join(PROJECT_ROOT, 'src', 'components')
ROOT_COMPONENTS_DIR = os.path.join(PROJECT_ROOT, 'components')

# Known content signature from initial_env — used to verify content was preserved
BUTTON_JSX_SIGNATURE = "const Button = ({ label, onClick, variant = 'primary', disabled = false })"


def verify_task():
    """
    Verify that the components/ folder was moved from project root into src/.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: src/components/ folder exists and contains all 3 expected files (0.5 points)
    # This FAILS on initial_env (files are at root-level components/) and PASSES on golden_env
    try:
        if os.path.isdir(SRC_COMPONENTS_DIR):
            found_files = []
            missing_files = []
            for fname in EXPECTED_FILES:
                fpath = os.path.join(SRC_COMPONENTS_DIR, fname)
                if os.path.isfile(fpath):
                    found_files.append(fname)
                else:
                    missing_files.append(fname)

            if len(found_files) == 3:
                print(f"PASS: Component 1 — src/components/ exists with all 3 files: {found_files} (0.5 pts)")
                total_score += 0.5
            elif len(found_files) > 0:
                partial = round(0.5 * len(found_files) / 3, 2)
                print(f"PARTIAL: Component 1 — src/components/ exists but missing files: {missing_files}. Found: {found_files} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 1 — src/components/ directory exists but contains none of the expected files")
        else:
            print(f"FAIL: Component 1 — src/components/ directory does not exist at {SRC_COMPONENTS_DIR}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Root-level components/ folder no longer exists (0.3 points)
    # This FAILS on initial_env (components/ is at project root) and PASSES on golden_env
    try:
        if not os.path.exists(ROOT_COMPONENTS_DIR):
            print(f"PASS: Component 2 — Root-level components/ folder no longer exists (0.3 pts)")
            total_score += 0.3
        else:
            # Check if it's non-empty (partial scenario: moved but not removed)
            remaining = os.listdir(ROOT_COMPONENTS_DIR) if os.path.isdir(ROOT_COMPONENTS_DIR) else []
            if remaining:
                print(f"FAIL: Component 2 — Root-level components/ still exists with files: {remaining}")
            else:
                print(f"FAIL: Component 2 — Root-level components/ folder still exists (empty)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: File contents are preserved — Button.jsx contains expected content signature (0.2 points)
    # This FAILS on initial_env (Button.jsx is not at src/components/ path) and PASSES on golden_env
    try:
        button_path = os.path.join(SRC_COMPONENTS_DIR, 'Button.jsx')
        if os.path.isfile(button_path):
            with open(button_path, 'r', encoding='utf-8') as f:
                content = f.read()
            if BUTTON_JSX_SIGNATURE in content:
                print(f"PASS: Component 3 — Button.jsx content preserved with expected signature (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Button.jsx exists at src/components/ but content signature not found")
                print(f"  Expected signature: {BUTTON_JSX_SIGNATURE!r}")
        else:
            print(f"FAIL: Component 3 — Button.jsx not found at {button_path} (cannot verify content)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Verify the project root exists as a basic precondition gate
if not os.path.isdir(PROJECT_ROOT):
    print(f"CRITICAL: Project root not found: {PROJECT_ROOT}")
    print("REWARD: 0.0")
else:
    verify_task()

"""
Reward Script: Start Node.js debug session for calc.js in VSCode via F5
Task ID: vscode_dbg_005
Domain: vs_code
Scoring:
  Component 1: debug_output.txt exists (0.4 pts)
  Component 2: Output contains calculator header and non-empty content (0.3 pts)
  Component 3: All expected calculation results are present (0.3 pts)
  Total: 1.0

This task asks the agent to open calc.js in VSCode and press F5 to start
a Node.js debug session. The golden artifact captures the output of running
calc.js (via `node calc.js`) into debug_output.txt, simulating the debug run.
This file is absent from the initial_env (pre-task state).
"""

import os

WORKDIR = '/home/user/projects/calculator'
TASK_ID = 'vscode_dbg_005'
DEBUG_OUTPUT_PATH = os.path.join(WORKDIR, 'debug_output.txt')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: debug_output.txt must exist (0.4 points)
    # This file is ONLY created in the golden_env by running the Node.js debug session.
    # It does NOT exist in initial_env, so this check distinguishes the two states.
    try:
        if os.path.isfile(DEBUG_OUTPUT_PATH):
            file_size = os.path.getsize(DEBUG_OUTPUT_PATH)
            if file_size > 0:
                print(f"PASS: Component 1 — debug_output.txt exists and is non-empty ({file_size} bytes) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — debug_output.txt exists but is empty (0 bytes)")
        else:
            print(f"FAIL: Component 1 — debug_output.txt not found at {DEBUG_OUTPUT_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Output must contain calculator header line (0.3 points)
    # Confirms the Node.js process actually ran calc.js (not some other content).
    # The header "=== Calculator Results ===" is the first output line of calc.js.
    try:
        if os.path.isfile(DEBUG_OUTPUT_PATH):
            with open(DEBUG_OUTPUT_PATH, 'r') as f:
                content = f.read()
            if '=== Calculator Results ===' in content:
                print("PASS: Component 2 — Output contains '=== Calculator Results ===' header (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Expected '=== Calculator Results ===' header in debug_output.txt, not found")
                print(f"  Actual content (first 200 chars): {content[:200]!r}")
        else:
            print("FAIL: Component 2 — debug_output.txt not found, cannot check content")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Key calculation results must be present (0.3 points)
    # Verifies that the full calc.js execution completed with expected results.
    # These specific lines confirm Node.js ran all 5 calculation pairs correctly.
    try:
        if os.path.isfile(DEBUG_OUTPUT_PATH):
            with open(DEBUG_OUTPUT_PATH, 'r') as f:
                content = f.read()

            # Expected results from the 5 calculation pairs in calc.js
            expected_results = [
                '15 + 4 = 19',
                '15 - 4 = 11',
                '15 * 4 = 60',
                '15 / 4 = 3.75',
                '120 + 8 = 128',
                '37 * 19 = 703',
                '256 / 16 = 16',
                '88 + 11 = 99',
                'All calculations complete.',
            ]

            missing = [line for line in expected_results if line not in content]
            if not missing:
                print(f"PASS: Component 3 — All {len(expected_results)} expected result lines found in debug_output.txt (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — {len(missing)} expected result line(s) missing from debug_output.txt:")
                for m in missing:
                    print(f"  Missing: '{m}'")
        else:
            print("FAIL: Component 3 — debug_output.txt not found, cannot check results")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

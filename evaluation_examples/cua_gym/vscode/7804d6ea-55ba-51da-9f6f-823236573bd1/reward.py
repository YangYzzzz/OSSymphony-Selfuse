"""
Reward Script: Step Out (Shift+F11) during VSCode debug session
Task ID: vscode_dbg_023
Domain: vs_code
Scoring:
  Component 1: debug_state.json marker file exists (0.4 pts)
  Component 2: step_out_executed == true AND debug_action == "stepOut" (0.3 pts)
  Component 3: current_file == "app.js" AND current_line == 21 (0.3 pts)

The task requires pressing Shift+F11 (Step Out) while paused inside
calculateTotal() in utils.js (line 15), which should return execution
to app.js at line 21 (the line after the calculateTotal() call at line 20).

A state marker file at /home/user/projects/deep-call/debug_state.json
is written by the golden setup to represent the post-Step-Out debugger state.
This file is absent in the initial env, so all components correctly score 0.0
on the initial artifact and 1.0 on the golden artifact.
"""

import json
import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_023'
MARKER_PATH = f'{WORKDIR}/projects/deep-call/debug_state.json'


def verify_task(marker_path):
    """
    Verify Step Out task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: debug_state.json marker file exists (0.4 points)
    # This file is absent in initial_env and present in golden_env.
    # Its presence signals that the "Step Out" action was completed/recorded.
    try:
        if os.path.exists(marker_path):
            print(f"PASS: Component 1 — debug_state.json exists at {marker_path} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — debug_state.json not found at {marker_path}")
            # File is missing; no point loading it for components 2 & 3
            final_score = min(total_score, 1.0)
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {final_score}")
            return final_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load the marker file for subsequent checks
    try:
        with open(marker_path, 'r') as f:
            state = json.load(f)
    except Exception as e:
        print(f"CRITICAL: Cannot parse debug_state.json: {e}")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: step_out_executed == true AND debug_action == "stepOut" (0.3 points)
    # Verifies that the marker records a Step Out action, not some other debug action.
    try:
        step_out_executed = state.get('step_out_executed')
        debug_action = state.get('debug_action')
        if step_out_executed is True and debug_action == 'stepOut':
            print(f"PASS: Component 2 — step_out_executed=true, debug_action='stepOut' (0.3 pts)")
            total_score += 0.3
        else:
            print(
                f"FAIL: Component 2 — expected step_out_executed=true/debug_action='stepOut', "
                f"found step_out_executed={step_out_executed!r}, debug_action={debug_action!r}"
            )
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: current_file == "app.js" AND current_line == 21 (0.3 points)
    # Verifies that after Step Out the debugger is paused at app.js line 21,
    # which is the line immediately after the calculateTotal() call (line 20).
    try:
        current_file = state.get('current_file')
        current_line = state.get('current_line')
        if current_file == 'app.js' and current_line == 21:
            print(
                f"PASS: Component 3 — current_file='app.js', current_line=21 (0.3 pts)"
            )
            total_score += 0.3
        else:
            print(
                f"FAIL: Component 3 — expected current_file='app.js' / current_line=21, "
                f"found current_file={current_file!r}, current_line={current_line!r}"
            )
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task(MARKER_PATH)

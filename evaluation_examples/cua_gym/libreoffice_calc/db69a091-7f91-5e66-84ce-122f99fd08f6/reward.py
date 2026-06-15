"""
Reward Script: Configure nano text editor with line numbers and smooth scrolling
Task ID: osworld_multi_apps_web_search_config_008
Domain: os (shell configuration)
Scoring:
  Component 1: ~/.nanorc contains 'set linenumbers'  — 0.5 points
  Component 2: ~/.nanorc contains 'set smooth'       — 0.5 points
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_search_config_008'
NANORC_PATH = os.path.join(WORKDIR, '.nanorc')


def verify_task(nanorc_path):
    """
    Verify that ~/.nanorc has been configured with line numbers and smooth scrolling.
    Both settings must be added as active (non-commented) directives.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist
    if not os.path.isfile(nanorc_path):
        print(f"CRITICAL: ~/.nanorc not found at {nanorc_path}")
        print("REWARD: 0.0")
        return 0.0

    # Read file content for verification
    try:
        with open(nanorc_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read {nanorc_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Check each line for an active (non-commented) directive
    lines = content.splitlines()
    active_lines = [ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith('#')]

    # Component 1: 'set linenumbers' is present as an active directive (0.5 points)
    # This setting enables line numbers in nano — introduced by the task
    try:
        linenumbers_found = any(
            ln == 'set linenumbers' or ln.startswith('set linenumbers ')
            for ln in active_lines
        )
        if linenumbers_found:
            print("PASS: Component 1 — 'set linenumbers' found as active directive in ~/.nanorc (0.5 pts)")
            total_score += 0.5
        else:
            # Also check raw content for the directive (in case of extra whitespace)
            import re
            if re.search(r'^\s*set\s+linenumbers\s*$', content, re.MULTILINE):
                print("PASS: Component 1 — 'set linenumbers' found (with whitespace) in ~/.nanorc (0.5 pts)")
                total_score += 0.5
            else:
                print("FAIL: Component 1 — 'set linenumbers' not found as active directive in ~/.nanorc")
                print(f"  Active directives found: {active_lines}")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check 'set linenumbers': {e}")

    # Component 2: 'set smooth' is present as an active directive (0.5 points)
    # This setting enables smooth scrolling in nano — introduced by the task
    try:
        smooth_found = any(
            ln == 'set smooth' or ln.startswith('set smooth ')
            for ln in active_lines
        )
        if smooth_found:
            print("PASS: Component 2 — 'set smooth' found as active directive in ~/.nanorc (0.5 pts)")
            total_score += 0.5
        else:
            import re
            if re.search(r'^\s*set\s+smooth\s*$', content, re.MULTILINE):
                print("PASS: Component 2 — 'set smooth' found (with whitespace) in ~/.nanorc (0.5 pts)")
                total_score += 0.5
            else:
                print("FAIL: Component 2 — 'set smooth' not found as active directive in ~/.nanorc")
                print(f"  Active directives found: {active_lines}")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check 'set smooth': {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification against the canonical path on the VM
if not os.path.isfile(NANORC_PATH):
    print(f"File not found: {NANORC_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(NANORC_PATH)

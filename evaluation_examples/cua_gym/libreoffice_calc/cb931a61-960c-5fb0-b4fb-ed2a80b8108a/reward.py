"""
Reward Script: Configure shell to auto-activate Python venv on terminal open
Task ID: osworld_multi_apps_cli_path_fix_006
Domain: os (shell configuration)
Scoring:
  Component 1 (0.6): ~/.bashrc contains a 'source' line activating /opt/venvs/datascience/bin/activate
  Component 2 (0.4): The activate script path referenced in ~/.bashrc actually exists on disk
Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_cli_path_fix_006'

BASHRC_PATH = os.path.join(WORKDIR, '.bashrc')
VENV_ACTIVATE_PATH = '/opt/venvs/datascience/bin/activate'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Task: ~/.bashrc must auto-activate /opt/venvs/datascience when a terminal opens.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: ~/.bashrc must exist
    if not os.path.isfile(BASHRC_PATH):
        print(f"CRITICAL: ~/.bashrc not found at {BASHRC_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Read .bashrc content
    try:
        with open(BASHRC_PATH, 'r') as f:
            bashrc_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read {BASHRC_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: ~/.bashrc contains a line that sources the datascience venv activate script (0.6 points)
    # This is the core task change: adding the venv activation to .bashrc.
    # The line must be a 'source' or '.' (dot) command referencing the datascience venv activate script.
    # This FAILS on initial_env (no such line) and PASSES on golden_env.
    try:
        # Pattern: 'source /opt/venvs/datascience/bin/activate' or
        #          '. /opt/venvs/datascience/bin/activate'
        activation_pattern = re.compile(
            r'^\s*(source|\.)\s+/opt/venvs/datascience/bin/activate\s*$',
            re.MULTILINE
        )
        match = activation_pattern.search(bashrc_content)
        if match:
            print(f"PASS: Component 1 — ~/.bashrc contains venv activation line: '{match.group(0).strip()}' (0.6 pts)")
            total_score += 0.6
        else:
            # Also check for any line that sources the activate path (possibly with variable)
            loose_pattern = re.compile(
                r'(source|\.)\s+.*datascience.*activate',
                re.MULTILINE | re.IGNORECASE
            )
            loose_match = loose_pattern.search(bashrc_content)
            if loose_match:
                print(f"PASS: Component 1 — ~/.bashrc contains venv activation line (loose match): '{loose_match.group(0).strip()}' (0.6 pts)")
                total_score += 0.6
            else:
                print(f"FAIL: Component 1 — ~/.bashrc does not contain a 'source /opt/venvs/datascience/bin/activate' line.")
                print(f"  Searched content snippet (last 300 chars): {bashrc_content[-300:]!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The activate script at the referenced path actually exists on disk (0.4 points)
    # This verifies the configuration points to a real, working venv.
    # Both environments have the venv pre-installed, so this passes only when Component 1 also passes
    # (we only check the existence as a quality gate tied to the activation being configured correctly).
    # NOTE: We award this only if Component 1 passed (bashrc has the line) AND the file exists.
    try:
        if total_score >= 0.6:
            # Component 1 passed — check that the referenced activate script actually exists
            if os.path.isfile(VENV_ACTIVATE_PATH):
                print(f"PASS: Component 2 — activate script exists at {VENV_ACTIVATE_PATH} (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — activate script NOT found at {VENV_ACTIVATE_PATH}")
                print(f"  The activation line in ~/.bashrc points to a missing file.")
        else:
            print(f"SKIP: Component 2 — skipped because Component 1 failed (no activation line in ~/.bashrc)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

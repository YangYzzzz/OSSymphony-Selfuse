"""
Reward Script: Install docker-compose plugin and configure permanent access
Task ID: osworld_multi_apps_cli_path_fix_007
Domain: os
Scoring:
  Component 1: ~/.bashrc contains a docker-compose alias or PATH entry (0.5 pts)
  Component 2: The alias/entry correctly maps docker-compose to 'docker compose' plugin syntax (0.5 pts)
Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_cli_path_fix_007'
BASHRC_PATH = '/home/user/.bashrc'


def verify_task():
    """
    Verify that docker-compose is configured to work permanently via ~/.bashrc.

    The task requires:
    1. A docker-compose alias or PATH configuration is present in ~/.bashrc
    2. The entry correctly delegates to the 'docker compose' plugin (i.e., 'docker compose')

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: .bashrc must be readable
    try:
        with open(BASHRC_PATH, 'r') as f:
            bashrc_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read {BASHRC_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: ~/.bashrc contains a docker-compose alias or PATH configuration (0.5 points)
    # This checks whether the user added any persistent configuration for docker-compose.
    # Acceptable forms:
    #   - alias docker-compose='...'
    #   - alias docker-compose="..."
    #   - export PATH=... (with docker cli-plugins path)
    try:
        # Look for alias docker-compose or PATH with docker cli-plugins
        has_alias = bool(re.search(
            r"""alias\s+docker-compose\s*=\s*['"]""",
            bashrc_content
        ))
        has_path_entry = bool(re.search(
            r'docker[/-]cli[-_]?plugins',
            bashrc_content,
            re.IGNORECASE
        ))

        if has_alias or has_path_entry:
            if has_alias:
                print(f"PASS: Component 1 — ~/.bashrc contains 'alias docker-compose' entry (0.5 pts)")
            else:
                print(f"PASS: Component 1 — ~/.bashrc contains docker cli-plugins PATH entry (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — ~/.bashrc does not contain alias docker-compose or cli-plugins PATH entry")
            print(f"  Searched content excerpt (last 500 chars): {bashrc_content[-500:]!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The alias/entry specifically maps docker-compose to 'docker compose' plugin (0.5 points)
    # The correct solution delegates to the Docker Compose V2 plugin via 'docker compose'.
    # This verifies the alias value is 'docker compose' (not an old standalone binary path).
    try:
        # Match alias docker-compose='docker compose' or alias docker-compose="docker compose"
        has_correct_plugin_alias = bool(re.search(
            r"""alias\s+docker-compose\s*=\s*['"]docker\s+compose['"]""",
            bashrc_content
        ))

        # Also accept function definition that calls docker compose
        has_compose_function = bool(re.search(
            r'docker-compose\s*\(\)',
            bashrc_content
        ))

        if has_correct_plugin_alias or has_compose_function:
            if has_correct_plugin_alias:
                print(f"PASS: Component 2 — alias correctly maps docker-compose to 'docker compose' plugin (0.5 pts)")
            else:
                print(f"PASS: Component 2 — function definition maps docker-compose to docker compose plugin (0.5 pts)")
            total_score += 0.5
        else:
            # Check if an alias exists but points to something else
            alias_match = re.search(
                r"""alias\s+docker-compose\s*=\s*['"](.+?)['"]""",
                bashrc_content
            )
            if alias_match:
                actual_value = alias_match.group(1)
                print(f"FAIL: Component 2 — alias docker-compose exists but maps to '{actual_value}', not 'docker compose'")
            else:
                print(f"FAIL: Component 2 — no valid docker-compose alias mapping to 'docker compose' found in ~/.bashrc")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

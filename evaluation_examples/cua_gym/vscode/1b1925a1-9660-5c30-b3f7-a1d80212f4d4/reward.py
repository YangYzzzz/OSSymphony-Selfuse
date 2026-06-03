"""
Reward Script: Write a bash script deploy.sh for rolling deployment
Task ID: vscode_ops_072
Domain: vs_code
Scoring:
  - Component 1: File exists with bash shebang + set -euo pipefail (0.20)
  - Component 2: Docker pull command present (0.20)
  - Component 3: Iterative container stop/start loop (0.25)
  - Component 4: Health check using curl (0.20)
  - Component 5: Executable permissions (0.15)
"""

import os
import re
import stat

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_072'
SCRIPT_PATH = os.path.join(WORKDIR, 'deploy-scripts', 'deploy.sh')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.isfile(SCRIPT_PATH):
        print(f"CRITICAL: deploy.sh not found at {SCRIPT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Read file content
    try:
        with open(SCRIPT_PATH, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read {SCRIPT_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    lines = content.strip().split('\n')

    # Component 1: Bash shebang + set -euo pipefail (0.20 points)
    try:
        has_shebang = len(lines) > 0 and lines[0].strip().startswith('#!/bin/bash')
        has_pipefail = 'set -euo pipefail' in content
        if has_shebang and has_pipefail:
            print(f"PASS: Component 1 — bash shebang and set -euo pipefail found (0.20 pts)")
            total_score += 0.20
        elif has_shebang:
            print(f"PARTIAL: Component 1 — shebang found but missing set -euo pipefail (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — shebang={has_shebang}, pipefail={has_pipefail}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Docker pull command (0.20 points)
    try:
        # Check for docker pull with an image name pattern
        has_docker_pull = bool(re.search(r'docker\s+pull\s+', content))
        if has_docker_pull:
            print(f"PASS: Component 2 — docker pull command found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — no docker pull command found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Iterative container stop/start (0.25 points)
    # Must have a loop structure AND docker stop AND docker run/start
    try:
        has_loop = bool(re.search(r'(for\s+|while\s+)', content))
        has_docker_stop = bool(re.search(r'docker\s+stop\s+', content))
        has_docker_start = bool(re.search(r'docker\s+(run|start)\s+', content))

        if has_loop and has_docker_stop and has_docker_start:
            print(f"PASS: Component 3 — loop with docker stop and start/run found (0.25 pts)")
            total_score += 0.25
        elif has_docker_stop and has_docker_start:
            # Has stop/start but no loop — partial credit
            print(f"PARTIAL: Component 3 — docker stop/start found but no loop structure (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — loop={has_loop}, stop={has_docker_stop}, start={has_docker_start}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Health check with curl (0.20 points)
    try:
        has_curl = bool(re.search(r'curl\s+', content))
        # Check for health-related URL or keyword near curl
        has_health = bool(re.search(r'health', content, re.IGNORECASE))

        if has_curl and has_health:
            print(f"PASS: Component 4 — curl health check found (0.20 pts)")
            total_score += 0.20
        elif has_curl:
            print(f"PARTIAL: Component 4 — curl found but no health keyword (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — curl={has_curl}, health={has_health}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Executable permissions (0.15 points)
    try:
        file_stat = os.stat(SCRIPT_PATH)
        is_executable = bool(file_stat.st_mode & stat.S_IXUSR)
        if is_executable:
            print(f"PASS: Component 5 — executable permission set (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — file is not executable (mode: {oct(file_stat.st_mode)})")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

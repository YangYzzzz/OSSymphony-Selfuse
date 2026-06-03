"""
Reward Script: Complete log_analyzer.py and generate log_summary.txt
Task ID: osworld_multi_apps_vscode_run_capture_009
Domain: multi_apps (VSCode + terminal + Python)
Scoring:
  Component 1: log_summary.txt exists on Desktop (0.3 pts)
  Component 2: log_summary.txt contains correct status code counts (0.4 pts)
  Component 3: log_summary.txt contains correct error rate (0.3 pts)
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_vscode_run_capture_009'

# Expected ground truth values from log_summary.txt (derived from task context & server.log)
EXPECTED_STATUS_COUNTS = {
    200: 10,
    201: 1,
    302: 1,
    304: 1,
    401: 1,
    403: 2,
    404: 2,
    500: 2,
}
EXPECTED_TOTAL = 20
EXPECTED_ERROR_RATE_STR = "35.00%"


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    summary_path = os.path.join(WORKDIR, 'log_summary.txt')

    # Component 1: log_summary.txt exists on Desktop (0.3 points)
    # This file is ABSENT in initial_env and PRESENT in golden_env — scores the task change
    try:
        if os.path.isfile(summary_path):
            print(f"PASS: Component 1 — log_summary.txt exists at {summary_path} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — log_summary.txt not found at {summary_path}")
            # Cannot check further components without the file
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Read the summary file content for further checks
    try:
        with open(summary_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR: Cannot read log_summary.txt: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: log_summary.txt contains correct HTTP status code counts (0.4 points)
    # The exact counts must match what the script computes from server.log
    try:
        missing_codes = []
        wrong_values = []

        for code, expected_count in EXPECTED_STATUS_COUNTS.items():
            # Match patterns like "  200: 10" or "200: 10"
            pattern = rf'\b{code}:\s*{expected_count}\b'
            if not re.search(pattern, content):
                # Check if the code is present at all with a wrong count
                code_pattern = rf'\b{code}:\s*(\d+)'
                match = re.search(code_pattern, content)
                if match:
                    wrong_values.append(f"{code}: expected {expected_count}, found {match.group(1)}")
                else:
                    missing_codes.append(str(code))

        # Also check total requests
        total_pattern = rf'Total Requests:\s*{EXPECTED_TOTAL}'
        if not re.search(total_pattern, content):
            total_match = re.search(r'Total Requests:\s*(\d+)', content)
            if total_match:
                wrong_values.append(f"Total: expected {EXPECTED_TOTAL}, found {total_match.group(1)}")
            else:
                missing_codes.append("Total Requests line")

        if not missing_codes and not wrong_values:
            print(f"PASS: Component 2 — All status code counts correct: {list(EXPECTED_STATUS_COUNTS.keys())}, Total={EXPECTED_TOTAL} (0.4 pts)")
            total_score += 0.4
        else:
            details = []
            if missing_codes:
                details.append(f"missing: {missing_codes}")
            if wrong_values:
                details.append(f"wrong: {wrong_values}")
            print(f"FAIL: Component 2 — Status code counts incorrect. {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: log_summary.txt contains correct error rate (0.3 points)
    # Error rate = (4xx + 5xx) / total = (1+2+2+2)/20 = 7/20 = 35.00%
    try:
        error_rate_pattern = rf'Error Rate.*?{re.escape(EXPECTED_ERROR_RATE_STR)}'
        if re.search(error_rate_pattern, content, re.IGNORECASE):
            print(f"PASS: Component 3 — Error rate is {EXPECTED_ERROR_RATE_STR} (0.3 pts)")
            total_score += 0.3
        else:
            # Try to find what error rate was reported
            er_match = re.search(r'Error Rate.*?(\d+\.?\d*%)', content, re.IGNORECASE)
            if er_match:
                print(f"FAIL: Component 3 — Expected error rate {EXPECTED_ERROR_RATE_STR}, found {er_match.group(1)}")
            else:
                print(f"FAIL: Component 3 — Error rate line not found in log_summary.txt")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: verify the task
verify_task()

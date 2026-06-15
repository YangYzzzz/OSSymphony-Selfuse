"""
Reward Script: Extract third column (IP addresses) from tab-separated log file and save to ips.txt
Task ID: vscode_edit_059
Domain: vs_code
Scoring:
  Component 1: ips.txt file exists (0.3 pts)
  Component 2: ips.txt has exactly 20 lines (0.3 pts)
  Component 3: All 20 IP addresses match expected IPs from access.log column 3, in correct order (0.4 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'vscode_edit_059'

# Expected IP addresses extracted from column 3 of access.log (tab-separated, 0-indexed column 2)
EXPECTED_IPS = [
    "192.168.1.101",
    "10.0.0.47",
    "172.16.5.23",
    "192.168.2.88",
    "10.10.1.15",
    "172.31.0.200",
    "192.168.1.101",
    "10.0.0.55",
    "172.16.8.9",
    "10.0.0.47",
    "192.168.3.142",
    "172.16.5.23",
    "10.20.1.77",
    "192.168.1.200",
    "172.31.4.18",
    "10.0.0.47",
    "192.168.5.66",
    "172.16.2.34",
    "10.0.1.99",
    "192.168.1.101",
]


def verify_task():
    """
    Verify that ips.txt contains the correct IP addresses extracted from access.log column 3.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    ips_path = os.path.join(WORKDIR, 'ips.txt')

    # Component 1: ips.txt file exists (0.3 points)
    # This FAILS on initial_env (file not present) and PASSES on golden_env
    try:
        if os.path.isfile(ips_path):
            print(f"PASS: Component 1 — ips.txt exists at {ips_path} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — ips.txt not found at {ips_path}")
            # Cannot proceed further without the file
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — could not check file existence: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Read ips.txt contents for further checks
    try:
        with open(ips_path, 'r') as f:
            raw_content = f.read()
        # Strip trailing newline and split into lines, filtering blank lines
        lines = [line.strip() for line in raw_content.splitlines()]
        # Non-empty lines only (the file might have trailing newline)
        non_empty_lines = [line for line in lines if line]
    except Exception as e:
        print(f"ERROR: Could not read ips.txt: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: ips.txt has exactly 20 lines (0.3 points)
    # This FAILS on initial_env (file doesn't exist) and PASSES on golden_env
    try:
        line_count = len(non_empty_lines)
        if line_count == 20:
            print(f"PASS: Component 2 — ips.txt has exactly 20 lines (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — expected 20 lines, found {line_count} lines")
    except Exception as e:
        print(f"ERROR: Component 2 — could not count lines: {e}")

    # Component 3: All 20 IP addresses match expected IPs from access.log column 3, in order (0.4 points)
    # This FAILS on initial_env (file doesn't exist) and PASSES on golden_env
    try:
        if len(non_empty_lines) == 20:
            mismatches = []
            for i, (actual, expected) in enumerate(zip(non_empty_lines, EXPECTED_IPS), start=1):
                if actual != expected:
                    mismatches.append(f"Line {i}: expected '{expected}', got '{actual}'")
            if not mismatches:
                print(f"PASS: Component 3 — all 20 IP addresses match expected values in correct order (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 3 — {len(mismatches)} IP address mismatches:")
                for m in mismatches[:5]:  # Show first 5 mismatches
                    print(f"  {m}")
                if len(mismatches) > 5:
                    print(f"  ... and {len(mismatches) - 5} more")
        else:
            print(f"FAIL: Component 3 — cannot verify IP correctness, line count is not 20 (found {len(non_empty_lines)})")
    except Exception as e:
        print(f"ERROR: Component 3 — could not verify IP addresses: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

"""
Reward Script: Verify bash string operations script
Task ID: os_gf2_039
Domain: libreoffice_calc (actual: OS/bash scripting)
Scoring:
  Component 1: IFS splitting with read -ra (0.20)
  Component 2: Substring extraction ${var:offset:length} (0.20)
  Component 3: Regex matching [[ =~ ]] (0.20)
  Component 4: Case conversion ${var^^} or ${var,,} (0.20)
  Component 5: bash -n syntax check passes (0.20)
"""

import os
import re
import stat

WORKDIR = '/home/user'
TASK_ID = 'os_gf2_039'

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be executable
    if not os.path.isfile(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    mode = stat.S_IMODE(os.stat(file_path).st_mode)
    if not (mode & 0o111):
        print(f"CRITICAL: File is not executable (mode: {oct(mode)})")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: IFS splitting with read -ra (0.20 points)
    # The script must use IFS=',' (or IFS=",") with read -ra to split CSV into array
    try:
        has_ifs = bool(re.search(r"IFS=['\",]", content))
        has_read_ra = bool(re.search(r'read\s+-ra\s+', content))
        if has_ifs and has_read_ra:
            print(f"PASS: Component 1 — IFS splitting with read -ra found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — IFS={has_ifs}, read -ra={has_read_ra}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Substring extraction ${var:offset:length} (0.20 points)
    # Must contain pattern like ${something:number:number} or ${something:number}
    try:
        has_substring = bool(re.search(r'\$\{[^}]+:\d+:\d+\}', content))
        if has_substring:
            print(f"PASS: Component 2 — Substring extraction pattern found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — No ${{var:offset:length}} pattern found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Regex matching [[ =~ ]] (0.20 points)
    # Must use [[ ... =~ ... ]] pattern for regex matching
    try:
        has_regex = bool(re.search(r'\[\[.*=~.*\]\]', content))
        if has_regex:
            print(f"PASS: Component 3 — Regex matching [[ =~ ]] found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — No [[ =~ ]] regex matching pattern found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Case conversion ${var^^} or ${var,,} (0.20 points)
    # Must use ${var^^} for uppercase or ${var,,} for lowercase
    try:
        has_upper = bool(re.search(r'\$\{[^}]+\^\^\}', content))
        has_lower = bool(re.search(r'\$\{[^}]+,,\}', content))
        if has_upper or has_lower:
            detail = []
            if has_upper:
                detail.append('${var^^}')
            if has_lower:
                detail.append('${var,,}')
            print(f"PASS: Component 4 — Case conversion found: {', '.join(detail)} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — No ${{var^^}} or ${{var,,}} case conversion found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: bash -n syntax check passes (0.20 points)
    # Run bash -n to verify script has no syntax errors
    try:
        exit_code = os.system(f'bash -n {file_path} > /tmp/bash_check.log 2>&1')
        if exit_code == 0:
            print(f"PASS: Component 5 — bash -n syntax check passed (0.20 pts)")
            total_score += 0.20
        else:
            err_msg = ''
            try:
                with open('/tmp/bash_check.log', 'r') as ef:
                    err_msg = ef.read().strip()
            except:
                pass
            print(f"FAIL: Component 5 — bash -n failed (exit {exit_code}): {err_msg}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/string_ops.sh'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

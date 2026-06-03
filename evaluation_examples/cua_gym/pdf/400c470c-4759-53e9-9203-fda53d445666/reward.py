"""
Reward Script: Verify permissions report for restricted PDF
Task ID: pdf_mbc_034
Domain: pdf
Scoring:
  Component 1 (0.30): Report file exists and is non-empty
  Component 2 (0.20): Printing reported as Allowed
  Component 3 (0.20): Copying reported as Disallowed
  Component 4 (0.15): Modifying reported as Disallowed
  Component 5 (0.15): Annotating reported as Allowed
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_034'
REPORT_PATH = os.path.join(WORKDIR, 'Secure', 'permissions_report.txt')


def verify_task(report_path):
    """
    Verify that the permissions report was correctly generated.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Report file exists and has content (0.30 points)
    try:
        if not os.path.exists(report_path):
            print(f"FAIL: Component 1 — Report file does not exist at {report_path}")
            # No file means nothing else can pass; bail early
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        content = open(report_path, 'r').read()
        if len(content.strip()) > 0:
            print(f"PASS: Component 1 — Report file exists and has {len(content)} chars (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Report file exists but is empty")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Normalize content for flexible matching
    content_lower = content.lower()

    # Component 2: Printing reported as Allowed (0.20 points)
    try:
        # Match patterns like "Printing: Allowed", "printing - allowed", "printing  allowed"
        if re.search(r'printing\s*[:\-–]\s*allowed', content_lower):
            print(f"PASS: Component 2 — Printing correctly reported as Allowed (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Printing not reported as Allowed in report")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Copying reported as Disallowed (0.20 points)
    try:
        # Match "Copying: Disallowed", "copy: not allowed", "copying: no", "copying: disabled", etc.
        if re.search(r'copy(?:ing)?\s*[:\-–]\s*(?:disallowed|not\s*allowed|no|disabled|denied|false|restricted)', content_lower):
            print(f"PASS: Component 3 — Copying correctly reported as Disallowed (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Copying not reported as Disallowed in report")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Modifying reported as Disallowed (0.15 points)
    try:
        if re.search(r'modif(?:ying|ication|y)?\s*[:\-–]\s*(?:disallowed|not\s*allowed|no|disabled|denied|false|restricted)', content_lower):
            print(f"PASS: Component 4 — Modifying correctly reported as Disallowed (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Modifying not reported as Disallowed in report")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Annotating reported as Allowed (0.15 points)
    try:
        if re.search(r'annotat(?:ing|ion|e)?\s*[:\-–]\s*allowed', content_lower):
            print(f"PASS: Component 5 — Annotating correctly reported as Allowed (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — Annotating not reported as Allowed in report")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
if not os.path.exists(REPORT_PATH):
    print(f"File not found: {REPORT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(REPORT_PATH)

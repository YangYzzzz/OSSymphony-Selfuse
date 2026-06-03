"""
Reward Script: Read PDF metadata and write creation info to a text file
Task ID: pdf_mbc_023
Domain: pdf / libreoffice_calc
Scoring:
  Component 1 (0.3) - creation_info.txt exists and is non-empty
  Component 2 (0.3) - Mentions LibreOffice (from Producer field)
  Component 3 (0.2) - Mentions Impress (from Creator field)
  Component 4 (0.2) - Mentions version 7.6 (from Producer field)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_023'
TARGET_FILE = os.path.join(WORKDIR, 'Documents', 'creation_info.txt')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: creation_info.txt exists and is non-empty (0.3 points)
    # This file does NOT exist in initial_env, so this checks a task-introduced change.
    try:
        if not os.path.exists(TARGET_FILE):
            print(f"FAIL: Component 1 — {TARGET_FILE} does not exist")
            # No file means nothing else to check
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        content = open(TARGET_FILE, 'r').read().strip()
        if len(content) > 0:
            print(f"PASS: Component 1 — creation_info.txt exists and has content ({len(content)} chars) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — creation_info.txt exists but is empty")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Content mentions LibreOffice (0.3 points)
    # The Producer field is 'LibreOffice 7.6'. The agent should identify this.
    try:
        content_lower = content.lower()
        if 'libreoffice' in content_lower:
            print(f"PASS: Component 2 — content mentions 'LibreOffice' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — content does not mention 'LibreOffice'. Content: {content[:200]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Content mentions Impress (0.2 points)
    # The Creator field is 'Impress'. The agent should identify this as the creating application.
    try:
        if 'impress' in content_lower:
            print(f"PASS: Component 3 — content mentions 'Impress' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — content does not mention 'Impress'. Content: {content[:200]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Content mentions version 7.6 (0.2 points)
    # The Producer field contains 'LibreOffice 7.6'. The version should appear in the output.
    try:
        if '7.6' in content:
            print(f"PASS: Component 4 — content mentions version '7.6' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — content does not mention version '7.6'. Content: {content[:200]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

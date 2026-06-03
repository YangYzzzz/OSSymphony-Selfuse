"""
Reward Script: Underline all email addresses in employee directory
Task ID: writer_hr_015
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): At least one email address is underlined
  Component 2 (0.7): All 10 email addresses are underlined (progressive partial credit)
"""

import os
import re

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_hr_015'
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
EXPECTED_EMAIL_COUNT = 10


def verify_task(file_path):
    """
    Verify that all email addresses in the employee directory are underlined.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect underline status for each email-containing run
    underlined_count = 0
    total_email_count = 0

    try:
        for para in doc.paragraphs:
            for run in para.runs:
                if EMAIL_PATTERN.search(run.text):
                    total_email_count += 1
                    if run.font.underline is True:
                        underlined_count += 1
                        print(f"  UNDERLINED: {run.text}")
                    else:
                        print(f"  NOT underlined: {run.text} (underline={run.font.underline})")
    except Exception as e:
        print(f"ERROR: Failed to iterate paragraphs/runs: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"\nFound {total_email_count} email runs, {underlined_count} underlined")

    # Precondition: document must contain expected emails
    if total_email_count == 0:
        print("FAIL: No email addresses found in document")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: At least one email is underlined (0.3 points)
    # This FAILS on initial (all underline=False) and PASSES on golden (all underline=True)
    try:
        if underlined_count >= 1:
            print(f"PASS: Component 1 — at least one email underlined ({underlined_count}/{total_email_count}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — no emails are underlined (0/{total_email_count})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 10 emails underlined (0.7 points, progressive)
    # Awards partial credit proportional to fraction underlined
    # This FAILS on initial (0/10 underlined) and PASSES on golden (10/10 underlined)
    try:
        fraction = underlined_count / total_email_count
        comp2_score = round(0.7 * fraction, 2)
        if fraction >= 1.0:
            print(f"PASS: Component 2 — all {total_email_count} emails underlined (0.7 pts)")
            total_score += 0.7
        elif fraction > 0:
            print(f"PARTIAL: Component 2 — {underlined_count}/{total_email_count} emails underlined ({comp2_score} pts)")
            total_score += comp2_score
        else:
            print(f"FAIL: Component 2 — 0/{total_email_count} emails underlined (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

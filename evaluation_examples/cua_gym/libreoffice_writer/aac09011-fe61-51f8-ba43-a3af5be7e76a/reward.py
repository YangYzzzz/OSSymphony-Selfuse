"""
Reward Script: Rename resume file and update date text
Task ID: writer_creative_032
Domain: libreoffice_writer + OS file management
Scoring:
  - Component 1 (0.4): Torres_Michael_Resume_2026.docx exists on Desktop
  - Component 2 (0.3): resume_old.docx no longer exists on Desktop
  - Component 3 (0.3): The last 'Last updated' line reads 'Last updated: March 2026'
"""

import os

# python-docx for reading .docx
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_creative_032'

NEW_FILENAME = 'Torres_Michael_Resume_2026.docx'
OLD_FILENAME = 'resume_old.docx'
DESKTOP_PATH = f'{WORKDIR}/Desktop'

NEW_FILE_PATH = os.path.join(DESKTOP_PATH, NEW_FILENAME)
OLD_FILE_PATH = os.path.join(DESKTOP_PATH, OLD_FILENAME)

EXPECTED_DATE_TEXT = 'Last updated: March 2026'
OLD_DATE_TEXT = 'Last updated: January 2025'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Torres_Michael_Resume_2026.docx exists on Desktop (0.4 points)
    # This FAILS on initial_env (file doesn't exist) and PASSES on golden_env
    try:
        if os.path.exists(NEW_FILE_PATH):
            print(f"PASS: Component 1 — '{NEW_FILENAME}' exists on Desktop (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — '{NEW_FILENAME}' not found at {NEW_FILE_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: resume_old.docx no longer exists on Desktop (0.3 points)
    # This FAILS on initial_env (old file exists) and PASSES on golden_env
    try:
        if not os.path.exists(OLD_FILE_PATH):
            print(f"PASS: Component 2 — '{OLD_FILENAME}' has been removed from Desktop (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — '{OLD_FILENAME}' still exists at {OLD_FILE_PATH}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The document contains 'Last updated: March 2026' (not 'January 2025') (0.3 points)
    # This FAILS on initial_env (date is January 2025) and PASSES on golden_env (date is March 2026)
    try:
        if not os.path.exists(NEW_FILE_PATH):
            print(f"FAIL: Component 3 — Cannot check date: '{NEW_FILENAME}' not found")
        else:
            doc = Document(NEW_FILE_PATH)
            date_text_found = None
            for para in doc.paragraphs:
                if 'Last updated' in para.text:
                    date_text_found = para.text.strip()
                    break

            if date_text_found is None:
                print(f"FAIL: Component 3 — No 'Last updated' line found in document")
            elif date_text_found == EXPECTED_DATE_TEXT:
                print(f"PASS: Component 3 — Date text is '{EXPECTED_DATE_TEXT}' (0.3 pts)")
                total_score += 0.3
            elif date_text_found == OLD_DATE_TEXT:
                print(f"FAIL: Component 3 — Date text still shows old value: '{date_text_found}'")
            else:
                print(f"FAIL: Component 3 — Expected '{EXPECTED_DATE_TEXT}', found: '{date_text_found}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

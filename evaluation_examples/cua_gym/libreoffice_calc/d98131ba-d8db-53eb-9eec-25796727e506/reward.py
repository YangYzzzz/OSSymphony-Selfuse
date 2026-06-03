"""
Reward Script: Log file archival with gzip compression and Writer summary
Task ID: osworld_multi_apps_code_batch_terminal_007
Domain: os + libreoffice_writer (multi-app)
Scoring:
  Component 1: /home/user/logs/archive/ directory exists and contains .gz files (0.4 pts)
  Component 2: Exactly 9 .gz files in archive directory (0.3 pts)
  Component 3: Writer document exists and contains "9" and "archived" summary text (0.3 pts)
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_batch_terminal_007'

ARCHIVE_DIR = '/home/user/logs/archive'
DOCX_PATH = f'{WORKDIR}/{TASK_ID}.docx'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: archive directory exists and contains .gz files (0.4 points)
    # This checks the main task outcome: archive dir was created and files were compressed/moved
    try:
        if os.path.isdir(ARCHIVE_DIR):
            gz_files = [f for f in os.listdir(ARCHIVE_DIR) if f.endswith('.log.gz')]
            if len(gz_files) > 0:
                print(f"PASS: Component 1 — archive dir exists with {len(gz_files)} .gz file(s) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — archive dir exists but contains no .gz files")
        else:
            print(f"FAIL: Component 1 — archive dir does not exist at {ARCHIVE_DIR}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Exactly 9 .gz files in archive directory (0.3 points)
    # Ground truth: 9 log files older than 7 days should have been compressed and moved
    try:
        if os.path.isdir(ARCHIVE_DIR):
            gz_files = [f for f in os.listdir(ARCHIVE_DIR) if f.endswith('.log.gz')]
            count = len(gz_files)
            if count == 9:
                print(f"PASS: Component 2 — exactly 9 .gz files in archive (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — expected 9 .gz files in archive, found {count}")
        else:
            print(f"FAIL: Component 2 — archive dir does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Writer document exists and contains summary noting "9 files archived" (0.3 points)
    # Ground truth: Writer document created with summary noting '9 files archived'
    try:
        if not os.path.isfile(DOCX_PATH):
            print(f"FAIL: Component 3 — Writer document not found at {DOCX_PATH}")
        else:
            from docx import Document
            doc = Document(DOCX_PATH)
            # Collect all text from the document
            all_text = ' '.join(para.text for para in doc.paragraphs).lower()
            # Check for "9" and "archived" appearing in the document
            has_nine = '9' in all_text
            has_archived = 'archived' in all_text or 'archive' in all_text
            if has_nine and has_archived:
                print(f"PASS: Component 3 — Writer document found and contains '9' and 'archived' text (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Writer document found but missing expected content. has_nine={has_nine}, has_archived={has_archived}")
                print(f"      Document text preview: {all_text[:300]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

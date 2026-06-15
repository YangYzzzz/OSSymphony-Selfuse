"""
Reward Script: Delete old sticky note on page 2 and add new one with specified text
Task ID: pdf_basic_092
Domain: pdf
Scoring:
  Component 1 (0.5 pts): Old sticky note ('Pending review...') is ABSENT from page 2
  Component 2 (0.5 pts): New sticky note ('Approved by steering committee 03/10/2025') is PRESENT on page 2
"""

import os

# Try PyMuPDF import (canonical import for newer versions)
try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_basic_092'
PDF_PATH = f'{WORKDIR}/Desktop/project_charter.pdf'

# The exact text of the OLD sticky note that must be removed
OLD_NOTE_TEXT = 'Pending review by finance committee - awaiting sign-off from CFO'

# The exact text the NEW sticky note must contain
NEW_NOTE_TEXT = 'Approved by steering committee 03/10/2025'

# Page 2 is 0-indexed as page index 1
PAGE_INDEX = 1


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Delete old sticky note on page 2, add new sticky note with
    'Approved by steering committee 03/10/2025' on page 2.

    Scoring:
      - Component 1 (0.5): Old sticky note content NOT present on page 2
      - Component 2 (0.5): New sticky note with exact text IS present on page 2
    """
    total_score = 0.0

    # Precondition: file must exist and be openable
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: file must have at least 2 pages
    if doc.page_count < 2:
        print(f"CRITICAL: Expected at least 2 pages, found {doc.page_count}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Gather all annotations from page 2 (index 1)
    try:
        page = doc[PAGE_INDEX]
        all_annots = []
        for annot in page.annots():
            info = annot.info
            all_annots.append({
                "type": annot.type[1],
                "content": info.get("content", ""),
            })
        print(f"INFO: Page 2 has {len(all_annots)} annotation(s)")
        for i, a in enumerate(all_annots):
            print(f"  [{i}] type={a['type']!r}  content={a['content']!r}")
    except Exception as e:
        print(f"ERROR: Could not read annotations from page 2: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    doc.close()

    # Component 1: Old sticky note is ABSENT from page 2 (0.5 points)
    # This FAILS on initial_env (old note is there) and PASSES on golden_env (old note removed)
    try:
        old_note_present = any(
            a["type"] == "Text" and OLD_NOTE_TEXT in a["content"]
            for a in all_annots
        )
        if not old_note_present:
            print(f"PASS: Component 1 — old sticky note is absent from page 2 (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — old sticky note still present on page 2 (expected it to be deleted)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: New sticky note with exact required text IS PRESENT on page 2 (0.5 points)
    # This FAILS on initial_env (new note not there) and PASSES on golden_env (new note added)
    try:
        new_note_present = any(
            a["type"] == "Text" and NEW_NOTE_TEXT in a["content"]
            for a in all_annots
        )
        if new_note_present:
            print(f"PASS: Component 2 — new sticky note with required text found on page 2 (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — new sticky note with text {NEW_NOTE_TEXT!r} not found on page 2")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(PDF_PATH):
    print(f"PRECONDITION FAIL: File not found: {PDF_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(PDF_PATH)

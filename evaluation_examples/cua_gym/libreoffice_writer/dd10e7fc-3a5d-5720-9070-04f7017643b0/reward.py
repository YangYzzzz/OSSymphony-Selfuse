"""
Reward Script: Set space before/after for Heading 2 paragraphs in operations_manual.docx
Task ID: writer_para_059
Domain: libreoffice_writer
Scoring:
  Component 1: All Heading 2 paragraphs have space_before == 18pt  (0.5 pts)
  Component 2: All Heading 2 paragraphs have space_after  == 6pt   (0.5 pts)
  Total: 1.0
"""

import os
from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'writer_para_059'

TARGET_SPACE_BEFORE_PT = 18.0
TARGET_SPACE_AFTER_PT = 6.0


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document — precondition gate
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all Heading 2 paragraphs
    heading2_paras = [p for p in doc.paragraphs if p.style.name == 'Heading 2']

    if not heading2_paras:
        print("FAIL: No Heading 2 paragraphs found in document")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    print(f"INFO: Found {len(heading2_paras)} Heading 2 paragraph(s)")

    # -----------------------------------------------------------------------
    # Component 1: All Heading 2 paragraphs have space_before == 18pt (0.5 pts)
    # -----------------------------------------------------------------------
    try:
        space_before_failures = 0
        for para in heading2_paras:
            sb = para.paragraph_format.space_before
            sb_pt = sb.pt if sb is not None else None
            if sb_pt != TARGET_SPACE_BEFORE_PT:
                print(f"FAIL: Component 1 — '{para.text[:40]}' space_before={sb_pt}pt, expected {TARGET_SPACE_BEFORE_PT}pt")
                space_before_failures += 1
            else:
                print(f"PASS: Component 1 check — '{para.text[:40]}' space_before={sb_pt}pt (correct)")

        if space_before_failures == 0:
            print(f"PASS: Component 1 — All Heading 2 paragraphs have space_before=18pt (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — {space_before_failures}/{len(heading2_paras)} Heading 2 paragraphs missing space_before=18pt")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: All Heading 2 paragraphs have space_after == 6pt (0.5 pts)
    # -----------------------------------------------------------------------
    try:
        space_after_failures = 0
        for para in heading2_paras:
            sa = para.paragraph_format.space_after
            sa_pt = sa.pt if sa is not None else None
            if sa_pt != TARGET_SPACE_AFTER_PT:
                print(f"FAIL: Component 2 — '{para.text[:40]}' space_after={sa_pt}pt, expected {TARGET_SPACE_AFTER_PT}pt")
                space_after_failures += 1
            else:
                print(f"PASS: Component 2 check — '{para.text[:40]}' space_after={sa_pt}pt (correct)")

        if space_after_failures == 0:
            print(f"PASS: Component 2 — All Heading 2 paragraphs have space_after=6pt (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — {space_after_failures}/{len(heading2_paras)} Heading 2 paragraphs missing space_after=6pt")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in a given env
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Set paragraph spacing for address block and body paragraphs
Task ID: writer_para_074
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.5 pts): Paragraphs 1-5 (address block) have space_before=0pt and space_after=0pt explicitly set
  - Component 2 (0.5 pts): Paragraphs 7-9 (body paragraphs) have space_after=10pt explicitly set
  - Precondition gate: document must have at least 11 paragraphs
  - Precondition note: unchanged paragraphs (6, 10, 11) retaining None spacing is a precondition, not a scored task change
"""

import os
from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'writer_para_074'

# Paragraph indices (0-based)
ADDRESS_BLOCK_INDICES = [0, 1, 2, 3, 4]   # Paragraphs 1-5 — must get space_before=0pt, space_after=0pt
BODY_PARA_INDICES = [6, 7, 8]              # Paragraphs 7-9 — must get space_after=10pt


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = doc.paragraphs

    # Precondition gate: document must have at least 11 paragraphs
    if len(paragraphs) < 11:
        print(f"CRITICAL: Expected at least 11 paragraphs, found {len(paragraphs)}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: unchanged paragraphs (6, 10, 11 — 0-indexed 5, 9, 10) should still have None spacing.
    # These should NOT be modified by the task. If they are modified, it means an over-application of formatting.
    # (Checked as a gate to detect corruption, not awarded points — this is true on both initial and golden)
    for idx in [5, 9, 10]:
        para = paragraphs[idx]
        pf = para.paragraph_format
        sb_pt = pf.space_before.pt if pf.space_before is not None else None
        sa_pt = pf.space_after.pt if pf.space_after is not None else None
        if sb_pt is not None or sa_pt is not None:
            print(f"WARN: Para {idx+1} '{para.text[:40]}' was unexpectedly modified: space_before={sb_pt}, space_after={sa_pt}")

    # Component 1: Address block paragraphs (1-5, 0-indexed 0-4) have space_before=0pt AND space_after=0pt (0.5 points)
    # FAILS on initial (all are None) — PASSES on golden (explicitly set to 0.0)
    try:
        address_pass = 0
        for idx in ADDRESS_BLOCK_INDICES:
            para = paragraphs[idx]
            pf = para.paragraph_format
            sb = pf.space_before
            sa = pf.space_after
            sb_pt = sb.pt if sb is not None else None
            sa_pt = sa.pt if sa is not None else None
            # Must be explicitly set to 0pt (not None/inherited)
            if sb_pt == 0.0 and sa_pt == 0.0:
                address_pass += 1
                print(f"PASS: Para {idx+1} '{para.text[:40]}' space_before={sb_pt}pt, space_after={sa_pt}pt")
            else:
                print(f"FAIL: Para {idx+1} '{para.text[:40]}' expected space_before=0pt/space_after=0pt, got space_before={sb_pt}/space_after={sa_pt}")

        if address_pass == 5:
            print(f"PASS: Component 1 — all 5 address block paragraphs have space_before=0pt and space_after=0pt (0.5 pts)")
            total_score += 0.5
        elif address_pass >= 1:
            partial = round(0.5 * address_pass / 5, 2)
            print(f"PARTIAL: Component 1 — {address_pass}/5 address block paragraphs correct, partial credit {partial} pts")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — no address block paragraphs have correct spacing")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Body paragraphs (7-9, 0-indexed 6-8) have space_after=10pt explicitly set (0.5 points)
    # FAILS on initial (all are None) — PASSES on golden (explicitly set to 10.0)
    try:
        body_pass = 0
        for idx in BODY_PARA_INDICES:
            para = paragraphs[idx]
            pf = para.paragraph_format
            sa = pf.space_after
            sa_pt = sa.pt if sa is not None else None
            if sa_pt == 10.0:
                body_pass += 1
                print(f"PASS: Para {idx+1} '{para.text[:40]}' space_after={sa_pt}pt")
            else:
                print(f"FAIL: Para {idx+1} '{para.text[:40]}' expected space_after=10pt, got space_after={sa_pt}")

        if body_pass == 3:
            print(f"PASS: Component 2 — all 3 body paragraphs have space_after=10pt (0.5 pts)")
            total_score += 0.5
        elif body_pass >= 1:
            partial = round(0.5 * body_pass / 3, 2)
            print(f"PARTIAL: Component 2 — {body_pass}/3 body paragraphs correct, partial credit {partial} pts")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — no body paragraphs have space_after=10pt")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in a given env
file_path = f'{WORKDIR}/Desktop/complaint_letter.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

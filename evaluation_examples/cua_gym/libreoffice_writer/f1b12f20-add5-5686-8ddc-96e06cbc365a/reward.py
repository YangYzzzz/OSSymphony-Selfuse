"""
Reward Script: Set paragraph spacing in resume_draft.docx
Task ID: writer_para_040
Domain: libreoffice_writer
Scoring:
  Component 1: All paragraphs have space_after == 6pt              (0.5 pts)
  Component 2: Section headings have space_before == 12pt          (0.3 pts)
  Component 3: Non-heading paragraphs have space_before == 0pt     (0.2 pts)
Total: 1.0
"""

import os
from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'writer_para_040'
FILE_PATH = f'{WORKDIR}/Desktop/resume_draft.docx'

# Section headings are the bold paragraphs that are section titles (not the name).
# Based on task context: 'Professional Experience', 'Education', 'Skills'
SECTION_HEADING_TEXTS = {'Professional Experience', 'Education', 'Skills'}


def is_section_heading(para):
    """Identify section headings by their text content matching known heading names."""
    return para.text.strip() in SECTION_HEADING_TEXTS


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Task: Set space_before=0pt and space_after=6pt for all content paragraphs,
          and space_before=12pt for section headings.
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
    if not paragraphs:
        print("CRITICAL: Document has no paragraphs")
        print("REWARD: 0.0")
        return 0.0

    print(f"Document loaded. Total paragraphs: {len(paragraphs)}")

    # Component 1: All paragraphs have space_after == 6pt (0.5 points)
    # This is the primary change — every paragraph should have 6pt after.
    try:
        all_after_correct = True
        fail_details = []
        for i, para in enumerate(paragraphs):
            pf = para.paragraph_format
            sa = pf.space_after
            sa_pt = sa.pt if sa is not None else None
            if sa_pt is None or abs(sa_pt - 6.0) > 0.1:
                all_after_correct = False
                fail_details.append(f"P{i} ({repr(para.text[:40])}): space_after={sa_pt}pt (expected 6pt)")

        if all_after_correct:
            print(f"PASS: Component 1 — All {len(paragraphs)} paragraphs have space_after=6pt (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — space_after != 6pt for some paragraphs:")
            for d in fail_details:
                print(f"  {d}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Section headings have space_before == 12pt (0.3 points)
    # Section headings: 'Professional Experience', 'Education', 'Skills'
    try:
        heading_paras = [p for p in paragraphs if is_section_heading(p)]
        if len(heading_paras) == 0:
            print("FAIL: Component 2 — No section headings found with expected text")
        else:
            all_headings_correct = True
            fail_details = []
            for para in heading_paras:
                pf = para.paragraph_format
                sb = pf.space_before
                sb_pt = sb.pt if sb is not None else None
                if sb_pt is None or abs(sb_pt - 12.0) > 0.1:
                    all_headings_correct = False
                    fail_details.append(f"  '{para.text.strip()}': space_before={sb_pt}pt (expected 12pt)")

            if all_headings_correct:
                print(f"PASS: Component 2 — All {len(heading_paras)} section headings have space_before=12pt (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Section headings with wrong space_before:")
                for d in fail_details:
                    print(d)
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Non-heading paragraphs have space_before == 0pt (0.2 points)
    # All paragraphs that are NOT section headings should have space_before=0pt
    try:
        non_heading_paras = [p for p in paragraphs if not is_section_heading(p)]
        if len(non_heading_paras) == 0:
            print("FAIL: Component 3 — No non-heading paragraphs found")
        else:
            all_nonheading_correct = True
            fail_details = []
            for para in non_heading_paras:
                pf = para.paragraph_format
                sb = pf.space_before
                sb_pt = sb.pt if sb is not None else None
                if sb_pt is None or abs(sb_pt - 0.0) > 0.1:
                    all_nonheading_correct = False
                    fail_details.append(f"  P: ({repr(para.text[:40])}): space_before={sb_pt}pt (expected 0pt)")

            if all_nonheading_correct:
                print(f"PASS: Component 3 — All {len(non_heading_paras)} content paragraphs have space_before=0pt (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Content paragraphs with wrong space_before:")
                for d in fail_details:
                    print(d)
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

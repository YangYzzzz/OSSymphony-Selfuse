"""
Reward Script: Center-align title/subtitle, right-align date, justify remaining paragraphs
Task ID: writer_para_058
Domain: libreoffice_writer
Scoring:
  Component 1: Paragraphs 0 and 1 (title/subtitle) have CENTER alignment — 0.40 pts
  Component 2: Paragraph 2 (date line) has RIGHT alignment — 0.25 pts
  Component 3: Paragraphs 3-7 (body/about) all have JUSTIFY alignment — 0.35 pts
  Total: 1.0
  Note: Text content is NOT scored — it is a precondition (unchanged between initial and golden).
"""

import os
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'writer_para_058'


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

    # Sanity gate: file must have at least 8 paragraphs
    if len(paragraphs) < 8:
        print(f"CRITICAL: Document has only {len(paragraphs)} paragraphs, expected at least 8")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Title (para 0) and subtitle (para 1) must be CENTER-aligned (0.40 pts)
    # These were LEFT-aligned initially; CENTER is the task-introduced change
    try:
        para0_align = paragraphs[0].paragraph_format.alignment
        para1_align = paragraphs[1].paragraph_format.alignment
        para0_center = (para0_align == WD_PARAGRAPH_ALIGNMENT.CENTER)
        para1_center = (para1_align == WD_PARAGRAPH_ALIGNMENT.CENTER)

        if para0_center and para1_center:
            print(f"PASS: Component 1 — Paras 0 and 1 are CENTER-aligned (0.40 pts)")
            total_score += 0.40
        else:
            if not para0_center:
                print(f"FAIL: Component 1 — Para 0 (title) expected CENTER, found {para0_align}")
            if not para1_center:
                print(f"FAIL: Component 1 — Para 1 (subtitle) expected CENTER, found {para1_align}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Date line (para 2) must be RIGHT-aligned (0.25 pts)
    # This was LEFT-aligned initially; RIGHT is the task-introduced change
    try:
        para2_align = paragraphs[2].paragraph_format.alignment
        if para2_align == WD_PARAGRAPH_ALIGNMENT.RIGHT:
            print(f"PASS: Component 2 — Para 2 (date) is RIGHT-aligned (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Para 2 (date) expected RIGHT, found {para2_align}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Paragraphs 3-7 (body paragraphs and about section) must be JUSTIFY-aligned (0.35 pts)
    # All were LEFT-aligned initially; JUSTIFY is the task-introduced change
    try:
        body_indices = [3, 4, 5, 6, 7]
        body_results = [(idx, paragraphs[idx].paragraph_format.alignment) for idx in body_indices]
        failed_body = [(idx, align) for idx, align in body_results if align != WD_PARAGRAPH_ALIGNMENT.JUSTIFY]

        if not failed_body:
            print(f"PASS: Component 3 — Paras 3-7 all have JUSTIFY alignment (0.35 pts)")
            total_score += 0.35
        else:
            for idx, align in failed_body:
                print(f"FAIL: Component 3 — Para {idx} expected JUSTIFY, found {align}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

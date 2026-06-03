"""
Reward Script: Apply page break before and Heading 1 style to paragraphs 5 and 9
Task ID: writer_para_067
Domain: libreoffice_writer
Scoring:
  Component 1: Para 5 has 'Heading 1' style (0.25 pts)
  Component 2: Para 5 has page_break_before=True (0.25 pts)
  Component 3: Para 9 has 'Heading 1' style (0.25 pts)
  Component 4: Para 9 has page_break_before=True (0.25 pts)
  Total: 1.0
"""

import os

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_para_067'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.

    Task: Apply page_break_before=True and 'Heading 1' style to paragraphs 5 and 9.
    Ground truth:
      - Para 5 (index 4): style='Heading 1', page_break_before=True
      - Para 9 (index 8): style='Heading 1', page_break_before=True
      - All other paragraphs: page_break_before=False (unchanged)
      - No text content changes

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: verify expected number of paragraphs (11 paragraphs)
    paras = doc.paragraphs
    if len(paras) < 9:
        print(f"CRITICAL: Expected at least 9 paragraphs, found {len(paras)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Para 5 (index 4) has 'Heading 1' style (0.25 pts)
    # This FAILS on initial (style='Normal') → PASSES on golden (style='Heading 1')
    try:
        para5 = paras[4]  # 0-indexed, paragraph 5
        style5 = para5.style.name if para5.style else None
        if style5 == 'Heading 1':
            print(f"PASS: Component 1 — Para 5 has 'Heading 1' style (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Para 5 expected style='Heading 1', found style={style5!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Para 5 (index 4) has page_break_before=True (0.25 pts)
    # This FAILS on initial (False) → PASSES on golden (True)
    try:
        para5 = paras[4]
        pbefore5 = para5.paragraph_format.page_break_before
        if pbefore5 is True:
            print(f"PASS: Component 2 — Para 5 has page_break_before=True (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Para 5 expected page_break_before=True, found {pbefore5}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Para 9 (index 8) has 'Heading 1' style (0.25 pts)
    # This FAILS on initial (style='Normal') → PASSES on golden (style='Heading 1')
    try:
        para9 = paras[8]  # 0-indexed, paragraph 9
        style9 = para9.style.name if para9.style else None
        if style9 == 'Heading 1':
            print(f"PASS: Component 3 — Para 9 has 'Heading 1' style (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Para 9 expected style='Heading 1', found style={style9!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Para 9 (index 8) has page_break_before=True (0.25 pts)
    # This FAILS on initial (False) → PASSES on golden (True)
    try:
        para9 = paras[8]
        pbefore9 = para9.paragraph_format.page_break_before
        if pbefore9 is True:
            print(f"PASS: Component 4 — Para 9 has page_break_before=True (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — Para 9 expected page_break_before=True, found {pbefore9}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Informational: verify other paragraphs do NOT have unwanted page breaks
    # (This is a postcondition check; not scored, but logged for debugging)
    try:
        other_indices = [0, 1, 2, 3, 5, 6, 7, 9, 10]  # 0-indexed for paras 1-4, 6-8, 10-11
        bad_breaks = []
        for idx in other_indices:
            if idx < len(paras):
                pb = paras[idx].paragraph_format.page_break_before
                if pb is True:
                    bad_breaks.append(idx + 1)
        if bad_breaks:
            print(f"INFO: Paragraphs with unexpected page_break_before=True: {bad_breaks}")
        else:
            print("INFO: No unexpected page breaks on other paragraphs — correct")
    except Exception as e:
        print(f"INFO: Could not check other paragraphs — {e}")

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

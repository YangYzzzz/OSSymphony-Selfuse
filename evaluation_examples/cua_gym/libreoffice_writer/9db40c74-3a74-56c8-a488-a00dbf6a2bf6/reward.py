"""
Reward Script: Promote outline items from level 2 to level 1
Task ID: writer_list_009
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.5): 'Methodology' paragraph is promoted from 'List Number 2' to 'List Number'
  - Component 2 (0.5): 'Analysis and Findings' paragraph is promoted from 'List Number 2' to 'List Number'
Total: 1.0
"""

import os

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_list_009'

FILE_PATH = f'{WORKDIR}/Desktop/report_outline.docx'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.

    Task: Promote items 'Methodology' and 'Analysis and Findings'
    from level 2 ('List Number 2') to level 1 ('List Number').

    In the initial file, these two items use 'List Number 2' style (level 2 sub-items).
    In the golden file, all seven items use 'List Number' style (level 1).

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Build a map from paragraph text to style name for the 7 list items
    para_styles = {}
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            para_styles[text] = para.style.name

    print(f"Paragraph styles found: {para_styles}")

    # Component 1: 'Methodology' is at level 1 (style='List Number') (0.5 points)
    # In initial_env: style='List Number 2' (level 2) — this FAILS on initial
    # In golden_env:  style='List Number'   (level 1) — this PASSES on golden
    try:
        methodology_style = para_styles.get('Methodology', None)
        if methodology_style == 'List Number':
            print(f"PASS: Component 1 — 'Methodology' is 'List Number' (level 1) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — 'Methodology' style expected 'List Number', found '{methodology_style}'")
    except Exception as e:
        print(f"ERROR: Component 1 — could not check 'Methodology' style: {e}")

    # Component 2: 'Analysis and Findings' is at level 1 (style='List Number') (0.5 points)
    # In initial_env: style='List Number 2' (level 2) — this FAILS on initial
    # In golden_env:  style='List Number'   (level 1) — this PASSES on golden
    try:
        analysis_style = para_styles.get('Analysis and Findings', None)
        if analysis_style == 'List Number':
            print(f"PASS: Component 2 — 'Analysis and Findings' is 'List Number' (level 1) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — 'Analysis and Findings' style expected 'List Number', found '{analysis_style}'")
    except Exception as e:
        print(f"ERROR: Component 2 — could not check 'Analysis and Findings' style: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

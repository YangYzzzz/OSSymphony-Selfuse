"""
Reward Script: Make 'WARNING' bold and red (#FF0000) in safety_manual.docx
Task ID: writer_txtfmt_019
Domain: libreoffice_writer

Scoring Rubric:
  Component 1: 'WARNING' run in paragraph 3 is bold                     — 0.5 points
  Component 2: 'WARNING' run in paragraph 3 has font color #FF0000      — 0.5 points
  Total: 1.0

Verification Strategy:
  - Load safety_manual.docx from Desktop using python-docx
  - Locate paragraph index 3 (0-based) which starts with 'WARNING'
  - Identify the run that contains the text 'WARNING'
  - Check bold and color properties independently for partial credit
"""

import os
from docx import Document
from docx.shared import RGBColor

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_txtfmt_019'
FILE_PATH = f'{WORKDIR}/safety_manual.docx'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document — gate check
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the paragraph containing 'WARNING' at the start (paragraph 3, 0-indexed)
    # The context states: paragraph 3 begins with 'WARNING: All personnel...'
    warning_run = None
    warning_para_index = None

    try:
        for idx, para in enumerate(doc.paragraphs):
            if para.text.startswith('WARNING'):
                # Find the run that contains the 'WARNING' text
                for run in para.runs:
                    if run.text == 'WARNING':
                        warning_run = run
                        warning_para_index = idx
                        break
                if warning_run is not None:
                    break

        if warning_run is None:
            print("FAIL: Could not find a run with text 'WARNING' at the start of any paragraph")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        print(f"INFO: Found 'WARNING' run in paragraph index {warning_para_index}")
        print(f"INFO: Run text = {repr(warning_run.text)}, bold = {warning_run.font.bold}, color = {warning_run.font.color.rgb if warning_run.font.color.type else None}")

    except Exception as e:
        print(f"ERROR: Could not locate 'WARNING' run: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 1: 'WARNING' run is bold (0.5 points)
    try:
        is_bold = warning_run.font.bold
        if is_bold is True:
            print("PASS: Component 1 — 'WARNING' run is bold (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — 'WARNING' run bold expected True, found {is_bold}")
    except Exception as e:
        print(f"ERROR: Component 1 — bold check failed: {e}")

    # Component 2: 'WARNING' run has font color #FF0000 (0.5 points)
    try:
        color_type = warning_run.font.color.type
        if color_type is not None:
            actual_rgb = warning_run.font.color.rgb
            expected_rgb = RGBColor(0xFF, 0x00, 0x00)
            if actual_rgb == expected_rgb:
                print(f"PASS: Component 2 — 'WARNING' run color is #FF0000 (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 2 — 'WARNING' run color expected #FF0000, found #{actual_rgb}")
        else:
            print(f"FAIL: Component 2 — 'WARNING' run has no explicit color set (color type is None)")
    except Exception as e:
        print(f"ERROR: Component 2 — color check failed: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path on VM
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

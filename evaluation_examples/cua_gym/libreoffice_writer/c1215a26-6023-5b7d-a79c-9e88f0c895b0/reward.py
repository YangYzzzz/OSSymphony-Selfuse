"""
Reward Script: Insert registered trademark symbol (®) as superscript after 'Microsoft' and 'Windows'
Task ID: writer_txtfmt_079
Domain: libreoffice_writer
Scoring:
  Component 1: ® after 'Microsoft' is superscript=True and font_size=8pt (0.5 pts)
  Component 2: ® after 'Windows' is superscript=True and font_size=8pt  (0.5 pts)
Total: 1.0
"""

import os

from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_txtfmt_079'

FILE_PATH = f'{WORKDIR}/compatibility.docx'

REG_TM = '\u00AE'  # ® character


def find_reg_runs(all_runs):
    """
    Return list of dicts for each run that contains the ® character,
    including its properties and the text of the preceding run.
    """
    result = []
    for idx, run in enumerate(all_runs):
        if REG_TM in run.text:
            is_super = run.font.superscript
            size_pt = run.font.size.pt if run.font.size else None
            prev_text = all_runs[idx - 1].text if idx > 0 else ''
            result.append({
                'idx': idx,
                'text': run.text,
                'superscript': is_super,
                'size_pt': size_pt,
                'preceding_text': prev_text,
            })
    return result


def check_reg_after(reg_runs, keyword):
    """
    Return a dict with 'found', 'superscript', 'size_pt' for the first ®
    run whose preceding run ends with `keyword`.
    """
    for r in reg_runs:
        if r['preceding_text'].rstrip().endswith(keyword):
            return {
                'found': True,
                'superscript': r['superscript'],
                'size_pt': r['size_pt'],
            }
    return {'found': False, 'superscript': None, 'size_pt': None}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Checks that the ® symbol (U+00AE) has been inserted after 'Microsoft' and
    after 'Windows', each with superscript=True and font_size=8pt.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        all_runs = [run for para in doc.paragraphs for run in para.runs]
        print(f"INFO: Total runs found: {len(all_runs)}")
    except Exception as e:
        print(f"CRITICAL: Cannot read paragraphs: {e}")
        print("REWARD: 0.0")
        return 0.0

    reg_runs = find_reg_runs(all_runs)
    print(f"INFO: {REG_TM} runs found: {len(reg_runs)}")
    for r in reg_runs:
        print(f"  Run[{r['idx']}]: text={repr(r['text'])} superscript={r['superscript']} "
              f"size_pt={r['size_pt']} preceding={repr(r['preceding_text'])}")

    # -------------------------------------------------------------------------
    # Component 1: ® after 'Microsoft' — superscript=True and font_size=8pt (0.5 pts)
    # -------------------------------------------------------------------------
    try:
        result1 = check_reg_after(reg_runs, 'Microsoft')
        if not result1['found']:
            print("FAIL: Component 1 — No ® run found immediately after a run ending with 'Microsoft'")
        elif result1['superscript'] is True and result1['size_pt'] is not None and abs(result1['size_pt'] - 8.0) < 0.5:
            print(f"PASS: Component 1 — ® after 'Microsoft' is superscript=True and "
                  f"size={result1['size_pt']}pt (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — ® after 'Microsoft' found but superscript={result1['superscript']}, "
                  f"size_pt={result1['size_pt']}. Expected superscript=True and size=8pt")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: ® after 'Windows' — superscript=True and font_size=8pt (0.5 pts)
    # -------------------------------------------------------------------------
    try:
        result2 = check_reg_after(reg_runs, 'Windows')
        if not result2['found']:
            print("FAIL: Component 2 — No ® run found immediately after a run ending with 'Windows'")
        elif result2['superscript'] is True and result2['size_pt'] is not None and abs(result2['size_pt'] - 8.0) < 0.5:
            print(f"PASS: Component 2 — ® after 'Windows' is superscript=True and "
                  f"size={result2['size_pt']}pt (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — ® after 'Windows' found but superscript={result2['superscript']}, "
                  f"size_pt={result2['size_pt']}. Expected superscript=True and size=8pt")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Final score
    # -------------------------------------------------------------------------
    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

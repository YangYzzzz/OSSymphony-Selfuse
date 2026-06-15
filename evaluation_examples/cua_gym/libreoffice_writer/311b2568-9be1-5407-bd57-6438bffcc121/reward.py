"""
Reward Script: Format ordinal suffixes as superscript in history_essay.docx
Task ID: writer_txtfmt_060
Domain: libreoffice_writer

Scoring Rubric:
- Component 1: 'st' in '1st' has superscript=True   (0.25 pts)
- Component 2: 'nd' in '2nd' has superscript=True   (0.25 pts)
- Component 3: 'rd' in '3rd' has superscript=True   (0.25 pts)
- Component 4: 'th' in '4th' has superscript=True   (0.25 pts)
Total: 1.0

Strategy:
  Parse paragraph 2 (the ordinal sentence) and find the runs carrying 'st', 'nd', 'rd', 'th'.
  Each suffix run must have font.superscript == True.
  The numeric runs ('1','2','3','4') must NOT be superscript (sanity gate).
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_txtfmt_060'

FILE_PATH = f'{WORKDIR}/Desktop/history_essay.docx'

# Expected ordinal suffixes, in order of their appearance in paragraph 2
ORDINAL_SUFFIXES = ['st', 'nd', 'rd', 'th']


def find_ordinal_paragraph(doc):
    """
    Return the paragraph that contains the ordinals 1st, 2nd, 3rd, 4th.
    """
    for para in doc.paragraphs:
        text = para.text
        if '1st' in text and '2nd' in text and '3rd' in text and '4th' in text:
            return para
    return None


def verify_task(file_path):
    """
    Verify that the ordinal suffixes 'st', 'nd', 'rd', 'th' in the history essay
    all have superscript=True formatting.
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Load document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Locate the ordinal paragraph
    try:
        para = find_ordinal_paragraph(doc)
        if para is None:
            print("CRITICAL: Could not find paragraph containing '1st', '2nd', '3rd', '4th'")
            print("REWARD: 0.0")
            return 0.0
        print(f"INFO: Found ordinal paragraph: {repr(para.text[:80])}")
    except Exception as e:
        print(f"CRITICAL: Error locating ordinal paragraph: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect the suffix runs in order: look for runs whose text is exactly one of the suffixes
    # We expect the paragraph structure: runs with '1', 'st', ..., '2', 'nd', ..., '3', 'rd', ..., '4', 'th'
    suffix_runs = {}
    i = 0
    for run in para.runs:
        text = run.text
        if text in ORDINAL_SUFFIXES and text not in suffix_runs:
            suffix_runs[text] = run
        i += 1

    # Component 1: 'st' in '1st' has superscript=True (0.25 pts)
    try:
        run_st = suffix_runs.get('st')
        if run_st is None:
            print("FAIL: Component 1 — run with text 'st' not found in ordinal paragraph")
        elif run_st.font.superscript is True:
            print(f"PASS: Component 1 — 'st' run has superscript=True (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — 'st' run superscript={run_st.font.superscript}, expected True")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'nd' in '2nd' has superscript=True (0.25 pts)
    try:
        run_nd = suffix_runs.get('nd')
        if run_nd is None:
            print("FAIL: Component 2 — run with text 'nd' not found in ordinal paragraph")
        elif run_nd.font.superscript is True:
            print(f"PASS: Component 2 — 'nd' run has superscript=True (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — 'nd' run superscript={run_nd.font.superscript}, expected True")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'rd' in '3rd' has superscript=True (0.25 pts)
    try:
        run_rd = suffix_runs.get('rd')
        if run_rd is None:
            print("FAIL: Component 3 — run with text 'rd' not found in ordinal paragraph")
        elif run_rd.font.superscript is True:
            print(f"PASS: Component 3 — 'rd' run has superscript=True (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — 'rd' run superscript={run_rd.font.superscript}, expected True")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 'th' in '4th' has superscript=True (0.25 pts)
    try:
        run_th = suffix_runs.get('th')
        if run_th is None:
            print("FAIL: Component 4 — run with text 'th' not found in ordinal paragraph")
        elif run_th.font.superscript is True:
            print(f"PASS: Component 4 — 'th' run has superscript=True (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — 'th' run superscript={run_th.font.superscript}, expected True")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Sanity check: the numeric runs ('1','2','3','4') should NOT be superscript
    try:
        bad_numeric_runs = [
            run.text for run in para.runs
            if run.text in ('1', '2', '3', '4') and run.font.superscript is True
        ]
        if bad_numeric_runs:
            print(f"WARN: Numeric run(s) {bad_numeric_runs} unexpectedly have superscript=True (not penalized)")
        else:
            print("INFO: Sanity check — numeric runs are not superscript (correct)")
    except Exception as e:
        print(f"WARN: Sanity check error: {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

"""
Reward Script: Make the '2' in H2O a subscript in chem_notes.docx
Task ID: writer_txtfmt_009
Domain: libreoffice_writer
Scoring:
  Component 1 (0.7 pts): The '2' character run in 'H2O' has subscript=True
  Component 2 (0.3 pts): The '2' run has subscript=True AND superscript is not True
                          (confirming correct subscript, not accidental superscript)
Both components require subscript=True on the '2' run, so both FAIL on initial_env.
"""

import os

from docx import Document

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_txtfmt_009'

FILE_PATH = f'{WORKDIR}/chem_notes.docx'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document — critical gate
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the paragraph containing H2O (the chemistry paragraph)
    h2o_para = None
    for para in doc.paragraphs:
        if 'H2O' in para.text and 'polar molecule' in para.text:
            h2o_para = para
            break

    if h2o_para is None:
        print("FAIL: Could not find paragraph containing 'H2O' and 'polar molecule'")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    print(f"INFO: Found H2O paragraph: '{h2o_para.text[:70]}...'")
    print(f"INFO: Number of runs: {len(h2o_para.runs)}")
    for i, run in enumerate(h2o_para.runs):
        print(f"  Run {i}: text={repr(run.text)}, subscript={run.font.subscript}, superscript={run.font.superscript}")

    # Find the '2' run that is part of the H2O formula
    # (Look for an isolated run with text='2' or a run containing '2' adjacent to H and O runs)
    two_run = None
    for run in h2o_para.runs:
        if run.text == '2':
            two_run = run
            break
    # Fallback: find any run containing '2' where the formula context is nearby
    if two_run is None:
        for run in h2o_para.runs:
            if '2' in run.text and len(run.text) < 5:
                two_run = run
                break

    if two_run is None:
        print("FAIL: Could not locate the '2' run within the H2O paragraph")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    print(f"INFO: '2' run found: text={repr(two_run.text)}, subscript={two_run.font.subscript}, superscript={two_run.font.superscript}")

    # Component 1: The '2' run in H2O has subscript=True (0.7 points)
    # This FAILS on initial_env (subscript=None) and PASSES on golden_env (subscript=True)
    try:
        if two_run.font.subscript is True:
            print(f"PASS: Component 1 — Run '2' has subscript=True (0.7 pts)")
            total_score += 0.7
        else:
            print(f"FAIL: Component 1 — Run '2' has subscript={two_run.font.subscript}, expected True")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The '2' run has subscript=True AND superscript is not True (0.3 points)
    # Validates that subscript (not superscript) was applied — correct chemical notation
    # This FAILS on initial_env (subscript=None) and PASSES on golden_env (subscript=True, superscript=False)
    try:
        if two_run.font.subscript is True and two_run.font.superscript is not True:
            print(f"PASS: Component 2 — Run '2' has subscript=True and superscript!=True (0.3 pts)")
            total_score += 0.3
        elif two_run.font.subscript is not True:
            print(f"FAIL: Component 2 — subscript is {two_run.font.subscript}, expected True")
        else:
            print(f"FAIL: Component 2 — superscript={two_run.font.superscript} should not be True")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

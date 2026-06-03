"""
Reward Script: Apply long-dash underline style to the signature line.
Task ID: writer_txtfmt_070
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6): Signature run has DASH_LONG underline (WD_UNDERLINE.DASH_LONG == 39)
  Component 2 (0.4): All runs in signature paragraph have DASH_LONG underline + text intact
"""

import os

from docx import Document
from docx.enum.text import WD_UNDERLINE

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_txtfmt_070'
FILE_PATH = f'{WORKDIR}/formal_correspondence.docx'

SIGNATURE_TEXT = 'James T. Morrison, Director of Operations'


def verify_task(file_path):
    """
    Verify that the signature line has long-dash underline applied.
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

    # Find the signature paragraph
    sig_para = None
    for para in doc.paragraphs:
        if SIGNATURE_TEXT in para.text:
            sig_para = para
            break

    if sig_para is None:
        print(f"FAIL: Signature paragraph '{SIGNATURE_TEXT}' not found in document.")
        print("\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found signature paragraph: '{sig_para.text}'")

    # Component 1: At least one run in signature paragraph has DASH_LONG underline (0.6 points)
    # This tests the core task requirement — the underline style must be 'dashLong' (WD_UNDERLINE.DASH_LONG = 39)
    try:
        runs_with_text = [r for r in sig_para.runs if r.text.strip()]
        dash_long_runs = []
        for run in runs_with_text:
            ul = run.font.underline
            if ul == WD_UNDERLINE.DASH_LONG:
                dash_long_runs.append(run.text)

        if dash_long_runs:
            print(f"PASS: Component 1 — DASH_LONG underline found on runs: {dash_long_runs} (0.6 pts)")
            total_score += 0.6
        else:
            # Report what was found instead
            found_underlines = [(r.text[:30], r.font.underline) for r in runs_with_text]
            print(f"FAIL: Component 1 — No DASH_LONG underline found. Found: {found_underlines}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: ALL text runs in signature paragraph have DASH_LONG underline AND text is preserved (0.4 points)
    # This verifies completeness: every run is underlined AND the content wasn't corrupted
    try:
        runs_with_text = [r for r in sig_para.runs if r.text.strip()]
        if not runs_with_text:
            print(f"FAIL: Component 2 — No text runs found in signature paragraph")
        else:
            all_dash_long = all(r.font.underline == WD_UNDERLINE.DASH_LONG for r in runs_with_text)
            text_intact = SIGNATURE_TEXT in sig_para.text

            if all_dash_long and text_intact:
                print(f"PASS: Component 2 — All {len(runs_with_text)} run(s) have DASH_LONG underline and text is intact (0.4 pts)")
                total_score += 0.4
            elif not all_dash_long:
                partial_info = [(r.text[:30], r.font.underline) for r in runs_with_text]
                print(f"FAIL: Component 2 — Not all runs have DASH_LONG underline: {partial_info}")
            elif not text_intact:
                print(f"FAIL: Component 2 — Signature text corrupted. Expected: '{SIGNATURE_TEXT}', Found: '{sig_para.text}'")
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

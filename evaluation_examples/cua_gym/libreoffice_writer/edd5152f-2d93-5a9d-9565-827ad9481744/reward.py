"""
Reward Script: Change 'sudo apt install python3' font to Liberation Mono 10pt
Task ID: writer_tech_002
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): Font name is Liberation Mono for the target text
  Component 2 (0.5): Font size is 10pt for the target text
"""

import os
from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_002'

TARGET_TEXT = 'sudo apt install python3'


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def find_target_run(doc):
    """
    Find a run that contains exactly 'sudo apt install python3' as a standalone run,
    or as a distinctly formatted substring within a paragraph.

    Returns the run if found with distinct formatting, else None.
    """
    for para in doc.paragraphs:
        # Strategy 1: Look for a run whose text matches exactly (possibly with whitespace)
        for run in para.runs:
            if run.text.strip() == TARGET_TEXT:
                return run

        # Strategy 2: Look for a run containing the target text that has
        # different formatting from neighboring runs (indicating it was styled separately)
        for run in para.runs:
            if TARGET_TEXT in run.text and len(para.runs) > 1:
                return run

    return None


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

    # Find the run containing the target text
    target_run = find_target_run(doc)

    if target_run is None:
        # The target text exists but is not in a separately formatted run.
        # This means no font change was applied -- the text is still part of
        # a larger uniformly-formatted run.
        print(f"FAIL: No distinctly formatted run found for '{TARGET_TEXT}'")
        print(f"  This means the text has not been given separate formatting.")
        print("REWARD: 0.0")
        return 0.0

    font_name = target_run.font.name
    font_size_pt = target_run.font.size.pt if target_run.font.size else None
    print(f"INFO: Found target run: text='{target_run.text}', font_name={font_name}, size={font_size_pt}pt")

    # Component 1: Font name is Liberation Mono (0.5 points)
    # This check FAILS on initial (Liberation Sans 12pt, single run) and
    # PASSES on golden (Liberation Mono 10pt, separate run)
    try:
        if font_name == 'Liberation Mono':
            print(f"PASS: Component 1 -- Font name is 'Liberation Mono' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 -- Expected font 'Liberation Mono', found '{font_name}'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Font size is 10pt (0.5 points)
    # This check FAILS on initial (12pt) and PASSES on golden (10pt)
    try:
        if font_size_pt is not None and abs(font_size_pt - 10.0) < 0.1:
            print(f"PASS: Component 2 -- Font size is 10pt (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 -- Expected 10pt, found {font_size_pt}pt")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state('libreoffice_writer')

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

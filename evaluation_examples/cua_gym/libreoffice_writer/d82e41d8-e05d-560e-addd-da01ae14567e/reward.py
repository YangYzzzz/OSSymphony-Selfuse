"""
Reward Script: Demote 'Summary of Findings' from Heading 1 to Heading 2 and adjust sub-headings
Task ID: writer_fp_040
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): 'Summary of Findings' is Heading 2 (not Heading 1)
  Component 2 (0.3): 'Key Metrics' is Heading 3 (not Heading 2)
  Component 3 (0.3): 'Statistical Significance' is Heading 3 (not Heading 2)
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_fp_040'


def persist_app_state(domain: str):
    """Attempt to save any unsaved LibreOffice state via Ctrl+S."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    We check three heading-level changes introduced by the task:
      1. 'Summary of Findings' demoted from Heading 1 -> Heading 2
      2. 'Key Metrics' demoted from Heading 2 -> Heading 3
      3. 'Statistical Significance' demoted from Heading 2 -> Heading 3
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Build a map of heading text -> style name for all heading paragraphs
    headings = {}
    for para in doc.paragraphs:
        if para.style.name.startswith('Heading'):
            # Use stripped text as key
            key = para.text.strip()
            headings[key] = para.style.name

    print(f"INFO: Found headings: {headings}")

    # Component 1: 'Summary of Findings' is Heading 2 (0.4 points)
    # Initial state: Heading 1 -> Golden state: Heading 2
    try:
        sof_style = headings.get('Summary of Findings')
        if sof_style == 'Heading 2':
            print(f"PASS: Component 1 — 'Summary of Findings' is {sof_style} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — 'Summary of Findings' expected Heading 2, found: {sof_style}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'Key Metrics' is Heading 3 (0.3 points)
    # Initial state: Heading 2 -> Golden state: Heading 3
    try:
        km_style = headings.get('Key Metrics')
        if km_style == 'Heading 3':
            print(f"PASS: Component 2 — 'Key Metrics' is {km_style} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — 'Key Metrics' expected Heading 3, found: {km_style}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'Statistical Significance' is Heading 3 (0.3 points)
    # Initial state: Heading 2 -> Golden state: Heading 3
    try:
        ss_style = headings.get('Statistical Significance')
        if ss_style == 'Heading 3':
            print(f"PASS: Component 3 — 'Statistical Significance' is {ss_style} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — 'Statistical Significance' expected Heading 3, found: {ss_style}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved state before verification
persist_app_state("libreoffice_writer")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

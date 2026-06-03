"""
Reward Script: Verify InsertDisclaimer macro result
Task ID: writer_tm_079
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): Disclaimer text present as last non-empty paragraph
  Component 2 (0.35): Disclaimer paragraph runs are italic
  Component 3 (0.30): Disclaimer paragraph runs have 9pt font size
"""

import os

from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'writer_tm_079'

DISCLAIMER_TEXT = (
    'This document is provided for informational purposes only '
    'and does not constitute legal advice.'
)


def persist_app_state(domain: str):
    """Attempt to save any unsaved LibreOffice edits via Ctrl+S."""
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

    # Find the last non-empty paragraph
    last_para = None
    for p in reversed(doc.paragraphs):
        if p.text.strip():
            last_para = p
            break

    if last_para is None:
        print("FAIL: Document has no non-empty paragraphs")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Disclaimer text is present as last non-empty paragraph (0.35 points)
    try:
        # Normalize whitespace for comparison
        actual_text = ' '.join(last_para.text.strip().split())
        expected_text = ' '.join(DISCLAIMER_TEXT.strip().split())
        if actual_text.lower() == expected_text.lower():
            print(f"PASS: Component 1 — Disclaimer text found as last paragraph (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — Last paragraph text does not match disclaimer")
            print(f"  Expected: {expected_text[:80]}...")
            print(f"  Found:    {actual_text[:80]}...")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Disclaimer paragraph is italic formatted (0.35 points)
    try:
        runs = [r for r in last_para.runs if r.text.strip()]
        if not runs:
            print("FAIL: Component 2 — Disclaimer paragraph has no runs with text")
        else:
            all_italic = all(r.font.italic is True for r in runs)
            if all_italic:
                print(f"PASS: Component 2 — All runs in disclaimer are italic (0.35 pts)")
                total_score += 0.35
            else:
                italic_status = [(r.text[:30], r.font.italic) for r in runs]
                print(f"FAIL: Component 2 — Not all runs are italic: {italic_status}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Disclaimer paragraph has 9pt font size (0.30 points)
    try:
        runs = [r for r in last_para.runs if r.text.strip()]
        if not runs:
            print("FAIL: Component 3 — Disclaimer paragraph has no runs with text")
        else:
            all_9pt = all(
                r.font.size is not None and abs(r.font.size.pt - 9.0) < 0.5
                for r in runs
            )
            if all_9pt:
                print(f"PASS: Component 3 — All runs have 9pt font size (0.30 pts)")
                total_score += 0.30
            else:
                size_info = [(r.text[:30], r.font.size.pt if r.font.size else None) for r in runs]
                print(f"FAIL: Component 3 — Not all runs have 9pt size: {size_info}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
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

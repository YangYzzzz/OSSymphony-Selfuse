"""
Reward Script: Convert two-column section to three-column layout with separator and column break
Task ID: writer_rd_018
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Column count changed from 2 to 3
  Component 2 (0.3): Vertical separator line enabled (sep="1")
  Component 3 (0.3): Column break inserted after paragraph 2
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_018'


def persist_app_state(domain: str):
    """Try to save any unsaved LibreOffice edits before verification."""
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

    Task: Convert two-column section to three-column layout with vertical
    separator line, and add a column break after the second paragraph.

    Initial state: 2 columns, sep=0, no column breaks
    Golden state: 3 columns, sep=1, column break after para 2
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    body = doc.element.body

    # Find the cols element in the section properties
    cols_elem = None
    for sectPr in body.iter(qn('w:sectPr')):
        c = sectPr.find(qn('w:cols'))
        if c is not None:
            cols_elem = c
            break

    if cols_elem is None:
        print("FAIL: No w:cols element found in document")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Column count is 3 (0.4 points)
    # Initial has num=2, golden has num=3
    try:
        num_cols = cols_elem.get(qn('w:num'))
        if num_cols is not None and int(num_cols) == 3:
            print(f"PASS: Component 1 — Column count is 3 (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Expected 3 columns, found num={num_cols}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Vertical separator line enabled (0.3 points)
    # Initial has sep=0, golden has sep=1
    try:
        sep_val = cols_elem.get(qn('w:sep'))
        if sep_val is not None and str(sep_val) == '1':
            print(f"PASS: Component 2 — Separator line enabled (sep=1) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected sep=1, found sep={sep_val}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Column break after paragraph 2 (0.3 points)
    # Initial has no column breaks, golden has one after para 2
    try:
        column_break_found = False
        # Check paragraphs for column breaks
        paragraphs = doc.paragraphs
        if len(paragraphs) >= 3:
            # The column break should be in paragraph 2 (0-indexed)
            # i.e., the third paragraph (para index 2) which is the paragraph
            # after the heading (para 0) and two content paragraphs (para 1, 2)
            # The break could be at the end of para 2 or beginning of para 3
            # Check paras around index 2 for column breaks
            for check_idx in range(len(paragraphs)):
                for run in paragraphs[check_idx].runs:
                    for br in run.element.findall(qn('w:br')):
                        br_type = br.get(qn('w:type'))
                        if br_type == 'column':
                            column_break_found = True
                            print(f"  Found column break in paragraph {check_idx}")

        if column_break_found:
            print(f"PASS: Component 3 — Column break found in document (0.3 pts)")
            total_score += 0.3
        else:
            # Also check for column breaks in the raw XML (might not be in runs)
            all_breaks = list(body.iter(qn('w:br')))
            for br in all_breaks:
                if br.get(qn('w:type')) == 'column':
                    column_break_found = True
                    break
            if column_break_found:
                print(f"PASS: Component 3 — Column break found via XML scan (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — No column break found in document")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

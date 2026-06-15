"""
Reward Script: Apply superscript to ordinal suffixes and subscript to chemical formula numbers
Task ID: writer_rd_092
Domain: libreoffice_writer
Scoring:
  Precondition gate: Document text integrity preserved (no points, early exit if corrupted)
  Component 1: Superscript on ordinal suffixes (st, nd, rd, th) — 0.55 points (progressive)
  Component 2: Subscript on chemical formula numbers — 0.45 points (progressive)
"""

import os
import re

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_092'


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
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all runs with their formatting info
    superscript_runs = []
    subscript_runs = []
    all_text = []

    for para in doc.paragraphs:
        all_text.append(para.text)
        for run in para.runs:
            if run.font.superscript:
                superscript_runs.append(run.text)
            if run.font.subscript:
                subscript_runs.append(run.text)

    full_text = '\n'.join(all_text)

    # Precondition gate: Document text integrity (no points — early exit if corrupted)
    # This is true in BOTH initial and golden, so it must NOT contribute to score.
    try:
        key_phrases = [
            "Annual Environmental Chemistry Report",
            "Water Quality Analysis",
            "Atmospheric Composition",
            "Chemical Analysis Summary",
            "Conclusions",
        ]
        has_ordinal = bool(re.search(r'\d+(st|nd|rd|th)', full_text))
        has_chemical = bool(re.search(r'(H2O|CO2|CH4|SO2|NaCl)', full_text))
        phrases_found = sum(1 for phrase in key_phrases if phrase in full_text)
        if phrases_found < 3 or not has_ordinal or not has_chemical:
            print(f"GATE FAIL: Document text corrupted — {phrases_found}/5 phrases, ordinal={has_ordinal}, chemical={has_chemical}")
            print("REWARD: 0.0")
            return 0.0
        else:
            print(f"GATE PASS: Document text intact ({phrases_found}/5 phrases, ordinals and chemicals present)")
    except Exception as e:
        print(f"GATE ERROR: {e} — continuing anyway")

    # Component 1: Superscript formatting on ordinal suffixes (0.55 points)
    # Expected: ordinal suffixes like 'st', 'nd', 'rd', 'th' should be superscript
    # Golden has 16 superscript runs; progressive scoring based on coverage
    try:
        # Count superscript runs that are valid ordinal suffixes
        valid_ordinal_suffixes = {'st', 'nd', 'rd', 'th'}
        ordinal_super_count = sum(
            1 for text in superscript_runs
            if text.strip().lower() in valid_ordinal_suffixes
        )

        # Expected ~16 ordinal suffixes in superscript
        expected_ordinal_super = 16
        if ordinal_super_count >= 1:
            ratio = min(ordinal_super_count / expected_ordinal_super, 1.0)
            points = round(0.55 * ratio, 4)
            label = "PASS" if ordinal_super_count >= 12 else "PARTIAL"
            print(f"{label}: Component 1 — {ordinal_super_count}/{expected_ordinal_super} ordinal suffixes superscripted ({points:.2f} pts)")
            total_score += points
        else:
            print(f"FAIL: Component 1 — No ordinal suffixes found with superscript formatting (found {ordinal_super_count})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Subscript formatting on chemical formula numbers (0.45 points)
    # Expected: numbers in chemical formulas (H2O, CO2, NaCl, CH4, SO2) should be subscript
    # Golden has 11 subscript runs, all with text '2' or '4'
    try:
        # Count subscript runs that are digit characters (chemical formula numbers)
        chem_sub_count = sum(
            1 for text in subscript_runs
            if text.strip().isdigit()
        )

        expected_chem_sub = 11
        if chem_sub_count >= 1:
            ratio = min(chem_sub_count / expected_chem_sub, 1.0)
            points = round(0.45 * ratio, 4)
            label = "PASS" if chem_sub_count >= 8 else "PARTIAL"
            print(f"{label}: Component 2 — {chem_sub_count}/{expected_chem_sub} chemical formula numbers subscripted ({points:.2f} pts)")
            total_score += points
        else:
            print(f"FAIL: Component 2 — No chemical formula numbers found with subscript formatting (found {chem_sub_count})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Attempt to persist unsaved state before verification
persist_app_state("libreoffice_writer")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

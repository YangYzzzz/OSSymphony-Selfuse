"""
Reward Script: Expand print area and configure comment printing
Task ID: calc_mcp_095
Domain: libreoffice_calc
Scoring:
  Component 1 (0.5): Print area expanded to A1:H50
  Component 2 (0.3): cellComments set to 'atEnd'
  Component 3 (0.2): Both print area AND cellComments correct together (consistency check)
"""

import os
import re
import time

WORKDIR = '/home/user'
TASK_ID = 'calc_mcp_095'


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
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

    Task: Expand print area from A1:D20 to A1:H50 and configure
    comments/notes to print at end of sheet.

    Scoring rubric:
      Component 1 (0.5 pts): Print area is A1:H50
      Component 2 (0.3 pts): cellComments is 'atEnd'
      Component 3 (0.2 pts): Both conditions met simultaneously (integrity check)
    """
    total_score = 0.0

    try:
        import openpyxl
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Verify sheet exists (precondition gate, not scored)
    if 'Print Preview' not in wb.sheetnames:
        print("CRITICAL: 'Print Preview' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Print Preview']

    print_area_ok = False
    comments_ok = False

    # Component 1: Print area expanded to A1:H50 (0.5 points)
    # Initial state has A1:D20, golden should have A1:H50
    try:
        raw_print_area = ws.print_area
        print(f"DEBUG: Raw print_area value: {raw_print_area!r}")

        if raw_print_area:
            # Normalize: remove sheet name prefix, quotes, and dollar signs
            # Could be: "'Print Preview'!$A$1:$H$50" or "''!$A$1:$H$50" etc.
            pa = str(raw_print_area)
            # Remove everything up to and including the '!'
            if '!' in pa:
                pa = pa.split('!')[-1]
            # Remove dollar signs
            pa = pa.replace('$', '')
            # Normalize to uppercase
            pa = pa.upper().strip()

            print(f"DEBUG: Normalized print area: {pa!r}")

            if pa == 'A1:H50':
                print(f"PASS: Component 1 — Print area is A1:H50 (0.5 pts)")
                total_score += 0.5
                print_area_ok = True
            else:
                print(f"FAIL: Component 1 — Expected print area A1:H50, found: {pa}")
        else:
            print(f"FAIL: Component 1 — No print area defined")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Comments configured to print at end of sheet (0.3 points)
    # Initial state has cellComments=None (default), golden should have 'atEnd'
    try:
        cell_comments = ws.page_setup.cellComments
        print(f"DEBUG: cellComments value: {cell_comments!r}")

        if cell_comments is not None and str(cell_comments).lower() == 'atend':
            print(f"PASS: Component 2 — cellComments is 'atEnd' (0.3 pts)")
            total_score += 0.3
            comments_ok = True
        else:
            print(f"FAIL: Component 2 — Expected cellComments='atEnd', found: {cell_comments}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Both print area AND cellComments correct (0.2 points)
    # This is a compound integrity check — only awards if BOTH changes are present
    try:
        if print_area_ok and comments_ok:
            print(f"PASS: Component 3 — Both print area and comment settings correct (0.2 pts)")
            total_score += 0.2
        else:
            missing = []
            if not print_area_ok:
                missing.append("print area")
            if not comments_ok:
                missing.append("cellComments")
            print(f"FAIL: Component 3 — Missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved GUI state before verification
persist_app_state("libreoffice_calc")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Configure page footer on 'Data' sheet with 'Page X of Y' centered
Task ID: calc_gg1_037
Domain: libreoffice_calc
Scoring:
  - Component 1 (0.60): Center footer contains 'Page &P of &N' pattern
  - Component 2 (0.20): Center footer correct AND left/right sections remain empty
  - Component 3 (0.20): Center footer correct AND all headers remain unaffected
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'calc_gg1_037'


def persist_app_state(domain: str):
    """Try to save any unsaved LibreOffice changes before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for libreoffice_calc")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    import openpyxl

    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: 'Data' sheet must exist
    if 'Data' not in wb.sheetnames:
        print("FAIL: 'Data' sheet not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Data']

    # Helper: check if center footer has the correct 'Page X of Y' pattern
    def get_center_footer_valid():
        """Returns True if center footer matches 'Page &P of &N' pattern."""
        try:
            center_text = None
            if ws.oddFooter and ws.oddFooter.center:
                center_text = ws.oddFooter.center.text
            if center_text is None:
                return False
            normalized = center_text.strip()
            pattern = re.compile(
                r'[Pp]age\s+&(P|PAGE)\s+of\s+&(N|PAGES)',
                re.IGNORECASE
            )
            return bool(pattern.search(normalized))
        except Exception:
            return False

    center_valid = get_center_footer_valid()

    # Component 1: Center footer contains 'Page &P of &N' pattern (0.60 points)
    # This is the core task requirement -- FAILS on initial (no footer), PASSES on golden
    try:
        center_text = None
        if ws.oddFooter and ws.oddFooter.center:
            center_text = ws.oddFooter.center.text

        if center_valid:
            print(f"PASS: Component 1 - Center footer has correct 'Page X of Y' pattern: '{center_text}' (0.60 pts)")
            total_score += 0.60
        else:
            print(f"FAIL: Component 1 - Center footer is empty or does not match pattern (found: '{center_text}')")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Center footer correct AND left/right sections are empty (0.20 points)
    # Anchored to the task change: only awards points if Component 1 also passes
    try:
        if not center_valid:
            print("FAIL: Component 2 - Skipped (center footer not set correctly)")
        else:
            left_text = None
            right_text = None
            if ws.oddFooter and ws.oddFooter.left:
                left_text = ws.oddFooter.left.text
            if ws.oddFooter and ws.oddFooter.right:
                right_text = ws.oddFooter.right.text

            left_empty = (left_text is None or left_text.strip() == '')
            right_empty = (right_text is None or right_text.strip() == '')

            if left_empty and right_empty:
                print(f"PASS: Component 2 - Center footer correct AND left/right are empty (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 - Left or right footer has unexpected content: left='{left_text}', right='{right_text}'")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Center footer correct AND all headers remain unaffected (0.20 points)
    # Anchored to the task change: only awards points if Component 1 also passes
    try:
        if not center_valid:
            print("FAIL: Component 3 - Skipped (center footer not set correctly)")
        else:
            header_texts = []
            for attr in ['left', 'center', 'right']:
                part = getattr(ws.oddHeader, attr, None) if ws.oddHeader else None
                if part and part.text and part.text.strip():
                    header_texts.append(f"{attr}='{part.text}'")

            if len(header_texts) == 0:
                print(f"PASS: Component 3 - Center footer correct AND headers are unaffected (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 - Headers have unexpected content: {', '.join(header_texts)}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_calc")

file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

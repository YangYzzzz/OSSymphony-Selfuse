"""
Reward Script: Navigate to 'Dept_15' sheet in a 20-sheet workbook
Task ID: calc_ps_092
Domain: libreoffice_calc
Scoring:
  Component 1 (0.6 pts): Active sheet is 'Dept_15' (activeTab == 14)
  Component 2 (0.4 pts): Active sheet is 'Dept_15' AND all 20 dept sheets intact
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'calc_ps_092'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            import time
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for libreoffice_calc")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Parse the raw XML to get activeTab reliably
    try:
        import xml.etree.ElementTree as ET
        from zipfile import ZipFile
        with ZipFile(file_path) as zf:
            with zf.open('xl/workbook.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                bv = root.find('.//ns:bookViews/ns:workbookView', ns)
                active_tab = int(bv.get('activeTab', '0')) if bv is not None else 0
    except Exception as e:
        print(f"CRITICAL: Cannot parse workbook XML from {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Also load with openpyxl for sheet name verification
    try:
        import openpyxl
        wb = openpyxl.load_workbook(file_path)
        sheet_names = wb.sheetnames
    except Exception as e:
        print(f"CRITICAL: Cannot load workbook {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Active sheet is Dept_15 (activeTab == 14) — 0.6 points
    # Initial env has activeTab=0 (Dept_01), golden should have activeTab=14 (Dept_15)
    try:
        if active_tab == 14:
            # Double-check that index 14 corresponds to 'Dept_15'
            if len(sheet_names) > 14 and sheet_names[14] == 'Dept_15':
                print(f"PASS: Component 1 — activeTab={active_tab}, sheet at index 14 is '{sheet_names[14]}' (0.6 pts)")
                total_score += 0.6
            else:
                print(f"FAIL: Component 1 — activeTab=14 but sheet at index 14 is '{sheet_names[14] if len(sheet_names) > 14 else 'N/A'}', expected 'Dept_15'")
        else:
            # Check if Dept_15 is active but at a different index (sheets may have been reordered)
            if active_tab < len(sheet_names) and sheet_names[active_tab] == 'Dept_15':
                print(f"PASS: Component 1 — activeTab={active_tab}, active sheet is 'Dept_15' (0.6 pts)")
                total_score += 0.6
            else:
                active_name = sheet_names[active_tab] if active_tab < len(sheet_names) else 'N/A'
                print(f"FAIL: Component 1 — activeTab={active_tab}, active sheet is '{active_name}', expected 'Dept_15'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Active sheet is Dept_15 AND all 20 department sheets exist in order — 0.4 points
    # This component is anchored to the task change (active sheet must be Dept_15)
    # and also verifies data integrity as a compound check
    try:
        expected_sheets = [f'Dept_{i:02d}' for i in range(1, 21)]
        sheets_intact = (sheet_names == expected_sheets)
        active_is_dept15 = (active_tab < len(sheet_names) and sheet_names[active_tab] == 'Dept_15')

        if active_is_dept15 and sheets_intact:
            print(f"PASS: Component 2 — Dept_15 is active AND all 20 sheets intact in correct order (0.4 pts)")
            total_score += 0.4
        elif active_is_dept15 and not sheets_intact:
            print(f"FAIL: Component 2 — Dept_15 is active but sheet list changed: {sheet_names}")
        elif not active_is_dept15:
            print(f"FAIL: Component 2 — Dept_15 is not the active sheet")
        else:
            print(f"FAIL: Component 2 — conditions not met")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

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

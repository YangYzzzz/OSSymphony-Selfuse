"""
Reward Script: Move 'Charts' sheet to be right after 'Data' sheet
Task ID: calc_ps_060
Domain: libreoffice_calc
Scoring:
  Component 1 (0.5): 'Charts' sheet is at index 2 (right after 'Data')
  Component 2 (0.3): 'Analysis' sheet is at index 3 (moved to last)
  Component 3 (0.2): Exact full sheet order AND data integrity preserved
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_ps_060'

EXPECTED_ORDER = ['Summary', 'Data', 'Charts', 'Analysis']


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    sheet_names = wb.sheetnames
    print(f"INFO: Found sheets: {sheet_names}")

    # Component 1: 'Charts' sheet is at index 2 (right after 'Data') (0.5 points)
    # In initial state, Charts is at index 3 (last). Task moves it to index 2.
    try:
        if 'Charts' in sheet_names:
            charts_idx = sheet_names.index('Charts')
            if charts_idx == 2:
                print(f"PASS: Component 1 — 'Charts' is at index 2 (right after 'Data') (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 1 — 'Charts' is at index {charts_idx}, expected index 2")
        else:
            print("FAIL: Component 1 — 'Charts' sheet not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'Analysis' sheet is at index 3 (0.3 points)
    # In initial state, Analysis is at index 2. After moving Charts, Analysis shifts to index 3.
    try:
        if 'Analysis' in sheet_names:
            analysis_idx = sheet_names.index('Analysis')
            if analysis_idx == 3:
                print(f"PASS: Component 2 — 'Analysis' is at index 3 (last position) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — 'Analysis' is at index {analysis_idx}, expected index 3")
        else:
            print("FAIL: Component 2 — 'Analysis' sheet not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Exact full sheet order AND data integrity (0.2 points)
    # Checks that the complete order is correct and key data cells are preserved.
    try:
        order_correct = (sheet_names == EXPECTED_ORDER)
        if not order_correct:
            print(f"FAIL: Component 3 — Sheet order {sheet_names} != expected {EXPECTED_ORDER}")
        else:
            # Verify data integrity: spot-check key cells in each sheet
            # Count how many integrity checks pass out of 8 total
            integrity_pass_count = 0
            integrity_total = 8

            # Summary sheet: A1 should be 'Metric', B2 should be 125400
            ws_summary = wb['Summary']
            if ws_summary['A1'].value == 'Metric':
                integrity_pass_count += 1
            else:
                print(f"FAIL: Component 3 — Summary!A1 expected 'Metric', found {ws_summary['A1'].value}")
            if ws_summary['B2'].value == 125400:
                integrity_pass_count += 1
            else:
                print(f"FAIL: Component 3 — Summary!B2 expected 125400, found {ws_summary['B2'].value}")

            # Data sheet: A1 should be 'Employee ID', B2 should be 'Sarah Chen'
            ws_data = wb['Data']
            if ws_data['A1'].value == 'Employee ID':
                integrity_pass_count += 1
            else:
                print(f"FAIL: Component 3 — Data!A1 expected 'Employee ID', found {ws_data['A1'].value}")
            if ws_data['B2'].value == 'Sarah Chen':
                integrity_pass_count += 1
            else:
                print(f"FAIL: Component 3 — Data!B2 expected 'Sarah Chen', found {ws_data['B2'].value}")

            # Charts sheet: A1 should be 'Department', B2 should be 460500
            ws_charts = wb['Charts']
            if ws_charts['A1'].value == 'Department':
                integrity_pass_count += 1
            else:
                print(f"FAIL: Component 3 — Charts!A1 expected 'Department', found {ws_charts['A1'].value}")
            if ws_charts['B2'].value == 460500:
                integrity_pass_count += 1
            else:
                print(f"FAIL: Component 3 — Charts!B2 expected 460500, found {ws_charts['B2'].value}")

            # Analysis sheet: A1 should be 'Department', B2 should be 5
            ws_analysis = wb['Analysis']
            if ws_analysis['A1'].value == 'Department':
                integrity_pass_count += 1
            else:
                print(f"FAIL: Component 3 — Analysis!A1 expected 'Department', found {ws_analysis['A1'].value}")
            if ws_analysis['B2'].value == 5:
                integrity_pass_count += 1
            else:
                print(f"FAIL: Component 3 — Analysis!B2 expected 5, found {ws_analysis['B2'].value}")

            if integrity_pass_count == integrity_total:
                print(f"PASS: Component 3 — Full sheet order correct AND data integrity verified ({integrity_pass_count}/{integrity_total} checks) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Sheet order correct but data integrity check failed ({integrity_pass_count}/{integrity_total} checks passed)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved GUI state before verification
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_calc")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)

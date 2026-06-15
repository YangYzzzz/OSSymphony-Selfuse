"""
Reward Script: Library Book Tracking System
Task ID: calc_wf_051
Domain: libreoffice_calc
Scoring:
  Component 1 (0.25) - Dashboard formulas: Currently Loaned, Overdue, Popular Book, Avg Duration
  Component 2 (0.25) - Dashboard formulas are correct type (COUNTBLANK, COUNTIFS, INDEX/COUNTIF, AVERAGEIF)
  Component 3 (0.25) - Conditional formatting on Loans sheet for overdue rows (red fill)
  Component 4 (0.25) - Line chart on Dashboard for monthly checkout trends
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'calc_wf_051'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
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

    Scoring rubric (only checks task-introduced changes):
      Component 1 (0.25): Dashboard cells B3-B6 have formulas (were None in initial)
      Component 2 (0.25): Dashboard formulas reference correct functions
      Component 3 (0.25): Conditional formatting on Loans for overdue rows
      Component 4 (0.25): Line chart exists on Dashboard for monthly checkout trends
    """
    import openpyxl

    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: required sheets must exist
    required_sheets = ['Catalog', 'Loans', 'Dashboard']
    for s in required_sheets:
        if s not in wb.sheetnames:
            print(f"CRITICAL: Missing required sheet '{s}'")
            print("REWARD: 0.0")
            return 0.0

    ws_dashboard = wb['Dashboard']
    ws_loans = wb['Loans']

    # =========================================================================
    # Component 1: Dashboard cells B3-B6 contain formulas (0.25 points)
    # In the initial file these cells are None/empty. The task requires
    # populating them with statistics formulas.
    # =========================================================================
    try:
        formula_cells = {
            'B3': 'Currently Loaned Books',
            'B4': 'Overdue Items',
            'B5': 'Most Popular Book',
            'B6': 'Average Loan Duration',
        }
        formulas_found = 0
        for cell_ref, desc in formula_cells.items():
            val = ws_dashboard[cell_ref].value
            if val is not None and isinstance(val, str) and val.startswith('='):
                formulas_found += 1
                print(f"  PASS: {cell_ref} has formula: {val[:60]}")
            elif val is not None:
                # Could be a cached numeric value (data_only effect or manual entry)
                formulas_found += 1
                print(f"  PASS: {cell_ref} has value: {val} (possibly computed)")
            else:
                print(f"  FAIL: {cell_ref} ({desc}) is empty/None")

        if formulas_found == 4:
            print(f"PASS: Component 1 -- All 4 dashboard statistics populated (0.25 pts)")
            total_score += 0.25
        elif formulas_found >= 2:
            partial = 0.25 * (formulas_found / 4)
            print(f"PARTIAL: Component 1 -- {formulas_found}/4 dashboard stats populated ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 -- Only {formulas_found}/4 dashboard stats populated")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # =========================================================================
    # Component 2: Dashboard formulas use correct function types (0.25 points)
    # B3 should use COUNTBLANK, B4 should use COUNTIFS, B5 should use
    # COUNTIF (for popularity), B6 should use AVERAGE/AVERAGEIF
    # =========================================================================
    try:
        formula_checks = {
            'B3': ('COUNTBLANK', 'Currently Loaned count'),
            'B4': ('COUNTIF', 'Overdue count'),  # COUNTIFS contains COUNTIF
            'B5': ('COUNTIF', 'Most Popular book'),
            'B6': ('AVERAGE', 'Average loan duration'),  # AVERAGEIF contains AVERAGE
        }
        correct_formulas = 0
        for cell_ref, (expected_func, desc) in formula_checks.items():
            val = ws_dashboard[cell_ref].value
            if val is not None and isinstance(val, str):
                val_upper = val.upper()
                if expected_func in val_upper:
                    correct_formulas += 1
                    print(f"  PASS: {cell_ref} contains {expected_func}: {val[:60]}")
                else:
                    print(f"  FAIL: {cell_ref} missing {expected_func}, found: {val[:60]}")
            else:
                print(f"  FAIL: {cell_ref} ({desc}) has no formula string")

        if correct_formulas == 4:
            print(f"PASS: Component 2 -- All 4 formulas use correct functions (0.25 pts)")
            total_score += 0.25
        elif correct_formulas >= 2:
            partial = 0.25 * (correct_formulas / 4)
            print(f"PARTIAL: Component 2 -- {correct_formulas}/4 correct formula types ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- Only {correct_formulas}/4 correct formula types")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # =========================================================================
    # Component 3: Conditional formatting on Loans sheet for overdue rows (0.25 pts)
    # The initial file has NO conditional formatting on Loans.
    # The golden file has a formula-based CF rule with red fill for overdue rows.
    # =========================================================================
    try:
        cf_rules = list(ws_loans.conditional_formatting)
        if len(cf_rules) > 0:
            # Check that at least one rule applies to the Loans data range
            has_overdue_rule = False
            has_red_fill = False
            for cf in cf_rules:
                for rule in cf.rules:
                    # Check for formula-based or expression rule
                    if rule.type in ('expression', 'cellIs'):
                        has_overdue_rule = True
                    # Check for red-ish fill in the DXF style
                    if rule.dxf and rule.dxf.fill:
                        try:
                            fg = rule.dxf.fill.fgColor
                            if fg and fg.rgb:
                                rgb = fg.rgb
                                # Check if it's reddish (R channel high)
                                if isinstance(rgb, str) and len(rgb) >= 6:
                                    r_val = int(rgb[-6:-4], 16) if len(rgb) >= 6 else 0
                                    if r_val >= 200:
                                        has_red_fill = True
                        except Exception:
                            pass

            if has_overdue_rule and has_red_fill:
                print(f"PASS: Component 3 -- Conditional formatting with red fill for overdue (0.25 pts)")
                total_score += 0.25
            elif has_overdue_rule:
                print(f"PARTIAL: Component 3 -- CF rule exists but no red fill detected (0.15 pts)")
                total_score += 0.15
            else:
                print(f"PARTIAL: Component 3 -- CF exists but no overdue rule found (0.10 pts)")
                total_score += 0.10
        else:
            print(f"FAIL: Component 3 -- No conditional formatting rules on Loans sheet")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # =========================================================================
    # Component 4: Line chart on Dashboard for monthly checkout trends (0.25 pts)
    # The initial file has NO charts. The golden has a LineChart on Dashboard.
    # =========================================================================
    try:
        charts = ws_dashboard._charts
        if len(charts) > 0:
            # Check for a line chart
            has_line_chart = False
            for ch in charts:
                chart_type = type(ch).__name__
                if 'Line' in chart_type:
                    has_line_chart = True
                    # Try to extract title text
                    title_text = ''
                    try:
                        if ch.title and ch.title.tx and ch.title.tx.rich:
                            for p in ch.title.tx.rich.p:
                                for run in p.r:
                                    title_text += run.t
                    except Exception:
                        pass
                    print(f"  Found LineChart with title: '{title_text}'")
                    break

            if has_line_chart:
                print(f"PASS: Component 4 -- Line chart exists on Dashboard (0.25 pts)")
                total_score += 0.25
            else:
                # There's a chart but not a line chart
                print(f"PARTIAL: Component 4 -- Chart exists but not a LineChart (0.10 pts)")
                total_score += 0.10
        else:
            print(f"FAIL: Component 4 -- No charts on Dashboard sheet")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

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

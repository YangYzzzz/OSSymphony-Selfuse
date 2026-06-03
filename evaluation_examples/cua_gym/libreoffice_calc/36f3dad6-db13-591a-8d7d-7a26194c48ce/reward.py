"""
Reward Script: Apply Data Bar conditional formatting to D2:D41 on 'Leaderboard' sheet
Task ID: calc_gg1_029
Domain: libreoffice_calc
Scoring:
  - Component 1 (0.35): Conditional formatting rule exists on D2:D41
  - Component 2 (0.30): Rule type is dataBar
  - Component 3 (0.20): DataBar showValue is True (numbers still visible)
  - Component 4 (0.15): DataBar uses min/max format objects for proportional bars
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gg1_029'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
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
    Verify that Data Bar conditional formatting has been applied to D2:D41
    on the 'Leaderboard' sheet.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load workbook
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Check 'Leaderboard' sheet exists (precondition gate)
    if 'Leaderboard' not in wb.sheetnames:
        print("CRITICAL: 'Leaderboard' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Leaderboard']

    # Collect all conditional formatting rules
    cf_list = list(ws.conditional_formatting)

    # Component 1: Conditional formatting rule exists covering D2:D41 (0.35 points)
    try:
        # Find any CF rule whose range includes D2:D41
        target_found = False
        matching_cf = None
        matching_rule = None

        for cf in cf_list:
            cf_range_str = str(cf).replace('<ConditionalFormatting ', '').replace('>', '').strip()
            # Check if the range covers D2:D41 - could be exact or a superset
            for rule in cf.rules:
                # We need to check if D2:D41 is covered
                # The range string from the CF object
                range_str = str(cf.sqref) if hasattr(cf, 'sqref') else str(cf)
                # Check if D2:D41 appears in the range
                if 'D2:D41' in range_str or 'D2:D41' in str(cf):
                    target_found = True
                    matching_cf = cf
                    matching_rule = rule
                    break
            if target_found:
                break

        if target_found:
            print(f"PASS: Component 1 - Conditional formatting rule found on D2:D41 (0.35 pts)")
            total_score += 0.35
        else:
            # Also try checking if any CF covers the range even without exact string match
            for cf in cf_list:
                for rule in cf.rules:
                    # Check individual cells in the range
                    cells_in_range = set()
                    for cell_range in cf.cells:
                        cells_in_range.add(str(cell_range))
                    # If we have CF rules at all, check the sqref
                    sqref_str = str(cf.sqref) if hasattr(cf, 'sqref') else ''
                    if 'D2' in sqref_str and 'D41' in sqref_str:
                        target_found = True
                        matching_cf = cf
                        matching_rule = rule
                        break
                if target_found:
                    break

            if target_found:
                print(f"PASS: Component 1 - Conditional formatting rule found covering D2:D41 (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 - No conditional formatting rule found on D2:D41. Found {len(cf_list)} rules total.")
                for cf in cf_list:
                    print(f"  Existing rule range: {cf}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Rule type is dataBar (0.30 points)
    try:
        if matching_rule is not None:
            if matching_rule.type == 'dataBar':
                print(f"PASS: Component 2 - Rule type is 'dataBar' (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 - Expected rule type 'dataBar', found '{matching_rule.type}'")
        else:
            # Search all rules for any dataBar type
            databar_found = False
            for cf in cf_list:
                for rule in cf.rules:
                    if rule.type == 'dataBar':
                        databar_found = True
                        matching_rule = rule
                        break
                if databar_found:
                    break

            if databar_found:
                print(f"PASS: Component 2 - dataBar rule found (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 - No dataBar rule found among {len(cf_list)} CF rules")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: DataBar showValue is True (numbers still visible) (0.20 points)
    try:
        if matching_rule is not None and matching_rule.type == 'dataBar' and matching_rule.dataBar:
            db = matching_rule.dataBar
            # showValue=True means numbers are visible alongside the bar
            # showValue could be True or None (None defaults to True in the spec)
            if db.showValue is True or db.showValue is None:
                print(f"PASS: Component 3 - DataBar showValue={db.showValue} (numbers visible) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 - DataBar showValue={db.showValue}, expected True")
        else:
            print(f"FAIL: Component 3 - No dataBar rule to check showValue")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: DataBar uses min/max cfvo for proportional scaling (0.15 points)
    try:
        if matching_rule is not None and matching_rule.type == 'dataBar' and matching_rule.dataBar:
            db = matching_rule.dataBar
            cfvo_list = db.cfvo if hasattr(db, 'cfvo') and db.cfvo else []
            if len(cfvo_list) >= 2:
                types_found = [fo.type for fo in cfvo_list]
                # Valid proportional scaling uses min/max, percent, percentile, or num
                # The standard default is min/max
                has_min_bound = any(t in ('min', 'percent', 'percentile', 'num') for t in types_found)
                has_max_bound = any(t in ('max', 'percent', 'percentile', 'num') for t in types_found)
                if has_min_bound and has_max_bound:
                    print(f"PASS: Component 4 - DataBar cfvo types: {types_found} (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 4 - DataBar cfvo types: {types_found}, expected min/max bounds")
            else:
                print(f"FAIL: Component 4 - DataBar has {len(cfvo_list)} cfvo objects, expected 2")
        else:
            print(f"FAIL: Component 4 - No dataBar rule to check cfvo")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
persist_app_state('libreoffice_calc')

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Gantt chart conditional formatting with blue fill
Task ID: calc_gg2_026
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): CF rule exists covering range C3:N20
  Component 2 (0.4): Rule uses correct AND formula with proper cell refs
  Component 3 (0.3): Rule applies solid blue fill
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'calc_gg2_026'


def persist_app_state(domain: str):
    """Best-effort save via Ctrl+S for LibreOffice."""
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
        import openpyxl
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Check sheet exists
    if 'Gantt' not in wb.sheetnames:
        print("FAIL: 'Gantt' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Gantt']

    # Gather all conditional formatting rules
    cf_rules_list = list(ws.conditional_formatting)

    # Component 1: A conditional formatting rule exists that covers range C3:N20 (0.3 points)
    try:
        target_found = False
        matching_cf = None
        matching_rule = None

        for cf in cf_rules_list:
            cf_range_str = str(cf).upper().replace(' ', '')
            # Check if C3:N20 is covered (exact match or containing)
            for rule in cf.rules:
                if rule.type == 'expression':
                    # Check if the range covers C3:N20
                    if 'C3:N20' in cf_range_str or 'C3:N20' == cf_range_str:
                        target_found = True
                        matching_cf = cf
                        matching_rule = rule
                        break
            if target_found:
                break

        if target_found:
            print(f"PASS: Component 1 — CF rule found on range C3:N20 (0.3 pts)")
            total_score += 0.3
        else:
            # Also check if any expression-type CF exists on any range that includes C3:N20
            for cf in cf_rules_list:
                for rule in cf.rules:
                    if rule.type == 'expression':
                        target_found = True
                        matching_cf = cf
                        matching_rule = rule
                        break
                if target_found:
                    break

            if target_found:
                print(f"PARTIAL: Component 1 — CF expression rule found but on range '{matching_cf}', expected C3:N20")
                # Give partial credit if a formula rule exists but on wrong range
                total_score += 0.1
            else:
                print(f"FAIL: Component 1 — No conditional formatting expression rules found. Total CF rules: {len(cf_rules_list)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Rule uses correct AND formula referencing week number and start/end (0.4 points)
    try:
        if matching_rule and matching_rule.formula:
            formula_str = str(matching_rule.formula[0]).upper().replace(' ', '')
            print(f"  DEBUG: Found formula: {matching_rule.formula[0]}")

            # The expected formula pattern: AND(C$2>=$A3,C$2<=$B3)
            # Normalize for comparison: remove spaces, uppercase
            # The key structure: AND(<col>$2>=..., <col>$2<=...)
            # with references to $A3 (start) and $B3 (end)

            has_and = 'AND(' in formula_str
            # Check for the mixed reference pattern: column-relative row-absolute $2 for week
            has_week_ref = bool(re.search(r'[C-N]\$2', formula_str))
            # Check for start week reference $A with relative row
            has_start_ref = bool(re.search(r'\$A\d+', formula_str) or re.search(r'\$A3', formula_str))
            # Check for end week reference $B with relative row
            has_end_ref = bool(re.search(r'\$B\d+', formula_str) or re.search(r'\$B3', formula_str))
            # Check comparison operators
            has_gte = '>=' in formula_str
            has_lte = '<=' in formula_str

            # Exact expected formula (normalized)
            expected_normalized = 'AND(C$2>=$A3,C$2<=$B3)'.upper().replace(' ', '')

            if formula_str == expected_normalized:
                print(f"PASS: Component 2 — Formula exactly matches AND(C$2>=$A3,C$2<=$B3) (0.4 pts)")
                total_score += 0.4
            elif has_and and has_week_ref and has_start_ref and has_end_ref and has_gte and has_lte:
                print(f"PASS: Component 2 — Formula has correct structure with AND, week ref, start/end refs, and comparisons (0.4 pts)")
                total_score += 0.4
            elif has_and and (has_gte or has_lte):
                print(f"PARTIAL: Component 2 — Formula has AND and comparison but missing proper refs: week={has_week_ref}, start={has_start_ref}, end={has_end_ref}")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — Formula structure incorrect. AND={has_and}, week_ref={has_week_ref}, start={has_start_ref}, end={has_end_ref}, gte={has_gte}, lte={has_lte}")
        else:
            print(f"FAIL: Component 2 — No matching expression rule found to check formula")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Rule applies solid blue fill (0.3 points)
    try:
        if matching_rule and hasattr(matching_rule, 'dxf') and matching_rule.dxf:
            dxf = matching_rule.dxf
            if dxf.fill:
                fill_type = dxf.fill.patternType
                fg_color = None
                try:
                    fg_color = dxf.fill.fgColor.rgb if dxf.fill.fgColor else None
                except:
                    pass

                print(f"  DEBUG: Fill type={fill_type}, fgColor={fg_color}")

                is_solid = fill_type == 'solid'
                # Check for blue-ish color: the expected is FF4472C4 but accept various blues
                is_blue = False
                if fg_color:
                    fg_upper = fg_color.upper()
                    # Check for common blue ARGB patterns
                    # FF4472C4 (the exact expected), FF0000FF, FF0070C0, FF0000FF, etc.
                    # Extract RGB components (skip alpha prefix)
                    if len(fg_upper) == 8:
                        r_hex = int(fg_upper[2:4], 16)
                        g_hex = int(fg_upper[4:6], 16)
                        b_hex = int(fg_upper[6:8], 16)
                        # Blue dominant: B component significantly higher than R, or recognized blue
                        is_blue = (b_hex > r_hex and b_hex >= 100) or fg_upper == 'FF4472C4'
                    elif len(fg_upper) == 6:
                        r_hex = int(fg_upper[0:2], 16)
                        g_hex = int(fg_upper[2:4], 16)
                        b_hex = int(fg_upper[4:6], 16)
                        is_blue = (b_hex > r_hex and b_hex >= 100)

                if is_solid and is_blue:
                    print(f"PASS: Component 3 — Solid blue fill applied (color={fg_color}) (0.3 pts)")
                    total_score += 0.3
                elif is_solid and fg_color:
                    print(f"PARTIAL: Component 3 — Solid fill applied but color '{fg_color}' is not blue")
                    total_score += 0.1
                elif is_blue:
                    print(f"PARTIAL: Component 3 — Blue color found but fill type is '{fill_type}', not solid")
                    total_score += 0.1
                else:
                    print(f"FAIL: Component 3 — Fill type={fill_type}, color={fg_color}, expected solid blue")
            else:
                print(f"FAIL: Component 3 — No fill in differential style")
        else:
            print(f"FAIL: Component 3 — No differential style found on the rule")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

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

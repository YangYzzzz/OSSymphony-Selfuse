"""
Reward Script: Conditional formatting for Critical+non-Resolved rows
Task ID: calc_gcv_051
Domain: libreoffice_calc
Scoring:
  - Component 1 (0.3): CF rule exists on correct range A2:F40
  - Component 2 (0.3): CF formula is AND($D2="Critical",$F2<>"Resolved")
  - Component 3 (0.2): CF fill color is red (#FF0000)
  - Component 4 (0.2): CF font color is white (#FFFFFF)
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_051'


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
    Verify that conditional formatting has been applied to highlight
    rows where Priority is 'Critical' AND Status is not 'Resolved'
    with red background (#FF0000) and white font (#FFFFFF).

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

    ws = wb.active

    # Find the relevant conditional formatting rule (expression type with our formula)
    target_rule = None
    target_range = None

    for cf in ws.conditional_formatting:
        for rule in cf.rules:
            if rule.type == 'expression' and rule.formula:
                # Check if formula references column D (Priority) and column F (Status)
                formula_str = rule.formula[0].upper().replace(" ", "")
                if 'CRITICAL' in formula_str and 'RESOLVED' in formula_str:
                    target_rule = rule
                    target_range = str(cf)
                    break
        if target_rule:
            break

    # Component 1: CF rule exists on correct range A2:F40 (0.3 points)
    try:
        if target_rule is not None and target_range is not None:
            # Normalize range string for comparison
            range_str = target_range.replace('<ConditionalFormatting ', '').replace('>', '').strip()
            # Check if range covers A2:F40
            if 'A2' in range_str and 'F40' in range_str:
                print(f"PASS: Component 1 — CF rule found on range {range_str} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — CF rule found but range is {range_str}, expected A2:F40")
        else:
            print("FAIL: Component 1 — No conditional formatting rule found with Critical/Resolved logic")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: CF formula is AND($D2="Critical",$F2<>"Resolved") (0.3 points)
    try:
        if target_rule is not None and target_rule.formula:
            formula = target_rule.formula[0]
            # Normalize for comparison: remove spaces, uppercase
            normalized = formula.upper().replace(" ", "")
            # Expected formula pattern: AND($D2="CRITICAL",$F2<>"RESOLVED")
            expected = 'AND($D2="CRITICAL",$F2<>"RESOLVED")'
            if normalized == expected:
                print(f"PASS: Component 2 — Formula matches exactly: {formula} (0.3 pts)")
                total_score += 0.3
            else:
                # Check for slight variations (e.g., different quoting or NOT()/!= patterns)
                has_d_critical = ('$D2="CRITICAL"' in normalized or '$D2="Critical"' in formula)
                has_f_not_resolved = ('<>"RESOLVED"' in normalized or '<>"Resolved"' in formula)
                has_and = normalized.startswith('AND(')
                if has_d_critical and has_f_not_resolved and has_and:
                    print(f"PASS: Component 2 — Formula has correct logic: {formula} (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 — Formula is '{formula}', expected AND($D2=\"Critical\",$F2<>\"Resolved\")")
        else:
            print("FAIL: Component 2 — No formula found in CF rule")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Fill color is red #FF0000 (0.2 points)
    try:
        if target_rule is not None and target_rule.dxf and target_rule.dxf.fill:
            fill = target_rule.dxf.fill
            fg_rgb = None
            if fill.fgColor and fill.fgColor.rgb:
                fg_rgb = str(fill.fgColor.rgb).upper()

            # Accept both FFFF0000 (8-char ARGB) and FF0000 (6-char RGB)
            if fg_rgb in ('FFFF0000', '00FF0000', 'FF0000'):
                print(f"PASS: Component 3 — Fill color is red: {fg_rgb} (0.2 pts)")
                total_score += 0.2
            else:
                # Also check bgColor as openpyxl sometimes uses it
                bg_rgb = None
                if fill.bgColor and fill.bgColor.rgb:
                    bg_rgb = str(fill.bgColor.rgb).upper()
                if bg_rgb in ('FFFF0000', '00FF0000', 'FF0000'):
                    print(f"PASS: Component 3 — Fill bgColor is red: {bg_rgb} (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 3 — Fill fgColor is {fg_rgb}, bgColor is {bg_rgb}, expected FFFF0000")
        else:
            print("FAIL: Component 3 — No fill defined in CF rule")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Font color is white #FFFFFF (0.2 points)
    try:
        if target_rule is not None and target_rule.dxf and target_rule.dxf.font:
            font = target_rule.dxf.font
            font_rgb = None
            if font.color and font.color.rgb:
                font_rgb = str(font.color.rgb).upper()

            # Accept FFFFFFFF, 00FFFFFF, FFFFFF
            if font_rgb and 'FFFFFF' in font_rgb:
                print(f"PASS: Component 4 — Font color is white: {font_rgb} (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 — Font color is {font_rgb}, expected FFFFFF")
        else:
            print("FAIL: Component 4 — No font defined in CF rule")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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

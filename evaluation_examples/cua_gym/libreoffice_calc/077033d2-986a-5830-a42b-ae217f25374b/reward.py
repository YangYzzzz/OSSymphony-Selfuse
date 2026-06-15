"""
Reward Script: Apply conditional formatting to highlight deals over $100,000 in bold red font
Task ID: calc_sales_015
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): CF rule exists on B2:B8 with cellIs > 100000
  Component 2 (0.3): CF rule differential style has bold=True
  Component 3 (0.3): CF rule differential style has red font color
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_sales_015'


def persist_app_state(domain: str):
    """Try to save any unsaved state in LibreOffice."""
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
    Verify conditional formatting was applied to highlight deals over $100,000
    in bold red font on the BigDeals sheet.
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

    # Precondition: BigDeals sheet must exist
    if 'BigDeals' not in wb.sheetnames:
        print("FAIL: 'BigDeals' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['BigDeals']

    # Find the matching conditional formatting rule
    matching_rule = None
    matching_range = None

    for cf in ws.conditional_formatting:
        cf_range = str(cf)
        for rule in cf.rules:
            # Check if this is a cellIs rule with greaterThan operator and formula 100000
            if rule.type == 'cellIs' and rule.operator == 'greaterThan':
                formulas = rule.formula if rule.formula else []
                for f in formulas:
                    # Accept variations: '100000', '100000.0', etc.
                    try:
                        val = float(str(f).strip())
                        if abs(val - 100000) < 0.01:
                            matching_rule = rule
                            matching_range = cf_range
                            break
                    except (ValueError, TypeError):
                        continue
                if matching_rule:
                    break
        if matching_rule:
            break

    # Component 1: CF rule exists on B2:B8 with cellIs > 100000 (0.4 points)
    try:
        if matching_rule is not None:
            # Check the range covers B2:B8 (may be expressed differently)
            range_str = matching_range.upper().replace(' ', '')
            # Accept if B2:B8 is in the range string
            if 'B2' in range_str and 'B8' in range_str:
                print(f"PASS: Component 1 — CF rule found: cellIs > 100000 on range {matching_range} (0.4 pts)")
                total_score += 0.4
            else:
                # Also accept if the range includes all of B2:B8 even if written differently
                print(f"PARTIAL: Component 1 — CF rule found but range is {matching_range}, expected B2:B8")
                # Give partial credit if at least a CF rule with correct logic exists
                total_score += 0.2
        else:
            print("FAIL: Component 1 — No conditional formatting rule with cellIs > 100000 found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Rule has bold font in differential style (0.3 points)
    try:
        if matching_rule is not None and matching_rule.dxf and matching_rule.dxf.font:
            if matching_rule.dxf.font.bold is True:
                print(f"PASS: Component 2 — CF rule has bold=True in differential style (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — CF rule font bold={matching_rule.dxf.font.bold}, expected True")
        else:
            print("FAIL: Component 2 — No differential font style found on CF rule")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Rule has red font color in differential style (0.3 points)
    try:
        if matching_rule is not None and matching_rule.dxf and matching_rule.dxf.font and matching_rule.dxf.font.color:
            color = matching_rule.dxf.font.color
            color_rgb = None
            if color.rgb is not None:
                color_rgb = str(color.rgb).upper()

            # Accept common red representations:
            # 00FF0000, FFFF0000, FF0000 (6-char)
            red_variants = ['00FF0000', 'FFFF0000', 'FF0000']
            if color_rgb and any(color_rgb.endswith(rv) or color_rgb == rv for rv in red_variants):
                print(f"PASS: Component 3 — CF rule has red font color (rgb={color_rgb}) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — CF rule font color rgb={color_rgb}, expected red (FF0000)")
        else:
            print("FAIL: Component 3 — No font color found on CF rule")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification
persist_app_state("libreoffice_calc")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

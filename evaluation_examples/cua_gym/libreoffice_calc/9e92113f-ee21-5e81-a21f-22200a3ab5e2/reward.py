"""
Reward Script: Conditional formatting with strikethrough and gray fill for 'Done' rows
Task ID: calc_gg2_043
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): CF rule exists on range A2:D51
  Component 2 (0.3): Formula is =$D2="Done"
  Component 3 (0.2): Strikethrough font in differential style
  Component 4 (0.2): Light gray fill in differential style
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gg2_043'


def persist_app_state(domain):
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
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: 'Checklist' sheet must exist
    if 'Checklist' not in wb.sheetnames:
        print("CRITICAL: 'Checklist' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Checklist']

    # Find the relevant CF rule (one that covers A2:D51 with a formula involving "Done")
    target_rule = None
    target_range_str = None
    for cf in ws.conditional_formatting:
        range_str = str(cf)
        for rule in cf.rules:
            if rule.type == 'expression' and rule.formula:
                formula_str = str(rule.formula[0]).upper().replace(' ', '')
                if 'DONE' in formula_str or 'Done' in str(rule.formula[0]):
                    target_rule = rule
                    target_range_str = range_str
                    break
        if target_rule:
            break

    # Component 1: CF rule exists on range covering A2:D51 (0.3 points)
    try:
        if target_rule is not None and target_range_str is not None:
            # Check that the range covers A2:D51
            range_upper = target_range_str.upper().replace(' ', '')
            # Accept various representations: "A2:D51", might have sheet prefix
            if 'A2:D51' in range_upper:
                print(f"PASS: Component 1 -- CF rule found on range {target_range_str} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 -- CF rule range is '{target_range_str}', expected A2:D51")
        else:
            print("FAIL: Component 1 -- No conditional formatting rule with 'Done' formula found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Formula is =$D2="Done" (0.3 points)
    try:
        if target_rule is not None:
            formula_raw = str(target_rule.formula[0])
            # Normalize: remove spaces, uppercase for comparison
            formula_norm = formula_raw.replace(' ', '').upper()
            # Accept: $D2="DONE" or $D2="Done" (the actual string comparison)
            # The formula stored may be: $D2="Done"
            expected_variants = ['$D2="DONE"', "$D2='DONE'"]
            if any(v in formula_norm for v in expected_variants):
                print(f"PASS: Component 2 -- Formula is '{formula_raw}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 -- Formula is '{formula_raw}', expected $D2=\"Done\"")
        else:
            print("FAIL: Component 2 -- No target rule found to check formula")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Strikethrough font in differential style (0.2 points)
    try:
        if target_rule is not None and target_rule.dxf:
            dxf = target_rule.dxf
            if dxf.font and dxf.font.strike:
                print(f"PASS: Component 3 -- Strikethrough enabled in CF style (0.2 pts)")
                total_score += 0.2
            else:
                strike_val = dxf.font.strike if dxf.font else None
                print(f"FAIL: Component 3 -- Strikethrough not enabled (font.strike={strike_val})")
        else:
            print("FAIL: Component 3 -- No differential style found on target rule")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Light gray fill in differential style (0.2 points)
    try:
        if target_rule is not None and target_rule.dxf:
            dxf = target_rule.dxf
            if dxf.fill and dxf.fill.patternType == 'solid':
                # Check fgColor for a light gray shade
                fg_rgb = None
                if dxf.fill.fgColor and dxf.fill.fgColor.rgb:
                    fg_rgb = str(dxf.fill.fgColor.rgb)

                # Light gray colors: D9D9D9, C0C0C0, BFBFBF, D3D3D3, etc.
                # Accept any grayish color (R~=G~=B, all above 0xA0)
                def check_light_gray(rgb_str):
                    """Check if an ARGB string represents a light gray color."""
                    if not rgb_str or len(rgb_str) < 6:
                        return False
                    hex_rgb = rgb_str[-6:]
                    try:
                        r = int(hex_rgb[0:2], 16)
                        g = int(hex_rgb[2:4], 16)
                        b = int(hex_rgb[4:6], 16)
                        spread = max(r, g, b) - min(r, g, b)
                        avg = (r + g + b) / 3
                        return spread <= 20 and avg >= 160
                    except ValueError:
                        return False

                if check_light_gray(fg_rgb):
                    print(f"PASS: Component 4 -- Light gray fill found (fgColor={fg_rgb}) (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 4 -- Fill fgColor is '{fg_rgb}', not a light gray")
            else:
                pt = dxf.fill.patternType if dxf.fill else None
                print(f"FAIL: Component 4 -- Fill pattern is '{pt}', expected 'solid' with gray color")
        else:
            print("FAIL: Component 4 -- No differential style found on target rule")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state("libreoffice_calc")
    verify_task(file_path)

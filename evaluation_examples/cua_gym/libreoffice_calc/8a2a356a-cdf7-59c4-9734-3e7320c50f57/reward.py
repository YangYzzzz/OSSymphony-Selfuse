"""
Reward Script: Data validation dropdown + conditional formatting on D2:D30
Task ID: calc_gcv_093
Domain: libreoffice_calc
Scoring:
  - Component 1 (0.30): Data validation list on D2:D30 with 'Passed,Failed,Pending,N/A'
  - Component 2 (0.175): CF rule for 'Passed' -> green bg (#00B050)
  - Component 3 (0.175): CF rule for 'Failed' -> red bg (#FF0000) + white font
  - Component 4 (0.175): CF rule for 'Pending' -> yellow bg (#FFFF00)
  - Component 5 (0.175): CF rule for 'N/A' -> gray bg (#D9D9D9) + italic font
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_093'


def persist_app_state(domain):
    """Save any unsaved LibreOffice edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
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

    ws = wb.active

    # ----------------------------------------------------------------
    # Component 1: Data validation on D2:D30 as list dropdown (0.30 pts)
    # The initial file has NO data validations; the task requires adding one.
    # ----------------------------------------------------------------
    try:
        matching_dv_count = 0
        if ws.data_validations and ws.data_validations.dataValidation:
            for dv in ws.data_validations.dataValidation:
                # Check type is "list"
                if dv.type != "list":
                    continue
                # Check formula contains the four required options
                formula = str(dv.formula1) if dv.formula1 else ""
                required_options = {"Passed", "Failed", "Pending", "N/A"}
                # formula looks like: "Passed,Failed,Pending,N/A" (with quotes)
                clean = formula.strip('"').strip("'")
                found_options = set(o.strip() for o in clean.split(","))
                if not required_options.issubset(found_options):
                    print(f"FAIL: Component 1 — validation options missing. Found: {found_options}, need: {required_options}")
                    continue
                # Check the range covers D2:D30
                sqref_str = str(dv.sqref)
                if "D2" in sqref_str and "D30" in sqref_str:
                    matching_dv_count += 1
                    break
                else:
                    print(f"FAIL: Component 1 — validation range mismatch. sqref={sqref_str}")

        if matching_dv_count > 0:
            print(f"PASS: Component 1 — Data validation list on D2:D30 with correct options (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — No matching data validation found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ----------------------------------------------------------------
    # Helper: parse conditional formatting rules into a lookup
    # ----------------------------------------------------------------
    cf_rules_by_value = {}  # maps value string -> (fill_fg_rgb, font_color_rgb, font_italic)
    try:
        for cf in ws.conditional_formatting:
            cf_range = str(cf)
            for rule in cf.rules:
                if rule.type == "cellIs" and rule.operator == "equal" and rule.formula:
                    val = rule.formula[0].strip('"').strip("'")
                    fill_rgb = None
                    font_rgb = None
                    font_italic = None
                    if rule.dxf:
                        if rule.dxf.fill and rule.dxf.fill.fgColor:
                            try:
                                fill_rgb = rule.dxf.fill.fgColor.rgb
                            except:
                                pass
                        if rule.dxf.font:
                            font_italic = rule.dxf.font.italic
                            if rule.dxf.font.color:
                                try:
                                    font_rgb = rule.dxf.font.color.rgb
                                except:
                                    pass
                    cf_rules_by_value[val] = {
                        "range": cf_range,
                        "fill_rgb": fill_rgb,
                        "font_rgb": font_rgb,
                        "font_italic": font_italic,
                    }
        print(f"INFO: Found CF rules for values: {list(cf_rules_by_value.keys())}")
    except Exception as e:
        print(f"ERROR: Parsing CF rules — {e}")

    # ----------------------------------------------------------------
    # Component 2: 'Passed' -> green bg #00B050 (0.175 pts)
    # ----------------------------------------------------------------
    try:
        if "Passed" in cf_rules_by_value:
            r = cf_rules_by_value["Passed"]
            fill = r["fill_rgb"]
            # Accept FF00B050 (8-char ARGB with full alpha)
            if fill and fill.upper().endswith("00B050"):
                print(f"PASS: Component 2 — 'Passed' has green bg fill={fill} (0.175 pts)")
                total_score += 0.175
            else:
                print(f"FAIL: Component 2 — 'Passed' fill={fill}, expected *00B050")
        else:
            print(f"FAIL: Component 2 — No CF rule for 'Passed'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ----------------------------------------------------------------
    # Component 3: 'Failed' -> red bg #FF0000 + white font (0.175 pts)
    # ----------------------------------------------------------------
    try:
        if "Failed" in cf_rules_by_value:
            r = cf_rules_by_value["Failed"]
            fill = r["fill_rgb"]
            font_c = r["font_rgb"]
            fill_ok = fill and fill.upper().endswith("FF0000")
            # White font: FFFFFF (with any alpha prefix)
            font_ok = font_c and font_c.upper().endswith("FFFFFF")
            if fill_ok and font_ok:
                print(f"PASS: Component 3 — 'Failed' has red bg + white font fill={fill}, font={font_c} (0.175 pts)")
                total_score += 0.175
            else:
                print(f"FAIL: Component 3 — 'Failed' fill={fill} (ok={fill_ok}), font={font_c} (ok={font_ok})")
        else:
            print(f"FAIL: Component 3 — No CF rule for 'Failed'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ----------------------------------------------------------------
    # Component 4: 'Pending' -> yellow bg #FFFF00 (0.175 pts)
    # ----------------------------------------------------------------
    try:
        if "Pending" in cf_rules_by_value:
            r = cf_rules_by_value["Pending"]
            fill = r["fill_rgb"]
            if fill and fill.upper().endswith("FFFF00"):
                print(f"PASS: Component 4 — 'Pending' has yellow bg fill={fill} (0.175 pts)")
                total_score += 0.175
            else:
                print(f"FAIL: Component 4 — 'Pending' fill={fill}, expected *FFFF00")
        else:
            print(f"FAIL: Component 4 — No CF rule for 'Pending'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ----------------------------------------------------------------
    # Component 5: 'N/A' -> gray bg #D9D9D9 + italic font (0.175 pts)
    # ----------------------------------------------------------------
    try:
        if "N/A" in cf_rules_by_value:
            r = cf_rules_by_value["N/A"]
            fill = r["fill_rgb"]
            italic = r["font_italic"]
            fill_ok = fill and fill.upper().endswith("D9D9D9")
            italic_ok = (italic is True)
            if fill_ok and italic_ok:
                print(f"PASS: Component 5 — 'N/A' has gray bg + italic font fill={fill}, italic={italic} (0.175 pts)")
                total_score += 0.175
            else:
                print(f"FAIL: Component 5 — 'N/A' fill={fill} (ok={fill_ok}), italic={italic} (ok={italic_ok})")
        else:
            print(f"FAIL: Component 5 — No CF rule for 'N/A'")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 4)
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

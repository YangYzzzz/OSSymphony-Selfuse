"""
Reward Script: 2-color scale conditional formatting on G2:G50
Task ID: calc_gcv_019
Domain: libreoffice_calc
Scoring:
  Component 1 (0.20): CF rule exists targeting G2:G50
  Component 2 (0.20): Rule is a colorScale with exactly 2 color stops
  Component 3 (0.20): Min CFVO is percentile type with value 10
  Component 4 (0.20): Max CFVO is percentile type with value 90
  Component 5 (0.20): Colors are white (#FFFFFF) for min and dark purple (#4A0082) for max
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_019'


def persist_app_state(domain):
    """Try to save any unsaved LibreOffice state via Ctrl+S."""
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

    # Find CF rule that covers G2:G50
    target_rule = None
    target_range = None

    # Component 1: CF rule exists on G2:G50 (0.20 points)
    try:
        cf_list = list(ws.conditional_formatting)
        for cf in cf_list:
            range_str = str(cf)
            # Check if G2:G50 is covered by this CF range
            if 'G2:G50' in range_str or 'G2:G50' == range_str:
                for rule in cf.rules:
                    if rule.type == 'colorScale':
                        target_rule = rule
                        target_range = range_str
                        break
            if target_rule:
                break

        if target_rule:
            print(f"PASS: Component 1 — colorScale CF rule found on range {target_range} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — No colorScale CF rule found covering G2:G50. Found {len(cf_list)} CF entries total.")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if not target_rule:
        # No point checking further components if no rule found
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    cs = target_rule.colorScale

    # Component 2: Exactly 2 color stops (2-color scale) (0.20 points)
    try:
        num_cfvo = len(cs.cfvo) if cs.cfvo else 0
        num_colors = len(cs.color) if cs.color else 0
        if num_cfvo == 2 and num_colors == 2:
            print(f"PASS: Component 2 — 2-color scale confirmed ({num_cfvo} stops, {num_colors} colors) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Expected 2 stops and 2 colors, found {num_cfvo} stops and {num_colors} colors")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Min CFVO is percentile type with value 10 (0.20 points)
    try:
        min_cfvo = cs.cfvo[0]
        min_type = min_cfvo.type
        min_val = min_cfvo.val
        if min_type == 'percentile' and float(min_val) == 10.0:
            print(f"PASS: Component 3 — Min CFVO type=percentile, val=10 (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Expected min CFVO type=percentile val=10, found type={min_type} val={min_val}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Max CFVO is percentile type with value 90 (0.20 points)
    try:
        max_cfvo = cs.cfvo[1]
        max_type = max_cfvo.type
        max_val = max_cfvo.val
        if max_type == 'percentile' and float(max_val) == 90.0:
            print(f"PASS: Component 4 — Max CFVO type=percentile, val=90 (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Expected max CFVO type=percentile val=90, found type={max_type} val={max_val}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Colors correct — min=white (#FFFFFF), max=dark purple (#4A0082) (0.20 points)
    try:
        min_color_rgb = cs.color[0].rgb
        max_color_rgb = cs.color[1].rgb
        # Normalize: compare last 6 chars (strip alpha prefix)
        min_hex = str(min_color_rgb)[-6:].upper()
        max_hex = str(max_color_rgb)[-6:].upper()

        min_ok = min_hex == 'FFFFFF'
        max_ok = max_hex == '4A0082'

        if min_ok and max_ok:
            print(f"PASS: Component 5 — Colors correct: min=#{min_hex} (white), max=#{max_hex} (dark purple) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 5 — Expected min=#FFFFFF max=#4A0082, found min=#{min_hex} max=#{max_hex}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
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

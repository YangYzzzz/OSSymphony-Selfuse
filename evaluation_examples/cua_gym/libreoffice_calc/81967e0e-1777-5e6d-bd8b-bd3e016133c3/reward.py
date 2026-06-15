"""
Reward Script: Rename 'Data Import' to 'Raw Data 2024', insert 'Archive 2023' after it, color its tab gray.
Task ID: calc_ggf_008
Domain: libreoffice_calc
Scoring:
  Component 1 (0.30): 'Data Import' renamed to 'Raw Data 2024'
  Component 2 (0.30): 'Archive 2023' sheet exists and positioned after 'Raw Data 2024'
  Component 3 (0.25): 'Archive 2023' tab color is gray
  Component 4 (0.15): Overall sheet order is correct
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_ggf_008'


def persist_app_state(domain):
    """Save any unsaved LibreOffice state before verification."""
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

    sheet_names = wb.sheetnames
    print(f"INFO: Sheet names found: {sheet_names}")

    # Component 1: 'Data Import' renamed to 'Raw Data 2024' (0.30 points)
    # This checks that 'Data Import' no longer exists AND 'Raw Data 2024' exists.
    # In initial_env, 'Data Import' exists and 'Raw Data 2024' does not -> FAIL
    # In golden_env, 'Data Import' is gone and 'Raw Data 2024' exists -> PASS
    try:
        has_raw_data_2024 = 'Raw Data 2024' in sheet_names
        no_data_import = 'Data Import' not in sheet_names
        if has_raw_data_2024 and no_data_import:
            print(f"PASS: Component 1 - 'Data Import' renamed to 'Raw Data 2024' (0.30 pts)")
            total_score += 0.30
        else:
            if not has_raw_data_2024:
                print(f"FAIL: Component 1 - 'Raw Data 2024' sheet not found")
            if not no_data_import:
                print(f"FAIL: Component 1 - 'Data Import' still exists (not renamed)")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: 'Archive 2023' sheet exists and is positioned after 'Raw Data 2024' (0.30 points)
    # In initial_env, 'Archive 2023' does not exist -> FAIL
    # In golden_env, 'Archive 2023' exists after 'Raw Data 2024' -> PASS
    try:
        has_archive = 'Archive 2023' in sheet_names
        if has_archive and has_raw_data_2024:
            idx_raw = sheet_names.index('Raw Data 2024')
            idx_archive = sheet_names.index('Archive 2023')
            if idx_archive == idx_raw + 1:
                print(f"PASS: Component 2 - 'Archive 2023' exists at index {idx_archive}, directly after 'Raw Data 2024' at index {idx_raw} (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 - 'Archive 2023' at index {idx_archive}, expected index {idx_raw + 1} (directly after 'Raw Data 2024')")
        elif has_archive:
            # Archive exists but Raw Data 2024 doesn't - partial situation
            print(f"FAIL: Component 2 - 'Archive 2023' exists but 'Raw Data 2024' not found for position check")
        else:
            print(f"FAIL: Component 2 - 'Archive 2023' sheet not found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: 'Archive 2023' tab color is gray (0.25 points)
    # In initial_env, 'Archive 2023' doesn't exist -> FAIL
    # In golden_env, 'Archive 2023' has gray tab color -> PASS
    try:
        if has_archive:
            ws_archive = wb['Archive 2023']
            tab_color = ws_archive.sheet_properties.tabColor
            if tab_color is not None:
                color_rgb = tab_color.rgb
                print(f"INFO: Archive 2023 tab color RGB: {color_rgb}")
                # Gray colors: accept various gray shades (808080, C0C0C0, A9A9A9, 999999, BEBEBE, etc.)
                # The color is stored as ARGB (8 chars) with alpha prefix
                # Strip alpha prefix to get 6-char RGB
                if color_rgb and len(color_rgb) >= 6:
                    rgb_part = color_rgb[-6:]  # last 6 chars are RGB
                    r = int(rgb_part[0:2], 16)
                    g = int(rgb_part[2:4], 16)
                    b = int(rgb_part[4:6], 16)
                    # Gray means R ~= G ~= B and not too bright (not white) and not too dark (not black)
                    is_neutral = (abs(r - g) <= 30 and abs(g - b) <= 30 and abs(r - b) <= 30)
                    is_gray_range = (50 <= r <= 210 and 50 <= g <= 210 and 50 <= b <= 210)
                    if is_neutral and is_gray_range:
                        print(f"PASS: Component 3 - 'Archive 2023' tab color is gray (R={r}, G={g}, B={b}) (0.25 pts)")
                        total_score += 0.25
                    else:
                        print(f"FAIL: Component 3 - Tab color R={r}, G={g}, B={b} is not gray (neutral={is_neutral}, range={is_gray_range})")
                else:
                    print(f"FAIL: Component 3 - Could not parse tab color RGB: {color_rgb}")
            else:
                print(f"FAIL: Component 3 - 'Archive 2023' has no tab color set")
        else:
            print(f"FAIL: Component 3 - 'Archive 2023' sheet not found, cannot check tab color")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Overall sheet order is correct (0.15 points)
    # Expected order: Summary, Raw Data 2024, Archive 2023, Charts
    # In initial_env, sheets are [Summary, Data Import, Charts] -> no match -> FAIL
    # In golden_env, sheets match expected order -> PASS
    try:
        expected_order = ['Summary', 'Raw Data 2024', 'Archive 2023', 'Charts']
        if sheet_names == expected_order:
            print(f"PASS: Component 4 - Sheet order matches expected {expected_order} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 - Sheet order {sheet_names} != expected {expected_order}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

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

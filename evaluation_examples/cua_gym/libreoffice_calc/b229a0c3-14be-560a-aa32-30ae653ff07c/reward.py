"""
Reward Script: Clone Formatting (format paintbrush) from A1 to A10, A20, A30, A40
Task ID: calc_gfl_086
Domain: libreoffice_calc
Scoring: 0.25 per target cell with matching formatting (bold, 14pt, dark blue font, gray fill, thick bottom border)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gfl_086'

TARGET_CELLS = ['A10', 'A20', 'A30', 'A40']
POINTS_PER_CELL = 0.25


def _check_font_color_dark_blue(cell):
    """Return whether the cell font color ends with 003366 (dark blue)."""
    try:
        if cell.font.color and cell.font.color.rgb:
            return str(cell.font.color.rgb).endswith('003366')
    except Exception:
        pass
    return False


def _check_fill_gray(cell):
    """Return whether the cell has solid fill ending with D9D9D9 (light gray)."""
    try:
        if cell.fill.patternType == 'solid':
            return str(cell.fill.fgColor.rgb).endswith('D9D9D9')
    except Exception:
        pass
    return False


def _check_border_thick(cell):
    """Return whether the cell has a thick bottom border."""
    try:
        return cell.border.bottom.style == 'thick'
    except Exception:
        return False


def check_cell_formatting(ws, cell_addr):
    """
    Check if a cell has the section header formatting matching A1:
    - Bold
    - Font size 14
    - Dark blue font color (003366)
    - Light gray background fill (D9D9D9), solid
    - Thick bottom border

    Returns (score_fraction, details) where score_fraction is 0.0-1.0
    for this cell's sub-checks.
    """
    cell = ws[cell_addr]
    passed = 0
    total_checks = 5
    details = []

    # Sub-check 1: Bold
    if cell.font.bold:
        passed += 1
        details.append("bold=OK")
    else:
        details.append(f"bold=FAIL(got {cell.font.bold})")

    # Sub-check 2: Font size 14
    if cell.font.size is not None and abs(cell.font.size - 14.0) < 0.5:
        passed += 1
        details.append("size=OK")
    else:
        details.append(f"size=FAIL(got {cell.font.size})")

    # Sub-check 3: Dark blue font color (003366)
    font_color_ok = _check_font_color_dark_blue(cell)
    if font_color_ok:
        passed += 1
        details.append("font_color=OK")
    else:
        try:
            fc = cell.font.color.rgb if cell.font.color else "None"
        except Exception:
            fc = "theme/error"
        details.append(f"font_color=FAIL(got {fc})")

    # Sub-check 4: Light gray background fill (D9D9D9), solid pattern
    fill_ok = _check_fill_gray(cell)
    if fill_ok:
        passed += 1
        details.append("fill=OK")
    else:
        try:
            ft = cell.fill.patternType
            fg = cell.fill.fgColor.rgb
        except Exception:
            ft, fg = "err", "err"
        details.append(f"fill=FAIL(type={ft}, fg={fg})")

    # Sub-check 5: Thick bottom border
    border_ok = _check_border_thick(cell)
    if border_ok:
        passed += 1
        details.append("border_bottom=OK")
    else:
        try:
            bs = cell.border.bottom.style
        except Exception:
            bs = "err"
        details.append(f"border_bottom=FAIL(got {bs})")

    fraction = passed / total_checks
    return fraction, details


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

    # Access the Template sheet
    try:
        ws = wb['Template']
    except KeyError:
        print("CRITICAL: Sheet 'Template' not found")
        print("REWARD: 0.0")
        return 0.0

    # Verify each target cell's formatting
    for cell_addr in TARGET_CELLS:
        try:
            fraction, details = check_cell_formatting(ws, cell_addr)
            cell_score = POINTS_PER_CELL * fraction
            if fraction >= 1.0:
                print(f"PASS: {cell_addr} — all formatting matches A1 ({POINTS_PER_CELL} pts) [{', '.join(details)}]")
                total_score += POINTS_PER_CELL
            elif fraction > 0:
                print(f"PARTIAL: {cell_addr} — {int(fraction*100)}% match ({cell_score:.3f} pts) [{', '.join(details)}]")
                total_score += cell_score
            else:
                print(f"FAIL: {cell_addr} — no formatting matches [{', '.join(details)}]")
        except Exception as e:
            print(f"ERROR: {cell_addr} — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice state before verification
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
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

"""
Reward Script: Set page to A4 landscape, 1.5cm margins, insert watermark image, set print order
Task ID: calc_gg3_048
Domain: libreoffice_calc

Scoring (only task-introduced changes):
  Component 1: Orientation set to landscape (0.25 points)
  Component 2: All 4 margins set to 1.5 cm (0.35 points)
  Component 3: Watermark image inserted on Print sheet (0.40 points)

Note: paperSize=9 (A4) and pageOrder=downThenOver are LibreOffice defaults that
exist after any Calc save. They are treated as precondition gates, not scored.
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gg3_048'


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
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: 'Print' sheet must exist
    if 'Print' not in wb.sheetnames:
        print("CRITICAL: 'Print' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Print']
    ps = ws.page_setup
    pm = ws.page_margins

    # Precondition gate: paper size should be A4 (9). This is a LibreOffice default
    # after save, so it is NOT scored, but if it's wrong the file is corrupt.
    paper_size = ps.paperSize
    if paper_size is not None and paper_size != 9:
        print(f"WARN: Paper size is {paper_size}, expected 9 (A4). File may be misconfigured.")

    # Precondition gate: page order should be downThenOver. Also a LibreOffice default.
    page_order = ps.pageOrder
    if page_order is not None and page_order != 'downThenOver':
        print(f"WARN: Page order is '{page_order}', expected 'downThenOver'.")

    # Component 1: Orientation is landscape (0.25 points)
    # Initial state has orientation=portrait (default). Task requires landscape.
    try:
        orientation = ps.orientation
        if orientation == 'landscape':
            print(f"PASS: Component 1 — Orientation is landscape (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected orientation='landscape', found: {orientation}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All margins set to 1.5 cm (0.5905511811 inches) (0.35 points)
    # Initial state has default margins (left/right=0.75, top/bottom=1.0 inches).
    # Tolerance: 0.02 inches (~0.5 mm)
    try:
        target_margin_inches = 1.5 / 2.54  # 0.5905511811...
        tolerance = 0.02
        margins = {
            'left': pm.left,
            'right': pm.right,
            'top': pm.top,
            'bottom': pm.bottom,
        }
        all_correct = True
        for name, val in margins.items():
            if val is None or abs(val - target_margin_inches) > tolerance:
                print(f"FAIL: Component 2 — Margin '{name}' expected ~{target_margin_inches:.4f} in, found: {val}")
                all_correct = False

        if all_correct:
            print(f"PASS: Component 2 — All 4 margins are ~1.5 cm ({target_margin_inches:.4f} in) (0.35 pts)")
            total_score += 0.35
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Watermark image inserted on 'Print' sheet (0.40 points)
    # Initial state has 0 images. Task requires inserting watermark.png.
    try:
        image_count = len(ws._images)
        if image_count >= 1:
            img = ws._images[0]
            print(f"PASS: Component 3 — Image found on 'Print' sheet (count={image_count}, size={img.width}x{img.height}) (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 3 — No images found on 'Print' sheet (expected watermark image)")
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

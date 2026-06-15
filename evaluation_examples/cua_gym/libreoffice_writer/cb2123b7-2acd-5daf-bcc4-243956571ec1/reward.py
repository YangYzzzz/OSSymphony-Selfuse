"""
Reward Script: Set margins to 1 inch on all sides, portrait orientation, A4 paper size
Task ID: writer_page_049
Domain: libreoffice_writer
Scoring:
  Component 1: Page size is A4 (21.0cm x 29.7cm)  — 0.4 points
  Component 2: Page orientation is PORTRAIT         — 0.3 points
  Component 3: All margins are 2.54cm (1 inch)      — 0.3 points
  Total: 1.0
"""

import os
from docx import Document
from docx.shared import Cm
from docx.enum.section import WD_ORIENT

WORKDIR = '/home/user'
TASK_ID = 'writer_page_049'
FILE_PATH = '/home/user/Desktop/standard_report.docx'

# Tolerance for dimension comparisons: 0.05 cm
TOLERANCE_CM = 0.05

# A4 dimensions in cm
A4_WIDTH_CM = 21.0
A4_HEIGHT_CM = 29.7

# Target margin in cm (1 inch = 2.54 cm)
TARGET_MARGIN_CM = 2.54


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Checks:
      1. Page size is A4 (width ~21.0cm, height ~29.7cm) - portrait orientation means
         width < height, so width ~21cm and height ~29.7cm
      2. Orientation is PORTRAIT
      3. All four margins are 2.54cm (1 inch)
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Use the first section (document may have only one)
    try:
        section = doc.sections[0]
    except Exception as e:
        print(f"CRITICAL: Cannot access sections: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Page size is A4 (0.4 points)
    # A4 portrait: width ~21.0cm, height ~29.7cm
    # We check the stored dimensions — for portrait, width should be the shorter side
    try:
        width_cm = section.page_width.cm
        height_cm = section.page_height.cm

        width_ok = abs(width_cm - A4_WIDTH_CM) <= TOLERANCE_CM
        height_ok = abs(height_cm - A4_HEIGHT_CM) <= TOLERANCE_CM

        if width_ok and height_ok:
            print(f"PASS: Component 1 — Page size is A4 ({width_cm:.4f}cm x {height_cm:.4f}cm) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Expected A4 (~{A4_WIDTH_CM}cm x ~{A4_HEIGHT_CM}cm), "
                  f"found ({width_cm:.4f}cm x {height_cm:.4f}cm)")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check page size: {e}")

    # Component 2: Orientation is PORTRAIT (0.3 points)
    try:
        orientation = section.orientation
        if orientation == WD_ORIENT.PORTRAIT:
            print(f"PASS: Component 2 — Orientation is PORTRAIT (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected PORTRAIT orientation, found: {orientation}")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check orientation: {e}")

    # Component 3: All margins are 2.54cm (1 inch) (0.3 points)
    # All four margins must be within tolerance of 2.54cm
    try:
        top_cm = section.top_margin.cm
        bottom_cm = section.bottom_margin.cm
        left_cm = section.left_margin.cm
        right_cm = section.right_margin.cm

        top_ok = abs(top_cm - TARGET_MARGIN_CM) <= TOLERANCE_CM
        bottom_ok = abs(bottom_cm - TARGET_MARGIN_CM) <= TOLERANCE_CM
        left_ok = abs(left_cm - TARGET_MARGIN_CM) <= TOLERANCE_CM
        right_ok = abs(right_cm - TARGET_MARGIN_CM) <= TOLERANCE_CM

        if top_ok and bottom_ok and left_ok and right_ok:
            print(f"PASS: Component 3 — All margins are 2.54cm: "
                  f"top={top_cm:.4f}, bottom={bottom_cm:.4f}, "
                  f"left={left_cm:.4f}, right={right_cm:.4f} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Expected all margins ~2.54cm, found: "
                  f"top={top_cm:.4f}, bottom={bottom_cm:.4f}, "
                  f"left={left_cm:.4f}, right={right_cm:.4f}")
    except Exception as e:
        print(f"ERROR: Component 3 — Could not check margins: {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

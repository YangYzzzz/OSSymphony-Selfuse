"""
Reward Script: Create a single shipping label (6x4 inches) centered on page
Task ID: writer_lec_054
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): Page width == 6 inches
  Component 2 (0.35): Page height == 4 inches
  Component 3 (0.30): Margins are symmetric and smaller than default (centering the label)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_054'

# Tolerance for dimension checks: 0.15 inches in EMU
TOLERANCE_EMU = int(0.15 * 914400)  # ~137160 EMU

# Target dimensions in EMU (1 inch = 914400 EMU)
TARGET_WIDTH_EMU = int(6 * 914400)    # 5486400
TARGET_HEIGHT_EMU = int(4 * 914400)   # 3657600

# Default page dimensions (letter: 8.5 x 11 inches)
DEFAULT_WIDTH_EMU = int(8.5 * 914400)   # 7772400
DEFAULT_HEIGHT_EMU = int(11 * 914400)   # 10058400
DEFAULT_MARGIN_EMU = int(1.0 * 914400)  # 914400


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: document must have at least one section
    if len(doc.sections) == 0:
        print("CRITICAL: No sections found in document")
        print("REWARD: 0.0")
        return 0.0

    section = doc.sections[0]

    # Component 1: Page width is 6 inches (0.35 points)
    # Task requires width of 6 inches (152.4 mm = 5486400 EMU)
    # Initial has 8.5 inches -- this check distinguishes golden from initial
    try:
        actual_width = section.page_width
        diff_width = abs(actual_width - TARGET_WIDTH_EMU)
        if diff_width <= TOLERANCE_EMU:
            print(f"PASS: Component 1 -- Page width is {actual_width/914400:.2f} inches "
                  f"(target: 6.00, diff: {diff_width/914400:.3f} inches) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 -- Page width is {actual_width/914400:.2f} inches, "
                  f"expected ~6.00 inches (diff: {diff_width/914400:.3f} inches)")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Page height is 4 inches (0.35 points)
    # Task requires height of 4 inches (101.6 mm = 3657600 EMU)
    # Initial has 11 inches -- this check distinguishes golden from initial
    try:
        actual_height = section.page_height
        diff_height = abs(actual_height - TARGET_HEIGHT_EMU)
        if diff_height <= TOLERANCE_EMU:
            print(f"PASS: Component 2 -- Page height is {actual_height/914400:.2f} inches "
                  f"(target: 4.00, diff: {diff_height/914400:.3f} inches) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 -- Page height is {actual_height/914400:.2f} inches, "
                  f"expected ~4.00 inches (diff: {diff_height/914400:.3f} inches)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Margins are symmetric and NOT default 1-inch (0.30 points)
    # The label should be "centered on the page" with reduced margins.
    # Initial has 1.0 inch margins on all sides. Golden should have smaller,
    # symmetric margins indicating the label is centered.
    # We check: (a) margins are non-default (changed from 1 inch), AND
    #           (b) left == right AND top == bottom (symmetric => centered)
    try:
        left_m = section.left_margin
        right_m = section.right_margin
        top_m = section.top_margin
        bottom_m = section.bottom_margin

        print(f"  Margins: L={left_m/914400:.2f}\" R={right_m/914400:.2f}\" "
              f"T={top_m/914400:.2f}\" B={bottom_m/914400:.2f}\"")

        # Check that margins are NOT the default 1-inch (with tolerance)
        margins_changed = (
            abs(left_m - DEFAULT_MARGIN_EMU) > TOLERANCE_EMU or
            abs(right_m - DEFAULT_MARGIN_EMU) > TOLERANCE_EMU or
            abs(top_m - DEFAULT_MARGIN_EMU) > TOLERANCE_EMU or
            abs(bottom_m - DEFAULT_MARGIN_EMU) > TOLERANCE_EMU
        )

        # Check symmetry: left ~= right AND top ~= bottom
        lr_symmetric = abs(left_m - right_m) <= TOLERANCE_EMU
        tb_symmetric = abs(top_m - bottom_m) <= TOLERANCE_EMU

        if margins_changed and lr_symmetric and tb_symmetric:
            print(f"PASS: Component 3 -- Margins are symmetric and non-default "
                  f"(centered label) (0.30 pts)")
            total_score += 0.30
        else:
            reasons = []
            if not margins_changed:
                reasons.append("margins still at default 1 inch")
            if not lr_symmetric:
                reasons.append(f"left/right not symmetric ({left_m/914400:.2f} vs {right_m/914400:.2f})")
            if not tb_symmetric:
                reasons.append(f"top/bottom not symmetric ({top_m/914400:.2f} vs {bottom_m/914400:.2f})")
            print(f"FAIL: Component 3 -- {'; '.join(reasons)}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

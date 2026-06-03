"""
Reward Script: Newsletter-style layout — three columns with separator, Letter landscape, 1.5cm margins
Task ID: writer_page_070
Domain: libreoffice_writer
Scoring:
  Component 1: Letter page size + landscape orientation (0.30 pts)
  Component 2: Three equal columns (0.30 pts)
  Component 3: Separator line between columns (0.20 pts)
  Component 4: Margins 1.5cm on all sides (0.20 pts)
  Total: 1.00 pts
"""

import os
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_page_070'

# Tolerance for margin comparison (EMU), ~0.05 cm = ~1800 EMU
MARGIN_TOLERANCE_EMU = 3600  # ~0.10 cm tolerance

# Letter page dimensions in EMU (27.94 cm x 21.59 cm in landscape → width > height)
LETTER_WIDTH_CM = 27.94   # landscape width
LETTER_HEIGHT_CM = 21.59  # landscape height
CM_TO_EMU = 914400 / 2.54

EXPECTED_WIDTH_EMU = int(LETTER_WIDTH_CM * CM_TO_EMU)   # 10058400
EXPECTED_HEIGHT_EMU = int(LETTER_HEIGHT_CM * CM_TO_EMU)  # 7772400
PAGE_SIZE_TOLERANCE_EMU = 18000  # ~0.05 cm tolerance

EXPECTED_MARGIN_CM = 1.5
EXPECTED_MARGIN_EMU = int(EXPECTED_MARGIN_CM * CM_TO_EMU)  # 540000


def verify_task(file_path):
    """
    Verify newsletter-style layout with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Use the first section for page layout properties
    try:
        s = doc.sections[0]
    except Exception as e:
        print(f"CRITICAL: Cannot access sections: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Letter page size + landscape orientation (0.30 points)
    # Initial: A4 portrait (~21.0 x 29.7 cm) → Golden: Letter landscape (27.94 x 21.59 cm)
    try:
        is_landscape = (s.orientation == WD_ORIENT.LANDSCAPE)
        width_ok = abs(s.page_width - EXPECTED_WIDTH_EMU) < PAGE_SIZE_TOLERANCE_EMU
        height_ok = abs(s.page_height - EXPECTED_HEIGHT_EMU) < PAGE_SIZE_TOLERANCE_EMU
        width_cm = s.page_width / CM_TO_EMU
        height_cm = s.page_height / CM_TO_EMU

        if is_landscape and width_ok and height_ok:
            print(f"PASS: Component 1 — Letter landscape page: {width_cm:.2f} x {height_cm:.2f} cm, orientation=LANDSCAPE (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Expected Letter landscape (27.94x21.59 cm), "
                  f"got {width_cm:.2f}x{height_cm:.2f} cm, orientation={s.orientation}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Three equal columns with 0.50 cm spacing (0.30 points)
    # Initial: single column → Golden: w:num=3, w:equalWidth=1, w:space=180000 EMU (0.5 cm)
    try:
        sectPr = s._sectPr
        cols = sectPr.find(qn('w:cols'))
        if cols is not None:
            num_cols = cols.get(qn('w:num'))
            equal_width = cols.get(qn('w:equalWidth'))
            col_space = cols.get(qn('w:space'))

            # num=3, equalWidth should be "1" (true)
            num_is_3 = (num_cols == '3')
            is_equal = (equal_width == '1')

            # col spacing: 0.50 cm = 180000 EMU
            EXPECTED_COL_SPACE_EMU = 180000
            space_ok = False
            if col_space is not None:
                try:
                    space_val = int(col_space)
                    space_ok = abs(space_val - EXPECTED_COL_SPACE_EMU) < 18000  # ~0.05 cm tolerance
                except ValueError:
                    pass

            if num_is_3 and is_equal:
                if space_ok:
                    print(f"PASS: Component 2 — 3 equal columns with spacing={col_space} EMU (~0.50 cm) (0.30 pts)")
                    total_score += 0.30
                else:
                    # Still pass column count/equal check even if spacing differs
                    print(f"PASS: Component 2 — 3 equal columns found (spacing={col_space} EMU, expected ~180000) (0.30 pts)")
                    total_score += 0.30
            else:
                print(f"FAIL: Component 2 — Expected 3 equal columns, "
                      f"got num={num_cols}, equalWidth={equal_width}")
        else:
            print(f"FAIL: Component 2 — No <w:cols> element found (single column)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Separator line between columns (0.20 points)
    # Initial: no sep → Golden: w:sep=1
    try:
        sectPr = s._sectPr
        cols = sectPr.find(qn('w:cols'))
        if cols is not None:
            sep_val = cols.get(qn('w:sep'))
            # sep="1" means separator line is enabled
            has_sep = (sep_val == '1')
            if has_sep:
                print(f"PASS: Component 3 — Separator line between columns enabled (w:sep=1) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — Separator line not enabled, w:sep={sep_val}")
        else:
            print(f"FAIL: Component 3 — No <w:cols> element, separator cannot be set")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Margins 1.5cm on all four sides (0.20 points)
    # Initial: all margins 2.54 cm → Golden: all margins 1.5 cm
    try:
        margins = {
            'top': s.top_margin,
            'bottom': s.bottom_margin,
            'left': s.left_margin,
            'right': s.right_margin,
        }
        all_correct = all(
            abs(v - EXPECTED_MARGIN_EMU) < MARGIN_TOLERANCE_EMU
            for v in margins.values()
        )
        margin_details = {k: f"{v / CM_TO_EMU:.3f}cm" for k, v in margins.items()}
        if all_correct:
            print(f"PASS: Component 4 — All margins ~1.5 cm: {margin_details} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Expected all margins=1.5 cm, got {margin_details}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Default: test against canonical artifact path
file_path = '/home/user/Desktop/school_newsletter.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

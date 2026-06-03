"""
Reward Script: Configure three columns in a LibreOffice Writer document
Task ID: writer_page_047
Domain: libreoffice_writer
Scoring:
  - Component 1: Document has exactly 3 columns (0.3 pts)
  - Component 2: Left and right column widths are ~5cm (2835 twips ±50) (0.3 pts)
  - Component 3: Middle column width is ~8cm (~4535 twips ±50) (0.2 pts)
  - Component 4: Column spacing between each pair is ~0.5cm (283 twips ±30) (0.2 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_page_047'
FILE_PATH = '/home/user/Desktop/magazine_layout.docx'

# Conversion constants
# 1 cm = 567 twips (20 twips per point, 72 points per inch, 2.54 cm per inch => 1440/2.54 ≈ 566.93)
TWIPS_PER_CM = 566.93
TOLERANCE_WIDTH = 60   # twips tolerance for width checks (~0.1 cm)
TOLERANCE_SPACE = 40   # twips tolerance for spacing checks (~0.07 cm)

TARGET_NARROW_CM = 5.0   # left and right columns: 5cm
TARGET_WIDE_CM   = 8.0   # middle column: 8cm
TARGET_SPACE_CM  = 0.5   # spacing between columns: 0.5cm

TARGET_NARROW_TWIPS = round(TARGET_NARROW_CM * TWIPS_PER_CM)  # ~2835
TARGET_WIDE_TWIPS   = round(TARGET_WIDE_CM   * TWIPS_PER_CM)  # ~4535
TARGET_SPACE_TWIPS  = round(TARGET_SPACE_CM  * TWIPS_PER_CM)  # ~283


def cm_from_twips(twips):
    return twips / TWIPS_PER_CM


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document
    try:
        from docx import Document
        from docx.oxml.ns import qn
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: at least 1 section exists
    if len(doc.sections) == 0:
        print("CRITICAL: No sections found in document")
        print("REWARD: 0.0")
        return 0.0

    # Retrieve the w:cols element from the first section's sectPr
    try:
        section = doc.sections[0]
        sect_pr = section._sectPr
        cols_elem = sect_pr.find(qn('w:cols'))
    except Exception as e:
        print(f"CRITICAL: Cannot read section XML: {e}")
        print("REWARD: 0.0")
        return 0.0

    if cols_elem is None:
        print("FAIL: No w:cols element found — document has default single-column layout")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 1: Document has exactly 3 columns (0.3 points)
    # The task requires 3 columns; initial state has 1 column (w:num="1")
    try:
        WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        num_attr = cols_elem.get(f'{{{WNS}}}num')
        col_children = cols_elem.findall(f'{{{WNS}}}col')

        # num attribute should be "3", OR there should be exactly 3 w:col children
        num_from_attr = int(num_attr) if num_attr is not None else len(col_children)
        num_from_children = len(col_children)

        # Primary check: num attribute
        if num_from_attr == 3:
            print(f"PASS: Component 1 — 3 columns (w:num=3) (0.3 pts)")
            total_score += 0.3
        elif num_from_children == 3:
            # Fallback: count w:col elements
            print(f"PASS: Component 1 — 3 w:col children found (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — expected 3 columns, found num={num_from_attr}, col_children={num_from_children}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Left and right column widths are ~5cm / 2835 twips (0.3 points)
    # Requires that exactly 3 w:col elements exist and first + last have width ~2835 twips
    try:
        WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        col_children = cols_elem.findall(f'{{{WNS}}}col')

        if len(col_children) < 3:
            print(f"FAIL: Component 2 — need 3 col elements to check widths, found {len(col_children)}")
        else:
            left_w_str  = col_children[0].get(f'{{{WNS}}}w')
            right_w_str = col_children[2].get(f'{{{WNS}}}w')
            left_w  = int(left_w_str)  if left_w_str  else 0
            right_w = int(right_w_str) if right_w_str else 0

            left_ok  = abs(left_w  - TARGET_NARROW_TWIPS) <= TOLERANCE_WIDTH
            right_ok = abs(right_w - TARGET_NARROW_TWIPS) <= TOLERANCE_WIDTH

            if left_ok and right_ok:
                print(f"PASS: Component 2 — left={cm_from_twips(left_w):.2f}cm ({left_w} twips), "
                      f"right={cm_from_twips(right_w):.2f}cm ({right_w} twips); target {TARGET_NARROW_CM}cm (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — left={cm_from_twips(left_w):.2f}cm ({left_w} twips), "
                      f"right={cm_from_twips(right_w):.2f}cm ({right_w} twips); "
                      f"expected {TARGET_NARROW_CM}cm ({TARGET_NARROW_TWIPS} twips) ±{TOLERANCE_WIDTH}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Middle column width is ~8cm / 4535 twips (0.2 points)
    try:
        WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        col_children = cols_elem.findall(f'{{{WNS}}}col')

        if len(col_children) < 3:
            print(f"FAIL: Component 3 — need 3 col elements to check middle width, found {len(col_children)}")
        else:
            mid_w_str = col_children[1].get(f'{{{WNS}}}w')
            mid_w = int(mid_w_str) if mid_w_str else 0

            mid_ok = abs(mid_w - TARGET_WIDE_TWIPS) <= TOLERANCE_WIDTH

            if mid_ok:
                print(f"PASS: Component 3 — middle={cm_from_twips(mid_w):.2f}cm ({mid_w} twips); "
                      f"target {TARGET_WIDE_CM}cm (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — middle={cm_from_twips(mid_w):.2f}cm ({mid_w} twips); "
                      f"expected {TARGET_WIDE_CM}cm ({TARGET_WIDE_TWIPS} twips) ±{TOLERANCE_WIDTH}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Spacing between columns is ~0.5cm / 283 twips (0.2 points)
    # Check w:space on the first two col elements (last col has no space after it)
    try:
        WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        col_children = cols_elem.findall(f'{{{WNS}}}col')

        if len(col_children) < 2:
            print(f"FAIL: Component 4 — need at least 2 col elements to check spacing, found {len(col_children)}")
        else:
            space1_str = col_children[0].get(f'{{{WNS}}}space')
            space2_str = col_children[1].get(f'{{{WNS}}}space')
            space1 = int(space1_str) if space1_str else 0
            space2 = int(space2_str) if space2_str else 0

            # Both spacings (after col1 and after col2) should be ~283 twips
            space1_ok = abs(space1 - TARGET_SPACE_TWIPS) <= TOLERANCE_SPACE
            space2_ok = abs(space2 - TARGET_SPACE_TWIPS) <= TOLERANCE_SPACE

            if space1_ok and space2_ok:
                print(f"PASS: Component 4 — spacing1={cm_from_twips(space1):.3f}cm ({space1} twips), "
                      f"spacing2={cm_from_twips(space2):.3f}cm ({space2} twips); target {TARGET_SPACE_CM}cm (0.2 pts)")
                total_score += 0.2
            elif space1_ok or space2_ok:
                # Partial: only one spacing is correct
                print(f"PARTIAL: Component 4 — spacing1={cm_from_twips(space1):.3f}cm ({space1} twips), "
                      f"spacing2={cm_from_twips(space2):.3f}cm ({space2} twips); "
                      f"only one matches target {TARGET_SPACE_CM}cm")
                # Do not award partial credit for this component
            else:
                print(f"FAIL: Component 4 — spacing1={cm_from_twips(space1):.3f}cm ({space1} twips), "
                      f"spacing2={cm_from_twips(space2):.3f}cm ({space2} twips); "
                      f"expected {TARGET_SPACE_CM}cm ({TARGET_SPACE_TWIPS} twips) ±{TOLERANCE_SPACE}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

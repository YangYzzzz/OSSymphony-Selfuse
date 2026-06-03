"""
Reward Script: Two-column layout verification
Task ID: writer_fs_003
Domain: libreoffice_writer
Scoring:
  - Component 1: Number of columns == 2 (0.25 pts)
  - Component 2: AutoWidth disabled (equalWidth=0) (0.15 pts)
  - Component 3: Left column width ~10 cm (0.25 pts)
  - Component 4: Right column width ~5 cm (0.20 pts)
  - Component 5: Column spacing ~0.8 cm (0.15 pts)
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_003'

# Conversion: 1 cm = 567 twips (1 twip = 1/20 pt, 1 cm = 28.3465 pt, 567 = 28.3465 * 20)
CM_TO_TWIPS = 567.0
TOLERANCE_TWIPS = 30  # ~0.05 cm tolerance


def verify_task(file_path):
    """
    Verify two-column layout with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get section properties
    try:
        section = doc.sections[0]
        sectPr = section._sectPr
        cols = sectPr.find(qn('w:cols'))
    except Exception as e:
        print(f"CRITICAL: Cannot access section properties: {e}")
        print("REWARD: 0.0")
        return 0.0

    if cols is None:
        print("FAIL: No w:cols element found in section properties")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Number of columns == 2 (0.25 points)
    try:
        num_attr = cols.get(qn('w:num'))
        col_elements = cols.findall(qn('w:col'))
        num_cols = int(num_attr) if num_attr else len(col_elements)
        if num_cols == 2:
            print(f"PASS: Component 1 - Number of columns is 2 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 - Expected 2 columns, found {num_cols}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: AutoWidth disabled (equalWidth=0) (0.15 points)
    try:
        eq_width = cols.get(qn('w:equalWidth'))
        # equalWidth=0 or "false" means auto-width is OFF (unequal columns allowed)
        if eq_width is not None and str(eq_width) in ('0', 'false'):
            print(f"PASS: Component 2 - AutoWidth disabled (equalWidth={eq_width}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 - Expected equalWidth=0, found equalWidth={eq_width}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Get individual column elements for width/spacing checks
    col_elements = cols.findall(qn('w:col'))
    if len(col_elements) < 2:
        print(f"FAIL: Expected 2 w:col elements, found {len(col_elements)}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {min(total_score, 1.0)}")
        return min(total_score, 1.0)

    # Component 3: Left column width ~10 cm (5670 twips) (0.25 points)
    try:
        col0_w = col_elements[0].get(qn('w:w'))
        if col0_w is not None:
            col0_twips = int(col0_w)
            expected_twips = round(10.0 * CM_TO_TWIPS)  # 5670
            diff = abs(col0_twips - expected_twips)
            if diff <= TOLERANCE_TWIPS:
                print(f"PASS: Component 3 - Left column width = {col0_twips} twips (~{col0_twips/CM_TO_TWIPS:.2f} cm) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 - Left column width = {col0_twips} twips (~{col0_twips/CM_TO_TWIPS:.2f} cm), expected ~5670 twips (10 cm), diff={diff}")
        else:
            print("FAIL: Component 3 - No width attribute on first column")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Right column width ~5 cm (2835 twips) (0.20 points)
    try:
        col1_w = col_elements[1].get(qn('w:w'))
        if col1_w is not None:
            col1_twips = int(col1_w)
            expected_twips = round(5.0 * CM_TO_TWIPS)  # 2835
            diff = abs(col1_twips - expected_twips)
            if diff <= TOLERANCE_TWIPS:
                print(f"PASS: Component 4 - Right column width = {col1_twips} twips (~{col1_twips/CM_TO_TWIPS:.2f} cm) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 - Right column width = {col1_twips} twips (~{col1_twips/CM_TO_TWIPS:.2f} cm), expected ~2835 twips (5 cm), diff={diff}")
        else:
            print("FAIL: Component 4 - No width attribute on second column")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Column spacing ~0.8 cm (453.6 twips) (0.15 points)
    try:
        col0_space = col_elements[0].get(qn('w:space'))
        if col0_space is not None:
            space_twips = int(col0_space)
            expected_space = round(0.8 * CM_TO_TWIPS)  # ~454
            diff = abs(space_twips - expected_space)
            if diff <= TOLERANCE_TWIPS:
                print(f"PASS: Component 5 - Column spacing = {space_twips} twips (~{space_twips/CM_TO_TWIPS:.2f} cm) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 - Column spacing = {space_twips} twips (~{space_twips/CM_TO_TWIPS:.2f} cm), expected ~454 twips (0.8 cm), diff={diff}")
        else:
            # Also check the cols-level space attribute
            cols_space = cols.get(qn('w:space'))
            if cols_space is not None:
                space_twips = int(cols_space)
                expected_space = round(0.8 * CM_TO_TWIPS)
                diff = abs(space_twips - expected_space)
                if diff <= TOLERANCE_TWIPS:
                    print(f"PASS: Component 5 - Column spacing (from cols) = {space_twips} twips (~{space_twips/CM_TO_TWIPS:.2f} cm) (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 5 - Column spacing (from cols) = {space_twips} twips (~{space_twips/CM_TO_TWIPS:.2f} cm), expected ~454 twips (0.8 cm)")
            else:
                print("FAIL: Component 5 - No space attribute found on column or cols element")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = min(total_score, 1.0)
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

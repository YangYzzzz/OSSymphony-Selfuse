"""
Reward Script: Convert single-column page layout to two-column layout with 2:1 ratio and 0.6 cm spacing
Task ID: writer_fs_040
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): Two columns configured (num=2)
  Component 2 (0.2): AutoWidth unchecked (equalWidth=0)
  Component 3 (0.2): Column spacing is 0.6 cm (216000 EMU)
  Component 4 (0.3): Column width ratio is approximately 2:1
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_040'

# Conversion constant: 1 cm = 360000 EMU
CM_TO_EMU = 360000


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    section = doc.sections[0]
    sectPr = section._sectPr
    cols = sectPr.find(qn('w:cols'))

    if cols is None:
        print("FAIL: No w:cols element found in section properties")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Two columns configured (0.3 points)
    # The w:cols element must have num="2" attribute
    try:
        num_cols = cols.get(qn('w:num'))
        if num_cols is not None and int(num_cols) == 2:
            print(f"PASS: Component 1 - Two columns configured (num={num_cols}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 - Expected num=2, found num={num_cols}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: AutoWidth unchecked / equalWidth=0 (0.2 points)
    # The w:cols element must have equalWidth="0"
    try:
        equal_width = cols.get(qn('w:equalWidth'))
        if equal_width is not None and equal_width == '0':
            print(f"PASS: Component 2 - AutoWidth unchecked (equalWidth={equal_width}) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 - Expected equalWidth=0, found equalWidth={equal_width}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Column spacing is 0.6 cm = 216000 EMU (0.2 points)
    # Check the space attribute on the first w:col element
    try:
        col_elements = cols.findall(qn('w:col'))
        if len(col_elements) >= 1:
            space_emu = int(col_elements[0].get(qn('w:space'), '0'))
            space_cm = space_emu / CM_TO_EMU
            # Allow 5% tolerance for spacing
            if abs(space_cm - 0.6) < 0.05:
                print(f"PASS: Component 3 - Column spacing is {space_cm:.3f} cm ({space_emu} EMU) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 - Expected spacing ~0.6 cm, found {space_cm:.3f} cm ({space_emu} EMU)")
        else:
            print("FAIL: Component 3 - No w:col elements found to check spacing")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Column width ratio is approximately 2:1 (0.3 points)
    # Left column should be ~11.07 cm, right column ~5.33 cm
    try:
        col_elements = cols.findall(qn('w:col'))
        if len(col_elements) >= 2:
            left_w = int(col_elements[0].get(qn('w:w'), '0'))
            right_w = int(col_elements[1].get(qn('w:w'), '0'))
            left_cm = left_w / CM_TO_EMU
            right_cm = right_w / CM_TO_EMU

            if right_w > 0:
                ratio = left_w / right_w
                # Allow tolerance: ratio should be ~2.0 (accept 1.8 to 2.2)
                if 1.8 <= ratio <= 2.2:
                    print(f"PASS: Component 4 - Column ratio is {ratio:.3f} (left={left_cm:.2f} cm, right={right_cm:.2f} cm) (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 4 - Expected ratio ~2.0, found {ratio:.3f} (left={left_cm:.2f} cm, right={right_cm:.2f} cm)")
            else:
                print("FAIL: Component 4 - Right column width is 0")
        else:
            print(f"FAIL: Component 4 - Expected 2 col elements, found {len(col_elements)}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

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

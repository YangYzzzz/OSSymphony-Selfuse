"""
Reward Script: Set up a three-column layout with separator lines between columns.
Task ID: writer_page_017
Domain: libreoffice_writer
Scoring:
  - Component 1: Number of columns == 3             (0.40 pts)
  - Component 2: Separator line enabled (sep=1)      (0.30 pts)
  - Component 3: Equal widths + spacing ~0.40cm      (0.30 pts)
  Total: 1.0
"""

import os
from docx import Document

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_page_017'
FILE_PATH = f'{WORKDIR}/church_bulletin.docx'

# Namespace constant for OOXML
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def verify_task(file_path):
    """
    Verify that the document has a 3-column layout with separator lines.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document — if it fails, nothing can be verified
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get the first section's sectPr (section properties XML element)
    try:
        section = doc.sections[0]
        sectPr = section._sectPr
        cols_elem = sectPr.find(f'{{{W}}}cols')
    except Exception as e:
        print(f"CRITICAL: Cannot read section properties: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Number of columns == 3 (0.40 points)
    # Initial state has num=1; golden state must have num=3
    try:
        if cols_elem is not None:
            num_str = cols_elem.attrib.get(f'{{{W}}}num', '1')
            num_cols = int(num_str)
        else:
            num_cols = 1  # No cols element means single-column

        if num_cols == 3:
            print(f"PASS: Component 1 — 3 columns configured (num={num_cols})")
            total_score += 0.40
        else:
            print(f"FAIL: Component 1 — expected 3 columns, found {num_cols}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Separator line enabled between columns (0.30 points)
    # The sep attribute should be "1" in the golden state.
    # Initial state has no sep attribute (or sep=0).
    try:
        if cols_elem is not None:
            sep_val = cols_elem.attrib.get(f'{{{W}}}sep', '0')
            sep_enabled = (sep_val == '1')
        else:
            sep_enabled = False

        if sep_enabled:
            print(f"PASS: Component 2 — separator line enabled (sep={sep_val})")
            total_score += 0.30
        else:
            sep_display = cols_elem.attrib.get(f'{{{W}}}sep', 'absent') if cols_elem is not None else 'absent'
            print(f"FAIL: Component 2 — separator line not enabled (sep={sep_display})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Equal column widths AND column spacing ~0.40cm (0.30 points)
    # Golden state: equalWidth=1, space=226 twips (~0.3986 cm, target 0.40cm)
    # Initial state: no equalWidth, no space attributes
    try:
        if cols_elem is not None:
            equal_width_val = cols_elem.attrib.get(f'{{{W}}}equalWidth', '0')
            equal_width = (equal_width_val == '1')

            space_str = cols_elem.attrib.get(f'{{{W}}}space', None)
            if space_str is not None:
                # space is in twips (1 twip = 1/1440 inch; 1 inch = 2.54 cm)
                space_twips = int(space_str)
                space_cm = space_twips / 1440 * 2.54
                # Allow ±0.05 cm tolerance around target of 0.40 cm
                spacing_ok = abs(space_cm - 0.40) <= 0.05
            else:
                space_cm = None
                spacing_ok = False
        else:
            equal_width = False
            space_cm = None
            spacing_ok = False

        if equal_width and spacing_ok:
            print(f"PASS: Component 3 — equal column widths (equalWidth={equal_width_val}) "
                  f"and spacing {space_cm:.4f}cm (~0.40cm)")
            total_score += 0.30
        else:
            ew_display = equal_width_val if cols_elem is not None else 'absent'
            sp_display = f"{space_cm:.4f}cm" if space_cm is not None else 'absent'
            print(f"FAIL: Component 3 — equalWidth={ew_display}, spacing={sp_display} "
                  f"(expected equalWidth=1 and spacing~0.40cm)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

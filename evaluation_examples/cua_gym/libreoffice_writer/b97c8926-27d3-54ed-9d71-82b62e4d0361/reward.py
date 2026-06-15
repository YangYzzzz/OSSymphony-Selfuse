"""
Reward Script: Change column layout to two unequal columns (2:1 ratio) with separator line
Task ID: writer_page_052
Domain: libreoffice_writer
Scoring:
  Component 1: equalWidth is disabled (unequal columns) — 0.35 pts
  Component 2: Separator line enabled (sep=1)            — 0.30 pts
  Component 3: Left column is ~2x the right column width — 0.35 pts
  Total: 1.0
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_page_052'
FILE_PATH = f'{WORKDIR}/Desktop/sidebar_layout.docx'


def verify_task(file_path):
    """
    Verify the column layout change:
    - Two unequal columns (equalWidth disabled)
    - Separator line enabled
    - Left column ~twice the width of the right column (2:1 ratio)

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get section and columns XML element
    try:
        section = doc.sections[0]
        sectPr = section._sectPr
        cols = sectPr.find(qn('w:cols'))
    except Exception as e:
        print(f"CRITICAL: Cannot find section/cols element: {e}")
        print("REWARD: 0.0")
        return 0.0

    if cols is None:
        print("CRITICAL: No w:cols element found in document")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: equalWidth is disabled — columns have custom (unequal) widths (0.35 pts)
    # Initial state has equalWidth='1'; golden state has equalWidth='0'
    try:
        equal_width = cols.get(qn('w:equalWidth'))
        # equalWidth='0' means custom widths (disabled); '1' or absent means equal widths
        if equal_width == '0':
            print("PASS: Component 1 — equalWidth=0 (custom column widths enabled) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — equalWidth={equal_width!r}, expected '0' (custom widths)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Separator line is enabled (sep=1) (0.30 pts)
    # Initial state has no sep attribute; golden state has sep='1'
    try:
        sep = cols.get(qn('w:sep'))
        if sep == '1':
            print("PASS: Component 2 — sep=1 (separator line enabled) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — sep={sep!r}, expected '1' (separator not enabled)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Left column is approximately twice the width of the right column (2:1 ratio) (0.35 pts)
    # Initial state: equal columns; Golden state: col[0] ~2x col[1]
    try:
        col_elements = cols.findall(qn('w:col'))
        if len(col_elements) == 2:
            left_w = int(col_elements[0].get(qn('w:w'), 0))
            right_w = int(col_elements[1].get(qn('w:w'), 0))
            if right_w > 0:
                ratio = left_w / right_w
                # Allow 5% tolerance around 2.0 ratio
                if 1.90 <= ratio <= 2.10:
                    print(f"PASS: Component 3 — left={left_w} twips, right={right_w} twips, ratio={ratio:.4f} (2:1 ratio verified) (0.35 pts)")
                    total_score += 0.35
                else:
                    print(f"FAIL: Component 3 — ratio={ratio:.4f} (expected ~2.0), left={left_w}, right={right_w}")
            else:
                print("FAIL: Component 3 — right column width is zero or missing")
        else:
            print(f"FAIL: Component 3 — expected 2 w:col elements, found {len(col_elements)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

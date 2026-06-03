"""
Reward Script: Change rectangle shape outline to red dashed 2pt line
Task ID: writer_obj_010
Domain: libreoffice_writer
Scoring:
  Component 1: Border color is red (#FF0000)   — 0.4 pts
  Component 2: Border dash style is 'dash'     — 0.3 pts
  Component 3: Border width is 25400 EMU (2pt) — 0.3 pts
  Total: 1.0
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_obj_010'

# DrawingML namespace map
A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'

def find_rectangle_ln_element(doc):
    """
    Search all paragraphs for the first inline drawing containing a rectangle (prstGeom prst='rect')
    and return its <a:ln> element, or None if not found.
    """
    for para in doc.paragraphs:
        for run in para.runs:
            xml = run._element.xml
            if 'drawing' not in xml:
                continue
            # Look for the <a:ln> within the run element
            drawing_elem = run._element
            # Find all a:ln elements
            ln_elems = drawing_elem.findall(
                './/{%s}ln' % A_NS
            )
            # Also check the shape is a rectangle (prstGeom prst='rect')
            geom_elems = drawing_elem.findall(
                './/{%s}prstGeom' % A_NS
            )
            is_rect = any(
                g.get('prst') == 'rect' for g in geom_elems
            )
            if is_rect and ln_elems:
                return ln_elems[0]
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Task: Change the rectangle border to red (#FF0000), dashed line, 2pt width.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Locate the rectangle's <a:ln> element
    ln_elem = find_rectangle_ln_element(doc)
    if ln_elem is None:
        print("FAIL: Could not find a rectangle shape with a line element in the document")
        print("\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Border color is red #FF0000 (0.4 points)
    # Initial state: srgbClr val="000000" (black)
    # Golden state: srgbClr val="FF0000" (red)
    try:
        solid_fill = ln_elem.find('.//{%s}solidFill' % A_NS)
        srgb_clr = None
        if solid_fill is not None:
            srgb_clr = solid_fill.find('{%s}srgbClr' % A_NS)

        if srgb_clr is not None:
            color_val = srgb_clr.get('val', '').upper()
        else:
            color_val = None

        if color_val == 'FF0000':
            print(f"PASS: Component 1 — border color is red (#FF0000) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — expected border color #FF0000, found: {color_val}")
    except Exception as e:
        print(f"ERROR: Component 1 (color check) — {e}")

    # Component 2: Border dash style is 'dash' (0.3 points)
    # Initial state: prstDash val="solid"
    # Golden state: prstDash val="dash"
    try:
        prst_dash = ln_elem.find('{%s}prstDash' % A_NS)
        if prst_dash is not None:
            dash_val = prst_dash.get('val', '')
        else:
            dash_val = None

        if dash_val == 'dash':
            print(f"PASS: Component 2 — border dash style is 'dash' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — expected dash style 'dash', found: {dash_val}")
    except Exception as e:
        print(f"ERROR: Component 2 (dash style check) — {e}")

    # Component 3: Border width is 25400 EMU (2pt) (0.3 points)
    # Initial state: w="12700" (~1pt)
    # Golden state: w="25400" (2pt)
    # Note: 1 point = 12700 EMU. 2pt = 25400 EMU. We allow a tolerance of ±1270 (0.1pt).
    try:
        w_val = ln_elem.get('w')
        if w_val is not None:
            w_int = int(w_val)
            # 2pt = 25400 EMU; accept range 24130–26670 (~1.9pt–2.1pt tolerance)
            if abs(w_int - 25400) <= 1270:
                print(f"PASS: Component 3 — border width is {w_int} EMU (~2pt) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — expected border width ~25400 EMU (2pt), found: {w_int} EMU")
        else:
            print("FAIL: Component 3 — <a:ln> has no 'w' attribute (width not set)")
    except Exception as e:
        print(f"ERROR: Component 3 (width check) — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Desktop/design_doc.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

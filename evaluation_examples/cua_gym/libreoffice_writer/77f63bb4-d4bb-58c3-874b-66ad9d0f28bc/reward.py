"""
Reward Script: Insert a text box on page 1 and set it to have 2 columns with 0.5cm spacing between the columns.
Task ID: writer_obj_034
Domain: libreoffice_writer
Scoring:
  Component 1: Textbox (drawing with txBx="1") exists in the document — 0.40 points
  Component 2: Textbox has 2 columns configured (w:cols w:num="2") — 0.35 points
  Component 3: Column spacing is 0.5cm / 180000 EMU (w:space="180000") — 0.25 points
  Total: 1.0
"""

import os
from docx import Document
from lxml import etree

WORKDIR = '/home/user/Desktop'
TASK_FILE = 'column_layout.docx'
FILE_PATH = os.path.join(WORKDIR, TASK_FILE)

# Namespace map for XML lookups
NS = {
    'w':   'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'wp':  'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a':   'http://schemas.openxmlformats.org/drawingml/2006/main',
    'wps': 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape',
}

# Target values from task specification
EXPECTED_COLS = 2
EXPECTED_SPACING_EMU = 180000  # 0.5 cm in EMU
SPACING_TOLERANCE_EMU = 10000  # ~0.03 cm tolerance


def verify_task(file_path):
    """
    Verify that a text box has been inserted with 2 columns and 0.5cm column spacing.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: load document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Locate all drawings in the document body
    drawings = doc.element.body.findall('.//w:drawing', NS)

    # Component 1: A textbox (drawing with wps:txbx / txBx="1") exists (0.40 points)
    textbox_found = False
    textbox_elem = None
    try:
        for drawing in drawings:
            # Check for wps:wsp element with txBx="1" on the cNvSpPr
            cnv_spr_list = drawing.findall('.//wps:cNvSpPr', NS)
            for cnv in cnv_spr_list:
                if cnv.get('{http://schemas.microsoft.com/office/word/2010/wordprocessingShape}txBx') == '1':
                    textbox_found = True
                    textbox_elem = drawing
                    break
                # Alternative attribute without namespace prefix (wps ns on txBx attr)
                if cnv.get('txBx') == '1':
                    textbox_found = True
                    textbox_elem = drawing
                    break
            # Also check via presence of wps:txbx child element (the content container)
            if not textbox_found:
                txbx_elems = drawing.findall('.//wps:txbx', NS)
                if txbx_elems:
                    textbox_found = True
                    textbox_elem = drawing
            if textbox_found:
                break

        if textbox_found:
            print("PASS: Component 1 — textbox (wps:txbx drawing) exists in the document (0.40 pts)")
            total_score += 0.40
        else:
            print("FAIL: Component 1 — no textbox found in the document. Expected a drawing with wps:txbx element.")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Textbox has 2 columns configured (0.35 points)
    # The 2-column setting lives in a w:sectPr > w:cols inside the textbox content
    num_cols_found = None
    cols_elem = None
    try:
        if textbox_found and textbox_elem is not None:
            # Find w:sectPr inside the textbox content
            sectprs = textbox_elem.findall('.//w:sectPr', NS)
            for sectpr in sectprs:
                cols = sectpr.find('w:cols', NS)
                if cols is not None:
                    cols_elem = cols
                    num_val = cols.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}num')
                    if num_val is None:
                        # Try without namespace
                        num_val = cols.get('num')
                    if num_val is not None:
                        num_cols_found = int(num_val)
                    break

            if num_cols_found == EXPECTED_COLS:
                print(f"PASS: Component 2 — textbox has {num_cols_found} columns configured (0.35 pts)")
                total_score += 0.35
            elif num_cols_found is not None:
                print(f"FAIL: Component 2 — expected {EXPECTED_COLS} columns, found {num_cols_found}")
            else:
                print("FAIL: Component 2 — no w:cols element found in textbox sectPr. Text box column layout not configured.")
        elif not textbox_found:
            print("SKIP: Component 2 — skipped because no textbox was found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Column spacing is 0.5cm = 180000 EMU (0.25 points)
    try:
        if cols_elem is not None:
            space_val = cols_elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}space')
            if space_val is None:
                space_val = cols_elem.get('space')

            if space_val is not None:
                space_emu = int(space_val)
                diff = abs(space_emu - EXPECTED_SPACING_EMU)
                space_cm = round(space_emu / 914400 * 2.54, 4)
                if diff <= SPACING_TOLERANCE_EMU:
                    print(f"PASS: Component 3 — column spacing is {space_emu} EMU ({space_cm} cm), expected 180000 EMU (0.5 cm) (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 3 — column spacing is {space_emu} EMU ({space_cm} cm), expected 180000 EMU (0.5 cm)")
            else:
                print("FAIL: Component 3 — w:cols element has no w:space attribute; column spacing not set")
        elif textbox_found:
            print("FAIL: Component 3 — skipped because no w:cols element was found in the textbox")
        else:
            print("SKIP: Component 3 — skipped because no textbox was found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {round(total_score, 4)}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical file path on VM
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

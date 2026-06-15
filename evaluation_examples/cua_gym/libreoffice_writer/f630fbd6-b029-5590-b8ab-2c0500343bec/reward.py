"""
Reward Script: Set text wrapping spacing around the image on page 1 to 0.5cm on all four sides
Task ID: writer_obj_011
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5 pts): wp:anchor distT/distB/distL/distR all == 180000 EMU (0.5cm)
  Component 2 (0.5 pts): wp:wrapSquare distT/distB/distL/distR all == 180000 EMU (0.5cm)
"""

import os
from lxml import etree

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_obj_011'
TARGET_FILE = f'{WORKDIR}/product_catalog.docx'

# Namespaces used in .docx XML
WP_NS = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
TARGET_DIST_EMU = 180000  # 0.5cm in EMU (1cm = 360000 EMU)
TOLERANCE = 1  # allow 1 EMU tolerance for rounding


def verify_task(file_path):
    """
    Verify task completion: text wrapping spacing changed from 0cm to 0.5cm on all four sides.
    Examines the wp:anchor and wp:wrapSquare elements for the floating image on page 1.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
    except ImportError:
        print("CRITICAL: python-docx not available")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the floating image's anchor element (wp:anchor)
    anchor_elem = None
    wrap_elem = None

    for para in doc.paragraphs:
        for run in para.runs:
            elem_xml = run._element.xml
            if '<wp:anchor' in elem_xml or 'wrapSquare' in elem_xml:
                # Navigate DOM to find wp:anchor
                for drawing in run._element.iter(
                    '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}drawing'
                ):
                    for anchor in drawing.iter(f'{{{WP_NS}}}anchor'):
                        anchor_elem = anchor
                        # Also find wrapSquare child
                        for ws in anchor.iter(f'{{{WP_NS}}}wrapSquare'):
                            wrap_elem = ws
                        break
                if anchor_elem is not None:
                    break
        if anchor_elem is not None:
            break

    if anchor_elem is None:
        print("FAIL: No floating image (wp:anchor) found in document")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: wp:anchor distT/distB/distL/distR all == 180000 EMU (0.5 pts)
    # The anchor element carries the object-level wrap distances in distT/B/L/R attributes.
    try:
        dist_top = int(anchor_elem.get('distT', '0'))
        dist_bottom = int(anchor_elem.get('distB', '0'))
        dist_left = int(anchor_elem.get('distL', '0'))
        dist_right = int(anchor_elem.get('distR', '0'))

        anchor_ok = (
            abs(dist_top - TARGET_DIST_EMU) <= TOLERANCE and
            abs(dist_bottom - TARGET_DIST_EMU) <= TOLERANCE and
            abs(dist_left - TARGET_DIST_EMU) <= TOLERANCE and
            abs(dist_right - TARGET_DIST_EMU) <= TOLERANCE
        )

        if anchor_ok:
            print(
                f"PASS: Component 1 — wp:anchor wrap distances all 180000 EMU (0.5cm): "
                f"T={dist_top} B={dist_bottom} L={dist_left} R={dist_right} (0.5 pts)"
            )
            total_score += 0.5
        else:
            print(
                f"FAIL: Component 1 — wp:anchor wrap distances not all 180000 EMU: "
                f"T={dist_top} B={dist_bottom} L={dist_left} R={dist_right} "
                f"(expected all 180000)"
            )
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: wp:wrapSquare distT/distB/distL/distR all == 180000 EMU (0.5 pts)
    # The wrapSquare element independently records wrap spacing on each side.
    try:
        if wrap_elem is None:
            print("FAIL: Component 2 — No wp:wrapSquare element found in anchor")
        else:
            ws_top = int(wrap_elem.get('distT', '0'))
            ws_bottom = int(wrap_elem.get('distB', '0'))
            ws_left = int(wrap_elem.get('distL', '0'))
            ws_right = int(wrap_elem.get('distR', '0'))

            wrap_ok = (
                abs(ws_top - TARGET_DIST_EMU) <= TOLERANCE and
                abs(ws_bottom - TARGET_DIST_EMU) <= TOLERANCE and
                abs(ws_left - TARGET_DIST_EMU) <= TOLERANCE and
                abs(ws_right - TARGET_DIST_EMU) <= TOLERANCE
            )

            if wrap_ok:
                print(
                    f"PASS: Component 2 — wp:wrapSquare distances all 180000 EMU (0.5cm): "
                    f"T={ws_top} B={ws_bottom} L={ws_left} R={ws_right} (0.5 pts)"
                )
                total_score += 0.5
            else:
                print(
                    f"FAIL: Component 2 — wp:wrapSquare distances not all 180000 EMU: "
                    f"T={ws_top} B={ws_bottom} L={ws_left} R={ws_right} "
                    f"(expected all 180000)"
                )
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(TARGET_FILE):
    print(f"File not found: {TARGET_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(TARGET_FILE)

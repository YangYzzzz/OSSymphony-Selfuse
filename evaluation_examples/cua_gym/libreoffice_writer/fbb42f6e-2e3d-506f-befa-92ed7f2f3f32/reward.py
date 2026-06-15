"""
Reward Script: Set image horizontal center alignment and vertical position to 2cm
Task ID: writer_obj_036
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5 pts): Image horizontal alignment is 'center' relative to 'page'
  Component 2 (0.5 pts): Image vertical position is 720000 EMU (2cm) from top of page
"""

import os
from docx import Document

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_obj_036'
FILE_PATH = f'{WORKDIR}/centered_image_doc.docx'

# EMU conversion: 1cm = 360000 EMU, so 2cm = 720000 EMU
TARGET_VERTICAL_EMU = 720000
# Allow a small tolerance of +/- 18000 EMU (~0.05cm)
VERTICAL_TOLERANCE_EMU = 18000


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.

    The task requires:
    1. Image horizontal alignment: wp:positionH relativeFrom="page" with <wp:align>center</wp:align>
    2. Image vertical position: wp:positionV relativeFrom="page" with posOffset == 720000 EMU (2cm)

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the anchor image element
    anchor_element = None
    for para in doc.paragraphs:
        for run in para.runs:
            xml = run._element.xml
            if 'graphicData' in xml and 'wp:anchor' in xml:
                # Get the anchor element from the run
                drawing = run._element.find('.//{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}anchor')
                if drawing is not None:
                    anchor_element = drawing
                    break
        if anchor_element is not None:
            break

    if anchor_element is None:
        print("CRITICAL: No floating (anchor) image found in document.")
        print("REWARD: 0.0")
        return 0.0

    WP_NS = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'

    # Component 1: Horizontal alignment is 'center' relative to 'page' (0.5 points)
    try:
        pos_h = anchor_element.find(f'{{{WP_NS}}}positionH')
        if pos_h is None:
            print("FAIL: Component 1 — <wp:positionH> element not found")
        else:
            relative_from_h = pos_h.get('relativeFrom', '')
            align_elem = pos_h.find(f'{{{WP_NS}}}align')
            pos_offset_elem = pos_h.find(f'{{{WP_NS}}}posOffset')

            if relative_from_h == 'page' and align_elem is not None and align_elem.text == 'center':
                print(f"PASS: Component 1 — Horizontal alignment is 'center' relative to 'page' (0.5 pts)")
                total_score += 0.5
            else:
                # Provide detailed failure info
                if relative_from_h != 'page':
                    print(f"FAIL: Component 1 — positionH relativeFrom='{relative_from_h}', expected 'page'")
                elif align_elem is None:
                    if pos_offset_elem is not None:
                        print(f"FAIL: Component 1 — positionH uses posOffset={pos_offset_elem.text} instead of <wp:align>center</wp:align>")
                    else:
                        print(f"FAIL: Component 1 — No <wp:align> or <wp:posOffset> found in positionH")
                else:
                    print(f"FAIL: Component 1 — Horizontal align='{align_elem.text}', expected 'center'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Vertical position is 720000 EMU (2cm) from top of page (0.5 points)
    try:
        pos_v = anchor_element.find(f'{{{WP_NS}}}positionV')
        if pos_v is None:
            print("FAIL: Component 2 — <wp:positionV> element not found")
        else:
            relative_from_v = pos_v.get('relativeFrom', '')
            pos_offset_elem = pos_v.find(f'{{{WP_NS}}}posOffset')
            align_elem_v = pos_v.find(f'{{{WP_NS}}}align')

            if pos_offset_elem is not None:
                try:
                    emu_value = int(pos_offset_elem.text)
                    emu_cm = emu_value / 360000
                    delta = abs(emu_value - TARGET_VERTICAL_EMU)

                    if relative_from_v == 'page' and delta <= VERTICAL_TOLERANCE_EMU:
                        print(f"PASS: Component 2 — Vertical posOffset={emu_value} EMU (~{emu_cm:.3f}cm) relative to 'page', expected 720000 EMU (2cm) (0.5 pts)")
                        total_score += 0.5
                    else:
                        if relative_from_v != 'page':
                            print(f"FAIL: Component 2 — positionV relativeFrom='{relative_from_v}', expected 'page'")
                        else:
                            print(f"FAIL: Component 2 — Vertical posOffset={emu_value} EMU (~{emu_cm:.3f}cm), expected 720000 EMU (2.0cm), delta={delta}")
                except ValueError:
                    print(f"FAIL: Component 2 — posOffset value '{pos_offset_elem.text}' is not a valid integer")
            elif align_elem_v is not None:
                print(f"FAIL: Component 2 — positionV uses align='{align_elem_v.text}' instead of posOffset=720000 EMU (2cm)")
            else:
                print(f"FAIL: Component 2 — No <wp:posOffset> or <wp:align> found in positionV")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

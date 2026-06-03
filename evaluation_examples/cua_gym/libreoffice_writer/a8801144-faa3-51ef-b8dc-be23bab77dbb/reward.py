"""
Reward Script: Move image to right-aligned horizontally and 5cm vertically from top
Task ID: writer_obj_076
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6 pts): Horizontal alignment is 'right' relative to 'margin' (page text area)
  Component 2 (0.4 pts): Vertical position is 5cm from top of page (posOffset ~1800000 EMU)
  Total: 1.0
"""

import os
from docx import Document

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_obj_076'
FILE_NAME = 'right_aligned_doc.docx'

# Tolerance for vertical position check: +/- 0.5cm in EMU (180000 EMU)
VERTICAL_TOLERANCE_EMU = 180000
TARGET_VERTICAL_EMU = 1800000  # 5cm = 1800000 EMU (1cm = 360000 EMU)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Task: Move image on page 1 so it is horizontally aligned to right side of page margin,
          and vertically positioned at 5cm from the top of the page.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Namespaces for XML parsing
    ns = {
        'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    }

    # Find anchor drawings in the document body
    body = doc.element.body
    anchors = body.findall('.//wp:anchor', ns)

    if not anchors:
        print("FAIL: No floating (anchor) image found in document")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Use the first anchor drawing (the product image on page 1)
    anchor = anchors[0]

    # Component 1: Horizontal alignment is 'right' relative to 'margin' (0.6 points)
    # Initial state: positionH relativeFrom='margin', align='center'
    # Golden state:  positionH relativeFrom='margin', align='right'
    try:
        positionH = anchor.find('wp:positionH', ns)
        if positionH is None:
            print("FAIL: Component 1 — positionH element not found")
        else:
            relative_from = positionH.get('relativeFrom', '')
            align_elem = positionH.find('wp:align', ns)
            align_text = align_elem.text.strip().lower() if align_elem is not None else None
            pos_offset_elem = positionH.find('wp:posOffset', ns)

            # Must use alignment (not manual offset) relative to 'margin'
            if relative_from == 'margin' and align_text == 'right':
                print(f"PASS: Component 1 — Horizontal alignment is 'right' relative to 'margin' (0.6 pts)")
                total_score += 0.6
            else:
                if relative_from != 'margin':
                    print(f"FAIL: Component 1 — Expected relativeFrom='margin', found relativeFrom='{relative_from}'")
                elif align_text != 'right':
                    print(f"FAIL: Component 1 — Expected align='right', found align='{align_text}' (posOffset={pos_offset_elem.text if pos_offset_elem is not None else 'N/A'})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Vertical position is 5cm from top of page (posOffset ~1800000 EMU) (0.4 points)
    # Initial state: positionV relativeFrom='page', posOffset=1080000 EMU (3cm)
    # Golden state:  positionV relativeFrom='page', posOffset=1800000 EMU (5cm)
    try:
        positionV = anchor.find('wp:positionV', ns)
        if positionV is None:
            print("FAIL: Component 2 — positionV element not found")
        else:
            relative_from_v = positionV.get('relativeFrom', '')
            align_v = positionV.find('wp:align', ns)
            pos_offset_v = positionV.find('wp:posOffset', ns)

            if pos_offset_v is not None:
                offset_emu = int(pos_offset_v.text)
                offset_cm = offset_emu / 360000.0
                deviation = abs(offset_emu - TARGET_VERTICAL_EMU)

                if relative_from_v == 'page' and deviation <= VERTICAL_TOLERANCE_EMU:
                    print(f"PASS: Component 2 — Vertical position is {offset_cm:.2f}cm from top of page "
                          f"(posOffset={offset_emu} EMU, target=1800000 EMU / 5cm) (0.4 pts)")
                    total_score += 0.4
                else:
                    if relative_from_v != 'page':
                        print(f"FAIL: Component 2 — Expected relativeFrom='page', found relativeFrom='{relative_from_v}'")
                    else:
                        print(f"FAIL: Component 2 — Vertical position is {offset_cm:.2f}cm "
                              f"(posOffset={offset_emu} EMU), expected ~5cm (1800000 EMU), "
                              f"deviation={deviation} EMU exceeds tolerance={VERTICAL_TOLERANCE_EMU} EMU")
            elif align_v is not None:
                # If using alignment keyword instead of offset — this would be wrong for task requirements
                print(f"FAIL: Component 2 — Vertical uses alignment='{align_v.text}' instead of posOffset, "
                      f"expected posOffset ~1800000 EMU (5cm)")
            else:
                print("FAIL: Component 2 — Neither posOffset nor align found in positionV")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against the canonical artifact path on the VM
file_path = os.path.join(WORKDIR, FILE_NAME)
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Position image at exactly X=2cm, Y=5cm from margin
Task ID: writer_obj_027
Domain: libreoffice_writer
Scoring:
  Component 1: Horizontal position is exactly 2cm (720000 EMU) from left margin (0.5 points)
  Component 2: Vertical position is exactly 5cm (1800000 EMU) from top margin (0.5 points)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_obj_027'

# 1 cm = 360000 EMU
CM_TO_EMU = 360000
TARGET_X_CM = 2.0
TARGET_Y_CM = 5.0
TARGET_X_EMU = int(TARGET_X_CM * CM_TO_EMU)   # 720000
TARGET_Y_EMU = int(TARGET_Y_CM * CM_TO_EMU)    # 1800000
# Allow tolerance of ±36000 EMU (±0.1 cm) for minor rounding
TOLERANCE_EMU = 36000


def get_image_position(docx_path):
    """
    Extract the first floating image's (anchor) horizontal and vertical
    position offsets (in EMU) from word/document.xml.

    Returns (pos_h_emu, pos_v_emu) or (None, None) on failure.
    The positions use relativeFrom="margin" as set by LibreOffice Writer.
    """
    ns = {
        'w':   'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'wp':  'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
        'a':   'http://schemas.openxmlformats.org/drawingml/2006/main',
    }

    with zipfile.ZipFile(docx_path, 'r') as z:
        xml_bytes = z.read('word/document.xml')

    root = ET.fromstring(xml_bytes)

    # Find all wp:anchor elements (floating images)
    # Use iterative search because namespaces vary
    for elem in root.iter():
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag == 'anchor':
            pos_h = None
            pos_v = None
            for child in elem:
                child_tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                if child_tag == 'positionH':
                    for sub in child:
                        sub_tag = sub.tag.split('}')[-1] if '}' in sub.tag else sub.tag
                        if sub_tag == 'posOffset':
                            try:
                                pos_h = int(sub.text.strip())
                            except (TypeError, ValueError):
                                pass
                elif child_tag == 'positionV':
                    for sub in child:
                        sub_tag = sub.tag.split('}')[-1] if '}' in sub.tag else sub.tag
                        if sub_tag == 'posOffset':
                            try:
                                pos_v = int(sub.text.strip())
                            except (TypeError, ValueError):
                                pass
            if pos_h is not None and pos_v is not None:
                return pos_h, pos_v

    return None, None


def verify_task(file_path):
    """
    Verify that the floating image in precise_doc.docx has been repositioned
    to exactly X=2cm, Y=5cm from the page margin.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must be loadable as a docx ZIP
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            if 'word/document.xml' not in z.namelist():
                print("CRITICAL: word/document.xml not found in docx")
                print("REWARD: 0.0")
                return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract image position
    try:
        pos_h, pos_v = get_image_position(file_path)
        if pos_h is None or pos_v is None:
            print("FAIL: No floating image (wp:anchor) found in document.xml")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
        print(f"INFO: Image position — posH={pos_h} EMU ({pos_h/CM_TO_EMU:.4f} cm), "
              f"posV={pos_v} EMU ({pos_v/CM_TO_EMU:.4f} cm)")
    except Exception as e:
        print(f"CRITICAL: Failed to parse document.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Horizontal position == 2cm (720000 EMU) from left margin (0.5 points)
    try:
        h_diff = abs(pos_h - TARGET_X_EMU)
        h_ok = h_diff <= TOLERANCE_EMU
        if h_ok:
            total_score += 0.5
            print(f"PASS: Component 1 — Horizontal position is {pos_h} EMU "
                  f"({pos_h/CM_TO_EMU:.3f} cm), target {TARGET_X_EMU} EMU "
                  f"({TARGET_X_CM} cm), diff={h_diff} EMU (0.5 pts)")
        else:
            print(f"FAIL: Component 1 — Horizontal position is {pos_h} EMU "
                  f"({pos_h/CM_TO_EMU:.3f} cm), expected {TARGET_X_EMU} EMU "
                  f"({TARGET_X_CM} cm), diff={h_diff} EMU (tolerance={TOLERANCE_EMU} EMU)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Vertical position == 5cm (1800000 EMU) from top margin (0.5 points)
    try:
        v_diff = abs(pos_v - TARGET_Y_EMU)
        v_ok = v_diff <= TOLERANCE_EMU
        if v_ok:
            total_score += 0.5
            print(f"PASS: Component 2 — Vertical position is {pos_v} EMU "
                  f"({pos_v/CM_TO_EMU:.3f} cm), target {TARGET_Y_EMU} EMU "
                  f"({TARGET_Y_CM} cm), diff={v_diff} EMU (0.5 pts)")
        else:
            print(f"FAIL: Component 2 — Vertical position is {pos_v} EMU "
                  f"({pos_v/CM_TO_EMU:.3f} cm), expected {TARGET_Y_EMU} EMU "
                  f"({TARGET_Y_CM} cm), diff={v_diff} EMU (tolerance={TOLERANCE_EMU} EMU)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path on VM
file_path = f'{WORKDIR}/precise_doc.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Insert blueprint.png with Through wrapping, 0.2cm spacing, 8x6cm size, X:8cm Y:4cm, foreground
Task ID: writer_obj_069
Domain: libreoffice_writer
Scoring:
  Component 1 - Floating anchor image exists in document         (0.20 pts)
  Component 2 - Wrap type is wrapThrough                         (0.20 pts)
  Component 3 - Wrap spacing 0.2cm on all four sides             (0.20 pts)
  Component 4 - Image size 8cm x 6cm                             (0.20 pts)
  Component 5 - Position X:8cm Y:4cm AND foreground (behindDoc=0)(0.20 pts)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_obj_069'

# EMU conversion constant: 1 inch = 914400 EMU; 1 cm = 914400/2.54 EMU
CM_TO_EMU = 914400 / 2.54  # = 360000 EMU per cm

# Tolerance: ±2% of target value (generous to allow minor rounding)
TOLERANCE_FRAC = 0.02

def approx_equal(actual, expected, tol_frac=TOLERANCE_FRAC):
    """Check if actual is within tol_frac of expected."""
    if expected == 0:
        return abs(actual) < 1
    return abs(actual - expected) / abs(expected) <= tol_frac


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Uses zipfile + xml.etree to parse .docx directly, bypassing Content_Types.xml
    issues that can prevent python-docx from loading the file.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be a valid zip
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
        doc_xml_bytes = zf.read('word/document.xml')
        zf.close()
    except Exception as e:
        print(f"CRITICAL: Cannot open docx as zip or read document.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        root = ET.fromstring(doc_xml_bytes)
    except Exception as e:
        print(f"CRITICAL: Cannot parse document.xml as XML: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Namespaces used in OOXML word processing drawing
    ns = {
        'w':   'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'wp':  'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
        'a':   'http://schemas.openxmlformats.org/drawingml/2006/main',
        'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
        'r':   'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    }

    # Find all wp:anchor elements (floating images)
    anchors = root.findall('.//wp:anchor', ns)

    # Component 1: Floating anchor image exists (0.20 points)
    # A floating image uses wp:anchor; inline images use wp:inline.
    # The task requires a floating image with specific position/wrap settings,
    # so it MUST be an anchor, not inline.
    try:
        if len(anchors) >= 1:
            print(f"PASS: Component 1 — Floating anchor image found ({len(anchors)} anchor(s)) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — No floating anchor image found (anchors={len(anchors)})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Only continue detailed checks if we have at least one anchor
    if len(anchors) == 0:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {min(total_score, 1.0)}")
        return min(total_score, 1.0)

    # Use the first anchor (should be the blueprint image)
    anchor = anchors[0]

    # Component 2: Wrap type is wrapThrough (0.20 points)
    # Through wrapping means text flows around the image contour.
    # In OOXML, this is represented by the wp:wrapThrough child element.
    try:
        wrap_through = anchor.find('wp:wrapThrough', ns)
        wrap_none = anchor.find('wp:wrapNone', ns)
        wrap_square = anchor.find('wp:wrapSquare', ns)
        wrap_tight = anchor.find('wp:wrapTight', ns)
        wrap_topbottom = anchor.find('wp:wrapTopAndBottom', ns)

        if wrap_through is not None:
            print(f"PASS: Component 2 — Wrap type is wrapThrough (0.20 pts)")
            total_score += 0.20
        else:
            found_wrap = 'none'
            if wrap_none is not None: found_wrap = 'wrapNone'
            elif wrap_square is not None: found_wrap = 'wrapSquare'
            elif wrap_tight is not None: found_wrap = 'wrapTight'
            elif wrap_topbottom is not None: found_wrap = 'wrapTopAndBottom'
            print(f"FAIL: Component 2 — Expected wrapThrough, found: {found_wrap}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Wrap spacing 0.2cm on all four sides (0.20 points)
    # distT, distB, distL, distR attributes on wp:anchor store the spacing in EMU.
    # 0.2 cm = 72000 EMU
    try:
        target_spacing_emu = 0.2 * CM_TO_EMU  # 72000 EMU
        dist_T = int(anchor.get('distT', 0))
        dist_B = int(anchor.get('distB', 0))
        dist_L = int(anchor.get('distL', 0))
        dist_R = int(anchor.get('distR', 0))

        t_ok = approx_equal(dist_T, target_spacing_emu)
        b_ok = approx_equal(dist_B, target_spacing_emu)
        l_ok = approx_equal(dist_L, target_spacing_emu)
        r_ok = approx_equal(dist_R, target_spacing_emu)

        if t_ok and b_ok and l_ok and r_ok:
            print(f"PASS: Component 3 — Wrap spacing 0.2cm on all sides "
                  f"(T={dist_T}, B={dist_B}, L={dist_L}, R={dist_R} EMU) (0.20 pts)")
            total_score += 0.20
        else:
            cm_T = dist_T / CM_TO_EMU
            cm_B = dist_B / CM_TO_EMU
            cm_L = dist_L / CM_TO_EMU
            cm_R = dist_R / CM_TO_EMU
            print(f"FAIL: Component 3 — Expected 0.2cm on all sides, "
                  f"found T={cm_T:.4f}cm B={cm_B:.4f}cm L={cm_L:.4f}cm R={cm_R:.4f}cm")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Image size 8cm x 6cm (0.20 points)
    # wp:extent cx/cy store width/height in EMU.
    # 8cm = 2880000 EMU, 6cm = 2160000 EMU
    try:
        target_cx = 8.0 * CM_TO_EMU  # 2880000 EMU
        target_cy = 6.0 * CM_TO_EMU  # 2160000 EMU

        extent = anchor.find('wp:extent', ns)
        if extent is not None:
            cx = int(extent.get('cx', 0))
            cy = int(extent.get('cy', 0))
            cx_ok = approx_equal(cx, target_cx)
            cy_ok = approx_equal(cy, target_cy)

            if cx_ok and cy_ok:
                print(f"PASS: Component 4 — Image size 8cm x 6cm "
                      f"(cx={cx}={cx/CM_TO_EMU:.4f}cm, cy={cy}={cy/CM_TO_EMU:.4f}cm) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — Expected 8cm x 6cm, "
                      f"found {cx/CM_TO_EMU:.4f}cm x {cy/CM_TO_EMU:.4f}cm")
        else:
            print("FAIL: Component 4 — wp:extent element not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Position X:8cm, Y:4cm AND foreground (behindDoc=0) (0.20 points)
    # X position: wp:positionH/wp:posOffset in EMU (from page); 8cm = 2880000 EMU
    # Y position: wp:positionV/wp:posOffset in EMU (from page); 4cm = 1440000 EMU
    # Foreground: behindDoc="0" on wp:anchor
    try:
        target_x = 8.0 * CM_TO_EMU  # 2880000 EMU
        target_y = 4.0 * CM_TO_EMU  # 1440000 EMU

        pos_h = anchor.find('wp:positionH', ns)
        pos_v = anchor.find('wp:positionV', ns)
        behind_doc = anchor.get('behindDoc', '1')

        x_ok = False
        y_ok = False
        fg_ok = (behind_doc == '0')

        if pos_h is not None:
            pos_offset_h = pos_h.find('wp:posOffset', ns)
            if pos_offset_h is not None:
                x_emu = int(pos_offset_h.text)
                x_ok = approx_equal(x_emu, target_x)
            else:
                x_emu = None
        else:
            x_emu = None

        if pos_v is not None:
            pos_offset_v = pos_v.find('wp:posOffset', ns)
            if pos_offset_v is not None:
                y_emu = int(pos_offset_v.text)
                y_ok = approx_equal(y_emu, target_y)
            else:
                y_emu = None
        else:
            y_emu = None

        if x_ok and y_ok and fg_ok:
            print(f"PASS: Component 5 — Position X:8cm Y:4cm and foreground "
                  f"(x={x_emu} EMU, y={y_emu} EMU, behindDoc={behind_doc}) (0.20 pts)")
            total_score += 0.20
        else:
            x_cm = x_emu / CM_TO_EMU if x_emu is not None else 'N/A'
            y_cm = y_emu / CM_TO_EMU if y_emu is not None else 'N/A'
            print(f"FAIL: Component 5 — Expected X=8cm Y=4cm foreground(behindDoc=0), "
                  f"found X={x_cm}cm Y={y_cm}cm behindDoc={behind_doc} "
                  f"(x_ok={x_ok}, y_ok={y_ok}, fg_ok={fg_ok})")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/design_review.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

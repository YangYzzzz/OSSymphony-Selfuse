"""
Reward Script: Create a text box on page 1 with specific dimensions, position, and internal margins
Task ID: writer_obj_028
Domain: libreoffice_writer
Scoring:
  - Component 1: Text box (drawing with txbxContent) exists in document (0.30 pts)
  - Component 2: Text box dimensions correct: Width=8cm (2880000 EMU), Height=5cm (1800000 EMU) (0.35 pts)
  - Component 3: Text box position correct: X=10cm (3600000 EMU), Y=3cm (1080000 EMU) (0.20 pts)
  - Component 4: Internal margins correct: 0.3cm (108000 EMU) on all four sides (0.15 pts)
  Total: 1.0
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_obj_028'

# Tolerance for EMU comparisons (±5% or 5000 EMU, whichever is larger)
# 0.3cm = 108000 EMU, 8cm = 2880000 EMU, 5cm = 1800000 EMU
# 10cm = 3600000 EMU, 3cm = 1080000 EMU
# Use a reasonable tolerance: 36000 EMU (~0.1cm) for position/size checks
EMU_TOLERANCE = 36000  # ~0.1cm

# Expected values in EMU
EXPECTED_WIDTH = 2880000   # 8cm
EXPECTED_HEIGHT = 1800000  # 5cm
EXPECTED_X = 3600000       # 10cm from page
EXPECTED_Y = 1080000       # 3cm from page
EXPECTED_MARGIN = 108000   # 0.3cm internal margin on all sides


def within_tolerance(actual, expected, tol=EMU_TOLERANCE):
    """Check if actual is within tolerance of expected."""
    return abs(actual - expected) <= tol


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

    body = doc.element.body

    # -------------------------------------------------------------------------
    # Component 1: Text box (drawing with txbxContent) exists (0.30 pts)
    # This FAILS on initial_env (no text box) and PASSES on golden_env
    # -------------------------------------------------------------------------
    try:
        # Find all drawing elements in body
        drawings = body.findall('.//' + qn('w:drawing'))
        # Find all txbxContent elements (text box content)
        txbx_contents = body.findall('.//' + qn('w:txbxContent'))

        if len(drawings) >= 1 and len(txbx_contents) >= 1:
            print(f"PASS: Component 1 — Text box exists: {len(drawings)} drawing(s), {len(txbx_contents)} txbxContent(s) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — No text box found. drawings={len(drawings)}, txbxContent={len(txbx_contents)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: Text box dimensions — Width=8cm (2880000 EMU), Height=5cm (1800000 EMU) (0.35 pts)
    # -------------------------------------------------------------------------
    try:
        # Look for wp:extent element with cx and cy attributes
        # Namespace for wordprocessingDrawing
        wp_ns = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
        extents = body.findall('.//{%s}extent' % wp_ns)

        width_ok = False
        height_ok = False
        actual_cx = None
        actual_cy = None

        for extent in extents:
            cx_str = extent.get('cx')
            cy_str = extent.get('cy')
            if cx_str is not None and cy_str is not None:
                actual_cx = int(cx_str)
                actual_cy = int(cy_str)
                if within_tolerance(actual_cx, EXPECTED_WIDTH) and within_tolerance(actual_cy, EXPECTED_HEIGHT):
                    width_ok = True
                    height_ok = True
                    break

        if width_ok and height_ok:
            print(f"PASS: Component 2 — Dimensions correct: cx={actual_cx} EMU (~{actual_cx/914400*2.54:.2f}cm), cy={actual_cy} EMU (~{actual_cy/914400*2.54:.2f}cm) (0.35 pts)")
            total_score += 0.35
        else:
            if actual_cx is not None:
                print(f"FAIL: Component 2 — Dimensions wrong: cx={actual_cx} (expected {EXPECTED_WIDTH}), cy={actual_cy} (expected {EXPECTED_HEIGHT})")
            else:
                print(f"FAIL: Component 2 — No extent element found (no text box?)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Text box position — X=10cm (3600000 EMU from page), Y=3cm (1080000 EMU from page) (0.20 pts)
    # -------------------------------------------------------------------------
    try:
        wp_ns = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
        anchors = body.findall('.//{%s}anchor' % wp_ns)

        pos_ok = False
        actual_x = None
        actual_y = None

        for anchor in anchors:
            # positionH/positionV with relativeFrom="page"
            pos_h = anchor.find('{%s}positionH' % wp_ns)
            pos_v = anchor.find('{%s}positionV' % wp_ns)

            if pos_h is not None and pos_v is not None:
                pos_h_from = pos_h.get('relativeFrom', '')
                pos_v_from = pos_v.get('relativeFrom', '')

                offset_h = pos_h.find('{%s}posOffset' % wp_ns)
                offset_v = pos_v.find('{%s}posOffset' % wp_ns)

                if offset_h is not None and offset_v is not None:
                    actual_x = int(offset_h.text)
                    actual_y = int(offset_v.text)

                    x_ok = within_tolerance(actual_x, EXPECTED_X)
                    y_ok = within_tolerance(actual_y, EXPECTED_Y)

                    if x_ok and y_ok:
                        pos_ok = True
                        break

        if pos_ok:
            print(f"PASS: Component 3 — Position correct: X={actual_x} EMU (~{actual_x/914400*2.54:.2f}cm), Y={actual_y} EMU (~{actual_y/914400*2.54:.2f}cm) (0.20 pts)")
            total_score += 0.20
        else:
            if actual_x is not None:
                print(f"FAIL: Component 3 — Position wrong: X={actual_x} (expected {EXPECTED_X}), Y={actual_y} (expected {EXPECTED_Y})")
            else:
                print(f"FAIL: Component 3 — No anchor position element found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------------
    # Component 4: Internal margins — 0.3cm (108000 EMU) on all four sides (0.15 pts)
    # -------------------------------------------------------------------------
    try:
        # The internal margins are in wps:txbx element (inT, inB, inL, inR attributes)
        # and/or wps:bodyPr element
        wps_ns = 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape'
        txbx_elements = body.findall('.//{%s}txbx' % wps_ns)
        bodypr_elements = body.findall('.//{%s}bodyPr' % wps_ns)

        margins_ok = False
        actual_margins = {}

        # Check wps:txbx attributes first
        for txbx in txbx_elements:
            in_t = txbx.get('inT')
            in_b = txbx.get('inB')
            in_l = txbx.get('inL')
            in_r = txbx.get('inR')

            if all(x is not None for x in [in_t, in_b, in_l, in_r]):
                actual_margins = {
                    'inT': int(in_t),
                    'inB': int(in_b),
                    'inL': int(in_l),
                    'inR': int(in_r)
                }
                if all(within_tolerance(v, EXPECTED_MARGIN) for v in actual_margins.values()):
                    margins_ok = True
                    break

        # If not found in txbx, check bodyPr
        if not margins_ok:
            for bodypr in bodypr_elements:
                in_t = bodypr.get('inT')
                in_b = bodypr.get('inB')
                in_l = bodypr.get('inL')
                in_r = bodypr.get('inR')

                if all(x is not None for x in [in_t, in_b, in_l, in_r]):
                    actual_margins = {
                        'inT': int(in_t),
                        'inB': int(in_b),
                        'inL': int(in_l),
                        'inR': int(in_r)
                    }
                    if all(within_tolerance(v, EXPECTED_MARGIN) for v in actual_margins.values()):
                        margins_ok = True
                        break

        if margins_ok:
            vals = list(actual_margins.values())
            print(f"PASS: Component 4 — Internal margins correct: T={vals[0]}, B={vals[1]}, L={vals[2]}, R={vals[3]} EMU (~{vals[0]/914400*2.54:.3f}cm each) (0.15 pts)")
            total_score += 0.15
        else:
            if actual_margins:
                print(f"FAIL: Component 4 — Internal margins wrong: {actual_margins} (expected all {EXPECTED_MARGIN} EMU)")
            else:
                print(f"FAIL: Component 4 — No internal margin attributes found in txbx/bodyPr")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -------------------------------------------------------------------------
    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Default: test against canonical artifact path in the VM env
file_path = f'{WORKDIR}/Desktop/sidebar_layout.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

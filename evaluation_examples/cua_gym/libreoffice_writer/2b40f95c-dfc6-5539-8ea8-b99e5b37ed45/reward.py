"""
Reward Script: Create a process flow diagram in workflow_doc.docx
Task ID: writer_obj_054
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.35): Three rectangles exist with correct text labels (Input, Process, Output)
  - Component 2 (0.15): Two right-pointing arrow shapes exist with dark blue fill (#1565C0)
  - Component 3 (0.20): Rectangles have correct fill (#E3F2FD) and border (#1565C0, ~1pt)
  - Component 4 (0.15): Rectangles have correct dimensions (4cm x 2cm)
  - Component 5 (0.15): All shapes vertically positioned at approximately Y=10cm
Total: 1.0
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_obj_054'

# EMU conversion helpers
EMU_PER_CM = 360000  # 1 cm = 360000 EMU
TOLERANCE_EMU = 180000  # ±0.5 cm tolerance for position checks
PT_1_EMU = 12700  # 1pt = 12700 EMU

def get_drawings(doc):
    """Extract all drawing elements from the document body."""
    body = doc.element.body
    return body.findall('.//' + qn('w:drawing'))

WP_NS = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
WPS_NS = 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape'
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

def get_shape_info(drawing):
    """Extract key properties from a drawing element."""
    info = {}

    # docPr name
    docPr = drawing.find('.//{%s}docPr' % WP_NS)
    info['name'] = docPr.get('name') if docPr is not None else ''

    # Preset geometry (shape type)
    prstGeom = drawing.find('.//{%s}prstGeom' % A_NS)
    info['prst'] = prstGeom.get('prst') if prstGeom is not None else ''

    # Position
    posH = drawing.find('.//{%s}positionH/{%s}posOffset' % (WP_NS, WP_NS))
    posV = drawing.find('.//{%s}positionV/{%s}posOffset' % (WP_NS, WP_NS))
    info['posH'] = int(posH.text) if posH is not None else 0
    info['posV'] = int(posV.text) if posV is not None else 0

    # Extent (size)
    extent = drawing.find('.//{%s}extent' % WP_NS)
    info['cx'] = int(extent.get('cx')) if extent is not None else 0
    info['cy'] = int(extent.get('cy')) if extent is not None else 0

    # Fill colors (first solidFill srgbClr)
    fills = drawing.findall('.//{%s}solidFill/{%s}srgbClr' % (A_NS, A_NS))
    info['fills'] = [f.get('val', '').upper() for f in fills]

    # Border line width
    ln = drawing.find('.//{%s}ln' % A_NS)
    if ln is not None:
        ln_w = ln.get('w')
        info['border_w'] = int(ln_w) if ln_w is not None else None
        # Check for noFill on the border line
        no_fill = ln.find('.//{%s}noFill' % A_NS)
        info['border_no_fill'] = (no_fill is not None)
        # Border color
        ln_clr = ln.find('.//{%s}srgbClr' % A_NS)
        info['border_color'] = ln_clr.get('val', '').upper() if ln_clr is not None else ''
    else:
        info['border_w'] = None
        info['border_no_fill'] = False
        info['border_color'] = ''

    # Text in textbox
    txbx = drawing.find('.//{%s}txbx' % WPS_NS)
    if txbx is not None:
        texts = []
        for r in txbx.findall('.//{%s}r' % W_NS):
            t = r.find('{%s}t' % W_NS)
            if t is not None and t.text:
                texts.append(t.text)
        info['text'] = ''.join(texts).strip()
    else:
        info['text'] = None

    return info


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print("CRITICAL: Cannot load file %s: %s" % (file_path, e))
        print("REWARD: 0.0")
        return 0.0

    # Get all drawing shapes
    try:
        drawings = get_drawings(doc)
        shapes = [get_shape_info(d) for d in drawings]
    except Exception as e:
        print("CRITICAL: Cannot parse drawings: %s" % e)
        print("REWARD: 0.0")
        return 0.0

    # Classify shapes
    rects = [s for s in shapes if s['prst'] == 'rect']
    arrows = [s for s in shapes if s['prst'] == 'rightArrow']

    print("Total shapes: %d (rects=%d, arrows=%d)" % (len(shapes), len(rects), len(arrows)))

    # -------------------------------------------------------------------------
    # Component 1: Three rectangles with correct labels (Input, Process, Output) — 0.35 points
    # -------------------------------------------------------------------------
    try:
        required_labels = {'Input', 'Process', 'Output'}
        found_labels = {s['text'] for s in rects if s['text'] in required_labels}

        if len(rects) >= 3 and found_labels == required_labels:
            print("PASS: Component 1 — Three labeled rectangles found: %s (0.35 pts)" % sorted(found_labels))
            total_score += 0.35
        else:
            missing = required_labels - found_labels
            print("FAIL: Component 1 — Expected rectangles with labels %s, found %d rects with labels %s" % (
                required_labels, len(rects), {s['text'] for s in rects}))
    except Exception as e:
        print("ERROR: Component 1 — %s" % e)

    # -------------------------------------------------------------------------
    # Component 2: Two right-pointing arrows with dark blue (#1565C0) fill — 0.15 points
    # -------------------------------------------------------------------------
    try:
        DARK_BLUE = '1565C0'
        blue_arrows = [s for s in arrows if DARK_BLUE in s['fills']]

        if len(blue_arrows) == 2:
            print("PASS: Component 2 — Two right arrows with #1565C0 fill found (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 2 — Expected 2 right arrows with #1565C0 fill, found %d (total arrows=%d, fills=%s)" % (
                len(blue_arrows), len(arrows), [s['fills'] for s in arrows]))
    except Exception as e:
        print("ERROR: Component 2 — %s" % e)

    # -------------------------------------------------------------------------
    # Component 3: Rectangles have correct fill (#E3F2FD) and border (#1565C0, ~1pt) — 0.20 points
    # -------------------------------------------------------------------------
    try:
        LIGHT_BLUE = 'E3F2FD'
        DARK_BLUE = '1565C0'
        PT1_TOLERANCE = 6350  # ±0.5pt tolerance = 6350 EMU

        correct_fill_and_border = 0
        for s in rects:
            has_fill = LIGHT_BLUE in s['fills']
            has_border_color = s['border_color'] == DARK_BLUE
            has_border_width = (s['border_w'] is not None and
                                abs(s['border_w'] - PT_1_EMU) <= PT1_TOLERANCE)
            if has_fill and has_border_color and has_border_width:
                correct_fill_and_border += 1

        if correct_fill_and_border == 3:
            print("PASS: Component 3 — All 3 rectangles have correct fill #E3F2FD and border #1565C0 1pt (0.20 pts)")
            total_score += 0.20
        elif correct_fill_and_border > 0:
            partial = 0.07 * correct_fill_and_border
            msg = "PARTIAL: Component 3 — %d/3 rects correct fill/border (%.2f pts)" % (correct_fill_and_border, partial)
            print(msg)
            if correct_fill_and_border > 0:
                total_score += partial
        else:
            for s in rects:
                print("FAIL: Component 3 — Rect %s: fills=%s, border_color=%s, border_w=%s" % (
                    s['name'], s['fills'], s['border_color'], s['border_w']))
    except Exception as e:
        print("ERROR: Component 3 — %s" % e)

    # -------------------------------------------------------------------------
    # Component 4: Rectangles have correct dimensions (4cm x 2cm = 1440000 x 720000 EMU) — 0.15 points
    # -------------------------------------------------------------------------
    try:
        SIZE_TOLERANCE = 72000  # ±0.2cm tolerance
        TARGET_CX = 4 * EMU_PER_CM   # 1440000
        TARGET_CY = 2 * EMU_PER_CM   # 720000

        correct_size = sum(
            1 for s in rects
            if abs(s['cx'] - TARGET_CX) <= SIZE_TOLERANCE and abs(s['cy'] - TARGET_CY) <= SIZE_TOLERANCE
        )

        if correct_size == 3:
            print("PASS: Component 4 — All 3 rectangles have correct dimensions 4cm x 2cm (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 4 — Only %d/3 rectangles have correct dimensions (target: %d x %d EMU)" % (
                correct_size, TARGET_CX, TARGET_CY))
            for s in rects:
                print("  Rect %s: cx=%d (%.2fcm), cy=%d (%.2fcm)" % (
                    s['name'], s['cx'], s['cx']/EMU_PER_CM, s['cy'], s['cy']/EMU_PER_CM))
    except Exception as e:
        print("ERROR: Component 4 — %s" % e)

    # -------------------------------------------------------------------------
    # Component 5: All shapes positioned at approximately Y=10cm — 0.15 points
    # Rectangles should have posV = 10cm = 3600000 EMU (±0.5cm)
    # Arrows should be vertically centered (posV near 10cm ± 1cm acceptable)
    # -------------------------------------------------------------------------
    try:
        TARGET_RECT_V = 10 * EMU_PER_CM  # 3600000
        V_TOLERANCE = TOLERANCE_EMU       # ±0.5cm = 180000 EMU

        rects_correct_v = sum(
            1 for s in rects
            if abs(s['posV'] - TARGET_RECT_V) <= V_TOLERANCE
        )
        arrows_correct_v = sum(
            1 for s in arrows
            if abs(s['posV'] - TARGET_RECT_V) <= V_TOLERANCE * 2  # arrows may be slightly offset for centering
        )

        if rects_correct_v == 3 and arrows_correct_v == 2:
            print("PASS: Component 5 — All shapes vertically at ~Y=10cm (0.15 pts)")
            total_score += 0.15
        elif rects_correct_v == 3:
            print("PARTIAL: Component 5 — Rectangles at Y=10cm but arrows not fully aligned (0.08 pts)")
            total_score += 0.08
        else:
            print("FAIL: Component 5 — Only %d/3 rects and %d/2 arrows at correct Y position" % (
                rects_correct_v, arrows_correct_v))
            for s in shapes:
                print("  Shape %s: posV=%d (%.2fcm)" % (s['name'], s['posV'], s['posV']/EMU_PER_CM))
    except Exception as e:
        print("ERROR: Component 5 — %s" % e)

    final_score = min(total_score, 1.0)
    print("\nScore: %.2f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


# Default: test against canonical artifact path
file_path = '%s/Desktop/workflow_doc.docx' % WORKDIR
if not os.path.exists(file_path):
    print("File not found: %s" % file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)

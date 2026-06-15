"""
Reward Script: Set up four linked text boxes in a 2x2 grid on page 1
Task ID: writer_obj_072
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): 4 text boxes exist in document
  Component 2 (0.35): Text boxes have correct positions and sizes (tolerance 50000 EMU ~1.4mm)
  Component 3 (0.25): Text boxes are linked in sequence: box1->box2->box3->box4
  Component 4 (0.15): All 4 boxes have 1pt #BDBDBD border and 0.2cm padding
Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_obj_072'
FILE_PATH = os.path.join(WORKDIR, 'Desktop', 'magazine_article.docx')

# EMU conversion constants
# 1cm = 360000 EMU, 1pt = 12700 EMU
# Expected positions (EMU):
#   Box 1: x=540000 (1.5cm), y=1080000 (3cm), w=2520000 (7cm), h=2880000 (8cm)
#   Box 2: x=3600000 (10cm), y=1080000 (3cm), w=2520000, h=2880000
#   Box 3: x=540000 (1.5cm), y=5040000 (14cm), w=2520000, h=2880000
#   Box 4: x=3600000 (10cm), y=5040000 (14cm), w=2520000, h=2880000
EXPECTED_BOXES = [
    {'x': 540000,  'y': 1080000, 'cx': 2520000, 'cy': 2880000},  # Box 1
    {'x': 3600000, 'y': 1080000, 'cx': 2520000, 'cy': 2880000},  # Box 2
    {'x': 540000,  'y': 5040000, 'cx': 2520000, 'cy': 2880000},  # Box 3
    {'x': 3600000, 'y': 5040000, 'cx': 2520000, 'cy': 2880000},  # Box 4
]
POSITION_TOLERANCE = 100000  # ~2.8mm tolerance
BORDER_WIDTH = 12700         # 1pt = 12700 EMU
BORDER_COLOR = 'BDBDBD'      # target gray border color
PADDING_INSET = 72000        # 0.2cm = 72000 EMU


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
    except ImportError:
        print("CRITICAL: python-docx not installed")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print("CRITICAL: Cannot load file %s: %s" % (file_path, e))
        print("REWARD: 0.0")
        return 0.0

    # Namespaces for XML parsing
    WPS = 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape'
    WP = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
    A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

    root = doc.element

    # Extract main textboxes (exclude fallback copies)
    # Main textboxes have docPr ids 1-4; fallbacks have ids 101-104
    drawings = root.findall('.//{%s}drawing' % W)

    # Build a list of main textboxes (id < 100, has txbx element)
    main_textboxes = []
    for drawing in drawings:
        anchor = drawing.find('{%s}anchor' % WP)
        if anchor is None:
            continue
        docPr = anchor.find('{%s}docPr' % WP)
        if docPr is None:
            continue
        shape_id = docPr.get('id')
        shape_name = docPr.get('name', '')
        try:
            shape_id_int = int(shape_id)
        except (TypeError, ValueError):
            continue
        # Exclude fallback shapes (id >= 100)
        if shape_id_int >= 100:
            continue
        txbx = drawing.find('.//{%s}txbx' % WPS)
        if txbx is None:
            continue
        main_textboxes.append((shape_id_int, shape_name, drawing))

    # Sort by shape id
    main_textboxes.sort(key=lambda t: t[0])

    # -------------------------------------------------------------------------
    # Component 1: Exactly 4 text boxes exist (0.25 points)
    # -------------------------------------------------------------------------
    try:
        num_boxes = len(main_textboxes)
        if num_boxes == 4:
            print("PASS: Component 1 — found 4 main text boxes (0.25 pts)")
            total_score += 0.25
        elif num_boxes > 0:
            print("FAIL: Component 1 — expected 4 text boxes, found %d" % num_boxes)
        else:
            print("FAIL: Component 1 — no main text boxes found in document")
    except Exception as e:
        print("ERROR: Component 1 — %s" % e)

    if len(main_textboxes) < 4:
        final_score = min(total_score, 1.0)
        print("\nScore: %s/1.0" % total_score)
        print("REWARD: %s" % final_score)
        return final_score

    # -------------------------------------------------------------------------
    # Component 2: Correct positions and sizes (0.35 points)
    # -------------------------------------------------------------------------
    try:
        pos_matches = 0
        for box_idx, (shape_id, shape_name, drawing) in enumerate(main_textboxes):
            expected = EXPECTED_BOXES[box_idx]
            anchor = drawing.find('{%s}anchor' % WP)
            pos_h = anchor.find('{%s}positionH' % WP)
            pos_v = anchor.find('{%s}positionV' % WP)
            extent = anchor.find('{%s}extent' % WP)

            h_off = pos_h.find('{%s}posOffset' % WP) if pos_h is not None else None
            v_off = pos_v.find('{%s}posOffset' % WP) if pos_v is not None else None

            actual_x = int(h_off.text) if h_off is not None and h_off.text else None
            actual_y = int(v_off.text) if v_off is not None and v_off.text else None
            actual_cx = int(extent.get('cx')) if extent is not None and extent.get('cx') else None
            actual_cy = int(extent.get('cy')) if extent is not None and extent.get('cy') else None

            x_ok = actual_x is not None and abs(actual_x - expected['x']) <= POSITION_TOLERANCE
            y_ok = actual_y is not None and abs(actual_y - expected['y']) <= POSITION_TOLERANCE
            cx_ok = actual_cx is not None and abs(actual_cx - expected['cx']) <= POSITION_TOLERANCE
            cy_ok = actual_cy is not None and abs(actual_cy - expected['cy']) <= POSITION_TOLERANCE

            if x_ok and y_ok and cx_ok and cy_ok:
                pos_matches += 1
                print("PASS: Component 2 — Box %d (%s) position/size correct x=%s y=%s cx=%s cy=%s" % (
                    box_idx + 1, shape_name, actual_x, actual_y, actual_cx, actual_cy))
            else:
                print("FAIL: Component 2 — Box %d (%s) position/size mismatch" % (box_idx + 1, shape_name))
                print("  Expected: x=%d y=%d cx=%d cy=%d" % (
                    expected['x'], expected['y'], expected['cx'], expected['cy']))
                print("  Actual:   x=%s y=%s cx=%s cy=%s" % (actual_x, actual_y, actual_cx, actual_cy))

        if pos_matches > 0:
            pos_score = 0.35 * (pos_matches / 4.0)
            print("PASS: Component 2 — %d/4 boxes have correct positions/sizes (%.2f pts)" % (pos_matches, pos_score))
            total_score += pos_score
        else:
            print("FAIL: Component 2 — no boxes have correct positions/sizes (0.00 pts)")
    except Exception as e:
        print("ERROR: Component 2 — %s" % e)

    # -------------------------------------------------------------------------
    # Component 3: Textbox linking chain 1->2->3->4 (0.25 points)
    # -------------------------------------------------------------------------
    try:
        # The linking is expressed via wps:linkedTxbx elements
        # Box N has linkedTxbx with id=(N+1) and seq=(N-1) in zero-based order
        # Box 1 should have linkedTxbx id=2 seq=0
        # Box 2 should have linkedTxbx id=3 seq=1
        # Box 3 should have linkedTxbx id=4 seq=2
        # Box 4 is the last, no linkedTxbx (or it's the terminal)
        link_checks_passed = 0

        # Expected links: boxes 0,1,2 each link to next box by shape id
        # main_textboxes[i] = (shape_id, shape_name, drawing)
        shape_ids = [t[0] for t in main_textboxes]

        for i in range(3):
            shape_id, shape_name, drawing = main_textboxes[i]
            linkedTxbx = drawing.find('.//{%s}linkedTxbx' % WPS)
            next_shape_id = shape_ids[i + 1]

            if linkedTxbx is not None:
                link_id = linkedTxbx.get('id')
                link_seq = linkedTxbx.get('seq')
                if link_id is not None and int(link_id) == next_shape_id:
                    print("PASS: Component 3 — Box %d links to Box %d (id=%s seq=%s)" % (
                        i + 1, i + 2, link_id, link_seq))
                    link_checks_passed += 1
                else:
                    print("FAIL: Component 3 — Box %d linkedTxbx id=%s, expected %d" % (
                        i + 1, link_id, next_shape_id))
            else:
                print("FAIL: Component 3 — Box %d (%s) has no linkedTxbx element (expected link to Box %d)" % (
                    i + 1, shape_name, i + 2))

        if link_checks_passed > 0:
            link_score = 0.25 * (link_checks_passed / 3.0)
            print("PASS: Component 3 — %d/3 required links present (%.2f pts)" % (link_checks_passed, link_score))
            total_score += link_score
        else:
            print("FAIL: Component 3 — no required links found (0.00 pts)")
    except Exception as e:
        print("ERROR: Component 3 — %s" % e)

    # -------------------------------------------------------------------------
    # Component 4: All 4 boxes have 1pt #BDBDBD border and 0.2cm padding (0.15 points)
    # -------------------------------------------------------------------------
    try:
        border_padding_ok = 0
        for box_idx, (shape_id, shape_name, drawing) in enumerate(main_textboxes):
            spPr = drawing.find('.//{%s}spPr' % WPS)
            bodyPr = drawing.find('.//{%s}bodyPr' % WPS)

            border_ok = False
            padding_ok = False

            if spPr is not None:
                ln = spPr.find('.//{%s}ln' % A)
                if ln is not None:
                    border_w = ln.get('w')
                    solidFill = ln.find('{%s}solidFill' % A)
                    color_ok = False
                    if solidFill is not None:
                        srgbClr = solidFill.find('{%s}srgbClr' % A)
                        if srgbClr is not None:
                            color_val = srgbClr.get('val', '').upper()
                            color_ok = color_val == BORDER_COLOR.upper()
                    border_w_ok = (border_w is not None and abs(int(border_w) - BORDER_WIDTH) <= 1270)
                    border_ok = border_w_ok and color_ok

            if bodyPr is not None:
                l_ins = bodyPr.get('lIns')
                t_ins = bodyPr.get('tIns')
                r_ins = bodyPr.get('rIns')
                b_ins = bodyPr.get('bIns')
                if all(v is not None for v in [l_ins, t_ins, r_ins, b_ins]):
                    padding_ok = all(
                        abs(int(v) - PADDING_INSET) <= 7200
                        for v in [l_ins, t_ins, r_ins, b_ins]
                    )

            if border_ok and padding_ok:
                border_padding_ok += 1
                print("PASS: Component 4 — Box %d border and padding correct" % (box_idx + 1))
            else:
                issues = []
                if not border_ok:
                    if spPr is not None:
                        ln = spPr.find('.//{%s}ln' % A)
                        if ln is not None:
                            print("  Box %d border line w=%s" % (box_idx+1, ln.get('w')))
                            sf = ln.find('{%s}solidFill' % A)
                            if sf is not None:
                                sc = sf.find('{%s}srgbClr' % A)
                                if sc is not None:
                                    print("  Box %d border color %s (expected %s)" % (
                                        box_idx+1, sc.get('val'), BORDER_COLOR))
                    issues.append('border')
                if not padding_ok:
                    issues.append('padding')
                print("FAIL: Component 4 — Box %d issues: %s" % (box_idx + 1, ', '.join(issues)))

        if border_padding_ok > 0:
            bp_score = 0.15 * (border_padding_ok / 4.0)
            print("PASS: Component 4 — %d/4 boxes have correct border+padding (%.2f pts)" % (border_padding_ok, bp_score))
            total_score += bp_score
        else:
            print("FAIL: Component 4 — no boxes have correct border+padding (0.00 pts)")
    except Exception as e:
        print("ERROR: Component 4 — %s" % e)

    final_score = min(total_score, 1.0)
    print("\nScore: %.4f/1.0" % total_score)
    print("REWARD: %.4f" % final_score)
    return final_score


if not os.path.exists(FILE_PATH):
    print("File not found: %s" % FILE_PATH)
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

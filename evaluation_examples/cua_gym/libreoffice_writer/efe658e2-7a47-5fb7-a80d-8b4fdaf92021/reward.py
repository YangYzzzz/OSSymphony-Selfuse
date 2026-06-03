"""
Reward Script: Arrange four shapes into a 2x2 grid layout in a Writer document
Task ID: writer_obj_058
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): All 4 shapes are exactly 6cm x 4cm
  Component 2 (0.3): Left column at same X and right column at same X; top row at same Y and bottom row at same Y; rows/cols properly ordered
  Component 3 (0.2): Exact grid positions match: red at (2cm, 5cm), blue at (9cm, 5cm), green at (2cm, 10cm), yellow at (9cm, 10cm)
  Component 4 (0.1): 1cm horizontal and vertical spacing between shapes
"""

import os

# python-docx for reading .docx files
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_obj_058'

# EMU conversion
CM_TO_EMU = 360000
# Tolerance for position/size comparisons in EMU (0.5cm)
TOLERANCE_EMU = int(0.5 * CM_TO_EMU)

WP_NS = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'

# Expected colors (lowercase hex)
KNOWN_COLORS = {'f44336', '1565c0', '4caf50', 'ffc107'}

# Expected dimensions
EXPECTED_WIDTH_EMU = int(6.0 * CM_TO_EMU)   # 6cm
EXPECTED_HEIGHT_EMU = int(4.0 * CM_TO_EMU)  # 4cm

# Expected positions (from task context - golden file values)
EXPECTED_POSITIONS = {
    'f44336': {'pos_h': int(2.0 * CM_TO_EMU), 'pos_v': int(5.0 * CM_TO_EMU)},   # red: top-left
    '1565c0': {'pos_h': int(9.0 * CM_TO_EMU), 'pos_v': int(5.0 * CM_TO_EMU)},   # blue: top-right
    '4caf50': {'pos_h': int(2.0 * CM_TO_EMU), 'pos_v': int(10.0 * CM_TO_EMU)},  # green: bottom-left
    'ffc107': {'pos_h': int(9.0 * CM_TO_EMU), 'pos_v': int(10.0 * CM_TO_EMU)},  # yellow: bottom-right
}

# Expected spacing
EXPECTED_GAP_EMU = int(1.0 * CM_TO_EMU)  # 1cm gap


def get_shape_data(doc):
    """
    Extract shape data from all anchored drawings in the document.
    Returns a list of dicts with keys: pos_h, pos_v, width, height, color (all in EMU)
    """
    body = doc.element.body
    shapes = body.findall('.//{%s}anchor' % WP_NS)
    result = []
    for shape in shapes:
        pos_h_elem = shape.find('{%s}positionH/{%s}posOffset' % (WP_NS, WP_NS))
        pos_v_elem = shape.find('{%s}positionV/{%s}posOffset' % (WP_NS, WP_NS))
        extent = shape.find('{%s}extent' % WP_NS)

        pos_h = int(pos_h_elem.text) if pos_h_elem is not None else None
        pos_v = int(pos_v_elem.text) if pos_v_elem is not None else None
        width = int(extent.get('cx')) if extent is not None else None
        height = int(extent.get('cy')) if extent is not None else None

        # Get fill color
        color = None
        solid_fill = shape.find('.//{%s}solidFill' % A_NS)
        if solid_fill is not None:
            srgb = solid_fill.find('{%s}srgbClr' % A_NS)
            if srgb is not None:
                color = srgb.get('val', '').lower()

        result.append({
            'pos_h': pos_h,
            'pos_v': pos_v,
            'width': width,
            'height': height,
            'color': color,
        })
    return result


def within_tolerance(actual, expected, tolerance):
    """Check if actual value is within tolerance of expected value."""
    return abs(actual - expected) <= tolerance


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document
    try:
        doc = Document(file_path)
    except Exception as e:
        print("CRITICAL: Cannot load file %s: %s" % (file_path, e))
        print("REWARD: 0.0")
        return 0.0

    # Extract shape data
    try:
        shapes = get_shape_data(doc)
    except Exception as e:
        print("CRITICAL: Cannot extract shape data: %s" % e)
        print("REWARD: 0.0")
        return 0.0

    if len(shapes) != 4:
        print("CRITICAL: Expected 4 shapes, found %d" % len(shapes))
        print("REWARD: 0.0")
        return 0.0

    print("Found %d shapes" % len(shapes))
    for i, s in enumerate(shapes):
        h_cm = s['pos_h'] / CM_TO_EMU if s['pos_h'] is not None else None
        v_cm = s['pos_v'] / CM_TO_EMU if s['pos_v'] is not None else None
        w_cm = s['width'] / CM_TO_EMU if s['width'] is not None else None
        ht_cm = s['height'] / CM_TO_EMU if s['height'] is not None else None
        print("  Shape %d: color=%s pos=(%.2f, %.2f)cm size=(%.2f x %.2f)cm" % (
            i+1, s['color'], h_cm or 0, v_cm or 0, w_cm or 0, ht_cm or 0))

    # Build color->shape map for targeted checks
    color_to_shape = {}
    for s in shapes:
        if s['color'] in KNOWN_COLORS:
            color_to_shape[s['color']] = s

    # -------------------------------------------------------------------------
    # Component 1: All 4 shapes are exactly 6cm x 4cm (0.4 points)
    # FAILS on initial (shapes are 8x3, 5x5, 7x2.5, 4x6) → PASSES on golden (all 6x4)
    # -------------------------------------------------------------------------
    try:
        size_failures = []
        size_details = []
        for i, s in enumerate(shapes):
            w_ok = s['width'] is not None and within_tolerance(s['width'], EXPECTED_WIDTH_EMU, TOLERANCE_EMU)
            h_ok = s['height'] is not None and within_tolerance(s['height'], EXPECTED_HEIGHT_EMU, TOLERANCE_EMU)
            w_cm = s['width'] / CM_TO_EMU if s['width'] else 0
            h_cm = s['height'] / CM_TO_EMU if s['height'] else 0
            size_details.append("shape%d(%.2fx%.2fcm)" % (i+1, w_cm, h_cm))
            if not (w_ok and h_ok):
                size_failures.append("shape%d" % (i+1))

        if len(size_failures) == 0:
            print("PASS: Component 1 — All 4 shapes are 6cm x 4cm: %s (0.4 pts)" % ', '.join(size_details))
            total_score += 0.4
        else:
            print("FAIL: Component 1 — Expected all shapes to be 6cm x 4cm, found: %s" % ', '.join(size_details))
    except Exception as e:
        print("ERROR: Component 1 — %s" % e)

    # -------------------------------------------------------------------------
    # Component 2: Correct 2x2 grid arrangement (0.3 points)
    # Left column shapes share same X, right column share same X,
    # top row shapes share same Y, bottom row shapes share same Y.
    # FAILS on initial (shapes at different X/Y) → PASSES on golden
    # -------------------------------------------------------------------------
    try:
        red = color_to_shape.get('f44336')
        blue = color_to_shape.get('1565c0')
        green = color_to_shape.get('4caf50')
        yellow = color_to_shape.get('ffc107')

        if not all([red, blue, green, yellow]):
            print("FAIL: Component 2 — Could not identify all 4 colored shapes by color")
        else:
            # Top row (red + blue) should share same Y
            top_y_match = within_tolerance(red['pos_v'], blue['pos_v'], TOLERANCE_EMU)
            # Bottom row (green + yellow) should share same Y
            bottom_y_match = within_tolerance(green['pos_v'], yellow['pos_v'], TOLERANCE_EMU)
            # Left column (red + green) should share same X
            left_x_match = within_tolerance(red['pos_h'], green['pos_h'], TOLERANCE_EMU)
            # Right column (blue + yellow) should share same X
            right_x_match = within_tolerance(blue['pos_h'], yellow['pos_h'], TOLERANCE_EMU)
            # Bottom row Y must be greater than top row Y
            rows_ordered = green['pos_v'] > red['pos_v']
            # Right column X must be greater than left column X
            cols_ordered = blue['pos_h'] > red['pos_h']

            grid_ok = (top_y_match and bottom_y_match and left_x_match and
                       right_x_match and rows_ordered and cols_ordered)

            if grid_ok:
                print("PASS: Component 2 — 2x2 grid layout correct: top_y_match=%s, bottom_y_match=%s, left_x_match=%s, right_x_match=%s (0.3 pts)" % (
                    top_y_match, bottom_y_match, left_x_match, right_x_match))
                total_score += 0.3
            else:
                print("FAIL: Component 2 — Grid layout incorrect: top_y_match=%s, bottom_y_match=%s, left_x_match=%s, right_x_match=%s, rows_ordered=%s, cols_ordered=%s" % (
                    top_y_match, bottom_y_match, left_x_match, right_x_match, rows_ordered, cols_ordered))
    except Exception as e:
        print("ERROR: Component 2 — %s" % e)

    # -------------------------------------------------------------------------
    # Component 3: Exact grid positions (0.2 points)
    # red at (2cm, 5cm), blue at (9cm, 5cm), green at (2cm, 10cm), yellow at (9cm, 10cm)
    # FAILS on initial (different positions: red@3,4; blue@11,3; green@4,12; yellow@10,14)
    # PASSES on golden (exact positions match)
    # -------------------------------------------------------------------------
    try:
        pos_failures = []
        pos_details = []
        for color_hex, expected_pos in EXPECTED_POSITIONS.items():
            shape = color_to_shape.get(color_hex)
            if shape is None:
                pos_failures.append("color %s: not found" % color_hex)
                continue
            h_ok = within_tolerance(shape['pos_h'], expected_pos['pos_h'], TOLERANCE_EMU)
            v_ok = within_tolerance(shape['pos_v'], expected_pos['pos_v'], TOLERANCE_EMU)
            actual_h_cm = shape['pos_h'] / CM_TO_EMU
            actual_v_cm = shape['pos_v'] / CM_TO_EMU
            exp_h_cm = expected_pos['pos_h'] / CM_TO_EMU
            exp_v_cm = expected_pos['pos_v'] / CM_TO_EMU
            if h_ok and v_ok:
                pos_details.append("%s@(%.1f,%.1f)cm OK" % (color_hex, actual_h_cm, actual_v_cm))
            else:
                pos_failures.append("%s@(%.1f,%.1f)cm expected(%.1f,%.1f)cm" % (
                    color_hex, actual_h_cm, actual_v_cm, exp_h_cm, exp_v_cm))

        if len(pos_failures) == 0:
            print("PASS: Component 3 — All shape positions correct: %s (0.2 pts)" % ', '.join(pos_details))
            total_score += 0.2
        else:
            print("FAIL: Component 3 — Position check failures: %s" % ', '.join(pos_failures))
    except Exception as e:
        print("ERROR: Component 3 — %s" % e)

    # -------------------------------------------------------------------------
    # Component 4: 1cm spacing between shapes (0.1 points)
    # Horizontal gap between left and right columns = 1cm
    # Vertical gap between top and bottom rows = 1cm
    # FAILS on initial (different spacing) → PASSES on golden
    # -------------------------------------------------------------------------
    try:
        red = color_to_shape.get('f44336')
        blue = color_to_shape.get('1565c0')
        green = color_to_shape.get('4caf50')

        if not all([red, blue, green]):
            print("FAIL: Component 4 — Could not identify shapes by color for spacing check")
        else:
            # Horizontal gap = right_col_x - (left_col_x + shape_width)
            h_gap_emu = blue['pos_h'] - (red['pos_h'] + red['width'])
            h_gap_cm = h_gap_emu / CM_TO_EMU
            h_gap_ok = within_tolerance(h_gap_emu, EXPECTED_GAP_EMU, TOLERANCE_EMU)

            # Vertical gap = bottom_row_y - (top_row_y + shape_height)
            v_gap_emu = green['pos_v'] - (red['pos_v'] + red['height'])
            v_gap_cm = v_gap_emu / CM_TO_EMU
            v_gap_ok = within_tolerance(v_gap_emu, EXPECTED_GAP_EMU, TOLERANCE_EMU)

            if h_gap_ok and v_gap_ok:
                print("PASS: Component 4 — Spacing correct: h_gap=%.2fcm, v_gap=%.2fcm (0.1 pts)" % (h_gap_cm, v_gap_cm))
                total_score += 0.1
            else:
                print("FAIL: Component 4 — Spacing incorrect: h_gap=%.2fcm (expected ~1cm), v_gap=%.2fcm (expected ~1cm)" % (h_gap_cm, v_gap_cm))
    except Exception as e:
        print("ERROR: Component 4 — %s" % e)

    final_score = min(total_score, 1.0)
    print("\nScore: %.1f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


# Default: test against canonical artifact path in the VM environment
file_path = '%s/Desktop/color_grid.docx' % WORKDIR
if not os.path.exists(file_path):
    print("File not found: %s" % file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)

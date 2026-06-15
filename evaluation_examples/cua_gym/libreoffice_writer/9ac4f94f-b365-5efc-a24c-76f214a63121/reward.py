"""
Reward Script: Set image text wrap to 'Through' mode with 0.5 cm spacing
Task ID: writer_fs_026
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.25): Image is anchored (not inline)
  - Component 2 (0.35): Wrap type is wrapThrough
  - Component 3 (0.25): Spacing is 0.5 cm (180000 EMU) on all four sides
  - Component 4 (0.15): wrapText attribute is "bothSides"
"""

import os
from docx import Document
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_026'

# Namespace map for XML queries
NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
}

# 0.5 cm in EMU (1 cm = 360000 EMU)
EXPECTED_SPACING_EMU = 180000
# Tolerance: +/- 10000 EMU (~0.028 cm) for rounding
SPACING_TOLERANCE = 10000


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

    # Find all drawing elements in the document body
    body = doc.element.body
    drawings = body.findall('.//w:drawing', NS)

    if len(drawings) == 0:
        print("FAIL: No drawing/image elements found in the document")
        print("REWARD: 0.0")
        return 0.0

    # We expect exactly one image on page 1
    drawing = drawings[0]

    # Component 1: Image is anchored (not inline) — 0.25 points
    # Initial state has wp:inline; golden state should have wp:anchor
    try:
        anchors = drawing.findall('.//wp:anchor', NS)
        inlines = drawing.findall('.//wp:inline', NS)
        if len(anchors) > 0:
            print(f"PASS: Component 1 — Image is anchored (found {len(anchors)} anchor element(s)) (0.25 pts)")
            total_score += 0.25
        else:
            if len(inlines) > 0:
                print("FAIL: Component 1 — Image is still inline (not anchored)")
            else:
                print("FAIL: Component 1 — No anchor or inline element found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If not anchored, remaining checks cannot pass
    if total_score < 0.25:
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    anchor = drawing.findall('.//wp:anchor', NS)[0]

    # Component 2: Wrap type is wrapThrough — 0.35 points
    # This is the key "Through" wrap mode element
    try:
        wrap_through = anchor.findall('wp:wrapThrough', NS)
        wrap_tight = anchor.findall('wp:wrapTight', NS)
        wrap_square = anchor.findall('wp:wrapSquare', NS)
        wrap_none = anchor.findall('wp:wrapNone', NS)
        wrap_top_bottom = anchor.findall('wp:wrapTopAndBottom', NS)

        if len(wrap_through) > 0:
            print(f"PASS: Component 2 — Wrap type is wrapThrough (0.35 pts)")
            total_score += 0.35
        else:
            found_types = []
            if wrap_tight:
                found_types.append("wrapTight")
            if wrap_square:
                found_types.append("wrapSquare")
            if wrap_none:
                found_types.append("wrapNone")
            if wrap_top_bottom:
                found_types.append("wrapTopAndBottom")
            print(f"FAIL: Component 2 — Expected wrapThrough, found: {found_types if found_types else 'unknown'}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Spacing is 0.5 cm (180000 EMU) on all four sides — 0.25 points
    # distT, distB, distL, distR attributes on the anchor element
    try:
        dist_t = int(anchor.get('distT', '0'))
        dist_b = int(anchor.get('distB', '0'))
        dist_l = int(anchor.get('distL', '0'))
        dist_r = int(anchor.get('distR', '0'))

        spacing_vals = [('distT', dist_t), ('distB', dist_b), ('distL', dist_l), ('distR', dist_r)]
        bad_sides = [(name, val) for name, val in spacing_vals if abs(val - EXPECTED_SPACING_EMU) > SPACING_TOLERANCE]
        for name, val in bad_sides:
            print(f"  {name}: {val} EMU (expected ~{EXPECTED_SPACING_EMU}, diff={abs(val - EXPECTED_SPACING_EMU)})")

        if len(bad_sides) == 0:
            print(f"PASS: Component 3 — All spacing is ~0.5 cm (T={dist_t}, B={dist_b}, L={dist_l}, R={dist_r} EMU) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Spacing not 0.5 cm on {len(bad_sides)} side(s) (T={dist_t}, B={dist_b}, L={dist_l}, R={dist_r} EMU)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: wrapText attribute is "bothSides" — 0.15 points
    try:
        wrap_through_elems = anchor.findall('wp:wrapThrough', NS)
        if wrap_through_elems:
            wrap_text_val = wrap_through_elems[0].get('wrapText', '')
            if wrap_text_val == 'bothSides':
                print(f"PASS: Component 4 — wrapText is 'bothSides' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — wrapText is '{wrap_text_val}', expected 'bothSides'")
        else:
            print("FAIL: Component 4 — No wrapThrough element to check wrapText attribute")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook for LibreOffice Writer
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)

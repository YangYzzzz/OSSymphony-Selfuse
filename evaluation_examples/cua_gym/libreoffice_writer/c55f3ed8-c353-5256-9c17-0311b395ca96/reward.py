"""
Reward Script: Insert numbered circles with arrows in steps_doc.docx
Task ID: writer_obj_064
Domain: libreoffice_writer
Scoring:
  Component 1: Three ellipse (circle) shapes present with correct size (0.30 pts)
  Component 2: Circle fill colors match #2E7D32, #1565C0, #E65100 (0.30 pts)
  Component 3: Circle text ('1','2','3') with white 20pt bold font (0.20 pts)
  Component 4: Two right-pointing arrows between circles (0.20 pts)
Total: 1.0
"""

import os
import re
from docx import Document
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_obj_064'
FILE_PATH = f'{WORKDIR}/steps_doc.docx'

# EMU conversion constants
EMU_PER_CM = 360000
TOLERANCE_EMU = 180000  # 0.5cm tolerance for positions

# Expected values derived from task requirements + page margin (3.175cm left margin)
EXPECTED_CIRCLES = [
    {'fill': '2E7D32', 'text': '1', 'x_emu': 2223000, 'y_emu': 3074400},
    {'fill': '1565C0', 'text': '2', 'x_emu': 4023000, 'y_emu': 3074400},
    {'fill': 'E65100', 'text': '3', 'x_emu': 5823000, 'y_emu': 3074400},
]
EXPECTED_CIRCLE_SIZE_EMU = 1080000   # 3cm diameter
EXPECTED_FONT_SIZE_HALFPT = 40       # 20pt = 40 half-points
EXPECTED_TEXT_COLOR = 'FFFFFF'       # white


def color_distance(hex1, hex2):
    """Compute Euclidean RGB distance between two hex color strings."""
    r1, g1, b1 = int(hex1[0:2], 16), int(hex1[2:4], 16), int(hex1[4:6], 16)
    r2, g2, b2 = int(hex2[0:2], 16), int(hex2[2:4], 16), int(hex2[4:6], 16)
    import math
    return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)


def verify_task(file_path):
    """
    Verify that the task was completed: 3 numbered circles with arrows inserted.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all drawing elements from body
    try:
        body = doc.element.body
        ns_w = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        all_drawings = body.findall(f'.//{{{ns_w}}}drawing')
        print(f"INFO: Found {len(all_drawings)} drawing element(s) in document.")
    except Exception as e:
        print(f"CRITICAL: Cannot parse drawing elements: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Identify circles (ellipse) and arrows (rightArrow)
    circles = []
    arrows = []
    for d in all_drawings:
        try:
            xml_str = etree.tostring(d, pretty_print=False).decode()
            shape_types = re.findall(r'prst="([^"]+)"', xml_str)
            if shape_types:
                stype = shape_types[0]
                if stype == 'ellipse':
                    circles.append(xml_str)
                elif 'Arrow' in stype or 'arrow' in stype:
                    arrows.append(xml_str)
        except Exception as e:
            print(f"WARN: Could not parse drawing: {e}")

    print(f"INFO: Ellipse circles found: {len(circles)}, Arrow shapes found: {len(arrows)}")

    # ------------------------------------------------------------------
    # Component 1: Three circles (ellipses) present with correct size (0.30 pts)
    # ------------------------------------------------------------------
    try:
        if len(circles) == 3:
            # Verify each circle has correct size (3cm = 1080000 EMU)
            all_correct_size = True
            for idx, c_xml in enumerate(circles):
                ext_matches = re.findall(r'<a:ext cx="(\d+)" cy="(\d+)"', c_xml)
                if ext_matches:
                    cx = int(ext_matches[0][0])
                    cy = int(ext_matches[0][1])
                    if abs(cx - EXPECTED_CIRCLE_SIZE_EMU) > TOLERANCE_EMU or abs(cy - EXPECTED_CIRCLE_SIZE_EMU) > TOLERANCE_EMU:
                        all_correct_size = False
                        print(f"FAIL: Component 1 — Circle[{idx}] size {cx}x{cy} EMU, expected ~{EXPECTED_CIRCLE_SIZE_EMU}")
                else:
                    all_correct_size = False
                    print(f"FAIL: Component 1 — Circle[{idx}] has no extent element")

            if all_correct_size:
                print(f"PASS: Component 1 — 3 ellipse circles with correct 3cm size (0.30 pts)")
                total_score += 0.30
            else:
                # Partial: circles exist but wrong size — give partial
                print(f"PARTIAL: Component 1 — 3 circles present but size mismatch (0.15 pts)")
                total_score += 0.15
        elif len(circles) > 0:
            print(f"FAIL: Component 1 — Expected 3 circles, found {len(circles)}")
        else:
            print(f"FAIL: Component 1 — No circles found (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ------------------------------------------------------------------
    # Component 2: Circle fill colors match expected values (0.30 pts)
    # #2E7D32 (green), #1565C0 (blue), #E65100 (orange)
    # ------------------------------------------------------------------
    try:
        if len(circles) == 3:
            expected_colors = ['2E7D32', '1565C0', 'E65100']
            color_matches = 0
            for idx, c_xml in enumerate(circles):
                fills = re.findall(r'<a:srgbClr val="([A-Fa-f0-9]+)"', c_xml)
                if fills:
                    actual_color = fills[0].upper()
                    expected_color = expected_colors[idx].upper()
                    dist = color_distance(actual_color, expected_color)
                    if dist < 30:
                        color_matches += 1
                        print(f"PASS: Circle[{idx}] fill #{actual_color} matches #{expected_color} (dist={dist:.1f})")
                    else:
                        print(f"FAIL: Circle[{idx}] fill #{actual_color}, expected #{expected_color} (dist={dist:.1f})")
                else:
                    print(f"FAIL: Circle[{idx}] has no solid fill color")

            if color_matches == 3:
                print(f"PASS: Component 2 — All 3 circle fill colors correct (0.30 pts)")
                total_score += 0.30
            elif color_matches == 2:
                print(f"PARTIAL: Component 2 — 2/3 colors correct (0.15 pts)")
                total_score += 0.15
            elif color_matches == 1:
                print(f"PARTIAL: Component 2 — 1/3 colors correct (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 2 — No correct fill colors (0.0 pts)")
        else:
            print(f"FAIL: Component 2 — Cannot verify colors, wrong circle count ({len(circles)})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ------------------------------------------------------------------
    # Component 3: Circle text ('1','2','3') with white 20pt bold font (0.20 pts)
    # ------------------------------------------------------------------
    try:
        if len(circles) == 3:
            expected_texts = ['1', '2', '3']
            text_checks_passed = 0
            for idx, c_xml in enumerate(circles):
                # Extract w:t text
                texts = re.findall(r'<w:t[^>]*>([^<]+)</w:t>', c_xml)
                text_val = texts[0].strip() if texts else ''

                # Text color (white = FFFFFF)
                text_colors = re.findall(r'<w:color w:val="([^"]+)"', c_xml)
                text_color = text_colors[0].upper() if text_colors else ''

                # Font size
                font_sz_list = re.findall(r'<w:sz w:val="(\d+)"', c_xml)
                font_sz = int(font_sz_list[0]) if font_sz_list else 0

                # Bold
                is_bold = '<w:b/>' in c_xml or '<w:b ' in c_xml

                text_ok = (text_val == expected_texts[idx])
                color_ok = (text_color == EXPECTED_TEXT_COLOR)
                size_ok = (font_sz == EXPECTED_FONT_SIZE_HALFPT)

                if text_ok and color_ok and size_ok and is_bold:
                    text_checks_passed += 1
                    print(f"PASS: Circle[{idx}] text='{text_val}', color=#{text_color}, size={font_sz/2}pt, bold={is_bold}")
                else:
                    reasons = []
                    if not text_ok:
                        reasons.append(f"text='{text_val}' (expected '{expected_texts[idx]}')")
                    if not color_ok:
                        reasons.append(f"color=#{text_color} (expected #FFFFFF)")
                    if not size_ok:
                        reasons.append(f"size={font_sz/2}pt (expected 20pt)")
                    if not is_bold:
                        reasons.append("not bold")
                    print(f"FAIL: Circle[{idx}] text check: {', '.join(reasons)}")

            if text_checks_passed == 3:
                print(f"PASS: Component 3 — All 3 circles have correct text (0.20 pts)")
                total_score += 0.20
            elif text_checks_passed == 2:
                print(f"PARTIAL: Component 3 — 2/3 circles have correct text (0.13 pts)")
                total_score += 0.13
            elif text_checks_passed == 1:
                print(f"PARTIAL: Component 3 — 1/3 circles have correct text (0.07 pts)")
                total_score += 0.07
            else:
                print(f"FAIL: Component 3 — No circles with correct text (0.0 pts)")
        else:
            print(f"FAIL: Component 3 — Cannot verify text, wrong circle count ({len(circles)})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ------------------------------------------------------------------
    # Component 4: Two right-pointing arrows between circles (0.20 pts)
    # ------------------------------------------------------------------
    try:
        right_arrows = [a for a in arrows if 'rightArrow' in a]
        print(f"INFO: rightArrow shapes found: {len(right_arrows)}")

        if len(right_arrows) >= 2:
            print(f"PASS: Component 4 — {len(right_arrows)} right-pointing arrows found (0.20 pts)")
            total_score += 0.20
        elif len(right_arrows) == 1:
            print(f"PARTIAL: Component 4 — Only 1 right-pointing arrow found (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — No right-pointing arrows found (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Final score
    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

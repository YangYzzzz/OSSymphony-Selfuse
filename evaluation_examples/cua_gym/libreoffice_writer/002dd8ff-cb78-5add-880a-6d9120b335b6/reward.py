"""
Reward Script: Insert decorative page border on all four sides
Task ID: writer_fs_043
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): pgBorders element exists with all 4 sides
  Component 2 (0.3): Border style is double-line on all sides
  Component 3 (0.2): Border width is 3 pt (sz=24) and color is navy #000080
  Component 4 (0.2): Border spacing ~1 cm from page edge on all sides
"""

import os
from docx import Document
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_043'

WML_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WML_NS}

SIDES = ['top', 'left', 'bottom', 'right']


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

    # Get section properties
    section = doc.sections[0]
    sectPr = section._sectPr
    pgBorders_list = sectPr.findall('.//w:pgBorders', NS)

    # Component 1: pgBorders element exists with all 4 sides (0.3 points)
    try:
        if not pgBorders_list:
            print("FAIL: Component 1 -- no pgBorders element found")
        else:
            pgBorders = pgBorders_list[0]
            found_sides = []
            for side in SIDES:
                elem = pgBorders.find('w:%s' % side, NS)
                if elem is not None:
                    found_sides.append(side)

            if len(found_sides) == 4:
                print("PASS: Component 1 -- pgBorders with all 4 sides present (0.3 pts)")
                total_score += 0.3
            else:
                print("FAIL: Component 1 -- only %d/4 sides found: %s" % (len(found_sides), found_sides))
    except Exception as e:
        print("ERROR: Component 1 -- %s" % e)

    # Component 2: Border style is double-line on all sides (0.3 points)
    try:
        if not pgBorders_list:
            print("FAIL: Component 2 -- no pgBorders element")
        else:
            pgBorders = pgBorders_list[0]
            double_sides = 0
            for side in SIDES:
                elem = pgBorders.find('w:%s' % side, NS)
                if elem is not None:
                    val = elem.get('{%s}val' % WML_NS)
                    if val == 'double':
                        double_sides += 1
                    else:
                        print("FAIL: Component 2 -- %s border val='%s', expected 'double'" % (side, val))

            if double_sides == 4:
                print("PASS: Component 2 -- all 4 sides have double-line style (0.3 pts)")
                total_score += 0.3
            elif double_sides > 0:
                partial = 0.3 * double_sides / 4.0
                print("PARTIAL: Component 2 -- %d/4 sides double-line (%.2f pts)" % (double_sides, partial))
                total_score += partial
            else:
                print("FAIL: Component 2 -- no sides have double-line style")
    except Exception as e:
        print("ERROR: Component 2 -- %s" % e)

    # Component 3: Border width ~3pt (sz=24) and color #000080 on all sides (0.2 points)
    try:
        if not pgBorders_list:
            print("FAIL: Component 3 -- no pgBorders element")
        else:
            pgBorders = pgBorders_list[0]
            correct_sides = 0
            for side in SIDES:
                elem = pgBorders.find('w:%s' % side, NS)
                if elem is not None:
                    sz = elem.get('{%s}sz' % WML_NS)
                    color = elem.get('{%s}color' % WML_NS)
                    # sz is in eighths of a point; 3pt = 24
                    sz_ok = sz is not None and int(sz) == 24
                    color_ok = color is not None and color.upper() == '000080'
                    if sz_ok and color_ok:
                        correct_sides += 1
                    else:
                        print("FAIL: Component 3 -- %s: sz=%s (expect 24), color=%s (expect 000080)" % (side, sz, color))

            if correct_sides == 4:
                print("PASS: Component 3 -- all 4 sides have sz=24 (3pt) and color=000080 (0.2 pts)")
                total_score += 0.2
            elif correct_sides > 0:
                partial = 0.2 * correct_sides / 4.0
                print("PARTIAL: Component 3 -- %d/4 sides correct (%.2f pts)" % (correct_sides, partial))
                total_score += partial
            else:
                print("FAIL: Component 3 -- no sides have correct width and color")
    except Exception as e:
        print("ERROR: Component 3 -- %s" % e)

    # Component 4: Border spacing ~1cm from page edge on all sides (0.2 points)
    # 1 cm = 28.35 pt; accept 24-32 range (inclusive tolerance)
    try:
        if not pgBorders_list:
            print("FAIL: Component 4 -- no pgBorders element")
        else:
            pgBorders = pgBorders_list[0]
            correct_sides = 0
            for side in SIDES:
                elem = pgBorders.find('w:%s' % side, NS)
                if elem is not None:
                    space = elem.get('{%s}space' % WML_NS)
                    if space is not None:
                        space_val = int(space)
                        # 1cm ~ 28.35pt, accept 24-32
                        if 24 <= space_val <= 32:
                            correct_sides += 1
                        else:
                            print("FAIL: Component 4 -- %s: space=%s pt, expected ~28 (1cm)" % (side, space))
                    else:
                        print("FAIL: Component 4 -- %s: no space attribute" % side)

            if correct_sides == 4:
                print("PASS: Component 4 -- all 4 sides have ~1cm spacing from page edge (0.2 pts)")
                total_score += 0.2
            elif correct_sides > 0:
                partial = 0.2 * correct_sides / 4.0
                print("PARTIAL: Component 4 -- %d/4 sides correct (%.2f pts)" % (correct_sides, partial))
                total_score += partial
            else:
                print("FAIL: Component 4 -- no sides have correct spacing")
    except Exception as e:
        print("ERROR: Component 4 -- %s" % e)

    final_score = min(total_score, 1.0)
    print("")
    print("Score: %.1f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


# Entry point
file_path = '%s/%s.docx' % (WORKDIR, TASK_ID)
if not os.path.exists(file_path):
    print("File not found: %s" % file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)

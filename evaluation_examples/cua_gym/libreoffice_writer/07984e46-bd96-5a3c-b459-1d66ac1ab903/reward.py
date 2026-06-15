"""
Reward Script: Modify footnote anchor style (blue, bold, 11pt)
Task ID: writer_bs_039
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): Bold enabled in Footnote Reference style
  Component 2 (0.30): Blue font color (#0000FF) in Footnote Reference style
  Component 3 (0.25): Font size 11pt (sz val=22) in Footnote Reference style
  Component 4 (0.20): Superscript retained in Footnote Reference style
"""

import os
import zipfile
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_039'
FILE_PATH = os.path.join(WORKDIR, f'{TASK_ID}.docx')

WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WNS}


def get_footnote_reference_style_rpr(file_path):
    """Extract the rPr element from the FootnoteReference character style in styles.xml."""
    with zipfile.ZipFile(file_path) as z:
        if 'word/styles.xml' not in z.namelist():
            return None
        styles_xml = z.read('word/styles.xml')
        root = etree.fromstring(styles_xml)
        for style in root.findall('.//w:style', NS):
            style_id = style.get(f'{{{WNS}}}styleId')
            style_type = style.get(f'{{{WNS}}}type')
            if style_id == 'FootnoteReference' and style_type == 'character':
                return style.find('w:rPr', NS)
    return None


def verify_task(file_path):
    """
    Verify that the Footnote Reference character style has been modified:
    - Bold, Blue (#0000FF), 11pt, superscript retained.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file exists and is a valid docx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        rpr = get_footnote_reference_style_rpr(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse styles.xml from {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if rpr is None:
        print("CRITICAL: FootnoteReference character style not found in styles.xml")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Bold enabled (0.25 points)
    try:
        b_el = rpr.find('w:b', NS)
        if b_el is not None:
            # <w:b/> or <w:b w:val="true"/> means bold
            b_val = b_el.get(f'{{{WNS}}}val')
            if b_val is None or b_val.lower() in ('true', '1', 'on'):
                print(f"PASS: Component 1 -- Bold is enabled in FootnoteReference style (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 -- w:b present but val={b_val} (expected true/absent)")
        else:
            print("FAIL: Component 1 -- No <w:b> element in FootnoteReference style rPr")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Blue font color #0000FF (0.30 points)
    try:
        color_el = rpr.find('w:color', NS)
        if color_el is not None:
            color_val = color_el.get(f'{{{WNS}}}val')
            if color_val is not None:
                color_upper = color_val.upper().lstrip('#')
                if color_upper == '0000FF':
                    print(f"PASS: Component 2 -- Font color is #0000FF (blue) (0.30 pts)")
                    total_score += 0.30
                else:
                    # Allow close shades of blue with tolerance
                    try:
                        r = int(color_upper[0:2], 16)
                        g = int(color_upper[2:4], 16)
                        b = int(color_upper[4:6], 16)
                        # Must be predominantly blue
                        if r <= 30 and g <= 30 and b >= 220:
                            print(f"PASS: Component 2 -- Font color #{color_upper} is close to blue (0.30 pts)")
                            total_score += 0.30
                        else:
                            print(f"FAIL: Component 2 -- Font color #{color_upper} is not blue (expected #0000FF)")
                    except Exception:
                        print(f"FAIL: Component 2 -- Cannot parse color value: {color_val}")
            else:
                print("FAIL: Component 2 -- w:color element has no val attribute")
        else:
            print("FAIL: Component 2 -- No <w:color> element in FootnoteReference style rPr")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Font size 11pt (w:sz val=22) (0.25 points)
    try:
        sz_el = rpr.find('w:sz', NS)
        if sz_el is not None:
            sz_val = sz_el.get(f'{{{WNS}}}val')
            if sz_val is not None:
                sz_int = int(sz_val)
                # 11pt = 22 half-points
                if sz_int == 22:
                    print(f"PASS: Component 3 -- Font size is 11pt (sz val=22) (0.25 pts)")
                    total_score += 0.25
                else:
                    pt_val = sz_int / 2.0
                    print(f"FAIL: Component 3 -- Font size is {pt_val}pt (sz val={sz_int}), expected 11pt (22)")
            else:
                print("FAIL: Component 3 -- w:sz element has no val attribute")
        else:
            print("FAIL: Component 3 -- No <w:sz> element in FootnoteReference style rPr")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Superscript retained AND at least one task change applied (0.20 points)
    # Superscript exists in initial_env too, so we gate this on having at least one
    # task-introduced change (bold, color, or size) to avoid scoring a precondition.
    try:
        vert_el = rpr.find('w:vertAlign', NS)
        has_superscript = (vert_el is not None and vert_el.get(f'{{{WNS}}}val') == 'superscript')
        has_any_task_change = (rpr.find('w:b', NS) is not None or
                               rpr.find('w:color', NS) is not None or
                               rpr.find('w:sz', NS) is not None)
        if has_superscript and has_any_task_change:
            print(f"PASS: Component 4 -- Superscript retained alongside task changes (0.20 pts)")
            total_score += 0.20
        elif has_superscript and not has_any_task_change:
            print(f"FAIL: Component 4 -- Superscript present but no task changes detected (precondition only)")
        elif not has_superscript:
            print(f"FAIL: Component 4 -- Superscript was removed (vertAlign missing or not 'superscript')")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

"""
Reward Script: Set text box border to 3pt solid navy (#1A237E) with 5pt padding on all sides
Task ID: writer_obj_048
Domain: libreoffice_writer
Scoring:
  Component 1: Text box border width is 3pt (0.5 pts)
  Component 2: Text box border color is navy #1A237E (0.3 pts)
  Component 3: Text box internal padding is ~5pt (63500 EMU) on all sides (0.2 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_obj_048'
FILE_PATH = '/home/user/Desktop/framed_note.docx'

# Tolerance for padding check: allow ±10% of 63500 EMU (5pt)
PADDING_TARGET_EMU = 63500   # 5pt exactly
PADDING_TOLERANCE = 7000     # ~0.55pt tolerance

# Border width target: 38100 EMU = 3pt (12700 EMU per point)
BORDER_WIDTH_TARGET_EMU = 38100
BORDER_WIDTH_TOLERANCE = 3000  # ~0.24pt tolerance

# Expected navy color
EXPECTED_COLOR = "1A237E"  # case-insensitive match


def verify_task(file_path):
    """
    Verify that the text box on page 1 of framed_note.docx has:
      - 3pt solid navy (#1A237E) border on all four sides
      - ~5pt internal padding on all four sides
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load XML from docx
    try:
        from docx import Document
        import lxml.etree as etree
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find text box shape (wps:wsp) in document body XML
    try:
        body = doc.element.body
        xml_str = etree.tostring(body).decode('utf-8')

        # Namespace definitions for XPath
        ns = {
            'wps': 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape',
            'a':   'http://schemas.openxmlformats.org/drawingml/2006/main',
        }

        # Find all wps:wsp elements (word processing shapes / text boxes)
        wsp_elements = body.findall('.//{%s}wsp' % 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape')

        if not wsp_elements:
            print("FAIL: No text box (wps:wsp) found in document")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        # Use the first text box found
        wsp = wsp_elements[0]
        print(f"INFO: Found {len(wsp_elements)} text box(es), verifying first one")

    except Exception as e:
        print(f"ERROR: Could not parse document XML: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Border width is 3pt (38100 EMU) (0.5 points)
    try:
        WPS_NS = 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape'
        A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'

        spPr = wsp.find('{%s}spPr' % WPS_NS)
        if spPr is None:
            print("FAIL: Component 1 — spPr element not found")
        else:
            ln_elem = spPr.find('{%s}ln' % A_NS)
            if ln_elem is None:
                print("FAIL: Component 1 — No <a:ln> border element found")
            else:
                w_attr = ln_elem.get('w')
                if w_attr is None:
                    print("FAIL: Component 1 — <a:ln> has no 'w' (width) attribute")
                else:
                    border_w = int(w_attr)
                    diff = abs(border_w - BORDER_WIDTH_TARGET_EMU)
                    if diff <= BORDER_WIDTH_TOLERANCE:
                        print(f"PASS: Component 1 — Border width is {border_w} EMU (~{border_w/12700:.2f}pt), expected ~38100 EMU (3pt) (0.5 pts)")
                        total_score += 0.5
                    else:
                        print(f"FAIL: Component 1 — Border width is {border_w} EMU (~{border_w/12700:.2f}pt), expected ~38100 EMU (3pt)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Border color is navy #1A237E (0.3 points)
    try:
        WPS_NS = 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape'
        A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'

        spPr = wsp.find('{%s}spPr' % WPS_NS)
        if spPr is None:
            print("FAIL: Component 2 — spPr element not found")
        else:
            ln_elem = spPr.find('{%s}ln' % A_NS)
            if ln_elem is None:
                print("FAIL: Component 2 — No <a:ln> border element found")
            else:
                solid_fill = ln_elem.find('{%s}solidFill' % A_NS)
                if solid_fill is None:
                    print("FAIL: Component 2 — No solidFill in border (not a solid border)")
                else:
                    srgb_clr = solid_fill.find('{%s}srgbClr' % A_NS)
                    if srgb_clr is None:
                        print("FAIL: Component 2 — No srgbClr in solidFill (may use theme color?)")
                    else:
                        color_val = srgb_clr.get('val', '')
                        if color_val.upper() == EXPECTED_COLOR.upper():
                            print(f"PASS: Component 2 — Border color is #{color_val.upper()} (navy #1A237E) (0.3 pts)")
                            total_score += 0.3
                        else:
                            print(f"FAIL: Component 2 — Border color is #{color_val.upper()}, expected #1A237E (navy)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Internal padding is ~5pt (63500 EMU) on all four sides (0.2 points)
    try:
        WPS_NS = 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape'

        bodyPr = wsp.find('{%s}bodyPr' % WPS_NS)
        if bodyPr is None:
            print("FAIL: Component 3 — bodyPr element not found")
        else:
            # Check all four padding attributes
            # lIns, tIns, rIns, bIns are in EMU
            padding_attrs = {
                'lIns': bodyPr.get('lIns'),
                'tIns': bodyPr.get('tIns'),
                'rIns': bodyPr.get('rIns'),
                'bIns': bodyPr.get('bIns'),
            }
            # Some implementations use insLEmu, insTwpEmu etc. — check both
            # The XML shows lIns/tIns/rIns/bIns in EMU
            all_set = all(v is not None for v in padding_attrs.values())
            if not all_set:
                print(f"FAIL: Component 3 — Some padding attributes missing: {padding_attrs}")
            else:
                padding_vals = {k: int(v) for k, v in padding_attrs.items()}
                within_tolerance = all(
                    abs(v - PADDING_TARGET_EMU) <= PADDING_TOLERANCE
                    for v in padding_vals.values()
                )
                if within_tolerance:
                    pts = {k: v/12700 for k, v in padding_vals.items()}
                    print(f"PASS: Component 3 — Internal padding L={pts['lIns']:.2f}pt, T={pts['tIns']:.2f}pt, R={pts['rIns']:.2f}pt, B={pts['bIns']:.2f}pt (~5pt each) (0.2 pts)")
                    total_score += 0.2
                else:
                    pts = {k: v/12700 for k, v in padding_vals.items()}
                    print(f"FAIL: Component 3 — Internal padding L={pts['lIns']:.2f}pt, T={pts['tIns']:.2f}pt, R={pts['rIns']:.2f}pt, B={pts['bIns']:.2f}pt, expected ~5pt (63500 EMU) each")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

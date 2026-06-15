"""
Reward Script: Insert DRAFT watermark text box on page 1
Task ID: writer_obj_059
Domain: libreoffice_writer
Scoring:
  Component 1: Textbox/drawing anchor exists in document (0.20 pts)
  Component 2: Text content is 'DRAFT', font size 48pt, bold (0.30 pts)
  Component 3: Text color is light gray #BDBDBD (0.20 pts)
  Component 4: Textbox rotation is approximately 30 degrees (0.15 pts)
  Component 5: No border and no background fill on textbox (0.15 pts)
  Total: 1.0
"""

import os
from docx import Document
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_obj_059'

# Namespace map for XML traversal
NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'wps': 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape',
}

# EMU per centimeter
EMU_PER_CM = 360000
# 60000ths of degree per degree
UNITS_PER_DEGREE = 60000


def verify_task(file_path):
    """
    Verify that the DRAFT watermark text box was correctly inserted on page 1.
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

    # Component 1: A drawing anchor (textbox) exists in the document (0.20 pts)
    # This FAILS on initial_env (no textbox) and PASSES on golden_env
    try:
        anchors = body.findall('.//wp:anchor', NS)
        if len(anchors) > 0:
            print(f"PASS: Component 1 — Found {len(anchors)} drawing anchor(s) in document (0.20 pts)")
            total_score += 0.20
        else:
            print("FAIL: Component 1 — No drawing anchors found; textbox not inserted")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # For remaining components, we need to find the textbox anchor
    anchor = None
    try:
        anchors = body.findall('.//wp:anchor', NS)
        if anchors:
            anchor = anchors[0]
    except Exception as e:
        print(f"ERROR: Could not retrieve anchor element — {e}")

    if anchor is None:
        print("SKIP: Components 2-5 require a textbox anchor (not found)")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Text content is 'DRAFT', font size 48pt (w:sz=96), and bold (0.30 pts)
    # w:sz stores half-points; 48pt = w:sz val "96"
    try:
        txbx = anchor.find('.//wps:txbx', NS)
        draft_text_found = False
        font_size_ok = False
        bold_ok = False

        if txbx is not None:
            txbx_content = txbx.find('w:txbxContent', NS)
            if txbx_content is not None:
                runs = txbx_content.findall('.//w:r', NS)
                for run in runs:
                    t_el = run.find('w:t', NS)
                    if t_el is not None and t_el.text and t_el.text.strip().upper() == 'DRAFT':
                        draft_text_found = True
                        rPr = run.find('w:rPr', NS)
                        if rPr is not None:
                            # Check bold: <w:b/> element present
                            b_el = rPr.find('w:b', NS)
                            bold_ok = (b_el is not None)

                            # Check font size: w:sz val="96" means 48pt
                            sz_el = rPr.find('w:sz', NS)
                            if sz_el is not None:
                                sz_val = sz_el.get(
                                    '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val'
                                )
                                if sz_val is None:
                                    sz_val = sz_el.get('w:val')
                                if sz_val is None:
                                    # Try direct attribute
                                    for attr_name, attr_val in sz_el.attrib.items():
                                        if 'val' in attr_name.lower():
                                            sz_val = attr_val
                                            break
                                if sz_val is not None:
                                    # 96 half-points = 48pt; allow 95-97 for tolerance
                                    sz_int = int(sz_val)
                                    font_size_ok = (90 <= sz_int <= 100)  # ~45-50pt range
                                    print(f"  Font size half-points: {sz_val} (expected ~96 for 48pt)")

        comp2_ok = draft_text_found and font_size_ok and bold_ok
        if comp2_ok:
            print(f"PASS: Component 2 — Text='DRAFT', size=48pt, bold=True (0.30 pts)")
            total_score += 0.30
        else:
            details = []
            if not draft_text_found:
                details.append("text 'DRAFT' not found in textbox")
            if not font_size_ok:
                details.append("font size not ~48pt")
            if not bold_ok:
                details.append("text not bold")
            print(f"FAIL: Component 2 — {'; '.join(details) if details else 'check failed'}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Text color is light gray #BDBDBD (0.20 pts)
    try:
        txbx = anchor.find('.//wps:txbx', NS)
        color_ok = False

        if txbx is not None:
            txbx_content = txbx.find('w:txbxContent', NS)
            if txbx_content is not None:
                runs = txbx_content.findall('.//w:r', NS)
                for run in runs:
                    t_el = run.find('w:t', NS)
                    if t_el is not None and t_el.text and t_el.text.strip().upper() == 'DRAFT':
                        rPr = run.find('w:rPr', NS)
                        if rPr is not None:
                            color_el = rPr.find('w:color', NS)
                            if color_el is not None:
                                color_val = color_el.get(
                                    '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val'
                                )
                                if color_val is None:
                                    for attr_name, attr_val in color_el.attrib.items():
                                        if 'val' in attr_name.lower():
                                            color_val = attr_val
                                            break
                                print(f"  Text color value: {color_val}")
                                if color_val is not None:
                                    # Accept BDBDBD (case-insensitive), allow slight tolerance
                                    color_upper = color_val.upper().lstrip('#')
                                    # Target: BDBDBD = (189, 189, 189)
                                    target = (0xBD, 0xBD, 0xBD)
                                    try:
                                        r_val = int(color_upper[0:2], 16)
                                        g_val = int(color_upper[2:4], 16)
                                        b_val = int(color_upper[4:6], 16)
                                        dist = ((r_val - target[0])**2 + (g_val - target[1])**2 + (b_val - target[2])**2) ** 0.5
                                        color_ok = dist < 30  # tolerance ~30 RGB distance
                                    except (ValueError, IndexError):
                                        color_ok = False

        if color_ok:
            print(f"PASS: Component 3 — Text color is light gray ~#BDBDBD (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Expected text color #BDBDBD; found different or missing color")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Textbox rotation is approximately 30 degrees (0.15 pts)
    # Rotation stored as rot attribute in 60000ths of degree: 30deg = 1800000
    try:
        xfrm = anchor.find('.//a:xfrm', NS)
        rotation_ok = False
        if xfrm is not None:
            rot_val = xfrm.get('rot')
            if rot_val is not None:
                rot_degrees = int(rot_val) / UNITS_PER_DEGREE
                print(f"  Rotation value: {rot_val} ({rot_degrees:.1f} degrees)")
                # Accept 28-32 degree range for tolerance
                rotation_ok = (28.0 <= rot_degrees <= 32.0)
            else:
                print("  Rotation: rot attribute not found on xfrm element")
        else:
            print("  Rotation: xfrm element not found")

        if rotation_ok:
            print(f"PASS: Component 4 — Textbox rotation is ~30 degrees (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Expected rotation ~30 degrees; found different or missing rotation")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: No border and no background fill on textbox (0.15 pts)
    # spPr should contain <a:noFill/> and <a:ln><a:noFill/></a:ln>
    try:
        spPr = anchor.find('.//wps:spPr', NS)
        no_fill_ok = False
        no_border_ok = False

        if spPr is not None:
            # Check for no background fill: <a:noFill/>
            no_fill_el = spPr.find('a:noFill', NS)
            no_fill_ok = (no_fill_el is not None)

            # Check for no border: <a:ln> with <a:noFill/> inside, OR no <a:ln> at all (default no border)
            ln_el = spPr.find('a:ln', NS)
            if ln_el is None:
                # No border element means default, which could be no border
                no_border_ok = True
            else:
                ln_no_fill = ln_el.find('a:noFill', NS)
                no_border_ok = (ln_no_fill is not None)

            print(f"  noFill (background): {no_fill_ok}")
            print(f"  noFill in border (ln): {no_border_ok}")
        else:
            print("  spPr element not found")

        comp5_ok = no_fill_ok and no_border_ok
        if comp5_ok:
            print(f"PASS: Component 5 — No border and no background fill on textbox (0.15 pts)")
            total_score += 0.15
        else:
            details = []
            if not no_fill_ok:
                details.append("background fill not removed (expected noFill)")
            if not no_border_ok:
                details.append("border not removed (expected noFill in ln)")
            print(f"FAIL: Component 5 — {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Desktop/draft_proposal.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

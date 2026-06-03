"""
Reward Script: Add slide number counter to master slide
Task ID: impress_gf3_037
Domain: libreoffice_impress
Scoring:
  Component 1 (0.25): Master slide has a new non-placeholder text box
  Component 2 (0.25): Text box contains 'Slide ' + auto slide number field
  Component 3 (0.20): Font size is 9pt
  Component 4 (0.15): Font color is #999999
  Component 5 (0.15): Position is at top-right corner
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf3_037'

# XML namespaces used in pptx
NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def find_slide_number_counter_shapes(master_xml_content):
    """
    Find non-placeholder text box shapes in the slide master that contain
    'Slide' text AND an auto slide number field (<a:fld type="slidenum">).
    Returns a list of matching shape XML elements.
    """
    root = ET.fromstring(master_xml_content)
    sp_tree = root.find('.//p:cSld/p:spTree', NS)
    if sp_tree is None:
        return []

    candidates = []
    for sp in sp_tree.findall('p:sp', NS):
        nv = sp.find('p:nvSpPr', NS)
        if nv is None:
            continue

        # Skip placeholders — we only want added text boxes
        nv_pr = nv.find('p:nvPr', NS)
        if nv_pr is not None:
            ph = nv_pr.find('p:ph', NS)
            if ph is not None:
                continue  # This is a placeholder, skip

        # Check if it's a text box
        cNvSpPr = nv.find('p:cNvSpPr', NS)
        is_textbox = False
        if cNvSpPr is not None and cNvSpPr.get('txBox') == '1':
            is_textbox = True

        # Check txBody for 'Slide' text and slidenum field
        txBody = sp.find('p:txBody', NS)
        if txBody is None:
            continue

        has_slide_text = False
        has_slidenum_field = False

        for para in txBody.findall('a:p', NS):
            # Check runs for 'Slide' text
            for run in para.findall('a:r', NS):
                t_elem = run.find('a:t', NS)
                if t_elem is not None and t_elem.text and 'Slide' in t_elem.text:
                    has_slide_text = True

            # Check for slidenum field
            for fld in para.findall('a:fld', NS):
                fld_type = fld.get('type', '')
                if fld_type == 'slidenum':
                    has_slidenum_field = True

        if has_slide_text or has_slidenum_field:
            candidates.append({
                'element': sp,
                'is_textbox': is_textbox,
                'has_slide_text': has_slide_text,
                'has_slidenum_field': has_slidenum_field,
            })

    return candidates


def get_shape_properties(sp):
    """Extract position, size, font size, font color from a shape element."""
    props = {}

    # Position and size from spPr/xfrm
    spPr = sp.find('p:spPr', NS)
    if spPr is not None:
        xfrm = spPr.find('a:xfrm', NS)
        if xfrm is not None:
            off = xfrm.find('a:off', NS)
            ext = xfrm.find('a:ext', NS)
            if off is not None:
                props['x'] = int(off.get('x', '0'))
                props['y'] = int(off.get('y', '0'))
            if ext is not None:
                props['cx'] = int(ext.get('cx', '0'))
                props['cy'] = int(ext.get('cy', '0'))

    # Font properties from txBody runs and fields
    txBody = sp.find('p:txBody', NS)
    font_sizes = []
    font_colors = []

    if txBody is not None:
        # Check runs
        for rPr in txBody.findall('.//a:rPr', NS):
            sz = rPr.get('sz')
            if sz is not None:
                font_sizes.append(int(sz))
            fill = rPr.find('a:solidFill', NS)
            if fill is not None:
                srgb = fill.find('a:srgbClr', NS)
                if srgb is not None:
                    font_colors.append(srgb.get('val', '').upper())

    props['font_sizes'] = font_sizes
    props['font_colors'] = font_colors
    return props


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            # Find and read the slide master XML
            master_path = 'ppt/slideMasters/slideMaster1.xml'
            if master_path not in zf.namelist():
                print(f"CRITICAL: No slide master found at {master_path}")
                print("REWARD: 0.0")
                return 0.0
            master_content = zf.read(master_path).decode('utf-8')
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find candidate shapes — non-placeholder shapes with slide text/number field
    candidates = find_slide_number_counter_shapes(master_content)

    if not candidates:
        print("FAIL: No non-placeholder shape with 'Slide' text or slidenum field found on master slide")
        print("REWARD: 0.0")
        return 0.0

    # Use the best candidate (one with both text and field)
    best = None
    for c in candidates:
        if c['has_slide_text'] and c['has_slidenum_field']:
            best = c
            break
    if best is None:
        # Fall back to any candidate
        best = candidates[0]

    sp = best['element']
    props = get_shape_properties(sp)

    # Get slide dimensions for position check
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            pres_content = zf.read('ppt/presentation.xml').decode('utf-8')
            pres_root = ET.fromstring(pres_content)
            sldSz = pres_root.find('.//p:sldSz', NS)
            slide_width = int(sldSz.get('cx', '12192000'))
            slide_height = int(sldSz.get('cy', '6858000'))
    except Exception:
        slide_width = 12192000
        slide_height = 6858000

    # Component 1: Master slide has a new non-placeholder text box (0.25 points)
    try:
        if best['is_textbox']:
            print(f"PASS: Component 1 — Non-placeholder text box found on master slide (0.25 pts)")
            total_score += 0.25
        else:
            # Even if not explicitly marked as textbox, if it's a non-placeholder shape with text, accept
            print(f"PASS: Component 1 — Non-placeholder shape with text found on master slide (0.25 pts)")
            total_score += 0.25
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Text box contains 'Slide ' + auto slide number field (0.25 points)
    try:
        if best['has_slide_text'] and best['has_slidenum_field']:
            print(f"PASS: Component 2 — Shape contains 'Slide' text and slidenum field (0.25 pts)")
            total_score += 0.25
        elif best['has_slidenum_field']:
            print(f"PARTIAL: Component 2 — Has slidenum field but missing 'Slide' text (0.10 pts)")
            total_score += 0.10
        elif best['has_slide_text']:
            print(f"PARTIAL: Component 2 — Has 'Slide' text but missing slidenum field (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 — Missing both 'Slide' text and slidenum field")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Font size is 9pt (sz=900 in hundredths of a point) (0.20 points)
    try:
        font_sizes = props.get('font_sizes', [])
        if font_sizes:
            # All font sizes in the shape should be 900 (9pt)
            all_9pt = all(sz == 900 for sz in font_sizes)
            if all_9pt:
                print(f"PASS: Component 3 — Font size is 9pt (900 hundredths) for all runs (0.20 pts)")
                total_score += 0.20
            else:
                # Check if at least one is 9pt
                any_9pt = any(sz == 900 for sz in font_sizes)
                if any_9pt:
                    print(f"PARTIAL: Component 3 — Some runs are 9pt but not all. Sizes: {font_sizes} (0.10 pts)")
                    total_score += 0.10
                else:
                    print(f"FAIL: Component 3 — Expected font size 900 (9pt), found: {font_sizes}")
        else:
            print(f"FAIL: Component 3 — No explicit font sizes set on shape runs")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Font color is #999999 (0.15 points)
    try:
        font_colors = props.get('font_colors', [])
        if font_colors:
            all_999 = all(c == '999999' for c in font_colors)
            if all_999:
                print(f"PASS: Component 4 — Font color is #999999 for all runs (0.15 pts)")
                total_score += 0.15
            else:
                any_999 = any(c == '999999' for c in font_colors)
                if any_999:
                    print(f"PARTIAL: Component 4 — Some runs have #999999 but not all. Colors: {font_colors} (0.07 pts)")
                    total_score += 0.07
                else:
                    print(f"FAIL: Component 4 — Expected color 999999, found: {font_colors}")
        else:
            print(f"FAIL: Component 4 — No explicit font colors set on shape runs")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Position is at top-right corner (0.15 points)
    try:
        x = props.get('x', 0)
        y = props.get('y', 0)
        cx = props.get('cx', 0)

        # Top-right: shape right edge (x + cx) should be near slide_width,
        # and y should be in the top ~15% of the slide
        right_edge = x + cx
        right_margin = slide_width - right_edge
        max_right_margin = slide_width * 0.10  # within 10% of right edge
        is_right = right_margin <= max_right_margin and x > slide_width * 0.5

        top_threshold = slide_height * 0.20  # top 20% of slide
        is_top = y < top_threshold

        if is_right and is_top:
            print(f"PASS: Component 5 — Position at top-right (x={x}, y={y}, right_edge={right_edge}, slide_w={slide_width}) (0.15 pts)")
            total_score += 0.15
        elif is_top:
            print(f"PARTIAL: Component 5 — At top but not right-aligned (x={x}, y={y}) (0.07 pts)")
            total_score += 0.07
        elif is_right:
            print(f"PARTIAL: Component 5 — Right-aligned but not at top (x={x}, y={y}) (0.07 pts)")
            total_score += 0.07
        else:
            print(f"FAIL: Component 5 — Not at top-right (x={x}, y={y}, slide_w={slide_width}, slide_h={slide_height})")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

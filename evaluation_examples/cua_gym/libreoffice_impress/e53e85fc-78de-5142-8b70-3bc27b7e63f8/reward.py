"""
Reward Script: Process diagram with 5 labeled rectangles, arrows, alternating colors, and animations on slide 2
Task ID: impress_gf4_010
Domain: libreoffice_impress
Scoring:
  Component 1: Five rectangles with correct labels (0.30)
  Component 2: Alternating fill colors #2563EB/#1E3A5F (0.20)
  Component 3: White bold text on all rectangles (0.15)
  Component 4: Four arrow shapes connecting rectangles (0.15)
  Component 5: Entrance animations present on shapes (0.20)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf4_010'

# Expected labels in order
EXPECTED_LABELS = ['Research', 'Design', 'Develop', 'Test', 'Deploy']
# Expected alternating colors for rectangles (by index 0-4)
EXPECTED_COLORS = ['2563EB', '1E3A5F', '2563EB', '1E3A5F', '2563EB']

# XML namespaces
NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def get_shape_text(sp_elem):
    """Extract concatenated text from a shape element."""
    texts = []
    for t in sp_elem.findall('.//a:t', NS):
        if t.text:
            texts.append(t.text)
    return ''.join(texts).strip()


def get_shape_fill_color(sp_elem):
    """Extract solid fill srgbClr value from shape's spPr."""
    spPr = sp_elem.find('p:spPr', NS)
    if spPr is not None:
        fill = spPr.find('a:solidFill', NS)
        if fill is not None:
            clr = fill.find('a:srgbClr', NS)
            if clr is not None:
                return clr.get('val', '').upper()
    return None


def get_shape_preset_geom(sp_elem):
    """Get the preset geometry type (rect, rightArrow, etc.)."""
    spPr = sp_elem.find('p:spPr', NS)
    if spPr is not None:
        prstGeom = spPr.find('a:prstGeom', NS)
        if prstGeom is not None:
            return prstGeom.get('prst', '')
    return ''


def get_text_runs_bold_and_color(sp_elem):
    """Get bold status and color for text runs in a shape."""
    results = []
    for rPr in sp_elem.findall('.//a:rPr', NS):
        bold = rPr.get('b', '0')
        is_bold = bold == '1'
        color = None
        solidFill = rPr.find('a:solidFill', NS)
        if solidFill is not None:
            clr = solidFill.find('a:srgbClr', NS)
            if clr is not None:
                color = clr.get('val', '').upper()
        results.append((is_bold, color))
    return results


def get_shape_left(sp_elem):
    """Get the left position (x) of a shape for ordering."""
    spPr = sp_elem.find('p:spPr', NS)
    if spPr is not None:
        xfrm = spPr.find('a:xfrm', NS)
        if xfrm is not None:
            off = xfrm.find('a:off', NS)
            if off is not None:
                return int(off.get('x', '0'))
    return 0


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
        slide2_xml = zf.open('ppt/slides/slide2.xml').read().decode('utf-8')
        root = ET.fromstring(slide2_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot load or parse file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all shapes from slide 2's spTree
    spTree = root.find('.//p:cSld/p:spTree', NS)
    if spTree is None:
        print("FAIL: No shape tree found on slide 2")
        print("REWARD: 0.0")
        return 0.0

    all_shapes = spTree.findall('p:sp', NS)

    # Separate rectangles (with text matching expected labels) and arrow shapes
    rect_shapes = []
    arrow_shapes = []
    for sp in all_shapes:
        geom = get_shape_preset_geom(sp)
        text = get_shape_text(sp)
        if geom == 'rect' and text in EXPECTED_LABELS:
            rect_shapes.append(sp)
        elif 'arrow' in geom.lower() or 'Arrow' in geom:
            arrow_shapes.append(sp)

    # Sort rectangles left-to-right by x position
    rect_shapes.sort(key=lambda sp: get_shape_left(sp))

    # Component 1: Five rectangles with correct labels in order (0.30 points)
    try:
        found_labels = [get_shape_text(sp) for sp in rect_shapes]
        if found_labels == EXPECTED_LABELS:
            print(f"PASS: Component 1 — Five rectangles with correct labels {found_labels} (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Expected labels {EXPECTED_LABELS}, found {found_labels}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Alternating fill colors (0.20 points)
    try:
        if len(rect_shapes) >= 5:
            colors_match = 0
            actual_colors = []
            for i, sp in enumerate(rect_shapes[:5]):
                fill_color = get_shape_fill_color(sp)
                actual_colors.append(fill_color)
                if fill_color and fill_color == EXPECTED_COLORS[i]:
                    colors_match += 1
            if colors_match == 5:
                print(f"PASS: Component 2 — All 5 rectangles have correct alternating colors {actual_colors} (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — Expected colors {EXPECTED_COLORS}, found {actual_colors} ({colors_match}/5 match)")
        else:
            print(f"FAIL: Component 2 — Need 5 rectangles, only found {len(rect_shapes)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: White bold text on all rectangles (0.15 points)
    try:
        if len(rect_shapes) >= 5:
            all_white_bold = 0
            for i, sp in enumerate(rect_shapes[:5]):
                runs_info = get_text_runs_bold_and_color(sp)
                if runs_info:
                    # Check that at least one run is bold with white color
                    has_white_bold = any(
                        is_bold and color and color == 'FFFFFF'
                        for is_bold, color in runs_info
                    )
                    if has_white_bold:
                        all_white_bold += 1
                    else:
                        label = get_shape_text(sp)
                        print(f"  INFO: Rectangle '{label}' runs: {runs_info}")
            if all_white_bold == 5:
                print(f"PASS: Component 3 — All 5 rectangles have white bold text (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — Only {all_white_bold}/5 rectangles have white bold text")
        else:
            print(f"FAIL: Component 3 — Need 5 rectangles, only found {len(rect_shapes)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Four arrow shapes connecting rectangles (0.15 points)
    try:
        num_arrows = len(arrow_shapes)
        if num_arrows >= 4:
            print(f"PASS: Component 4 — Found {num_arrows} arrow shapes (need >= 4) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Expected >= 4 arrows, found {num_arrows}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Entrance animations present on shapes (0.20 points)
    try:
        timing = root.find('.//p:timing', NS)
        if timing is not None:
            # Check for entrance animations (presetClass="entr")
            anim_nodes = timing.findall('.//' + '{http://schemas.openxmlformats.org/presentationml/2006/main}cTn[@presetClass="entr"]')
            # Also count animated shape targets
            anim_targets = set()
            for spTgt in timing.findall('.//p:spTgt', NS):
                spid = spTgt.get('spid')
                if spid:
                    anim_targets.add(spid)

            if len(anim_nodes) >= 5 and len(anim_targets) >= 5:
                print(f"PASS: Component 5 — Found {len(anim_nodes)} entrance animations targeting {len(anim_targets)} shapes (0.20 pts)")
                total_score += 0.20
            elif len(anim_nodes) >= 3:
                # Partial: some animations present
                partial = 0.10
                print(f"PARTIAL: Component 5 — Found {len(anim_nodes)} entrance animations targeting {len(anim_targets)} shapes ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — Expected >= 5 entrance animations, found {len(anim_nodes)} targeting {len(anim_targets)} shapes")
        else:
            print(f"FAIL: Component 5 — No timing/animation section found on slide 2")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    try:
        zf.close()
    except:
        pass

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

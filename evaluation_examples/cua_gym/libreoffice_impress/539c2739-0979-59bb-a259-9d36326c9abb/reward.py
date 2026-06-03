"""
Reward Script: Verify 5 custom master slide layouts for training manual
Task ID: impress_gf2_039
Domain: libreoffice_impress
Scoring:
  Component 1: 5 custom layouts exist by name (0.25)
  Component 2: Chapter Title - dark background #1E293B + centered title (0.20)
  Component 3: Instructional - title + content + picture placeholders (0.15)
  Component 4: Exercise - yellow header bar #FCD34D + two content columns (0.20)
  Component 5: Summary - title + 3 icon placeholders + full-width text (0.10)
  Component 6: Assessment - plain white, single content placeholder with generous margins (0.10)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf2_039'

NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
}

REQUIRED_LAYOUTS = ['Chapter Title', 'Instructional', 'Exercise', 'Summary', 'Assessment']


def find_layout_files(zf):
    """Map layout cSld name -> layout XML filename for all layouts in the file."""
    name_to_file = {}
    layout_files = sorted([f for f in zf.namelist() if 'slideLayout' in f and f.endswith('.xml')])
    for lf in layout_files:
        root = ET.parse(zf.open(lf)).getroot()
        cSld = root.find('p:cSld', NS)
        if cSld is not None:
            name = cSld.get('name', '')
            if name:
                name_to_file[name] = lf
    return name_to_file


def get_layout_root(zf, layout_file):
    """Parse and return the root element for a layout file."""
    return ET.parse(zf.open(layout_file)).getroot()


def get_shapes(root):
    """Get all sp shapes from the cSld/spTree."""
    cSld = root.find('p:cSld', NS)
    if cSld is None:
        return []
    spTree = cSld.find('p:spTree', NS)
    if spTree is None:
        return []
    return spTree.findall('p:sp', NS)


def get_shape_info(sp):
    """Extract key info from a shape element."""
    nvSpPr = sp.find('p:nvSpPr', NS)
    nvPr = nvSpPr.find('p:nvPr', NS) if nvSpPr is not None else None
    ph = nvPr.find('p:ph', NS) if nvPr is not None else None

    cNvPr = nvSpPr.find('p:cNvPr', NS) if nvSpPr is not None else None
    shape_name = cNvPr.get('name', '') if cNvPr is not None else ''

    ph_type = ph.get('type', 'content') if ph is not None else None
    ph_idx = ph.get('idx', '0') if ph is not None else None

    xfrm = sp.find('.//a:xfrm', NS)
    x, y, cx, cy = 0, 0, 0, 0
    if xfrm is not None:
        off = xfrm.find('a:off', NS)
        ext = xfrm.find('a:ext', NS)
        if off is not None:
            x = int(off.get('x', '0'))
            y = int(off.get('y', '0'))
        if ext is not None:
            cx = int(ext.get('cx', '0'))
            cy = int(ext.get('cy', '0'))

    # Check fill color
    fill_color = None
    spPr = sp.find('p:spPr', NS)
    if spPr is not None:
        sf = spPr.find('a:solidFill', NS)
        if sf is not None:
            srgb = sf.find('a:srgbClr', NS)
            if srgb is not None:
                fill_color = srgb.get('val', '').upper()

    return {
        'name': shape_name,
        'ph_type': ph_type,
        'ph_idx': ph_idx,
        'x': x, 'y': y, 'cx': cx, 'cy': cy,
        'fill_color': fill_color,
        'is_placeholder': ph is not None,
    }


def get_bg_color(root):
    """Get the background solid fill color of a layout (from cSld/bg)."""
    cSld = root.find('p:cSld', NS)
    if cSld is None:
        return None
    bg = cSld.find('p:bg', NS)
    if bg is None:
        return None
    solidFill = bg.find('.//a:solidFill', NS)
    if solidFill is None:
        return None
    srgb = solidFill.find('a:srgbClr', NS)
    if srgb is not None:
        return srgb.get('val', '').upper()
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print("CRITICAL: Cannot open file %s: %s" % (file_path, e))
        print("REWARD: 0.0")
        return 0.0

    try:
        name_to_file = find_layout_files(zf)
    except Exception as e:
        print("CRITICAL: Cannot parse layouts: %s" % e)
        print("REWARD: 0.0")
        zf.close()
        return 0.0

    all_layout_names = list(name_to_file.keys())
    print("Found layouts: %s" % all_layout_names)

    # Component 1: All 5 required layouts exist by name (0.25 points)
    # Each named layout is worth 0.05 points
    try:
        found_count = 0
        for req_name in REQUIRED_LAYOUTS:
            if req_name in name_to_file:
                found_count += 1
                print("PASS: Layout '%s' exists" % req_name)
            else:
                print("FAIL: Layout '%s' not found" % req_name)
        if found_count == 5:
            print("PASS: Component 1 - All 5 required layouts exist (0.25 pts)")
            total_score += 0.25
        elif found_count > 0:
            partial = 0.05 * found_count
            print("PARTIAL: Component 1 - %d/5 layouts exist (%.2f pts)" % (found_count, partial))
            total_score += partial
        else:
            print("FAIL: Component 1 - No required layouts found")
    except Exception as e:
        print("ERROR: Component 1 - %s" % e)

    # Component 2: Chapter Title layout - dark background #1E293B + centered title placeholder (0.20 points)
    try:
        if 'Chapter Title' in name_to_file:
            root = get_layout_root(zf, name_to_file['Chapter Title'])
            bg_color = get_bg_color(root)
            shapes = get_shapes(root)
            shape_infos = [get_shape_info(sp) for sp in shapes]

            comp2_score = 0.0

            # Check dark background (0.10)
            if bg_color is not None and bg_color == '1E293B':
                print("PASS: Chapter Title has dark background #1E293B")
                comp2_score += 0.10
            else:
                print("FAIL: Chapter Title background expected #1E293B, found %s" % bg_color)

            # Check title placeholder exists (ctrTitle type) (0.10)
            has_title = any(s['ph_type'] in ('ctrTitle', 'title') for s in shape_infos if s['is_placeholder'])
            if has_title:
                print("PASS: Chapter Title has title placeholder")
                comp2_score += 0.10
            else:
                print("FAIL: Chapter Title missing title placeholder")

            if comp2_score > 0:
                print("PASS: Component 2 - Chapter Title layout (%.2f pts)" % comp2_score)
                total_score += comp2_score
            else:
                print("FAIL: Component 2 - Chapter Title layout checks failed")
        else:
            print("FAIL: Component 2 - 'Chapter Title' layout not found")
    except Exception as e:
        print("ERROR: Component 2 - %s" % e)

    # Component 3: Instructional layout - title + content + picture placeholders (0.15 points)
    try:
        if 'Instructional' in name_to_file:
            root = get_layout_root(zf, name_to_file['Instructional'])
            shapes = get_shapes(root)
            shape_infos = [get_shape_info(sp) for sp in shapes]

            comp3_score = 0.0

            # Check title placeholder (0.05)
            has_title = any(s['ph_type'] in ('title', 'ctrTitle') for s in shape_infos if s['is_placeholder'])
            if has_title:
                print("PASS: Instructional has title placeholder")
                comp3_score += 0.05
            else:
                print("FAIL: Instructional missing title placeholder")

            # Check content/body placeholder (0.05)
            body_phs = [s for s in shape_infos if s['is_placeholder'] and s['ph_type'] in ('body', 'content', None)]
            if len(body_phs) >= 1:
                print("PASS: Instructional has content placeholder")
                comp3_score += 0.05
            else:
                print("FAIL: Instructional missing content placeholder")

            # Check picture placeholder (0.05)
            pic_phs = [s for s in shape_infos if s['is_placeholder'] and s['ph_type'] == 'pic']
            if len(pic_phs) >= 1:
                print("PASS: Instructional has picture placeholder")
                comp3_score += 0.05
            else:
                print("FAIL: Instructional missing picture placeholder")

            if comp3_score > 0:
                print("PASS: Component 3 - Instructional layout (%.2f pts)" % comp3_score)
                total_score += comp3_score
            else:
                print("FAIL: Component 3 - Instructional layout checks failed")
        else:
            print("FAIL: Component 3 - 'Instructional' layout not found")
    except Exception as e:
        print("ERROR: Component 3 - %s" % e)

    # Component 4: Exercise layout - yellow header bar #FCD34D + two content columns (0.20 points)
    try:
        if 'Exercise' in name_to_file:
            root = get_layout_root(zf, name_to_file['Exercise'])
            shapes = get_shapes(root)
            shape_infos = [get_shape_info(sp) for sp in shapes]

            comp4_score = 0.0

            # Check yellow header bar (non-placeholder shape with fill #FCD34D) (0.10)
            yellow_bars = [s for s in shape_infos if not s['is_placeholder'] and s['fill_color'] == 'FCD34D']
            if len(yellow_bars) >= 1:
                bar = yellow_bars[0]
                # Verify it's roughly full-width and header-positioned
                print("PASS: Exercise has yellow header bar #FCD34D (pos y=%d, height=%d)" % (bar['y'], bar['cy']))
                comp4_score += 0.10
            else:
                # Also check for close yellows
                any_yellow = [s for s in shape_infos if not s['is_placeholder'] and s['fill_color'] is not None]
                if any_yellow:
                    print("FAIL: Exercise has non-placeholder shape(s) with fill %s, expected #FCD34D" % [s['fill_color'] for s in any_yellow])
                else:
                    print("FAIL: Exercise missing yellow header bar")

            # Check two content placeholders (0.10)
            body_phs = [s for s in shape_infos if s['is_placeholder'] and s['ph_type'] in ('body', 'content', None)]
            if len(body_phs) >= 2:
                print("PASS: Exercise has %d content placeholders" % len(body_phs))
                comp4_score += 0.10
            else:
                print("FAIL: Exercise has %d content placeholders, expected >= 2" % len(body_phs))

            if comp4_score > 0:
                print("PASS: Component 4 - Exercise layout (%.2f pts)" % comp4_score)
                total_score += comp4_score
            else:
                print("FAIL: Component 4 - Exercise layout checks failed")
        else:
            print("FAIL: Component 4 - 'Exercise' layout not found")
    except Exception as e:
        print("ERROR: Component 4 - %s" % e)

    # Component 5: Summary layout - title + 3 icon placeholders + full-width text (0.10 points)
    try:
        if 'Summary' in name_to_file:
            root = get_layout_root(zf, name_to_file['Summary'])
            shapes = get_shapes(root)
            shape_infos = [get_shape_info(sp) for sp in shapes]

            comp5_score = 0.0

            # Check title placeholder
            has_title = any(s['ph_type'] in ('title', 'ctrTitle') for s in shape_infos if s['is_placeholder'])

            # Check at least 3 picture/icon placeholders
            pic_phs = [s for s in shape_infos if s['is_placeholder'] and s['ph_type'] == 'pic']

            # Check body/text placeholder
            body_phs = [s for s in shape_infos if s['is_placeholder'] and s['ph_type'] in ('body', 'content', None)]

            if has_title and len(pic_phs) >= 3 and len(body_phs) >= 1:
                print("PASS: Summary has title + %d icon placeholders + text area" % len(pic_phs))
                comp5_score = 0.10
            elif has_title and (len(pic_phs) >= 3 or len(body_phs) >= 1):
                comp5_score = 0.05
                print("PARTIAL: Summary has title + %d icon phs + %d body phs (0.05 pts)" % (len(pic_phs), len(body_phs)))
            else:
                print("FAIL: Summary - title=%s, icon_phs=%d, body_phs=%d" % (has_title, len(pic_phs), len(body_phs)))

            if comp5_score > 0:
                total_score += comp5_score
        else:
            print("FAIL: Component 5 - 'Summary' layout not found")
    except Exception as e:
        print("ERROR: Component 5 - %s" % e)

    # Component 6: Assessment layout - single content placeholder with generous margins (0.10 points)
    try:
        if 'Assessment' in name_to_file:
            root = get_layout_root(zf, name_to_file['Assessment'])
            shapes = get_shapes(root)
            shape_infos = [get_shape_info(sp) for sp in shapes]

            # Should have no dark/colored background (plain white - inherited or white)
            bg_color = get_bg_color(root)

            # Should have a content placeholder with generous margins
            # (left margin > 1 inch = 914400 EMU, or similar)
            body_phs = [s for s in shape_infos if s['is_placeholder'] and s['ph_type'] in ('body', 'content', None)]

            comp6_score = 0.0

            # No explicit dark background (plain white means either no bg or white bg)
            if bg_color is None or bg_color == 'FFFFFF':
                # Has single content placeholder
                if len(body_phs) >= 1:
                    ph = body_phs[0]
                    # Check generous margins: left margin > ~1 inch (914400 EMU)
                    if ph['x'] >= 900000:
                        print("PASS: Assessment has content placeholder with left margin %d EMU (generous)" % ph['x'])
                        comp6_score = 0.10
                    else:
                        print("PARTIAL: Assessment has content placeholder but left margin %d EMU is not generous" % ph['x'])
                        comp6_score = 0.05
                else:
                    print("FAIL: Assessment has no content placeholder")
            else:
                print("FAIL: Assessment has non-white background #%s" % bg_color)

            if comp6_score > 0:
                print("PASS: Component 6 - Assessment layout (%.2f pts)" % comp6_score)
                total_score += comp6_score
        else:
            print("FAIL: Component 6 - 'Assessment' layout not found")
    except Exception as e:
        print("ERROR: Component 6 - %s" % e)

    zf.close()

    final_score = min(total_score, 1.0)
    print("\nScore: %.2f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


# Entry point
file_path = '%s/%s.pptx' % (WORKDIR, TASK_ID)
if not os.path.exists(file_path):
    print("File not found: %s" % file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)

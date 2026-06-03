"""
Reward Script: Master slide layout 'Photo Left' with photo placeholder, teal overlay, and content area
Task ID: impress_gf2_030
Domain: libreoffice_impress
Scoring:
  Component 1 (0.25) - Layout named 'Photo Left' exists
  Component 2 (0.25) - Picture placeholder on the left half
  Component 3 (0.25) - Teal overlay rectangle with correct color and ~60% transparency
  Component 4 (0.25) - Content/title placeholders on the right half
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf2_030'

NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_A = 'http://schemas.openxmlformats.org/drawingml/2006/main'


def find_photo_left_layout(zf):
    """Find and return the XML filename of a layout named 'Photo Left'."""
    layout_files = sorted([f for f in zf.namelist()
                           if 'slideLayout' in f and f.endswith('.xml')])
    for lf in layout_files:
        with zf.open(lf) as f:
            root = ET.parse(f).getroot()
            csld = root.find(f'{{{NS_P}}}cSld')
            if csld is not None and csld.get('name', '').strip().lower() == 'photo left':
                return lf, root
    return None, None


def get_shapes_info(root):
    """Extract shape information from the layout XML."""
    csld = root.find(f'{{{NS_P}}}cSld')
    if csld is None:
        return []

    sp_tree = csld.find(f'{{{NS_P}}}spTree')
    if sp_tree is None:
        return []

    shapes = []
    for child in sp_tree:
        tag = child.tag.split('}')[-1]
        if tag not in ('sp', 'pic', 'grpSp', 'cxnSp'):
            continue

        info = {'tag': tag, 'name': '', 'ph_type': None, 'ph_idx': None,
                'x': None, 'y': None, 'cx': None, 'cy': None,
                'fill_color': None, 'fill_alpha': None, 'geom': None}

        for el in child.iter():
            el_tag = el.tag.split('}')[-1]
            if el_tag == 'cNvPr':
                info['name'] = el.get('name', '')
            elif el_tag == 'ph':
                info['ph_type'] = el.get('type', None)
                info['ph_idx'] = el.get('idx', None)
            elif el_tag == 'off':
                info['x'] = int(el.get('x', 0))
                info['y'] = int(el.get('y', 0))
            elif el_tag == 'ext':
                # Only take the first ext (shape extent), not nested ones
                if info['cx'] is None:
                    info['cx'] = int(el.get('cx', 0))
                    info['cy'] = int(el.get('cy', 0))
            elif el_tag == 'srgbClr':
                info['fill_color'] = el.get('val', '').upper()
                alpha_el = el.find(f'{{{NS_A}}}alpha')
                if alpha_el is not None:
                    info['fill_alpha'] = int(alpha_el.get('val', '100000'))
            elif el_tag == 'prstGeom':
                info['geom'] = el.get('prst', '')

        shapes.append(info)
    return shapes


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    slide_width = 12193200  # EMU, 33.87 cm
    half_width = slide_width / 2  # ~6096600

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open ZIP {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Layout named 'Photo Left' exists (0.25 points)
    try:
        layout_file, layout_root = find_photo_left_layout(zf)
        if layout_file is not None:
            print(f"PASS: Component 1 - Layout 'Photo Left' found in {layout_file} (0.25 pts)")
            total_score += 0.25
        else:
            print("FAIL: Component 1 - No layout named 'Photo Left' found")
            # If no layout, nothing else to check
            zf.close()
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    shapes = get_shapes_info(layout_root)
    print(f"  Found {len(shapes)} shapes in layout")
    for s in shapes:
        print(f"    name='{s['name']}', ph_type={s['ph_type']}, x={s['x']}, cx={s['cx']}, fill={s['fill_color']}, alpha={s['fill_alpha']}")

    # Component 2: Picture placeholder on the left half (0.25 points)
    # Must have a placeholder with type='pic' positioned in left half
    try:
        pic_placeholders = [s for s in shapes if s['ph_type'] == 'pic']
        found_left_pic = False
        for p in pic_placeholders:
            # Check it is in the left half: x should be near 0, width should be roughly half the slide
            if p['x'] is not None and p['cx'] is not None:
                right_edge = p['x'] + p['cx']
                # Left half: x starts near 0, right edge <= half_width + 10% tolerance
                if p['x'] <= half_width * 0.15 and right_edge <= half_width * 1.15:
                    found_left_pic = True
                    print(f"PASS: Component 2 - Picture placeholder on left half: x={p['x']}, w={p['cx']}, right_edge={right_edge} (0.25 pts)")
                    total_score += 0.25
                    break
        if not found_left_pic:
            if pic_placeholders:
                print(f"FAIL: Component 2 - Picture placeholder found but not in left half: {[(p['x'], p['cx']) for p in pic_placeholders]}")
            else:
                print("FAIL: Component 2 - No picture placeholder found in layout")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Teal overlay rectangle with #0D9488 color and ~60% transparency (0.25 points)
    # 60% transparency = alpha 40000 in OOXML (40% opacity) — or alpha 60000 depending on interpretation
    # Task says "60% transparency" meaning 40% opacity => alpha=40000
    # But also accept reasonable range: 35000-65000
    try:
        teal_found = False
        for s in shapes:
            if s['fill_color'] and s['fill_color'] == '0D9488':
                # Check alpha - 60% transparency means alpha around 40000 (40% opacity)
                # Accept range 30000-70000 for flexibility
                has_transparency = False
                if s['fill_alpha'] is not None and 20000 <= s['fill_alpha'] <= 70000:
                    has_transparency = True

                if has_transparency:
                    # Also verify it covers the left half area
                    if s['x'] is not None and s['x'] <= half_width * 0.15:
                        teal_found = True
                        print(f"PASS: Component 3 - Teal overlay #0D9488 with alpha={s['fill_alpha']} at x={s['x']} (0.25 pts)")
                        total_score += 0.25
                        break
                    else:
                        print(f"PARTIAL: Component 3 - Teal #0D9488 found with alpha={s['fill_alpha']} but x={s['x']} not on left side")
                else:
                    print(f"PARTIAL: Component 3 - Teal #0D9488 found but alpha={s['fill_alpha']} not in expected range")

        if not teal_found:
            # Check if any shape has teal-ish color
            teal_shapes = [s for s in shapes if s['fill_color'] and s['fill_color'].startswith('0D94')]
            if teal_shapes:
                print(f"FAIL: Component 3 - Teal-ish shape found but did not meet all criteria: {[(s['fill_color'], s['fill_alpha'], s['x']) for s in teal_shapes]}")
            else:
                print(f"FAIL: Component 3 - No teal overlay (#0D9488) found. Colors present: {[s['fill_color'] for s in shapes if s['fill_color']]}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Title and content placeholders on the right half (0.25 points)
    # Title placeholder with type='title' or 'ctrTitle' on right half
    # Content/body placeholder on right half
    try:
        title_on_right = False
        content_on_right = False

        for s in shapes:
            if s['x'] is not None and s['x'] >= half_width * 0.85:
                # This shape starts in the right half
                if s['ph_type'] == 'title' or s['ph_type'] == 'ctrTitle':
                    title_on_right = True
                    print(f"  Found title placeholder on right: x={s['x']}, name='{s['name']}'")
                elif s['ph_type'] is not None and s['ph_type'] not in ('dt', 'ftr', 'sldNum', 'pic', 'title', 'ctrTitle'):
                    content_on_right = True
                    print(f"  Found content placeholder on right: x={s['x']}, ph_type={s['ph_type']}, name='{s['name']}'")
                elif s['ph_type'] is None and s['ph_idx'] is not None:
                    # Placeholder with idx but no type = generic content placeholder
                    content_on_right = True
                    print(f"  Found content placeholder (idx={s['ph_idx']}) on right: x={s['x']}, name='{s['name']}'")

        if title_on_right and content_on_right:
            print(f"PASS: Component 4 - Title and content placeholders both on right half (0.25 pts)")
            total_score += 0.25
        elif title_on_right or content_on_right:
            partial = 0.125
            what = 'title' if title_on_right else 'content'
            missing = 'content' if title_on_right else 'title'
            print(f"PARTIAL: Component 4 - {what} on right but {missing} missing ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 - No title or content placeholder found on right half")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    zf.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

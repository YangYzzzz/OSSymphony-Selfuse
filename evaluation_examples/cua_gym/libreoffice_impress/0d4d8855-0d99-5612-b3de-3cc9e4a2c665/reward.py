"""
Reward Script: Grow & Shrink animation on company logo (slide 1)
Task ID: impress_gf3_020
Domain: libreoffice_impress
Scoring:
  - Component 1 (0.30): Animation exists on slide 1 with presetClass='emph' and presetID='6' (Grow & Shrink)
  - Component 2 (0.25): Animation targets the logo image shape (picture shape on slide 1)
  - Component 3 (0.20): Scale is 125% (animScale by x=125000 y=125000)
  - Component 4 (0.15): Repeat count is 3 (repeatCount='300000')
  - Component 5 (0.10): Auto-trigger (nodeType='afterEffect' or similar auto start)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf3_020'

NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def find_picture_spids(pptx_path, slide_idx=0):
    """Find shape IDs of picture shapes on a given slide via XML."""
    pic_spids = set()
    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            slide_xml = f'ppt/slides/slide{slide_idx + 1}.xml'
            with zf.open(slide_xml) as f:
                root = ET.parse(f).getroot()
                spTree = root.find('.//' + '{http://schemas.openxmlformats.org/presentationml/2006/main}cSld/'
                                   '{http://schemas.openxmlformats.org/presentationml/2006/main}spTree')
                if spTree is None:
                    # Try with explicit namespace
                    for elem in root.iter():
                        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                        if tag == 'pic':
                            nvPicPr = None
                            for child in elem:
                                ctag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                                if ctag == 'nvPicPr':
                                    nvPicPr = child
                                    break
                            if nvPicPr is not None:
                                for child in nvPicPr:
                                    ctag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                                    if ctag == 'cNvPr':
                                        spid = child.get('id')
                                        if spid:
                                            pic_spids.add(spid)
                else:
                    for elem in root.iter():
                        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                        if tag == 'pic':
                            for child in elem:
                                ctag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                                if ctag == 'nvPicPr':
                                    for sub in child:
                                        stag = sub.tag.split('}')[-1] if '}' in sub.tag else sub.tag
                                        if stag == 'cNvPr':
                                            spid = sub.get('id')
                                            if spid:
                                                pic_spids.add(spid)
    except Exception as e:
        print(f"WARN: Could not find picture spids: {e}")
    return pic_spids


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse slide 1 XML for timing/animation
    timing_elem = None
    try:
        with zf.open('ppt/slides/slide1.xml') as f:
            root = ET.parse(f).getroot()
            timing_elem = root.find('.//p:timing', NS)
    except Exception as e:
        print(f"ERROR: Cannot parse slide1.xml: {e}")
        print("REWARD: 0.0")
        return 0.0
    finally:
        zf.close()

    if timing_elem is None:
        print("FAIL: No timing/animation element found on slide 1")
        print("REWARD: 0.0")
        return 0.0

    # Find the animation cTn node with presetID and presetClass
    anim_ctn = None
    for ctn in timing_elem.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}cTn'):
        pid = ctn.get('presetID')
        pcls = ctn.get('presetClass')
        if pid is not None and pcls is not None:
            anim_ctn = ctn
            break

    # Component 1: Animation exists with presetClass='emph' and presetID='6' (Grow & Shrink) (0.30 pts)
    try:
        if anim_ctn is not None:
            preset_id = anim_ctn.get('presetID', '')
            preset_class = anim_ctn.get('presetClass', '')
            if preset_class == 'emph' and preset_id == '6':
                print(f"PASS: Component 1 — Grow & Shrink emphasis animation found (presetID=6, presetClass=emph) (0.30 pts)")
                total_score += 0.30
            elif preset_class == 'emph':
                print(f"FAIL: Component 1 — Emphasis animation found but presetID={preset_id}, expected 6 (Grow & Shrink)")
            else:
                print(f"FAIL: Component 1 — Animation found but presetClass={preset_class}, expected 'emph'")
        else:
            print("FAIL: Component 1 — No animation preset found on slide 1")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Animation targets the logo (picture shape) (0.25 pts)
    try:
        if anim_ctn is not None:
            # Find spTgt within the animation's children
            target_spid = None
            for spTgt in anim_ctn.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}spTgt'):
                target_spid = spTgt.get('spid')
                break

            if target_spid is not None:
                # Get picture shape IDs from slide 1
                pic_spids = find_picture_spids(file_path, slide_idx=0)
                print(f"  DEBUG: Animation targets spid={target_spid}, picture spids on slide 1: {pic_spids}")
                if target_spid in pic_spids:
                    print(f"PASS: Component 2 — Animation targets picture shape (spid={target_spid}) (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 2 — Animation targets spid={target_spid} which is not a picture shape (pictures: {pic_spids})")
            else:
                print("FAIL: Component 2 — No shape target found in animation")
        else:
            print("FAIL: Component 2 — No animation preset to check target")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Scale is 125% (animScale by x=125000, y=125000) (0.20 pts)
    try:
        if anim_ctn is not None:
            anim_scale = None
            for elem in anim_ctn.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}animScale'):
                anim_scale = elem
                break
            # Also check drawingml namespace
            if anim_scale is None:
                for elem in anim_ctn.iter():
                    tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                    if tag == 'animScale':
                        anim_scale = elem
                        break

            if anim_scale is not None:
                by_elem = None
                for child in anim_scale:
                    tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                    if tag == 'by':
                        by_elem = child
                        break

                if by_elem is not None:
                    x_val = by_elem.get('x', '')
                    y_val = by_elem.get('y', '')
                    # 125000 = 125% in OOXML thousandths of a percent
                    if x_val == '125000' and y_val == '125000':
                        print(f"PASS: Component 3 — Scale is 125% (x={x_val}, y={y_val}) (0.20 pts)")
                        total_score += 0.20
                    else:
                        # Accept some reasonable range (120000-130000 as partial)
                        try:
                            x_int = int(x_val)
                            y_int = int(y_val)
                            if 120000 <= x_int <= 130000 and 120000 <= y_int <= 130000:
                                print(f"PASS (partial): Component 3 — Scale approximately 125% (x={x_val}, y={y_val}) (0.10 pts)")
                                total_score += 0.10
                            else:
                                print(f"FAIL: Component 3 — Scale values x={x_val}, y={y_val}, expected 125000")
                        except ValueError:
                            print(f"FAIL: Component 3 — Cannot parse scale values x={x_val}, y={y_val}")
                else:
                    print("FAIL: Component 3 — animScale found but no 'by' element with scale values")
            else:
                print("FAIL: Component 3 — No animScale element found in animation")
        else:
            print("FAIL: Component 3 — No animation preset to check scale")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Repeat count is 3 (repeatCount='300000') (0.15 pts)
    try:
        if anim_ctn is not None:
            repeat_count = anim_ctn.get('repeatCount', '')
            # OOXML repeatCount: 300000 = 3.0 times (1000x multiplier)
            # Also accept '3' or '3.0' in case of different encoding
            if repeat_count == '300000':
                print(f"PASS: Component 4 — Repeat count is 3 (repeatCount={repeat_count}) (0.15 pts)")
                total_score += 0.15
            elif repeat_count:
                try:
                    rc_val = int(repeat_count)
                    if rc_val == 3:
                        print(f"PASS: Component 4 — Repeat count is 3 (repeatCount={repeat_count}) (0.15 pts)")
                        total_score += 0.15
                    elif 200000 <= rc_val <= 400000:
                        # Close but not exact
                        actual_repeats = rc_val / 100000
                        print(f"FAIL: Component 4 — Repeat count is {actual_repeats}, expected 3.0 (repeatCount={repeat_count})")
                    else:
                        print(f"FAIL: Component 4 — repeatCount={repeat_count}, expected 300000 (3 repeats)")
                except ValueError:
                    print(f"FAIL: Component 4 — Cannot parse repeatCount={repeat_count}")
            else:
                print("FAIL: Component 4 — No repeatCount attribute on animation node")
        else:
            print("FAIL: Component 4 — No animation preset to check repeat count")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Auto-trigger (nodeType='afterEffect' or 'withEffect', or start condition delay=0) (0.10 pts)
    try:
        if anim_ctn is not None:
            node_type = anim_ctn.get('nodeType', '')
            # afterEffect = After Previous (automatic)
            # withEffect = With Previous (automatic)
            # clickEffect = On Click (manual - should NOT be this)
            if node_type in ('afterEffect', 'withEffect'):
                print(f"PASS: Component 5 — Auto-trigger set (nodeType={node_type}) (0.10 pts)")
                total_score += 0.10
            elif node_type == 'clickEffect':
                print(f"FAIL: Component 5 — Trigger is On Click (nodeType=clickEffect), expected automatic")
            else:
                # Check start condition - delay=0 with no click event could also indicate auto
                start_conds = anim_ctn.findall('.//p:stCondLst/p:cond', NS)
                auto_start_found = any(
                    cond.get('evt', '') == '' and cond.get('delay', '') == '0'
                    for cond in start_conds
                )
                if auto_start_found and node_type == '':
                    # No explicit nodeType but has auto start condition
                    print(f"PASS: Component 5 — Auto start condition found (delay=0, no click event) (0.10 pts)")
                    total_score += 0.10
                else:
                    print(f"FAIL: Component 5 — nodeType='{node_type}', expected 'afterEffect' or 'withEffect'")
        else:
            print("FAIL: Component 5 — No animation preset to check trigger")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
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

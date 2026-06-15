"""
Reward Script: Verify Fly In and Fade In animations on slide 3
Task ID: impress_teach_034
Domain: libreoffice_impress
Scoring:
  Component 1 (0.25) - Image (Picture 3) has Fly In entrance animation (presetID=2, presetClass=entr)
  Component 2 (0.15) - Fly In direction is from left (presetSubtype=8)
  Component 3 (0.10) - Image animation triggers on click (nodeType=clickEffect)
  Component 4 (0.25) - Text box (TextBox 4) has Fade In entrance animation (presetID=10, presetClass=entr)
  Component 5 (0.10) - Text animation triggers after previous (nodeType=afterEffect)
  Component 6 (0.15) - Text animation has 0.5s delay (delay=500)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_teach_034'

def find_shape_id_by_type(pptx_path, slide_num, shape_type):
    """Find shape IDs on a given slide. shape_type: 'pic' for picture, 'sp' for shape/textbox."""
    ns_p = 'http://schemas.openxmlformats.org/presentationml/2006/main'
    ns_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    ns_r = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

    results = []
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        with zf.open(f'ppt/slides/slide{slide_num}.xml') as f:
            root = ET.parse(f).getroot()

        spTree = root.find(f'.//{{{ns_p}}}cSld/{{{ns_p}}}spTree')
        if spTree is None:
            return results

        for child in spTree:
            tag = child.tag.split('}')[-1]
            if tag == shape_type or (shape_type == 'textbox' and tag == 'sp'):
                # Extract id and name from cNvPr
                for elem in child.iter():
                    if elem.tag.endswith('cNvPr'):
                        results.append({
                            'id': elem.get('id'),
                            'name': elem.get('name', ''),
                            'tag': tag
                        })
                        break
    return results


def parse_animations(pptx_path, slide_num):
    """Parse animation timing XML from a specific slide.
    Returns list of animation dicts with properties."""
    ns_p = 'http://schemas.openxmlformats.org/presentationml/2006/main'

    animations = []
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        with zf.open(f'ppt/slides/slide{slide_num}.xml') as f:
            root = ET.parse(f).getroot()

    timing = root.find(f'.//{{{ns_p}}}timing')
    if timing is None:
        print("DEBUG: No timing element found on slide")
        return animations

    # Find all cTn elements with presetID (these are the actual animation effects)
    for cTn in timing.iter(f'{{{ns_p}}}cTn'):
        preset_id = cTn.get('presetID')
        if preset_id is None:
            continue

        preset_class = cTn.get('presetClass', '')
        preset_subtype = cTn.get('presetSubtype', '')
        node_type = cTn.get('nodeType', '')

        # Find target shape ID
        target_spid = None
        for spTgt in cTn.iter(f'{{{ns_p}}}spTgt'):
            target_spid = spTgt.get('spid')
            break

        # Find delay from parent's stCondLst
        delay = None
        parent_cTn = None
        # Walk up: the delay is on the parent <par>'s <cTn> stCondLst
        # We need to find the delay on the enclosing par's cTn, not the animation cTn itself
        # The structure is: par > cTn(delay=X) > childTnLst > par > cTn(presetID=...)
        # So we look at the grandparent par's cTn for the delay
        # Instead, search for cond elements with delay in the parent context
        parent = cTn.find(f'..', )  # ET doesn't support parent lookup easily

        anim_info = {
            'preset_id': preset_id,
            'preset_class': preset_class,
            'preset_subtype': preset_subtype,
            'node_type': node_type,
            'target_spid': target_spid,
        }
        animations.append(anim_info)

    return animations


def find_animation_delays(pptx_path, slide_num):
    """Parse the full timing tree to find delays associated with each animation."""
    ns_p = 'http://schemas.openxmlformats.org/presentationml/2006/main'

    with zipfile.ZipFile(pptx_path, 'r') as zf:
        with zf.open(f'ppt/slides/slide{slide_num}.xml') as f:
            root = ET.parse(f).getroot()

    timing = root.find(f'.//{{{ns_p}}}timing')
    if timing is None:
        return {}

    # The animation sequence structure:
    # tmRoot > mainSeq > par(click group) > par(delay container) > par(animation cTn with presetID)
    # The delay is on the middle par's cTn stCondLst
    delays = {}
    main_seq = None
    for cTn in timing.iter(f'{{{ns_p}}}cTn'):
        if cTn.get('nodeType') == 'mainSeq':
            main_seq = cTn
            break

    if main_seq is None:
        return delays

    child_list = main_seq.find(f'{{{ns_p}}}childTnLst')
    if child_list is None:
        return delays

    # Each top-level par in mainSeq is a click group
    for click_par in child_list.findall(f'{{{ns_p}}}par'):
        click_cTn = click_par.find(f'{{{ns_p}}}cTn')
        if click_cTn is None:
            continue

        click_children = click_cTn.find(f'{{{ns_p}}}childTnLst')
        if click_children is None:
            continue

        for delay_par in click_children.findall(f'{{{ns_p}}}par'):
            delay_cTn = delay_par.find(f'{{{ns_p}}}cTn')
            if delay_cTn is None:
                continue

            # Get delay from this level's stCondLst
            par_delay = '0'
            st_cond = delay_cTn.find(f'{{{ns_p}}}stCondLst/{{{ns_p}}}cond')
            if st_cond is not None:
                par_delay = st_cond.get('delay', '0')

            # Now find the animation cTn with presetID inside
            for anim_cTn in delay_cTn.iter(f'{{{ns_p}}}cTn'):
                pid = anim_cTn.get('presetID')
                if pid is not None:
                    # Get target spid
                    target = None
                    for spTgt in anim_cTn.iter(f'{{{ns_p}}}spTgt'):
                        target = spTgt.get('spid')
                        break
                    if target:
                        delays[target] = par_delay

    return delays


def verify_task(file_path):
    """
    Verify animation task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # First, identify shape IDs on slide 3
    try:
        pics = find_shape_id_by_type(file_path, 3, 'pic')
        shapes = find_shape_id_by_type(file_path, 3, 'sp')
        print(f"DEBUG: Pictures on slide 3: {pics}")
        print(f"DEBUG: Shapes on slide 3: {shapes}")
    except Exception as e:
        print(f"CRITICAL: Cannot parse slide 3 shapes: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Identify the image and text box
    # The image is a 'pic' element; the text box is an 'sp' that is NOT the title
    image_spid = None
    textbox_spid = None

    for p in pics:
        image_spid = p['id']
        print(f"DEBUG: Image shape: id={p['id']}, name={p['name']}")

    for s in shapes:
        name = s['name'].lower()
        if 'title' not in name and 'textbox' in name:
            # Pick the last textbox (TextBox 4 in our case - the content text box)
            textbox_spid = s['id']
            print(f"DEBUG: Text box candidate: id={s['id']}, name={s['name']}")

    if image_spid is None:
        print("CRITICAL: No image found on slide 3")
        print("REWARD: 0.0")
        return 0.0

    if textbox_spid is None:
        # Fallback: pick any non-title sp
        for s in shapes:
            if 'title' not in s['name'].lower():
                textbox_spid = s['id']
        if textbox_spid is None:
            print("CRITICAL: No text box found on slide 3")
            print("REWARD: 0.0")
            return 0.0

    print(f"DEBUG: Target image spid={image_spid}, textbox spid={textbox_spid}")

    # Parse animations
    try:
        animations = parse_animations(file_path, 3)
        delays = find_animation_delays(file_path, 3)
        print(f"DEBUG: Found {len(animations)} animations")
        print(f"DEBUG: Delays: {delays}")
        for a in animations:
            print(f"DEBUG: Animation: {a}")
    except Exception as e:
        print(f"CRITICAL: Cannot parse animations: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find animations targeting our shapes
    image_anim = None
    text_anim = None
    for a in animations:
        if a['target_spid'] == image_spid:
            image_anim = a
        elif a['target_spid'] == textbox_spid:
            text_anim = a

    # Component 1: Image has Fly In entrance animation (0.25 points)
    # presetID=2 is "Fly In", presetClass="entr" is entrance
    try:
        if image_anim is not None and image_anim['preset_id'] == '2' and image_anim['preset_class'] == 'entr':
            print(f"PASS: Component 1 - Image has Fly In entrance animation (presetID=2, class=entr) (0.25 pts)")
            total_score += 0.25
        else:
            if image_anim is None:
                print(f"FAIL: Component 1 - No animation found for image (spid={image_spid})")
            else:
                print(f"FAIL: Component 1 - Image animation: presetID={image_anim['preset_id']} (expected 2), class={image_anim['preset_class']} (expected entr)")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Fly In direction is from left (0.15 points)
    # presetSubtype=8 means "from left"
    try:
        if image_anim is not None and image_anim['preset_subtype'] == '8':
            print(f"PASS: Component 2 - Fly In from left (presetSubtype=8) (0.15 pts)")
            total_score += 0.15
        else:
            subtype = image_anim['preset_subtype'] if image_anim else 'N/A'
            print(f"FAIL: Component 2 - Image fly in subtype={subtype} (expected 8 for from-left)")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Image animation triggers on click (0.10 points)
    # nodeType="clickEffect"
    try:
        if image_anim is not None and image_anim['node_type'] == 'clickEffect':
            print(f"PASS: Component 3 - Image animation on click (nodeType=clickEffect) (0.10 pts)")
            total_score += 0.10
        else:
            ntype = image_anim['node_type'] if image_anim else 'N/A'
            print(f"FAIL: Component 3 - Image nodeType={ntype} (expected clickEffect)")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Text box has Fade In entrance animation (0.25 points)
    # presetID=10 is "Fade", presetClass="entr" is entrance
    try:
        if text_anim is not None and text_anim['preset_id'] == '10' and text_anim['preset_class'] == 'entr':
            print(f"PASS: Component 4 - Text box has Fade In entrance animation (presetID=10, class=entr) (0.25 pts)")
            total_score += 0.25
        else:
            if text_anim is None:
                print(f"FAIL: Component 4 - No animation found for text box (spid={textbox_spid})")
            else:
                print(f"FAIL: Component 4 - Text animation: presetID={text_anim['preset_id']} (expected 10), class={text_anim['preset_class']} (expected entr)")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Text animation triggers after previous (0.10 points)
    # nodeType="afterEffect"
    try:
        if text_anim is not None and text_anim['node_type'] == 'afterEffect':
            print(f"PASS: Component 5 - Text animation after previous (nodeType=afterEffect) (0.10 pts)")
            total_score += 0.10
        else:
            ntype = text_anim['node_type'] if text_anim else 'N/A'
            print(f"FAIL: Component 5 - Text nodeType={ntype} (expected afterEffect)")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: Text animation has 0.5s delay (0.15 points)
    # delay=500 (milliseconds) on the parent par's cTn stCondLst
    try:
        text_delay = delays.get(textbox_spid, None)
        if text_delay is not None and str(text_delay) == '500':
            print(f"PASS: Component 6 - Text animation delay is 500ms (0.5s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 - Text animation delay={text_delay} (expected 500)")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

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

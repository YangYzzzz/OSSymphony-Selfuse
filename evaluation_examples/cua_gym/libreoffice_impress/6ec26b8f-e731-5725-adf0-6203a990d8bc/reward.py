"""
Reward Script: Verify animation sequence on slide 2
Task ID: impress_ma_082
Domain: libreoffice_impress
Scoring:
  Component 1 (0.25): Title has Fade entrance on click
  Component 2 (0.25): Bullet 1 has Fly In from Right, After Previous, 1s delay
  Component 3 (0.25): Bullet 2 has Fly In from Right, With Previous
  Component 4 (0.25): Bullet 3 has Fly In from Right, With Previous
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ma_082'


def parse_animations(pptx_path, slide_idx=1):
    """
    Parse animation entries from a specific slide (0-indexed).
    Returns a list of dicts with animation properties per shape.
    """
    ns_p = 'http://schemas.openxmlformats.org/presentationml/2006/main'
    animations = []

    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            slide_name = f'ppt/slides/slide{slide_idx + 1}.xml'
            if slide_name not in zf.namelist():
                print(f"FAIL: {slide_name} not found in archive")
                return animations
            with zf.open(slide_name) as f:
                root = ET.parse(f).getroot()
    except Exception as e:
        print(f"ERROR: Cannot parse {pptx_path}: {e}")
        return animations

    # Find all cTn elements with presetID (these are animation effects)
    for elem in root.iter(f'{{{ns_p}}}cTn'):
        preset_id = elem.get('presetID')
        if preset_id is None:
            continue

        preset_class = elem.get('presetClass', '')
        preset_subtype = elem.get('presetSubtype', '')
        node_type = elem.get('nodeType', '')

        # Find target shape ID from child elements
        target_spid = None
        for spTgt in elem.iter(f'{{{ns_p}}}spTgt'):
            target_spid = spTgt.get('spid')
            break

        # Find the parent delay (stCondLst > cond delay on the grandparent cTn)
        # The delay is on the parent par's cTn stCondLst
        parent_delay = None
        parent = None
        # Walk up to find the containing par > cTn with stCondLst
        # We look at the stCondLst of the parent cTn (the wrapper)
        for cond in elem.iter(f'{{{ns_p}}}cond'):
            d = cond.get('delay')
            if d is not None:
                parent_delay = d
                break

        animations.append({
            'presetID': preset_id,
            'presetClass': preset_class,
            'presetSubtype': preset_subtype,
            'nodeType': node_type,
            'target_spid': target_spid,
            'delay': parent_delay,
        })

    return animations


def get_shape_id_text_map(pptx_path, slide_idx=1):
    """
    Return a dict mapping shape id -> shape text for slide (0-indexed).
    """
    ns_p = 'http://schemas.openxmlformats.org/presentationml/2006/main'
    ns_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    shape_map = {}

    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            slide_name = f'ppt/slides/slide{slide_idx + 1}.xml'
            with zf.open(slide_name) as f:
                root = ET.parse(f).getroot()
    except Exception:
        return shape_map

    for sp in root.iter(f'{{{ns_p}}}sp'):
        cNvPr = sp.find(f'.//{{{ns_p}}}cNvPr')
        if cNvPr is not None:
            spid = cNvPr.get('id', '')
            texts = []
            for t in sp.iter(f'{{{ns_a}}}t'):
                if t.text:
                    texts.append(t.text)
            shape_map[spid] = ' '.join(texts).strip()

    return shape_map


def find_animations_with_context(pptx_path, slide_idx=1):
    """
    More robust animation parser that extracts parent delay context.
    Returns list of animation dicts with proper delay from parent cTn.
    """
    ns_p = 'http://schemas.openxmlformats.org/presentationml/2006/main'
    animations = []

    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            slide_name = f'ppt/slides/slide{slide_idx + 1}.xml'
            with zf.open(slide_name) as f:
                content = f.read()
        root = ET.fromstring(content)
    except Exception as e:
        print(f"ERROR: Cannot parse slide: {e}")
        return animations

    # Build parent map for traversal
    parent_map = {}
    for parent in root.iter():
        for child in parent:
            parent_map[child] = parent

    # Find all animation cTn nodes (ones with presetID)
    for ctn in root.iter(f'{{{ns_p}}}cTn'):
        preset_id = ctn.get('presetID')
        if preset_id is None:
            continue

        preset_class = ctn.get('presetClass', '')
        preset_subtype = ctn.get('presetSubtype', '')
        node_type = ctn.get('nodeType', '')

        # Find target shape ID
        target_spid = None
        for spTgt in ctn.iter(f'{{{ns_p}}}spTgt'):
            target_spid = spTgt.get('spid')
            break

        # Find the grandparent delay: go up to find the wrapper cTn's stCondLst delay
        # Structure: par > cTn(wrapper with delay) > childTnLst > par > cTn(this anim)
        # We need to go up: cTn(preset) -> par -> childTnLst -> cTn(wrapper) -> stCondLst -> cond[delay]
        wrapper_delay = '0'
        try:
            par_elem = parent_map.get(ctn)  # <par>
            if par_elem is not None:
                childTnLst = parent_map.get(par_elem)  # <childTnLst>
                if childTnLst is not None:
                    wrapper_ctn = parent_map.get(childTnLst)  # wrapper <cTn>
                    if wrapper_ctn is not None and wrapper_ctn.tag == f'{{{ns_p}}}cTn':
                        stCondLst = wrapper_ctn.find(f'{{{ns_p}}}stCondLst')
                        if stCondLst is not None:
                            cond = stCondLst.find(f'{{{ns_p}}}cond')
                            if cond is not None:
                                wrapper_delay = cond.get('delay', '0')
        except Exception:
            pass

        animations.append({
            'presetID': preset_id,
            'presetClass': preset_class,
            'presetSubtype': preset_subtype,
            'nodeType': node_type,
            'target_spid': target_spid,
            'wrapper_delay': wrapper_delay,
        })

    return animations


def verify_task(file_path):
    """
    Verify animation sequence on slide 2 of the presentation.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Get shape-text mapping for slide 2 (index 1)
    shape_map = get_shape_id_text_map(file_path, slide_idx=1)
    print(f"INFO: Shapes on slide 2: {shape_map}")

    # Identify title and bullet shapes by text content
    title_spid = None
    bullet_spids = []
    for spid, text in shape_map.items():
        if not text:
            continue
        # Title is typically a short heading; bullets are longer content
        lower = text.lower()
        if 'key campaign objectives' in lower or 'objectives' in lower:
            title_spid = spid
        elif any(kw in lower for kw in ['increase brand', 'drive 50,000', 'establish strategic',
                                          'brand awareness', 'qualified leads', 'co-marketing']):
            bullet_spids.append(spid)

    if title_spid is None:
        # Fallback: first shape is title
        if shape_map:
            sorted_ids = sorted(shape_map.keys(), key=lambda x: int(x) if x.isdigit() else 0)
            title_spid = sorted_ids[0] if sorted_ids else None
            bullet_spids = sorted_ids[1:4] if len(sorted_ids) > 1 else []

    print(f"INFO: Title shape id={title_spid}, Bullet shape ids={bullet_spids}")

    # Parse animations
    animations = find_animations_with_context(file_path, slide_idx=1)
    print(f"INFO: Found {len(animations)} animation entries")
    for anim in animations:
        print(f"  Animation: presetID={anim['presetID']} class={anim['presetClass']} "
              f"subtype={anim['presetSubtype']} nodeType={anim['nodeType']} "
              f"target={anim['target_spid']} wrapper_delay={anim['wrapper_delay']}")

    if len(animations) == 0:
        print("FAIL: No animations found on slide 2")
        print("REWARD: 0.0")
        return 0.0

    # Build lookup: target_spid -> animation info
    anim_by_target = {}
    for anim in animations:
        spid = anim.get('target_spid')
        if spid:
            anim_by_target[spid] = anim

    # Component 1: Title has Fade entrance on click (0.25 points)
    # presetID=10 = Fade, presetClass=entr, nodeType=clickEffect
    try:
        title_anim = anim_by_target.get(title_spid)
        if title_anim is not None:
            is_fade = title_anim['presetID'] == '10'
            is_entrance = title_anim['presetClass'] == 'entr'
            is_on_click = title_anim['nodeType'] == 'clickEffect'

            if is_fade and is_entrance and is_on_click:
                print(f"PASS: Component 1 -- Title (spid={title_spid}) has Fade entrance on click (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 -- Title animation: fade={is_fade}, entrance={is_entrance}, "
                      f"onClick={is_on_click}. presetID={title_anim['presetID']}, "
                      f"class={title_anim['presetClass']}, nodeType={title_anim['nodeType']}")
        else:
            print(f"FAIL: Component 1 -- No animation found for title shape (spid={title_spid})")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Components 2-4: Bullet points with Fly In from Right
    # presetID=2 = Fly In, presetSubtype=2 = from right, presetClass=entr
    # Bullet 1: nodeType=afterEffect, wrapper_delay=1000
    # Bullet 2: nodeType=withEffect
    # Bullet 3: nodeType=withEffect

    if len(bullet_spids) < 3:
        print(f"WARN: Expected 3 bullet shapes, found {len(bullet_spids)}")
        # Try to find bullet animations by looking at non-title animations
        non_title_anims = [a for a in animations if a.get('target_spid') != title_spid]
        # Sort by animation order (by target spid as proxy)
        non_title_anims.sort(key=lambda a: int(a.get('target_spid', '0')) if a.get('target_spid', '0').isdigit() else 0)

        # Component 2: First bullet - After Previous with 1s delay (0.25 points)
        try:
            if len(non_title_anims) >= 1:
                b1 = non_title_anims[0]
                is_fly_in = b1['presetID'] == '2'
                is_from_right = b1['presetSubtype'] == '2'
                is_entrance = b1['presetClass'] == 'entr'
                is_after_prev = b1['nodeType'] == 'afterEffect'
                has_delay = b1['wrapper_delay'] == '1000'

                if is_fly_in and is_from_right and is_entrance and is_after_prev and has_delay:
                    print(f"PASS: Component 2 -- Bullet 1 Fly In from Right, After Previous, 1s delay (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 2 -- Bullet 1: flyIn={is_fly_in}, fromRight={is_from_right}, "
                          f"entrance={is_entrance}, afterPrev={is_after_prev}, delay1s={has_delay}")
            else:
                print("FAIL: Component 2 -- No bullet animations found")
        except Exception as e:
            print(f"ERROR: Component 2 -- {e}")

        # Component 3: Second bullet - With Previous (0.25 points)
        try:
            if len(non_title_anims) >= 2:
                b2 = non_title_anims[1]
                is_fly_in = b2['presetID'] == '2'
                is_from_right = b2['presetSubtype'] == '2'
                is_entrance = b2['presetClass'] == 'entr'
                is_with_prev = b2['nodeType'] == 'withEffect'

                if is_fly_in and is_from_right and is_entrance and is_with_prev:
                    print(f"PASS: Component 3 -- Bullet 2 Fly In from Right, With Previous (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 3 -- Bullet 2: flyIn={is_fly_in}, fromRight={is_from_right}, "
                          f"entrance={is_entrance}, withPrev={is_with_prev}")
            else:
                print("FAIL: Component 3 -- Less than 2 bullet animations found")
        except Exception as e:
            print(f"ERROR: Component 3 -- {e}")

        # Component 4: Third bullet - With Previous (0.25 points)
        try:
            if len(non_title_anims) >= 3:
                b3 = non_title_anims[2]
                is_fly_in = b3['presetID'] == '2'
                is_from_right = b3['presetSubtype'] == '2'
                is_entrance = b3['presetClass'] == 'entr'
                is_with_prev = b3['nodeType'] == 'withEffect'

                if is_fly_in and is_from_right and is_entrance and is_with_prev:
                    print(f"PASS: Component 4 -- Bullet 3 Fly In from Right, With Previous (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 4 -- Bullet 3: flyIn={is_fly_in}, fromRight={is_from_right}, "
                          f"entrance={is_entrance}, withPrev={is_with_prev}")
            else:
                print("FAIL: Component 4 -- Less than 3 bullet animations found")
        except Exception as e:
            print(f"ERROR: Component 4 -- {e}")
    else:
        # We have identified bullet shapes by content
        bullet_spids.sort(key=lambda x: int(x) if x.isdigit() else 0)

        # Component 2: First bullet - After Previous with 1s delay (0.25 points)
        try:
            b1_anim = anim_by_target.get(bullet_spids[0])
            if b1_anim is not None:
                is_fly_in = b1_anim['presetID'] == '2'
                is_from_right = b1_anim['presetSubtype'] == '2'
                is_entrance = b1_anim['presetClass'] == 'entr'
                is_after_prev = b1_anim['nodeType'] == 'afterEffect'
                has_delay = b1_anim['wrapper_delay'] == '1000'

                if is_fly_in and is_from_right and is_entrance and is_after_prev and has_delay:
                    print(f"PASS: Component 2 -- Bullet 1 (spid={bullet_spids[0]}) Fly In from Right, After Previous, 1s delay (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 2 -- Bullet 1: flyIn={is_fly_in}, fromRight={is_from_right}, "
                          f"entrance={is_entrance}, afterPrev={is_after_prev}, delay1s={has_delay}")
            else:
                print(f"FAIL: Component 2 -- No animation for bullet 1 (spid={bullet_spids[0]})")
        except Exception as e:
            print(f"ERROR: Component 2 -- {e}")

        # Component 3: Second bullet - With Previous (0.25 points)
        try:
            b2_anim = anim_by_target.get(bullet_spids[1])
            if b2_anim is not None:
                is_fly_in = b2_anim['presetID'] == '2'
                is_from_right = b2_anim['presetSubtype'] == '2'
                is_entrance = b2_anim['presetClass'] == 'entr'
                is_with_prev = b2_anim['nodeType'] == 'withEffect'

                if is_fly_in and is_from_right and is_entrance and is_with_prev:
                    print(f"PASS: Component 3 -- Bullet 2 (spid={bullet_spids[1]}) Fly In from Right, With Previous (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 3 -- Bullet 2: flyIn={is_fly_in}, fromRight={is_from_right}, "
                          f"entrance={is_entrance}, withPrev={is_with_prev}")
            else:
                print(f"FAIL: Component 3 -- No animation for bullet 2 (spid={bullet_spids[1]})")
        except Exception as e:
            print(f"ERROR: Component 3 -- {e}")

        # Component 4: Third bullet - With Previous (0.25 points)
        try:
            b3_anim = anim_by_target.get(bullet_spids[2])
            if b3_anim is not None:
                is_fly_in = b3_anim['presetID'] == '2'
                is_from_right = b3_anim['presetSubtype'] == '2'
                is_entrance = b3_anim['presetClass'] == 'entr'
                is_with_prev = b3_anim['nodeType'] == 'withEffect'

                if is_fly_in and is_from_right and is_entrance and is_with_prev:
                    print(f"PASS: Component 4 -- Bullet 3 (spid={bullet_spids[2]}) Fly In from Right, With Previous (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 4 -- Bullet 3: flyIn={is_fly_in}, fromRight={is_from_right}, "
                          f"entrance={is_entrance}, withPrev={is_with_prev}")
            else:
                print(f"FAIL: Component 4 -- No animation for bullet 3 (spid={bullet_spids[2]})")
        except Exception as e:
            print(f"ERROR: Component 4 -- {e}")

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

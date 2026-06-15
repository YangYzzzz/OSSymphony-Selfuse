"""
Reward Script: Verify entrance animations on slide 1 of Product_Launch.pptx
Task ID: impress_rp_004
Domain: libreoffice_impress
Scoring:
  Component 1 (0.30): Title has Fly In entrance animation from left (presetID=2, presetClass=entr, presetSubtype=4)
  Component 2 (0.20): Subtitle has Fade In entrance animation (presetID=10, presetClass=entr)
  Component 3 (0.20): Image has Wipe entrance animation from bottom (presetID=22, presetClass=entr, presetSubtype=4)
  Component 4 (0.15): Animation sequence order: Title first (clickEffect), Subtitle second (afterEffect), Image third (afterEffect)
  Component 5 (0.15): Subtitle and Image both have 0.5s (500ms) delay after previous
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_rp_004'


def parse_animations(pptx_path, slide_idx=0):
    """
    Parse the animation timing XML from a slide.
    Returns a list of animation dicts with presetID, presetClass, presetSubtype,
    nodeType, target spid, and delay info.
    """
    ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
    animations = []

    with zipfile.ZipFile(pptx_path, 'r') as zf:
        slide_name = f'ppt/slides/slide{slide_idx + 1}.xml'
        try:
            with zf.open(slide_name) as f:
                content = f.read().decode()
        except KeyError:
            print(f"ERROR: {slide_name} not found in archive")
            return animations

    root = ET.fromstring(content)

    # Find the timing element
    timing = root.find('.//{http://schemas.openxmlformats.org/presentationml/2006/main}timing')
    if timing is None:
        print("No timing/animation section found in slide XML")
        return animations

    # Find mainSeq node (contains animation sequence)
    main_seq = None
    for ctn in root.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}cTn'):
        if ctn.get('nodeType') == 'mainSeq':
            main_seq = ctn
            break

    if main_seq is None:
        print("No mainSeq node found in timing")
        return animations

    # Each direct child <par> of mainSeq's childTnLst is one animation entry
    child_tn_lst = main_seq.find('{http://schemas.openxmlformats.org/presentationml/2006/main}childTnLst')
    if child_tn_lst is None:
        return animations

    p_ns = 'http://schemas.openxmlformats.org/presentationml/2006/main'

    for seq_idx, top_par in enumerate(child_tn_lst.findall(f'{{{p_ns}}}par')):
        anim_info = {'sequence': seq_idx + 1}

        # Walk down to find the cTn with presetID (the actual animation node)
        for ctn in top_par.iter(f'{{{p_ns}}}cTn'):
            preset_id = ctn.get('presetID')
            if preset_id:
                anim_info['presetID'] = preset_id
                anim_info['presetClass'] = ctn.get('presetClass', '')
                anim_info['presetSubtype'] = ctn.get('presetSubtype', '')
                anim_info['nodeType'] = ctn.get('nodeType', '')
                break

        # Find target shape ID from spTgt
        for sp_tgt in top_par.iter(f'{{{p_ns}}}spTgt'):
            anim_info['spid'] = sp_tgt.get('spid')
            break

        # Find delay: look for the intermediate par's stCondLst delay
        # The delay is on the second-level par's cTn stCondLst
        pars = list(top_par.iter(f'{{{p_ns}}}par'))
        if len(pars) >= 2:
            # The second par (index 1) usually contains the delay
            inner_par = pars[1]
            inner_ctn = inner_par.find(f'{{{p_ns}}}cTn')
            if inner_ctn is not None:
                st_cond_lst = inner_ctn.find(f'{{{p_ns}}}stCondLst')
                if st_cond_lst is not None:
                    cond = st_cond_lst.find(f'{{{p_ns}}}cond')
                    if cond is not None:
                        anim_info['delay'] = cond.get('delay', '0')

        # Find animEffect filter if present
        for anim_eff in top_par.iter(f'{{{p_ns}}}animEffect'):
            anim_info['filter'] = anim_eff.get('filter', '')
            break

        animations.append(anim_info)

    return animations


def get_shape_name_map(pptx_path, slide_idx=0):
    """Get mapping of shape id -> shape name from slide XML."""
    shape_map = {}
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        slide_name = f'ppt/slides/slide{slide_idx + 1}.xml'
        try:
            with zf.open(slide_name) as f:
                content = f.read().decode()
        except KeyError:
            return shape_map

    root = ET.fromstring(content)
    # Find all cNvPr elements which have id and name
    for elem in root.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}cNvPr'):
        shape_map[elem.get('id')] = elem.get('name', '')
    for elem in root.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}cNvPr'):
        shape_map[elem.get('id')] = elem.get('name', '')
    # Also from the pml namespace
    p_ns = 'http://schemas.openxmlformats.org/presentationml/2006/main'
    for sp in root.iter(f'{{{p_ns}}}nvSpPr'):
        cnv = sp.find(f'{{{p_ns}}}cNvPr')
        if cnv is not None:
            shape_map[cnv.get('id')] = cnv.get('name', '')
    for sp in root.iter(f'{{{p_ns}}}nvPicPr'):
        cnv = sp.find(f'{{{p_ns}}}cNvPr')
        if cnv is not None:
            shape_map[cnv.get('id')] = cnv.get('name', '')

    return shape_map


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Parse animations from slide 1
    try:
        animations = parse_animations(file_path, slide_idx=0)
        shape_map = get_shape_name_map(file_path, slide_idx=0)
    except Exception as e:
        print(f"CRITICAL: Cannot parse file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found {len(animations)} animation(s) on slide 1")
    for a in animations:
        name = shape_map.get(a.get('spid', ''), 'unknown')
        print(f"  Seq {a.get('sequence')}: spid={a.get('spid')} ({name}), "
              f"presetID={a.get('presetID')}, presetClass={a.get('presetClass')}, "
              f"presetSubtype={a.get('presetSubtype')}, nodeType={a.get('nodeType')}, "
              f"delay={a.get('delay', 'N/A')}, filter={a.get('filter', 'N/A')}")

    # Need at least 3 animations to proceed
    if len(animations) < 3:
        print(f"FAIL: Expected at least 3 animations, found {len(animations)}")
        print(f"REWARD: {total_score}")
        return total_score

    # Build lookup: find animations targeting title (spid 3), subtitle (spid 4), image (spid 5)
    # Also match by shape name in case spids differ
    title_anim = None
    subtitle_anim = None
    image_anim = None

    for a in animations:
        spid = a.get('spid', '')
        name = shape_map.get(spid, '').lower()
        if spid == '3' or 'title' in name and 'sub' not in name:
            if title_anim is None:
                title_anim = a
        elif spid == '4' or 'subtitle' in name or 'sub' in name:
            if subtitle_anim is None:
                subtitle_anim = a
        elif spid == '5' or 'image' in name or 'product' in name or 'picture' in name:
            if image_anim is None:
                image_anim = a

    # Component 1: Title has Fly In entrance animation from left (0.30 points)
    # presetID=2 = Fly In, presetClass=entr = entrance, presetSubtype=4 = from left
    try:
        if title_anim is not None:
            pid = title_anim.get('presetID', '')
            pclass = title_anim.get('presetClass', '')
            psub = title_anim.get('presetSubtype', '')
            if pid == '2' and pclass == 'entr' and psub == '4':
                print(f"PASS: Component 1 - Title has Fly In entrance from left (presetID=2, class=entr, sub=4) (0.30 pts)")
                total_score += 0.30
            elif pid == '2' and pclass == 'entr':
                # Fly In but wrong direction - partial credit
                print(f"PARTIAL: Component 1 - Title has Fly In entrance but wrong direction (subtype={psub}, expected 4) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 - Title animation: presetID={pid} (expected 2), class={pclass} (expected entr), sub={psub} (expected 4)")
        else:
            print("FAIL: Component 1 - No animation found targeting the title shape")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Subtitle has Fade In entrance animation (0.20 points)
    # presetID=10 = Fade, presetClass=entr = entrance
    try:
        if subtitle_anim is not None:
            pid = subtitle_anim.get('presetID', '')
            pclass = subtitle_anim.get('presetClass', '')
            if pid == '10' and pclass == 'entr':
                print(f"PASS: Component 2 - Subtitle has Fade In entrance (presetID=10, class=entr) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 - Subtitle animation: presetID={pid} (expected 10), class={pclass} (expected entr)")
        else:
            print("FAIL: Component 2 - No animation found targeting the subtitle shape")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Image has Wipe entrance animation from bottom (0.20 points)
    # presetID=22 = Wipe, presetClass=entr = entrance, presetSubtype=4 = from bottom
    try:
        if image_anim is not None:
            pid = image_anim.get('presetID', '')
            pclass = image_anim.get('presetClass', '')
            psub = image_anim.get('presetSubtype', '')
            if pid == '22' and pclass == 'entr' and psub == '4':
                print(f"PASS: Component 3 - Image has Wipe entrance from bottom (presetID=22, class=entr, sub=4) (0.20 pts)")
                total_score += 0.20
            elif pid == '22' and pclass == 'entr':
                print(f"PARTIAL: Component 3 - Image has Wipe entrance but wrong direction (subtype={psub}, expected 4) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 - Image animation: presetID={pid} (expected 22), class={pclass} (expected entr), sub={psub} (expected 4)")
        else:
            print("FAIL: Component 3 - No animation found targeting the image shape")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Animation sequence order (0.15 points)
    # Title = seq 1 with clickEffect, Subtitle = seq 2 with afterEffect, Image = seq 3 with afterEffect
    try:
        if title_anim and subtitle_anim and image_anim:
            t_seq = title_anim.get('sequence', 0)
            s_seq = subtitle_anim.get('sequence', 0)
            i_seq = image_anim.get('sequence', 0)
            t_type = title_anim.get('nodeType', '')
            s_type = subtitle_anim.get('nodeType', '')
            i_type = image_anim.get('nodeType', '')

            order_correct = (t_seq < s_seq < i_seq)
            type_correct = (t_type == 'clickEffect' and s_type == 'afterEffect' and i_type == 'afterEffect')

            if order_correct and type_correct:
                print(f"PASS: Component 4 - Correct sequence order (Title={t_seq}/click, Subtitle={s_seq}/after, Image={i_seq}/after) (0.15 pts)")
                total_score += 0.15
            elif order_correct:
                print(f"PARTIAL: Component 4 - Correct order but wrong start types (title={t_type}, sub={s_type}, img={i_type}) (0.07 pts)")
                total_score += 0.07
            else:
                print(f"FAIL: Component 4 - Wrong sequence: Title seq={t_seq}, Subtitle seq={s_seq}, Image seq={i_seq}")
        else:
            print("FAIL: Component 4 - Missing animations, cannot verify sequence")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Subtitle and Image delays are 500ms (0.5s after previous) (0.15 points)
    try:
        if subtitle_anim and image_anim:
            s_delay = subtitle_anim.get('delay', '0')
            i_delay = image_anim.get('delay', '0')

            s_ok = (s_delay == '500')
            i_ok = (i_delay == '500')

            if s_ok and i_ok:
                print(f"PASS: Component 5 - Subtitle delay={s_delay}ms, Image delay={i_delay}ms (both 500ms) (0.15 pts)")
                total_score += 0.15
            elif s_ok or i_ok:
                print(f"PARTIAL: Component 5 - Subtitle delay={s_delay}ms (want 500), Image delay={i_delay}ms (want 500) (0.07 pts)")
                total_score += 0.07
            else:
                print(f"FAIL: Component 5 - Subtitle delay={s_delay}ms, Image delay={i_delay}ms (both should be 500)")
        else:
            print("FAIL: Component 5 - Missing animations, cannot verify delays")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook for LibreOffice Impress
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_impress")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
persist_app_state()

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

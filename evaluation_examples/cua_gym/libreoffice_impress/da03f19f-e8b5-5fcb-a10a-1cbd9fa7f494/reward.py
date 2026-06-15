"""
Reward Script: Reorder animations on slide 3 - chart first, then title, then bullet list
Task ID: impress_ma_068
Domain: libreoffice_impress
Scoring:
  Component 1 (0.4): First animation targets Chart (spid=5) with Wipe (presetID=22)
  Component 2 (0.3): Second animation targets Title (spid=3) with Fade In (presetID=10)
  Component 3 (0.3): Third animation targets Bullet List (spid=4) with Appear (presetID=1)
"""

import os
import time
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ma_068'

# Persistence hook: save any unsaved GUI state
def persist_app_state():
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_impress")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def extract_animation_sequence(pptx_path, slide_idx):
    """
    Extract the animation sequence from a slide's XML.
    Returns list of dicts: [{spid, presetID, presetClass, filter}, ...]
    in the order they appear in the mainSeq childTnLst.
    """
    ns_p = 'http://schemas.openxmlformats.org/presentationml/2006/main'
    ns_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'

    animations = []
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        slide_name = f'ppt/slides/slide{slide_idx + 1}.xml'
        try:
            with zf.open(slide_name) as f:
                root = ET.parse(f).getroot()
        except KeyError:
            print(f"ERROR: {slide_name} not found in archive")
            return animations

    # Find the timing element
    timing = root.find(f'.//{{{ns_p}}}timing')
    if timing is None:
        print("ERROR: No timing element found in slide")
        return animations

    # Find mainSeq node (nodeType="mainSeq")
    main_seq = None
    for ctn in root.iter(f'{{{ns_p}}}cTn'):
        if ctn.get('nodeType') == 'mainSeq':
            main_seq = ctn
            break

    if main_seq is None:
        print("ERROR: No mainSeq found in timing")
        return animations

    # The direct children of mainSeq's childTnLst are the click-group <p:par> elements
    child_list = main_seq.find(f'{{{ns_p}}}childTnLst')
    if child_list is None:
        print("ERROR: mainSeq has no childTnLst")
        return animations

    for click_par in child_list.findall(f'{{{ns_p}}}par'):
        # Each click_par contains nested par elements down to the actual animation cTn
        # Find the deepest cTn with presetID attribute
        anim_info = {}
        for ctn in click_par.iter(f'{{{ns_p}}}cTn'):
            preset_id = ctn.get('presetID')
            if preset_id:
                anim_info['presetID'] = preset_id
                anim_info['presetClass'] = ctn.get('presetClass', '')
                anim_info['presetSubtype'] = ctn.get('presetSubtype', '')
                anim_info['nodeType'] = ctn.get('nodeType', '')
                break

        # Find spTgt to get the target shape ID
        for sp_tgt in click_par.iter(f'{{{ns_p}}}spTgt'):
            anim_info['spid'] = sp_tgt.get('spid')
            break

        # Find animEffect filter if present
        for anim_eff in click_par.iter(f'{{{ns_p}}}animEffect'):
            anim_info['filter'] = anim_eff.get('filter', '')
            break

        if 'spid' in anim_info and 'presetID' in anim_info:
            animations.append(anim_info)

    return animations


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Extract animation sequence from slide 3 (0-indexed: 2)
    try:
        animations = extract_animation_sequence(file_path, 2)
    except Exception as e:
        print(f"CRITICAL: Cannot parse animations from {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found {len(animations)} animations on slide 3:")
    for i, anim in enumerate(animations):
        print(f"  [{i+1}] spid={anim.get('spid')} presetID={anim.get('presetID')} "
              f"presetClass={anim.get('presetClass')} filter={anim.get('filter', 'N/A')}")

    if len(animations) < 3:
        print(f"FAIL: Expected 3 animations, found {len(animations)}")
        print("REWARD: 0.0")
        return 0.0

    # Expected golden order:
    #   1st: Chart (spid=5), Wipe (presetID=22)
    #   2nd: Title (spid=3), Fade In (presetID=10)
    #   3rd: Bullet List (spid=4), Appear (presetID=1)

    # Component 1: First animation is Chart with Wipe (0.4 points)
    try:
        anim1 = animations[0]
        is_chart_first = (anim1.get('spid') == '5' and anim1.get('presetID') == '22')
        if is_chart_first:
            print(f"PASS: Component 1 -- First animation is Chart (spid=5) with Wipe (presetID=22) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- Expected first animation: spid=5, presetID=22; "
                  f"found spid={anim1.get('spid')}, presetID={anim1.get('presetID')}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Second animation is Title with Fade In (0.3 points)
    try:
        anim2 = animations[1]
        is_title_second = (anim2.get('spid') == '3' and anim2.get('presetID') == '10')
        if is_title_second:
            print(f"PASS: Component 2 -- Second animation is Title (spid=3) with Fade In (presetID=10) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- Expected second animation: spid=3, presetID=10; "
                  f"found spid={anim2.get('spid')}, presetID={anim2.get('presetID')}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Third animation is Bullet List with Appear (0.3 points)
    try:
        anim3 = animations[2]
        is_bullets_third = (anim3.get('spid') == '4' and anim3.get('presetID') == '1')
        if is_bullets_third:
            print(f"PASS: Component 3 -- Third animation is Bullet List (spid=4) with Appear (presetID=1) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 -- Expected third animation: spid=4, presetID=1; "
                  f"found spid={anim3.get('spid')}, presetID={anim3.get('presetID')}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved state before verification
persist_app_state()

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

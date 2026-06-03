"""
Reward Script: Add 0.5-second delay between animations on slide 4
Task ID: impress_fix_061
Domain: libreoffice_impress
Scoring:
  Component 1 (0.5 pts): Animations 2-5 have nodeType="afterEffect" (changed from "withEffect")
  Component 2 (0.5 pts): Animations 2-5 have delay=500 on parent par element
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_fix_061'

# Namespace for PresentationML
NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}


def parse_animation_nodes(pptx_path, slide_num=4):
    """
    Parse the animation timing XML for a given slide.
    Returns a list of dicts, one per animation, with keys:
      - preset_id: the presetID attribute
      - preset_class: the presetClass attribute (e.g. 'entr')
      - node_type: the nodeType attribute (e.g. 'clickEffect', 'withEffect', 'afterEffect')
      - parent_delay: the delay on the grandparent <par> element's stCondLst/cond
      - spid: target shape ID
    """
    animations = []
    slide_path = f'ppt/slides/slide{slide_num}.xml'

    with zipfile.ZipFile(pptx_path, 'r') as zf:
        with zf.open(slide_path) as f:
            root = ET.fromstring(f.read())

    # Navigate: timing > tnLst > par > cTn > childTnLst > seq > cTn > childTnLst
    # Each child <par> in mainSeq's childTnLst is one animation group
    timing = root.find('.//p:timing', NS)
    if timing is None:
        print("FAIL: No timing element found in slide 4")
        return animations

    # Find the mainSeq node
    main_seq_ctn = None
    for seq in timing.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}seq'):
        ctn = seq.find('p:cTn', NS)
        if ctn is not None and ctn.get('nodeType') == 'mainSeq':
            main_seq_ctn = ctn
            break

    if main_seq_ctn is None:
        print("FAIL: No mainSeq found in timing")
        return animations

    child_list = main_seq_ctn.find('p:childTnLst', NS)
    if child_list is None:
        print("FAIL: No childTnLst in mainSeq")
        return animations

    # Each direct <par> child represents one animation group
    for group_par in child_list.findall('p:par', NS):
        group_ctn = group_par.find('p:cTn', NS)
        if group_ctn is None:
            continue

        # Get the delay on this group's stCondLst
        parent_delay = "0"
        st_cond_list = group_ctn.find('p:stCondLst', NS)
        if st_cond_list is not None:
            cond = st_cond_list.find('p:cond', NS)
            if cond is not None:
                parent_delay = cond.get('delay', '0')

        # Drill down to find the actual animation cTn with presetID
        # Structure: group_par > cTn > childTnLst > par > cTn > childTnLst > par > cTn (with presetID)
        anim_ctn = None
        for ctn_elem in group_par.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}cTn'):
            if ctn_elem.get('presetID') is not None:
                anim_ctn = ctn_elem
                break

        if anim_ctn is None:
            continue

        # Find target shape ID
        spid = None
        for sp_tgt in anim_ctn.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}spTgt'):
            spid = sp_tgt.get('spid')
            break

        animations.append({
            'preset_id': anim_ctn.get('presetID'),
            'preset_class': anim_ctn.get('presetClass'),
            'node_type': anim_ctn.get('nodeType', 'unknown'),
            'parent_delay': parent_delay,
            'spid': spid,
        })

    return animations


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Parse animations on slide 4
    try:
        animations = parse_animation_nodes(file_path, slide_num=4)
    except Exception as e:
        print(f"CRITICAL: Cannot parse animations: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must have exactly 5 animations
    if len(animations) != 5:
        print(f"FAIL: Expected 5 animations on slide 4, found {len(animations)}")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(animations)} animations on slide 4")
    for i, anim in enumerate(animations):
        print(f"  Anim {i+1}: nodeType={anim['node_type']}, parent_delay={anim['parent_delay']}, "
              f"spid={anim['spid']}, presetID={anim['preset_id']}, presetClass={anim['preset_class']}")

    # Component 1: Animations 2-5 should have nodeType="afterEffect" (0.5 points)
    # In the initial state they are "withEffect". This is the core timing change.
    try:
        after_count = 0
        for i in range(1, 5):  # animations index 1-4 (2nd through 5th)
            anim = animations[i]
            if anim['node_type'] == 'afterEffect':
                after_count += 1
            else:
                print(f"FAIL: Animation {i+1} nodeType={anim['node_type']}, expected 'afterEffect'")

        if after_count == 4:
            print(f"PASS: Component 1 -- All 4 subsequent animations have nodeType='afterEffect' (0.5 pts)")
            total_score += 0.5
        elif after_count > 0:
            partial = 0.5 * (after_count / 4)
            print(f"PARTIAL: Component 1 -- {after_count}/4 animations have 'afterEffect' ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 -- No animations changed to 'afterEffect' (0 pts)")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Animations 2-5 should have parent delay=500 (0.5 seconds = 500ms) (0.5 points)
    # In the initial state they all have delay="0".
    try:
        delay_count = 0
        for i in range(1, 5):  # animations index 1-4
            anim = animations[i]
            try:
                delay_val = int(anim['parent_delay'])
            except (ValueError, TypeError):
                delay_val = 0

            if delay_val == 500:
                delay_count += 1
            else:
                print(f"FAIL: Animation {i+1} parent_delay={anim['parent_delay']}, expected '500'")

        if delay_count == 4:
            print(f"PASS: Component 2 -- All 4 subsequent animations have 500ms delay (0.5 pts)")
            total_score += 0.5
        elif delay_count > 0:
            partial = 0.5 * (delay_count / 4)
            print(f"PARTIAL: Component 2 -- {delay_count}/4 animations have 500ms delay ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- No animations have 500ms delay (0 pts)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

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

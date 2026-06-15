"""
Reward Script: Sequential Wipe Entrance Animations on Slide 5
Task ID: impress_anim_060
Domain: libreoffice_impress
Scoring:
  Component 1: 5 Wipe entrance animations exist on slide 5 (0.4 pts)
  Component 2: All 5 animations triggered After Previous with 0.20s delay (0.3 pts)
  Component 3: Animations target M1-M5 milestone shapes in correct order (0.3 pts)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user/Desktop'
TASK_ID = 'impress_anim_060'

# Shape IDs for M1-M5 on slide 5 (confirmed via exploration)
MILESTONE_SHAPE_IDS = ['5', '7', '9', '11', '13']  # M1, M2, M3, M4, M5 respectively


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Build a sequential reveal on slide 5 with 5 Wipe entrance animations,
    each triggered After Previous with a 0.2-second delay, in order M1->M5.
    """
    total_score = 0.0

    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            slide_files = [n for n in zf.namelist() if n.startswith('ppt/slides/slide')]
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Verify the file has at least 5 slides (slide 5 = slide5.xml)
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            slide5_name = 'ppt/slides/slide5.xml'
            if slide5_name not in zf.namelist():
                print("FAIL: slide5.xml not found in presentation")
                print("REWARD: 0.0")
                return 0.0
            with zf.open(slide5_name) as f:
                content = f.read().decode('utf-8')
    except Exception as e:
        print(f"CRITICAL: Cannot read slide5.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    }

    try:
        root = ET.fromstring(content)
    except Exception as e:
        print(f"CRITICAL: Cannot parse slide5.xml XML: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Gate: Check timing element exists at all
    timing = root.find('.//p:timing', ns)
    if timing is None:
        print("FAIL: No timing element found on slide 5 — no animations present")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 1: Exactly 5 Wipe entrance animations on slide 5 (0.4 points)
    # Wipe animations use animEffect with filter containing "wipe"
    try:
        anim_effects = root.findall('.//p:animEffect', ns)
        wipe_effects = [ae for ae in anim_effects
                        if ae.get('filter') is not None and 'wipe' in ae.get('filter', '').lower()
                        and ae.get('transition') == 'in']
        if len(wipe_effects) == 5:
            print(f"PASS: Component 1 — Found exactly 5 Wipe entrance (animEffect filter=wipe*) animations (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Expected 5 Wipe entrance animations, found {len(wipe_effects)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 5 animations have nodeType=afterPrev with delay=200ms (0.3 points)
    # Each main animation container should have nodeType="afterPrev" and stCondLst/cond[@delay="200"]
    try:
        all_cTns = root.findall('.//p:cTn', ns)
        # Find outer-level animation containers with grpId and nodeType="afterPrev"
        after_prev_containers = []
        for cTn in all_cTns:
            grpId = cTn.get('grpId')
            nodeType = cTn.get('nodeType')
            if grpId is not None and nodeType == 'afterPrev':
                cond = cTn.find('p:stCondLst/p:cond', ns)
                delay = cond.get('delay') if cond is not None else None
                after_prev_containers.append({
                    'grpId': grpId,
                    'nodeType': nodeType,
                    'delay': delay
                })

        # Check all 5 milestone animations are afterPrev with 200ms delay
        correct_triggers = [c for c in after_prev_containers if c['delay'] == '200']
        if len(correct_triggers) == 5:
            print(f"PASS: Component 2 — All 5 animations have nodeType=afterPrev with delay=200ms (0.3 pts)")
            total_score += 0.3
        else:
            afterprev_count = len(after_prev_containers)
            print(f"FAIL: Component 2 — Expected 5 afterPrev/200ms triggers, "
                  f"found {afterprev_count} afterPrev containers, {len(correct_triggers)} with 200ms delay")
            # Detail each
            for c in after_prev_containers:
                print(f"  grpId={c['grpId']} nodeType={c['nodeType']} delay={c['delay']}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Animations target M1-M5 shapes in correct sequential order (0.3 points)
    # Target shape IDs in order: 5 (M1), 7 (M2), 9 (M3), 11 (M4), 13 (M5)
    try:
        # Collect animation targets in order of grpId (0, 1, 2, 3, 4)
        # For each grpId, find the clickEffect cTn with a spTgt
        anim_targets_by_grp = {}
        for cTn in all_cTns:
            grpId = cTn.get('grpId')
            nodeType = cTn.get('nodeType')
            if grpId is not None and nodeType == 'clickEffect':
                spTgt = cTn.find('.//p:spTgt', ns)
                if spTgt is not None:
                    spid = spTgt.get('spid')
                    if grpId not in anim_targets_by_grp:
                        anim_targets_by_grp[grpId] = spid

        # Sort by grpId numerically to get order
        ordered_targets = [anim_targets_by_grp[gid]
                           for gid in sorted(anim_targets_by_grp.keys(), key=int)
                           if gid in anim_targets_by_grp]

        if ordered_targets == MILESTONE_SHAPE_IDS:
            print(f"PASS: Component 3 — Animations target M1-M5 shapes in correct order "
                  f"(spids: {ordered_targets}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Expected animation targets {MILESTONE_SHAPE_IDS} in order, "
                  f"found {ordered_targets}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

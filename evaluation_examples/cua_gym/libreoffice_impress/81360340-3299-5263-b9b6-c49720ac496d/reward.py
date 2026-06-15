"""
Reward Script: Add exit animations to all objects on slide 9
Task ID: impress_fix_063
Domain: libreoffice_impress
Scoring:
  Component 1 (0.25): Exit animations exist for all 4 target objects
  Component 2 (0.25): Exit animations use Fade Out effect (presetID=10, filter=fade)
  Component 3 (0.25): Exit animations have 3-second delay (delay=3000)
  Component 4 (0.25): Exit animations are interleaved correctly after entrance anims
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_fix_063'

# Target shape IDs on slide 9 (Picture, TextBox, Rounded Rectangle, Right Arrow)
TARGET_SPIDS = {'3', '4', '5', '6'}
SLIDE_INDEX = 9  # 1-based


def parse_animations(pptx_path, slide_num):
    """
    Parse the animation timeline from slide XML.
    Returns a list of animation dicts with keys:
      preset_id, preset_class, spid, delay, node_type, filter_type
    """
    ns = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    }
    animations = []

    with zipfile.ZipFile(pptx_path, 'r') as zf:
        slide_xml = f'ppt/slides/slide{slide_num}.xml'
        if slide_xml not in zf.namelist():
            print(f"ERROR: {slide_xml} not found in archive")
            return animations

        with zf.open(slide_xml) as f:
            root = ET.parse(f).getroot()

    # Find the mainSeq node: p:timing/p:tnLst/p:par/p:cTn/p:childTnLst/p:seq/p:cTn[@nodeType='mainSeq']
    # Then iterate its child p:par elements which each contain one animation
    timing = root.find('.//p:timing', ns)
    if timing is None:
        print("No timing element found on slide")
        return animations

    # Find all p:cTn elements that have presetClass attribute (these are animation nodes)
    for ctn in timing.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}cTn'):
        preset_class = ctn.get('presetClass')
        if preset_class is None:
            continue

        preset_id = ctn.get('presetID')
        node_type = ctn.get('nodeType', '')

        # Get delay from start condition
        delay = None
        st_cond_lst = ctn.find('p:stCondLst', ns)
        if st_cond_lst is not None:
            cond = st_cond_lst.find('p:cond', ns)
            if cond is not None:
                delay = cond.get('delay')

        # Get target shape ID from child elements
        spid = None
        filter_type = None

        for child in ctn.iter():
            tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag

            # Find spTgt for shape ID
            if tag == 'spTgt' and spid is None:
                spid = child.get('spid')

            # Find animEffect for filter type
            if tag == 'animEffect':
                filter_type = child.get('filter')

        anim = {
            'preset_id': preset_id,
            'preset_class': preset_class,
            'spid': spid,
            'delay': delay,
            'node_type': node_type,
            'filter_type': filter_type,
        }
        animations.append(anim)

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

    try:
        animations = parse_animations(file_path, SLIDE_INDEX)
    except Exception as e:
        print(f"CRITICAL: Cannot parse animations from {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found {len(animations)} animation nodes on slide {SLIDE_INDEX}")
    for i, a in enumerate(animations):
        print(f"  Anim {i}: class={a['preset_class']}, id={a['preset_id']}, "
              f"spid={a['spid']}, delay={a['delay']}, node={a['node_type']}, "
              f"filter={a['filter_type']}")

    # Separate entrance and exit animations
    entrance_anims = [a for a in animations if a['preset_class'] == 'entr']
    exit_anims = [a for a in animations if a['preset_class'] == 'exit']

    print(f"\nEntrance animations: {len(entrance_anims)}")
    print(f"Exit animations: {len(exit_anims)}")

    # Component 1: Exit animations exist for all 4 target objects (0.25 points)
    # This FAILS on initial (no exit anims) and PASSES on golden (4 exit anims)
    try:
        exit_spids = {a['spid'] for a in exit_anims if a['spid'] is not None}
        missing_exit = TARGET_SPIDS - exit_spids
        if len(missing_exit) == 0:
            print(f"PASS: Component 1 - All 4 target objects have exit animations (spids: {exit_spids}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 - Missing exit animations for spids: {missing_exit}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Exit animations use Fade Out effect (presetID=10, filter=fade) (0.25 points)
    # This FAILS on initial (no exit anims) and PASSES on golden
    try:
        fade_exit_count = 0
        for a in exit_anims:
            if a['spid'] in TARGET_SPIDS:
                if a['preset_id'] == '10' and a['filter_type'] == 'fade':
                    fade_exit_count += 1
                else:
                    print(f"  Non-fade exit for spid {a['spid']}: presetID={a['preset_id']}, filter={a['filter_type']}")

        if fade_exit_count == 4:
            print(f"PASS: Component 2 - All 4 exit animations use Fade Out (presetID=10, filter=fade) (0.25 pts)")
            total_score += 0.25
        elif fade_exit_count > 0:
            partial = 0.25 * (fade_exit_count / 4)
            print(f"PARTIAL: Component 2 - {fade_exit_count}/4 exit animations use Fade Out ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - No exit animations use Fade Out effect")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Exit animations have 3-second delay (delay=3000) (0.25 points)
    # This FAILS on initial (no exit anims) and PASSES on golden
    try:
        correct_delay_count = 0
        for a in exit_anims:
            if a['spid'] in TARGET_SPIDS:
                if a['delay'] == '3000':
                    correct_delay_count += 1
                else:
                    print(f"  Wrong delay for spid {a['spid']}: delay={a['delay']} (expected 3000)")

        if correct_delay_count == 4:
            print(f"PASS: Component 3 - All 4 exit animations have 3-second delay (0.25 pts)")
            total_score += 0.25
        elif correct_delay_count > 0:
            partial = 0.25 * (correct_delay_count / 4)
            print(f"PARTIAL: Component 3 - {correct_delay_count}/4 exit animations have correct delay ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 - No exit animations have 3-second delay")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Exit animations are properly sequenced (afterEffect, interleaved) (0.25 points)
    # Check that exit anims appear AFTER their corresponding entrance anim in the sequence
    # and that they use afterEffect nodeType
    # This FAILS on initial (no exit anims) and PASSES on golden
    try:
        # Build ordered list of (preset_class, spid) from all animations
        anim_sequence = [(a['preset_class'], a['spid']) for a in animations]
        print(f"\nAnimation sequence: {anim_sequence}")

        interleave_ok = 0
        after_effect_ok = 0

        for spid in TARGET_SPIDS:
            # Find indices of entrance and exit for this spid
            entr_indices = [i for i, (cls, sid) in enumerate(anim_sequence) if cls == 'entr' and sid == spid]
            exit_indices = [i for i, (cls, sid) in enumerate(anim_sequence) if cls == 'exit' and sid == spid]

            if entr_indices and exit_indices:
                # Exit should come after entrance
                if exit_indices[0] > entr_indices[0]:
                    interleave_ok += 1

            # Check node_type is afterEffect for exit anims
            for a in exit_anims:
                if a['spid'] == spid and a['node_type'] == 'afterEffect':
                    after_effect_ok += 1
                    break

        # Both conditions: correct order (4/4) and afterEffect (4/4)
        sequence_score = 0.0
        if interleave_ok == 4:
            sequence_score += 0.125
            print(f"PASS: Component 4a - All exit anims follow their entrance anims (0.125 pts)")
        else:
            print(f"FAIL: Component 4a - Only {interleave_ok}/4 exits follow entrances")

        if after_effect_ok == 4:
            sequence_score += 0.125
            print(f"PASS: Component 4b - All exit anims use afterEffect trigger (0.125 pts)")
        else:
            print(f"FAIL: Component 4b - Only {after_effect_ok}/4 exit anims use afterEffect")

        if sequence_score > 0:
            total_score += sequence_score

    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

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

"""
Reward Script: Add Wipe transition (left-to-right) on slides 2-8 with 0.75s duration
Task ID: impress_stu_029
Domain: libreoffice_impress
Scoring:
  Component 1 (0.50): Slides 2-8 have wipe transitions with correct direction
  Component 2 (0.30): Slides 2-8 have correct duration (750ms / 0.75s)
  Component 3 (0.20): Slides 1 and 9 have NO transitions
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_stu_029'

NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_P14 = 'http://schemas.microsoft.com/office/powerpoint/2010/main'


def get_transition_info(zf, slide_num):
    """
    Parse transition element from a slide XML.
    Returns dict with 'has_transition', 'type', 'dir', 'duration_ms' or None values.
    slide_num is 1-based.
    """
    info = {'has_transition': False, 'type': None, 'dir': None, 'duration_ms': None}
    try:
        with zf.open(f'ppt/slides/slide{slide_num}.xml') as f:
            root = ET.parse(f).getroot()
            tr = root.find(f'.//{{{NS_P}}}transition')
            if tr is None:
                return info
            info['has_transition'] = True

            # Duration: check both standard 'spd'/'dur' and p14:dur
            # p14:dur is in milliseconds
            dur_p14 = tr.attrib.get(f'{{{NS_P14}}}dur')
            if dur_p14 is not None:
                info['duration_ms'] = int(dur_p14)

            # Standard dur attribute (also milliseconds in some implementations)
            dur_std = tr.attrib.get('dur')
            if dur_std is not None and info['duration_ms'] is None:
                info['duration_ms'] = int(dur_std)

            # Check for wipe child element
            wipe = tr.find(f'{{{NS_P}}}wipe')
            if wipe is not None:
                info['type'] = 'wipe'
                # dir attribute: default is 'l' (left = left-to-right)
                info['dir'] = wipe.attrib.get('dir', 'l')

            # Check other transition types
            if info['type'] is None:
                for child in tr:
                    tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                    info['type'] = tag
                    break

    except Exception as e:
        print(f"ERROR: Could not parse slide{slide_num}.xml: {e}")

    return info


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

    # Gather transition info for all 9 slides
    slide_info = {}
    for i in range(1, 10):
        slide_info[i] = get_transition_info(zf, i)
        print(f"  Slide {i}: transition={slide_info[i]['has_transition']}, "
              f"type={slide_info[i]['type']}, dir={slide_info[i]['dir']}, "
              f"dur={slide_info[i]['duration_ms']}ms")

    zf.close()

    # Component 1: Slides 2-8 have wipe transitions with left-to-right direction (0.50 points)
    # Each slide contributes ~0.0714 points
    try:
        comp1_score = 0.0
        wipe_slides_pass = 0
        for slide_num in range(2, 9):  # slides 2-8
            info = slide_info[slide_num]
            if info['has_transition'] and info['type'] == 'wipe':
                # Direction: 'l' = left-to-right (default), which is what task asks for
                if info['dir'] in ('l', None):
                    wipe_slides_pass += 1

        if wipe_slides_pass == 7:
            comp1_score = 0.50
            print(f"PASS: Component 1 -- All 7 slides (2-8) have wipe transition, left-to-right (0.50 pts)")
        elif wipe_slides_pass > 0:
            comp1_score = round(0.50 * (wipe_slides_pass / 7), 2)
            print(f"PARTIAL: Component 1 -- {wipe_slides_pass}/7 slides have correct wipe transition ({comp1_score} pts)")
        else:
            print(f"FAIL: Component 1 -- No slides have wipe transition with correct direction")
        total_score += comp1_score
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Slides 2-8 have correct duration of 750ms (0.30 points)
    # Each slide contributes ~0.0429 points
    try:
        comp2_score = 0.0
        dur_slides_pass = 0
        for slide_num in range(2, 9):  # slides 2-8
            info = slide_info[slide_num]
            if info['has_transition'] and info['duration_ms'] == 750:
                dur_slides_pass += 1

        if dur_slides_pass == 7:
            comp2_score = 0.30
            print(f"PASS: Component 2 -- All 7 slides (2-8) have 750ms duration (0.30 pts)")
        elif dur_slides_pass > 0:
            comp2_score = round(0.30 * (dur_slides_pass / 7), 2)
            print(f"PARTIAL: Component 2 -- {dur_slides_pass}/7 slides have correct duration ({comp2_score} pts)")
        else:
            print(f"FAIL: Component 2 -- No slides have 750ms duration")
        total_score += comp2_score
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Selective application -- slides 2-8 have transitions while slides 1 and 9 do NOT (0.20 points)
    # This verifies the agent correctly applied transitions only to the specified range.
    # Gate: at least one slide in 2-8 must have a transition (prevents scoring on initial state where nothing has transitions)
    try:
        comp3_score = 0.0
        any_transition_in_range = any(slide_info[i]['has_transition'] for i in range(2, 9))

        if any_transition_in_range:
            if not slide_info[1]['has_transition']:
                comp3_score += 0.10
                print(f"PASS: Component 3a -- Slide 1 correctly has no transition while slides 2-8 do (0.10 pts)")
            else:
                print(f"FAIL: Component 3a -- Slide 1 should have no transition but has {slide_info[1]['type']}")

            if not slide_info[9]['has_transition']:
                comp3_score += 0.10
                print(f"PASS: Component 3b -- Slide 9 correctly has no transition while slides 2-8 do (0.10 pts)")
            else:
                print(f"FAIL: Component 3b -- Slide 9 should have no transition but has {slide_info[9]['type']}")
        else:
            print(f"FAIL: Component 3 -- No transitions found on slides 2-8, cannot verify selective application")

        total_score += comp3_score
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(round(total_score, 2), 1.0)
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

"""
Reward Script: Change Wipe transition direction on slide 3 from default to 'From Right'
Task ID: impress_tm_017
Domain: libreoffice_impress
Scoring:
  Component 1 (0.5): Slide 3 has Wipe transition with dir='r' (From Right)
  Component 2 (0.3): Wipe transition direction is specifically 'r' AND transition type unchanged (wipe)
  Component 3 (0.2): No unintended transition changes on other slides, anchored to slide 3 correctness
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tm_017'

NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS = {'p': NS_P}


def get_slide_transition_info(pptx_path, slide_num):
    """
    Extract transition type and attributes from slide N (1-based).
    Returns dict with 'type' and 'dir' keys, or None if no transition.
    """
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        slide_xml = f'ppt/slides/slide{slide_num}.xml'
        try:
            with zf.open(slide_xml) as f:
                root = ET.parse(f).getroot()
                tr = root.find('.//p:transition', NS)
                if tr is None:
                    return None
                children = list(tr)
                if len(children) == 0:
                    return {'type': None, 'dir': None, 'attrs': {}}
                child = children[0]
                tag = child.tag
                local_name = tag.split('}')[-1] if '}' in tag else tag
                return {
                    'type': local_name,
                    'dir': child.get('dir', None),
                    'attrs': dict(child.attrib),
                }
        except KeyError:
            return None


def has_any_transition(pptx_path, slide_num):
    """Check if a slide has any transition element with children."""
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        slide_xml = f'ppt/slides/slide{slide_num}.xml'
        try:
            with zf.open(slide_xml) as f:
                root = ET.parse(f).getroot()
                tr = root.find('.//p:transition', NS)
                return tr is not None and len(list(tr)) > 0
        except KeyError:
            return False


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

    # Precondition: file must be a valid pptx (zip)
    try:
        zf = zipfile.ZipFile(file_path, 'r')
        zf.close()
    except Exception as e:
        print(f"CRITICAL: Cannot open pptx file: {e}")
        print("REWARD: 0.0")
        return 0.0

    info = get_slide_transition_info(file_path, 3)

    # Component 1: Slide 3 wipe direction is 'r' (From Right) (0.5 points)
    # INITIAL: dir='l' -> FAIL. GOLDEN: dir='r' -> PASS.
    try:
        if info is not None and info['type'] == 'wipe' and info['dir'] == 'r':
            print(f"PASS: Component 1 -- Slide 3 wipe direction is 'r' (From Right) (0.5 pts)")
            total_score += 0.5
        elif info is None:
            print(f"FAIL: Component 1 -- No transition found on slide 3")
        elif info['type'] != 'wipe':
            print(f"FAIL: Component 1 -- Transition type is '{info['type']}', expected 'wipe'")
        else:
            print(f"FAIL: Component 1 -- Wipe direction is '{info['dir']}', expected 'r'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Transition type is still 'wipe' (not changed) AND direction is 'r' (0.3 points)
    # This compound check ensures the agent only changed direction, not the transition type.
    # INITIAL: type=wipe but dir='l' -> FAIL. GOLDEN: type=wipe and dir='r' -> PASS.
    try:
        if info is not None:
            type_ok = (info['type'] == 'wipe')
            dir_ok = (info['dir'] == 'r')
            if type_ok and dir_ok:
                print(f"PASS: Component 2 -- Transition type unchanged (wipe) + direction correct (0.3 pts)")
                total_score += 0.3
            elif not type_ok:
                print(f"FAIL: Component 2 -- Transition type changed to '{info['type']}', should remain 'wipe'")
            else:
                print(f"FAIL: Component 2 -- Direction is '{info['dir']}', expected 'r'")
        else:
            print(f"FAIL: Component 2 -- No transition on slide 3")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: No unintended transitions on other slides + slide 3 correct (0.2 points)
    # Other slides (1,2,4,5,6) must have no transitions (matching initial state).
    # Anchored to slide 3 correctness to ensure initial_env scores 0.
    try:
        unexpected = [s for s in [1, 2, 4, 5, 6] if has_any_transition(file_path, s)]
        for s in unexpected:
            print(f"  INFO: Slide {s} has unexpected transition")
        other_slides_clean = (len(unexpected) == 0)

        slide3_correct = (info is not None and info['type'] == 'wipe' and info['dir'] == 'r')

        if other_slides_clean and slide3_correct:
            print(f"PASS: Component 3 -- No unintended transitions + slide 3 correct (0.2 pts)")
            total_score += 0.2
        elif not other_slides_clean:
            print(f"FAIL: Component 3 -- Unintended transitions found on other slides")
        else:
            print(f"FAIL: Component 3 -- Slide 3 not yet correct (sub-condition)")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

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

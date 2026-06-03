"""
Reward Script: Verify slide transitions on Chem_Lecture.pptx
Task ID: impress_teach_029
Domain: libreoffice_impress
Scoring:
  Component 1: Slides 2-5 have 'wipe' transition type (0.25)
  Component 2: Wipe direction is right ('r') on slides 2-5 (0.15)
  Component 3: Wipe duration is 1000ms on slides 2-5 (0.15)
  Component 4: Slides 6-8 have 'dissolve' transition type (0.20)
  Component 5: Dissolve duration is 800ms on slides 6-8 (0.15)
  Component 6: Slides 1, 9, 10 have NO transitions (0.10)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_teach_029'

P_NS = 'http://schemas.openxmlformats.org/presentationml/2006/main'
P14_NS = 'http://schemas.microsoft.com/office/powerpoint/2010/main'


def parse_transition(zf, slide_num):
    """Parse transition info for a given slide number (1-based).
    Returns dict with keys: has_transition, type, dir, duration_ms
    """
    result = {'has_transition': False, 'type': None, 'dir': None, 'duration_ms': None}
    try:
        with zf.open(f'ppt/slides/slide{slide_num}.xml') as f:
            root = ET.parse(f).getroot()
            tr = root.find(f'.//{{{P_NS}}}transition')
            if tr is None:
                return result
            result['has_transition'] = True
            # Get duration from p14:dur attribute
            dur = tr.attrib.get(f'{{{P14_NS}}}dur')
            if dur is not None:
                result['duration_ms'] = int(dur)
            # Get transition type from child element
            for child in tr:
                tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                result['type'] = tag
                result['dir'] = child.attrib.get('dir')
                break
    except Exception as e:
        print(f"  ERROR parsing slide {slide_num}: {e}")
    return result


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
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open ZIP: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse all slide transitions
    transitions = {}
    slide_files = [f for f in zf.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
    num_slides = len(slide_files)
    print(f"Found {num_slides} slides")

    for i in range(1, num_slides + 1):
        transitions[i] = parse_transition(zf, i)
        print(f"  Slide {i}: {transitions[i]}")

    zf.close()

    # Component 1: Slides 2-5 have 'wipe' transition type (0.25 points)
    try:
        wipe_count = 0
        for s in [2, 3, 4, 5]:
            if s in transitions and transitions[s]['has_transition'] and transitions[s]['type'] == 'wipe':
                wipe_count += 1
        if wipe_count == 4:
            print(f"PASS: Component 1 - All slides 2-5 have wipe transition ({wipe_count}/4) (0.25 pts)")
            total_score += 0.25
        elif wipe_count > 0:
            partial = round(0.25 * wipe_count / 4, 3)
            print(f"PARTIAL: Component 1 - {wipe_count}/4 slides have wipe transition ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 - No slides 2-5 have wipe transition")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Wipe direction is 'r' (right) on slides 2-5 (0.15 points)
    try:
        dir_count = 0
        for s in [2, 3, 4, 5]:
            if s in transitions and transitions[s]['type'] == 'wipe' and transitions[s]['dir'] == 'r':
                dir_count += 1
        if dir_count == 4:
            print(f"PASS: Component 2 - All wipe transitions have dir='r' ({dir_count}/4) (0.15 pts)")
            total_score += 0.15
        elif dir_count > 0:
            partial = round(0.15 * dir_count / 4, 3)
            print(f"PARTIAL: Component 2 - {dir_count}/4 wipe transitions have dir='r' ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - No wipe transitions have direction 'r'")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Wipe duration is 1000ms on slides 2-5 (0.15 points)
    try:
        dur_count = 0
        for s in [2, 3, 4, 5]:
            if s in transitions and transitions[s]['type'] == 'wipe' and transitions[s]['duration_ms'] == 1000:
                dur_count += 1
        if dur_count == 4:
            print(f"PASS: Component 3 - All wipe transitions have 1000ms duration ({dur_count}/4) (0.15 pts)")
            total_score += 0.15
        elif dur_count > 0:
            partial = round(0.15 * dur_count / 4, 3)
            print(f"PARTIAL: Component 3 - {dur_count}/4 wipe transitions have 1000ms duration ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 - No wipe transitions have 1000ms duration")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Slides 6-8 have 'dissolve' transition type (0.20 points)
    try:
        dissolve_count = 0
        for s in [6, 7, 8]:
            if s in transitions and transitions[s]['has_transition'] and transitions[s]['type'] == 'dissolve':
                dissolve_count += 1
        if dissolve_count == 3:
            print(f"PASS: Component 4 - All slides 6-8 have dissolve transition ({dissolve_count}/3) (0.20 pts)")
            total_score += 0.20
        elif dissolve_count > 0:
            partial = round(0.20 * dissolve_count / 3, 3)
            print(f"PARTIAL: Component 4 - {dissolve_count}/3 slides have dissolve transition ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 - No slides 6-8 have dissolve transition")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Dissolve duration is 800ms on slides 6-8 (0.15 points)
    try:
        dur_count = 0
        for s in [6, 7, 8]:
            if s in transitions and transitions[s]['type'] == 'dissolve' and transitions[s]['duration_ms'] == 800:
                dur_count += 1
        if dur_count == 3:
            print(f"PASS: Component 5 - All dissolve transitions have 800ms duration ({dur_count}/3) (0.15 pts)")
            total_score += 0.15
        elif dur_count > 0:
            partial = round(0.15 * dur_count / 3, 3)
            print(f"PARTIAL: Component 5 - {dur_count}/3 dissolve transitions have 800ms duration ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 - No dissolve transitions have 800ms duration")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: Slides 1, 9, 10 have NO transitions (0.10 points)
    try:
        no_transition_slides = [1, 9, 10]
        clean_count = 0
        for s in no_transition_slides:
            if s in transitions and not transitions[s]['has_transition']:
                clean_count += 1
        if clean_count == len(no_transition_slides):
            print(f"PASS: Component 6 - Slides 1,9,10 have no transitions ({clean_count}/{len(no_transition_slides)}) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 - {len(no_transition_slides) - clean_count} of slides 1,9,10 unexpectedly have transitions")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
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
persist_app_state()
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

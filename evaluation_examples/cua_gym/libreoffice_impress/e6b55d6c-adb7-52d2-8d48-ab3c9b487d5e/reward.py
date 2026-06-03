"""
Reward Script: Configure rehearsed-timing presentation with precise slide timings and Fade transitions
Task ID: impress_gf4_038
Domain: libreoffice_impress
Scoring:
  Component 1 (0.4): Fade transition applied to all 10 slides
  Component 2 (0.5): Correct advance timing per slide (0.05 each)
  Component 3 (0.1): All slides have auto-advance enabled (advTm present)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf4_038'

# Expected timings in milliseconds per task spec
EXPECTED_TIMINGS = {
    1: 5000,    # slide 1 = 5s
    2: 10000,   # slide 2 = 10s
    3: 10000,   # slide 3 = 10s
    4: 10000,   # slide 4 = 10s
    5: 20000,   # slide 5 = 20s (chart explanation)
    6: 10000,   # slide 6 = 10s
    7: 10000,   # slide 7 = 10s
    8: 10000,   # slide 8 = 10s
    9: 15000,   # slide 9 = 15s
    10: 8000,   # slide 10 = 8s
}

NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'


def get_transition_info(pptx_path, slide_num):
    """Extract transition element info for a given 1-based slide number."""
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        fname = f'ppt/slides/slide{slide_num}.xml'
        try:
            with zf.open(fname) as f:
                root = ET.parse(f).getroot()
                tr = root.find('.//{%s}transition' % NS_P)
                if tr is None:
                    return None
                info = {
                    'advTm': tr.get('advTm'),
                    'advClick': tr.get('advClick'),
                    'children': [c.tag.split('}')[-1] for c in tr],
                }
                return info
        except KeyError:
            return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid zip (pptx)
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            # Quick validity check
            namelist = zf.namelist()
            if 'ppt/slides/slide1.xml' not in namelist:
                print("CRITICAL: Not a valid pptx file")
                print("REWARD: 0.0")
                return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot open file as zip: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Fade transition applied to all 10 slides (0.4 points)
    # This checks that every slide has a <p:transition> with a <p:fade> child.
    try:
        fade_count = 0
        for slide_num in range(1, 11):
            info = get_transition_info(file_path, slide_num)
            if info is not None and 'fade' in info['children']:
                fade_count += 1
            else:
                children = info['children'] if info else 'no transition'
                print(f"  Slide {slide_num}: expected fade, found {children}")

        if fade_count == 10:
            print(f"PASS: Component 1 - Fade transition on all 10 slides (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 - Fade transition on {fade_count}/10 slides")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Correct advance timing values per slide (0.5 points, 0.05 each)
    # Each slide must have the exact advTm value specified in the task.
    try:
        timing_score = 0.0
        for slide_num in range(1, 11):
            info = get_transition_info(file_path, slide_num)
            expected_ms = EXPECTED_TIMINGS[slide_num]
            if info is not None and info['advTm'] is not None:
                actual_ms = int(info['advTm'])
                if actual_ms == expected_ms:
                    timing_score += 0.05
                    print(f"  Slide {slide_num}: timing {actual_ms}ms == {expected_ms}ms OK")
                else:
                    print(f"  Slide {slide_num}: timing {actual_ms}ms != expected {expected_ms}ms")
            else:
                print(f"  Slide {slide_num}: no advTm attribute found")

        if timing_score > 0:
            print(f"PASS: Component 2 - Timing correct on {int(timing_score/0.05)}/10 slides ({timing_score:.2f} pts)")
            total_score += timing_score
        else:
            print(f"FAIL: Component 2 - No slide timings match expected values")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: All slides have auto-advance enabled (advTm present) (0.1 points)
    # This is a structural check: every slide must have the advTm attribute,
    # confirming automatic advance is configured (not just mouse-click).
    try:
        auto_advance_count = 0
        for slide_num in range(1, 11):
            info = get_transition_info(file_path, slide_num)
            if info is not None and info['advTm'] is not None:
                auto_advance_count += 1

        if auto_advance_count == 10:
            print(f"PASS: Component 3 - Auto-advance (advTm) on all 10 slides (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 3 - Auto-advance on {auto_advance_count}/10 slides")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

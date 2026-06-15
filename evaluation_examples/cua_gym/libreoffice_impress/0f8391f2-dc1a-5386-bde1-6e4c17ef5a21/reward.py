"""
Reward Script: Verify slide transitions in product_roadmap.pptx
Task ID: impress_tm_022
Domain: libreoffice_impress
Scoring:
  - Component 1 (0.30): Slides 1-3 have Fade transition with 2000ms duration
  - Component 2 (0.40): Slides 4-6 have Push Right transition with 1500ms duration
  - Component 3 (0.30): Slides 7-9 have Dissolve transition with 1000ms duration
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tm_022'
NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}


def get_transition_info(pptx_path, slide_num):
    """
    Extract transition type, duration, and direction for a given slide (1-based).
    Returns (type_tag, duration_ms, direction) or (None, None, None) if no transition.
    """
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        fname = f'ppt/slides/slide{slide_num}.xml'
        try:
            with zf.open(fname) as f:
                root = ET.parse(f).getroot()
                tr = root.find('.//p:transition', NS)
                if tr is None:
                    return (None, None, None)
                dur = tr.get('dur')
                dur_ms = int(dur) if dur else None
                # The transition type is the first child element
                children = list(tr)
                if not children:
                    return (None, dur_ms, None)
                child = children[0]
                # Extract local tag name (strip namespace)
                tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                direction = child.get('dir')
                return (tag, dur_ms, direction)
        except (KeyError, ET.ParseError):
            return (None, None, None)


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

    # Precondition: must be a valid zip/pptx
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            names = zf.namelist()
            if not any('ppt/slides/slide1.xml' in n for n in names):
                print("CRITICAL: Not a valid pptx file")
                print("REWARD: 0.0")
                return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot open pptx: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Slides 1-3 have Fade transition with 2000ms duration (0.30 points)
    # 0.10 per slide: 0.05 for correct type + 0.05 for correct duration
    try:
        comp1_score = 0.0
        for slide_num in [1, 2, 3]:
            t_type, t_dur, t_dir = get_transition_info(file_path, slide_num)
            if t_type == 'fade':
                comp1_score += 0.05
                print(f"PASS: Slide {slide_num} has Fade transition")
            else:
                print(f"FAIL: Slide {slide_num} expected Fade, found: {t_type}")
            if t_dur == 2000:
                comp1_score += 0.05
                print(f"PASS: Slide {slide_num} has 2000ms duration")
            else:
                print(f"FAIL: Slide {slide_num} expected 2000ms duration, found: {t_dur}")
        if comp1_score > 0:
            print(f"Component 1 subtotal: {comp1_score:.2f}/0.30")
            total_score += comp1_score
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Slides 4-6 have Push Right transition with 1500ms duration (0.40 points)
    # Per slide: 0.05 for type, 0.05 for direction, 0.0333 for duration = 0.1333 per slide
    try:
        comp2_score = 0.0
        for slide_num in [4, 5, 6]:
            t_type, t_dur, t_dir = get_transition_info(file_path, slide_num)
            if t_type == 'push':
                comp2_score += 0.05
                print(f"PASS: Slide {slide_num} has Push transition")
            else:
                print(f"FAIL: Slide {slide_num} expected Push, found: {t_type}")
            if t_dir == 'r':
                comp2_score += 0.05
                print(f"PASS: Slide {slide_num} has direction 'r' (right)")
            else:
                print(f"FAIL: Slide {slide_num} expected direction 'r', found: {t_dir}")
            if t_dur == 1500:
                comp2_score += 0.0333
                print(f"PASS: Slide {slide_num} has 1500ms duration")
            else:
                print(f"FAIL: Slide {slide_num} expected 1500ms duration, found: {t_dur}")
        if comp2_score > 0:
            print(f"Component 2 subtotal: {comp2_score:.4f}/0.40")
            total_score += comp2_score
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Slides 7-9 have Dissolve transition with 1000ms duration (0.30 points)
    # 0.10 per slide: 0.05 for correct type + 0.05 for correct duration
    try:
        comp3_score = 0.0
        for slide_num in [7, 8, 9]:
            t_type, t_dur, t_dir = get_transition_info(file_path, slide_num)
            if t_type == 'dissolve':
                comp3_score += 0.05
                print(f"PASS: Slide {slide_num} has Dissolve transition")
            else:
                print(f"FAIL: Slide {slide_num} expected Dissolve, found: {t_type}")
            if t_dur == 1000:
                comp3_score += 0.05
                print(f"PASS: Slide {slide_num} has 1000ms duration")
            else:
                print(f"FAIL: Slide {slide_num} expected 1000ms duration, found: {t_dur}")
        if comp3_score > 0:
            print(f"Component 3 subtotal: {comp3_score:.2f}/0.30")
            total_score += comp3_score
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

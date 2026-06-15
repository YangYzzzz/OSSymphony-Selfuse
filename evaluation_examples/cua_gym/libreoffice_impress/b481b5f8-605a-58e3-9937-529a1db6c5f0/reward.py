"""
Reward Script: Cybersecurity Awareness Training with quiz animations
Task ID: impress_wf_026
Domain: libreoffice_impress
Scoring:
  - 5 components (0.2 each): Slides 9-13 each have Appear entrance animations
    on the quiz answer option rectangles (A-D), triggered sequentially.
  The ONLY task-introduced change between initial and golden is the addition
  of entrance animations on the quiz slides. All other content (slides, text,
  shapes, colors, table, certificate) is identical in both envs.
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_wf_026'

# Namespace map for OOXML
NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def check_slide_animations(pptx_path, slide_num):
    """
    Check if a given slide has Appear entrance animations on answer option shapes.
    Returns (has_timing, num_appear_entrance_anims) where:
      - has_timing: whether the slide has a timing element at all
      - num_appear_entrance_anims: count of entrance animations with presetID=1 (Appear)
    """
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        fname = f'ppt/slides/slide{slide_num}.xml'
        try:
            with zf.open(fname) as f:
                root = ET.parse(f).getroot()
        except KeyError:
            return False, 0

        timing = root.find('.//p:timing', NS)
        if timing is None:
            return False, 0

        # Count entrance animations: presetClass="entr" and presetID="1" (Appear)
        appear_count = 0
        for ctn in timing.iter():
            tag = ctn.tag.split('}')[-1] if '}' in ctn.tag else ctn.tag
            if tag == 'cTn':
                preset_class = ctn.get('presetClass', '')
                preset_id = ctn.get('presetID', '')
                if preset_class == 'entr' and preset_id == '1':
                    appear_count += 1

        return True, appear_count


def check_sequential_triggering(pptx_path, slide_num):
    """
    Check if animations are triggered sequentially (After Previous pattern).
    In the XML, this means at least some animations have nodeType="afterEffect".
    Returns True if sequential triggering is detected.
    """
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        fname = f'ppt/slides/slide{slide_num}.xml'
        try:
            with zf.open(fname) as f:
                root = ET.parse(f).getroot()
        except KeyError:
            return False

        timing = root.find('.//p:timing', NS)
        if timing is None:
            return False

        after_effect_count = 0
        for ctn in timing.iter():
            tag = ctn.tag.split('}')[-1] if '}' in ctn.tag else ctn.tag
            if tag == 'cTn':
                node_type = ctn.get('nodeType', '')
                if node_type == 'afterEffect':
                    after_effect_count += 1

        # Expect at least 3 afterEffect nodes (options B, C, D after the first click)
        return after_effect_count >= 3


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Only scores the task-introduced change: entrance animations on quiz slides 9-13.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid pptx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        # Quick validity check - can we open as zip?
        with zipfile.ZipFile(file_path, 'r') as zf:
            if 'ppt/presentation.xml' not in zf.namelist():
                print("CRITICAL: Not a valid pptx file")
                print("REWARD: 0.0")
                return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot open file as pptx: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Quiz slides are slides 9-13 (1-indexed)
    quiz_slides = [9, 10, 11, 12, 13]

    for idx, slide_num in enumerate(quiz_slides):
        comp_num = idx + 1
        comp_points = 0.2

        # Component N: Slide X has Appear entrance animations on answer rectangles (0.2 points)
        try:
            has_timing, appear_count = check_slide_animations(file_path, slide_num)
            is_sequential = check_sequential_triggering(file_path, slide_num)

            if has_timing and appear_count >= 4 and is_sequential:
                print(f"PASS: Component {comp_num} — Slide {slide_num} has {appear_count} Appear entrance animations with sequential triggering ({comp_points} pts)")
                total_score += comp_points
            elif has_timing and appear_count >= 4:
                # Partial credit: animations exist but not sequential
                partial = comp_points * 0.5
                total_score += partial
                print(f"PARTIAL: Component {comp_num} — Slide {slide_num} has {appear_count} Appear animations but not sequentially triggered ({partial} pts)")
            elif not has_timing:
                print(f"FAIL: Component {comp_num} — Slide {slide_num} has no timing/animation element")
            else:
                print(f"FAIL: Component {comp_num} — Slide {slide_num} has {appear_count} Appear entrance animations, expected >= 4")

        except Exception as e:
            print(f"ERROR: Component {comp_num} — Slide {slide_num}: {e}")

    final_score = round(min(total_score, 1.0), 2)
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

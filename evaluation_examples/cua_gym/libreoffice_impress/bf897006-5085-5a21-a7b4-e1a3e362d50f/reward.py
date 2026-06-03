"""
Reward Script: Replace Fade transitions with Dissolve and reduce duration from 3s to 1s
Task ID: impress_tm_019
Domain: libreoffice_impress
Scoring:
  Component 1 (0.5): All 15 slides have 'dissolve' transition type
  Component 2 (0.5): All 15 slides have duration=1000ms (1 second)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tm_019'
EXPECTED_SLIDES = 15

NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def get_slide_transitions(pptx_path):
    """Extract transition info for every slide from the PPTX ZIP."""
    results = {}
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        slide_files = sorted(
            [f for f in zf.namelist()
             if f.startswith('ppt/slides/slide') and f.endswith('.xml')],
            key=lambda x: int(x.replace('ppt/slides/slide', '').replace('.xml', ''))
        )
        for idx, sf in enumerate(slide_files):
            slide_num = idx + 1
            with zf.open(sf) as f:
                root = ET.parse(f).getroot()
                tr = root.find('.//p:transition', NS)
                if tr is not None:
                    dur = tr.attrib.get('dur', None)
                    children = [child.tag.split('}')[-1] for child in tr]
                    results[slide_num] = {
                        'dur': dur,
                        'type': children[0] if children else None
                    }
                else:
                    results[slide_num] = {'dur': None, 'type': None}
    return results


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid PPTX
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        transitions = get_slide_transitions(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse PPTX {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    num_slides = len(transitions)
    if num_slides == 0:
        print("CRITICAL: No slides found in presentation")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {num_slides} slides")

    # Component 1: All slides have 'dissolve' transition type (0.5 points)
    # Proportional: each slide contributes 0.5/num_slides points
    try:
        dissolve_count = 0
        for slide_num in sorted(transitions.keys()):
            t = transitions[slide_num]
            if t['type'] == 'dissolve':
                dissolve_count += 1
            else:
                print(f"FAIL: Slide {slide_num} transition type is '{t['type']}', expected 'dissolve'")

        comp1_score = 0.5 * (dissolve_count / num_slides)
        if comp1_score > 0:
            total_score += comp1_score
        if dissolve_count == num_slides:
            print(f"PASS: Component 1 -- All {num_slides} slides have 'dissolve' transition ({comp1_score:.3f} pts)")
        else:
            print(f"PARTIAL: Component 1 -- {dissolve_count}/{num_slides} slides have 'dissolve' transition ({comp1_score:.3f} pts)")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: All slides have duration=1000ms (0.5 points)
    # Proportional: each slide contributes 0.5/num_slides points
    try:
        dur_count = 0
        for slide_num in sorted(transitions.keys()):
            t = transitions[slide_num]
            if t['dur'] == '1000':
                dur_count += 1
            else:
                print(f"FAIL: Slide {slide_num} duration is '{t['dur']}', expected '1000'")

        comp2_score = 0.5 * (dur_count / num_slides)
        if comp2_score > 0:
            total_score += comp2_score
        if dur_count == num_slides:
            print(f"PASS: Component 2 -- All {num_slides} slides have duration=1000ms ({comp2_score:.3f} pts)")
        else:
            print(f"PARTIAL: Component 2 -- {dur_count}/{num_slides} slides have duration=1000ms ({comp2_score:.3f} pts)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.3f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_impress")

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

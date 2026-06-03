"""
Reward Script: Apply Barn Door Open transition to slide 2, Barn Door Close to slide 3
Task ID: impress_tm_037
Domain: libreoffice_impress
Scoring:
  Component 1 (0.5): Slide 2 has Barn Door Open transition (split, orient=horz, dir=out)
  Component 2 (0.5): Slide 3 has Barn Door Close transition (split, orient=horz, dir=in)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tm_037'

P_NS = 'http://schemas.openxmlformats.org/presentationml/2006/main'


def get_transition_info(pptx_path, slide_number):
    """
    Get transition info for a given slide (1-based slide_number).
    Returns dict with 'element_name', 'orient', 'dir' or None if no transition.
    """
    ns = {'p': P_NS}
    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            slide_xml = f'ppt/slides/slide{slide_number}.xml'
            if slide_xml not in zf.namelist():
                return None
            with zf.open(slide_xml) as f:
                root = ET.parse(f).getroot()
                tr = root.find('.//p:transition', ns)
                if tr is None:
                    return None
                # Get the child element (the transition type)
                for child in tr:
                    tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                    return {
                        'element_name': tag,
                        'orient': child.get('orient', ''),
                        'dir': child.get('dir', ''),
                    }
                return None
    except Exception as e:
        print(f"ERROR reading transition for slide {slide_number}: {e}")
        return None


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

    # Quick check: is it a valid pptx (zip)?
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            pass
    except Exception as e:
        print(f"CRITICAL: Cannot open as ZIP: {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Slide 2 has Barn Door Open transition (0.5 points)
    # Barn Door Open = <p:split orient="horz" dir="out"/>
    try:
        tr_info = get_transition_info(file_path, 2)
        if tr_info is not None:
            is_split = (tr_info['element_name'] == 'split')
            is_horz = (tr_info['orient'] == 'horz')
            is_out = (tr_info['dir'] == 'out')
            if is_split and is_horz and is_out:
                print(f"PASS: Component 1 -- Slide 2 has Barn Door Open (split, horz, out) (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 1 -- Slide 2 transition mismatch: "
                      f"element={tr_info['element_name']}, orient={tr_info['orient']}, dir={tr_info['dir']}. "
                      f"Expected split/horz/out.")
        else:
            print(f"FAIL: Component 1 -- Slide 2 has no transition. Expected Barn Door Open.")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Slide 3 has Barn Door Close transition (0.5 points)
    # Barn Door Close = <p:split orient="horz" dir="in"/>
    try:
        tr_info = get_transition_info(file_path, 3)
        if tr_info is not None:
            is_split = (tr_info['element_name'] == 'split')
            is_horz = (tr_info['orient'] == 'horz')
            is_in = (tr_info['dir'] == 'in')
            if is_split and is_horz and is_in:
                print(f"PASS: Component 2 -- Slide 3 has Barn Door Close (split, horz, in) (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 2 -- Slide 3 transition mismatch: "
                      f"element={tr_info['element_name']}, orient={tr_info['orient']}, dir={tr_info['dir']}. "
                      f"Expected split/horz/in.")
        else:
            print(f"FAIL: Component 2 -- Slide 3 has no transition. Expected Barn Door Close.")
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

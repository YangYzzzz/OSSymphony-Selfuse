"""
Reward Script: Set slide 1 Fade transition with 3s advance and loop continuously
Task ID: impress_tm_024
Domain: libreoffice_impress
Scoring:
  Component 1 (0.35): Fade transition on slide 1
  Component 2 (0.35): Advance automatically after 3 seconds (advTm=3000)
  Component 3 (0.30): Loop continuously enabled in slideshow properties
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tm_024'

NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
}


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

    # --- Read slide1.xml for transition checks ---
    try:
        with zf.open('ppt/slides/slide1.xml') as f:
            slide_root = ET.parse(f).getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot read slide1.xml: {e}")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    transition_el = slide_root.find('.//p:transition', NS)

    # Component 1: Fade transition on slide 1 (0.35 points)
    try:
        if transition_el is not None:
            fade_el = transition_el.find('p:fade', NS)
            if fade_el is not None:
                print(f"PASS: Component 1 — Fade transition found on slide 1 (0.35 pts)")
                total_score += 0.35
            else:
                # Check what transition type is actually present
                children = [child.tag.split('}')[-1] for child in transition_el]
                print(f"FAIL: Component 1 — Expected 'fade' transition, found child elements: {children}")
        else:
            print("FAIL: Component 1 — No transition element found on slide 1")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Advance automatically after 3 seconds (0.35 points)
    try:
        if transition_el is not None:
            adv_tm = transition_el.get('advTm')
            if adv_tm is not None:
                adv_tm_int = int(adv_tm)
                if adv_tm_int == 3000:
                    print(f"PASS: Component 2 — advTm=3000 (3 seconds) (0.35 pts)")
                    total_score += 0.35
                else:
                    print(f"FAIL: Component 2 — advTm={adv_tm_int}, expected 3000")
            else:
                print("FAIL: Component 2 — No advTm attribute on transition element")
        else:
            print("FAIL: Component 2 — No transition element, cannot check advTm")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # --- Read presentation.xml for loop setting ---
    # Component 3: Loop continuously enabled (0.30 points)
    try:
        with zf.open('ppt/presentation.xml') as f:
            pres_root = ET.parse(f).getroot()

        show_pr = pres_root.find('.//p:showPr', NS)
        if show_pr is not None:
            loop_val = show_pr.get('loop')
            if loop_val == '1':
                print(f"PASS: Component 3 — loop='1' in showPr (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 — showPr loop='{loop_val}', expected '1'")
        else:
            print("FAIL: Component 3 — No showPr element in presentation.xml (loop not enabled)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    zf.close()

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

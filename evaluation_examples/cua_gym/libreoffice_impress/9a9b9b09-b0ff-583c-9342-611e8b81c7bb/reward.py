"""
Reward Script: Set slide auto-advance timings for gallery slideshow
Task ID: impress_tm_036
Domain: libreoffice_impress
Scoring:
  Component 1 (0.5): Each slide has correct advTm (auto-advance timing) — 0.1 per slide
  Component 2 (0.5): Each slide has advClick='0' (mouse click disabled) — 0.1 per slide
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tm_036'

# Expected timings in milliseconds per slide (1-indexed key)
EXPECTED_TIMINGS = {
    1: '3000',
    2: '5000',
    3: '4000',
    4: '6000',
    5: '3000',
}


def persist_app_state(domain: str):
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

    ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open zip: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Correct auto-advance timing (advTm) per slide (0.1 pts each, 0.5 total)
    for slide_num in range(1, 6):
        expected_tm = EXPECTED_TIMINGS[slide_num]
        try:
            with zf.open(f'ppt/slides/slide{slide_num}.xml') as f:
                root = ET.parse(f).getroot()
                tr = root.find('.//p:transition', ns)
                if tr is not None:
                    actual_tm = tr.get('advTm')
                    if actual_tm == expected_tm:
                        print(f"PASS: Slide {slide_num} advTm={actual_tm}ms (0.1 pts)")
                        total_score += 0.1
                    else:
                        print(f"FAIL: Slide {slide_num} advTm expected {expected_tm}, found {actual_tm}")
                else:
                    print(f"FAIL: Slide {slide_num} has no transition element (expected advTm={expected_tm})")
        except Exception as e:
            print(f"ERROR: Slide {slide_num} timing check: {e}")

    # Component 2: Mouse click advance disabled (advClick='0') per slide (0.1 pts each, 0.5 total)
    for slide_num in range(1, 6):
        try:
            with zf.open(f'ppt/slides/slide{slide_num}.xml') as f:
                root = ET.parse(f).getroot()
                tr = root.find('.//p:transition', ns)
                if tr is not None:
                    adv_click = tr.get('advClick')
                    if adv_click == '0':
                        print(f"PASS: Slide {slide_num} advClick=0 (mouse click disabled) (0.1 pts)")
                        total_score += 0.1
                    else:
                        print(f"FAIL: Slide {slide_num} advClick expected '0', found '{adv_click}'")
                else:
                    print(f"FAIL: Slide {slide_num} has no transition element (expected advClick='0')")
        except Exception as e:
            print(f"ERROR: Slide {slide_num} advClick check: {e}")

    zf.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved GUI state before verification
persist_app_state("libreoffice_impress")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Verify slide show rehearsal timings
Task ID: impress_gf2_017
Domain: libreoffice_impress
Scoring:
  - Component 1 (0.5): Each slide has an automatic advance timing set (advTm present)
  - Component 2 (0.5): Each slide has the correct advTm value
    Slide 1=8s, Slide 2=12s, Slide 3=15s, Slide 4=10s, Slide 5=10s
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf2_017'

# Expected advance timings in milliseconds
EXPECTED_TIMINGS = {
    1: 8000,
    2: 12000,
    3: 15000,
    4: 10000,
    5: 10000,
}

NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}


def persist_app_state(domain):
    """Save any unsaved LibreOffice edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def get_slide_timings(pptx_path):
    """Parse transition advTm from each slide XML inside the PPTX ZIP."""
    timings = {}
    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            for slide_num in range(1, 6):
                fname = f'ppt/slides/slide{slide_num}.xml'
                try:
                    with zf.open(fname) as f:
                        root = ET.parse(f).getroot()
                        tr = root.find('.//p:transition', NS)
                        if tr is not None:
                            adv_tm = tr.attrib.get('advTm')
                            if adv_tm is not None:
                                timings[slide_num] = int(adv_tm)
                            else:
                                timings[slide_num] = None
                        else:
                            timings[slide_num] = None
                except KeyError:
                    timings[slide_num] = None
    except Exception as e:
        print(f"ERROR: Cannot open ZIP: {e}")
    return timings


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
        with zipfile.ZipFile(file_path, 'r') as zf:
            # Quick check that it has 5 slides
            slide_files = [n for n in zf.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')]
            if len(slide_files) < 5:
                print(f"CRITICAL: Expected 5 slides, found {len(slide_files)}")
                print("REWARD: 0.0")
                return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot open PPTX as ZIP: {e}")
        print("REWARD: 0.0")
        return 0.0

    timings = get_slide_timings(file_path)
    print(f"Detected timings: {timings}")

    # Component 1: Each slide has an automatic advance timing (advTm present)
    # 0.1 points per slide = 0.5 total
    # This checks that timing EXISTS — it fails on initial (no transition elements)
    for slide_num in range(1, 6):
        try:
            actual = timings.get(slide_num)
            if actual is not None:
                print(f"PASS: Component 1.{slide_num} — Slide {slide_num} has advTm={actual}ms (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 1.{slide_num} — Slide {slide_num} has no advTm set")
        except Exception as e:
            print(f"ERROR: Component 1.{slide_num} — {e}")

    # Component 2: Each slide has the CORRECT advance timing value
    # 0.1 points per slide = 0.5 total
    # This checks the exact value matches the task specification
    for slide_num in range(1, 6):
        try:
            actual = timings.get(slide_num)
            expected = EXPECTED_TIMINGS[slide_num]
            if actual == expected:
                print(f"PASS: Component 2.{slide_num} — Slide {slide_num} advTm={actual}ms matches expected {expected}ms (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 2.{slide_num} — Slide {slide_num} advTm={actual}ms, expected {expected}ms")
        except Exception as e:
            print(f"ERROR: Component 2.{slide_num} — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
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

"""
Reward Script: Set slide 4 to advance after 15 seconds automatically and disable mouse click advancement
Task ID: impress_tm_034
Domain: libreoffice_impress
Scoring:
  - Component 1 (0.5): Mouse click advancement disabled on slide 4 (advClick="0")
  - Component 2 (0.5): Auto-advance set to 15 seconds on slide 4 (advTm="15000")
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tm_034'
FILE_NAME = 'impress_tm_034.pptx'

NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}

# Slide 4 is slide index 3 (0-based), but in the ZIP it's slide4.xml
SLIDE_NUM = 4


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
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

    # Precondition: file must exist and be a valid pptx (ZIP)
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open as ZIP: {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse slide 4 XML for transition element
    transition = None
    try:
        with zf.open(f'ppt/slides/slide{SLIDE_NUM}.xml') as f:
            root = ET.parse(f).getroot()
            transition = root.find('.//p:transition', NS)
    except KeyError:
        print(f"CRITICAL: slide{SLIDE_NUM}.xml not found in archive")
        print("REWARD: 0.0")
        zf.close()
        return 0.0
    except Exception as e:
        print(f"CRITICAL: Error parsing slide{SLIDE_NUM}.xml: {e}")
        print("REWARD: 0.0")
        zf.close()
        return 0.0
    finally:
        zf.close()

    # Component 1: Mouse click advancement disabled (advClick="0") — 0.5 points
    # In the initial file, there is no <transition> element, so advClick defaults to "1" (enabled).
    # The golden file must have advClick="0" to disable mouse click advancement.
    try:
        if transition is not None:
            adv_click = transition.get('advClick')
            if adv_click == '0':
                print(f"PASS: Component 1 — advClick='0' (mouse click disabled) (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 1 — advClick='{adv_click}', expected '0'")
        else:
            print("FAIL: Component 1 — No <transition> element on slide 4; mouse click not configured")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Auto-advance set to 15 seconds (advTm="15000") — 0.5 points
    # In the initial file, there is no <transition> element, so no auto-advance.
    # The golden file must have advTm="15000" (15000 milliseconds = 15 seconds).
    try:
        if transition is not None:
            adv_tm = transition.get('advTm')
            if adv_tm is not None:
                adv_tm_int = int(adv_tm)
                if adv_tm_int == 15000:
                    print(f"PASS: Component 2 — advTm='15000' (15 seconds auto-advance) (0.5 pts)")
                    total_score += 0.5
                else:
                    print(f"FAIL: Component 2 — advTm='{adv_tm}' ({adv_tm_int/1000}s), expected '15000' (15s)")
            else:
                print("FAIL: Component 2 — advTm attribute not set on <transition> element")
        else:
            print("FAIL: Component 2 — No <transition> element on slide 4; auto-advance not configured")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_impress")

file_path = f'{WORKDIR}/{FILE_NAME}'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

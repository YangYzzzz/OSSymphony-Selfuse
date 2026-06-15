"""
Reward Script: Set slide 2 to advance on mouse click AND automatically after 10 seconds
Task ID: impress_tm_020
Domain: libreoffice_impress
Scoring:
  Component 1 (0.5): advTm attribute exists on slide 2 transition
  Component 2 (0.3): advTm value equals 10000 (10 seconds)
  Component 3 (0.2): advClick still enabled ("1") AND advTm present (compound check)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tm_020'

# Persistence hook: save any unsaved GUI state before verification
def persist_app_state():
    try:
        os.environ["DISPLAY"] = ":0"
        import pyautogui
        import time
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_impress")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}

    # Load the pptx as a ZIP and parse slide2.xml for transition attributes
    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with zf.open('ppt/slides/slide2.xml') as f:
            root = ET.parse(f).getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot parse slide2.xml: {e}")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    # Find the transition element on slide 2
    tr = root.find('.//p:transition', ns)
    if tr is None:
        print("FAIL: No <transition> element found on slide 2")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    adv_click = tr.get('advClick')
    adv_tm = tr.get('advTm')

    print(f"DEBUG: transition attributes — advClick={adv_click}, advTm={adv_tm}")

    # Component 1: advTm attribute exists on slide 2 transition (0.5 points)
    # This is the core task-introduced change: adding automatic advance timing.
    # Initial state has no advTm, so this correctly differentiates.
    try:
        if adv_tm is not None:
            print(f"PASS: Component 1 — advTm attribute present (value: {adv_tm}) (0.5 pts)")
            total_score += 0.5
        else:
            print("FAIL: Component 1 — advTm attribute not found on slide 2 transition")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: advTm value equals 10000 (10 seconds) (0.3 points)
    # The task specifies exactly 10 seconds = 10000 milliseconds.
    try:
        if adv_tm is not None:
            adv_tm_int = int(adv_tm)
            if adv_tm_int == 10000:
                print(f"PASS: Component 2 — advTm is exactly 10000ms (10s) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — advTm is {adv_tm_int}ms, expected 10000ms")
        else:
            print("FAIL: Component 2 — advTm not present, cannot check value")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: advClick still "1" AND advTm present (0.2 points)
    # Compound check: the task says "both on mouse click AND automatically".
    # advClick was already "1" initially, but we anchor this to the change by
    # requiring advTm to also be present. This fails on initial (no advTm).
    try:
        if adv_click == "1" and adv_tm is not None:
            print(f"PASS: Component 3 — advClick=1 AND advTm present (both modes active) (0.2 pts)")
            total_score += 0.2
        else:
            if adv_click != "1":
                print(f"FAIL: Component 3 — advClick is {adv_click}, expected '1'")
            if adv_tm is None:
                print("FAIL: Component 3 — advTm not present (compound condition not met)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    zf.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: persist app state then verify
persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

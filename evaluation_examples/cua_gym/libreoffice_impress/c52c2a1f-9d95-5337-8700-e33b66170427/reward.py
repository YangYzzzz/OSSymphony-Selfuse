"""
Reward Script: Apply a Clock transition to slide 5 with 3.0 second duration
Task ID: impress_tm_018
Domain: libreoffice_impress
Scoring:
  Component 1: Slide 5 has a transition element (0.3 pts)
  Component 2: Transition type is 'wheel' with spokes='1' (Clock) (0.4 pts)
  Component 3: Transition duration is 3000ms (3.0 seconds) (0.3 pts)
"""

import os
import zipfile
import xml.etree.ElementTree as ET


WORKDIR = '/home/user'
TASK_ID = 'impress_tm_018'

# Persistence hook: save any unsaved GUI edits before verification
def persist_app_state():
    try:
        import pyautogui
        os.environ["DISPLAY"] = ":0"
        pyautogui.hotkey("ctrl", "s")
        import time
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

    ns_p = 'http://schemas.openxmlformats.org/presentationml/2006/main'
    ns_p14 = 'http://schemas.microsoft.com/office/powerpoint/2010/main'
    ns = {'p': ns_p, 'p14': ns_p14}

    # Load the pptx as a ZIP and parse slide5.xml
    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open ZIP {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with zf.open('ppt/slides/slide5.xml') as f:
            root = ET.parse(f).getroot()
    except KeyError:
        print("CRITICAL: slide5.xml not found in pptx")
        zf.close()
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot parse slide5.xml: {e}")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    zf.close()

    # Find the transition element on slide 5
    transition_elem = root.find(f'.//{{{ns_p}}}transition')

    # Component 1: Slide 5 has a Clock (wheel) transition element (0.3 points)
    # The Clock transition in OOXML is represented as <p:wheel> child inside <p:transition>
    # A bare <p:transition> without a type child is NOT a Clock transition
    wheel_elem = None
    try:
        if transition_elem is not None:
            wheel_elem = transition_elem.find(f'{{{ns_p}}}wheel')
        if wheel_elem is not None:
            print(f"PASS: Component 1 -- Slide 5 has a Clock (wheel) transition (0.3 pts)")
            total_score += 0.3
        else:
            children = []
            if transition_elem is not None:
                children = [child.tag.split('}')[-1] for child in transition_elem]
            print(f"FAIL: Component 1 -- No 'wheel' transition on slide 5. Transition children: {children}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Wheel element has spokes='1' (clockwise, single spoke = Clock) (0.4 points)
    try:
        if wheel_elem is not None:
            spokes = wheel_elem.get('spokes', '')
            if spokes == '1':
                print(f"PASS: Component 2 -- Clock transition has spokes=1 (clockwise) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 -- wheel spokes='{spokes}', expected '1'")
        else:
            print(f"FAIL: Component 2 -- No wheel element, cannot check spokes")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Transition duration is 3000ms (3.0 seconds) (0.3 points)
    # Duration is in p14:dur attribute (milliseconds)
    # Only award points if BOTH the wheel transition exists AND duration is correct
    try:
        if wheel_elem is not None and transition_elem is not None:
            dur_p14 = transition_elem.get(f'{{{ns_p14}}}dur')
            dur_plain = transition_elem.get('dur')

            duration_ms = None
            if dur_p14 is not None:
                duration_ms = int(dur_p14)
            elif dur_plain is not None:
                duration_ms = int(dur_plain)

            if duration_ms == 3000:
                print(f"PASS: Component 3 -- Duration is 3000ms (3.0 seconds) (0.3 pts)")
                total_score += 0.3
            elif duration_ms is not None:
                print(f"FAIL: Component 3 -- Duration is {duration_ms}ms, expected 3000ms")
            else:
                # Check spd as fallback indicator
                spd = transition_elem.get('spd')
                print(f"FAIL: Component 3 -- No explicit duration found. dur_p14={dur_p14}, dur={dur_plain}, spd={spd}")
        else:
            print(f"FAIL: Component 3 -- No wheel transition, cannot check duration")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state()
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

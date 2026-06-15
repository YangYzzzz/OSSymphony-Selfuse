"""
Reward Script: Trade show booth kiosk presentation configuration
Task ID: impress_gf2_050
Domain: libreoffice_impress
Scoring:
  - Component 1: Cross Fade transition on all 8 slides (0.25)
  - Component 2: Transition speed 1.5s (med) on all slides (0.15)
  - Component 3: Auto-advance timings correct per slide group (0.30)
  - Component 4: advClick disabled on all slides (0.10)
  - Component 5: Kiosk mode enabled in presProps (0.10)
  - Component 6: Loop continuously enabled in presProps (0.10)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf2_050'

NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}

def get_transition_elements(pptx_path, num_slides=8):
    """Parse transition elements from all slides. Returns dict: slide_num -> (transition_elem, fade_child)"""
    results = {}
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        for i in range(1, num_slides + 1):
            fname = f'ppt/slides/slide{i}.xml'
            try:
                with zf.open(fname) as f:
                    root = ET.parse(f).getroot()
                    tr = root.find('.//p:transition', NS)
                    fade = None
                    if tr is not None:
                        fade = tr.find('p:fade', NS)
                    results[i] = (tr, fade)
            except KeyError:
                results[i] = (None, None)
    return results

def get_show_properties(pptx_path):
    """Parse showPr from presProps.xml. Returns (showPr_elem, kiosk_elem) or (None, None)."""
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        if 'ppt/presProps.xml' not in zf.namelist():
            return None, None
        with zf.open('ppt/presProps.xml') as f:
            content = f.read().decode()
            # Parse with namespace awareness
            root = ET.fromstring(content)
            # showPr can be in default namespace or p: namespace
            # Try both patterns
            show_pr = None
            kiosk = None
            for elem in root.iter():
                tag = elem.tag
                # Strip namespace
                local = tag.split('}')[1] if '}' in tag else tag
                if local == 'showPr':
                    show_pr = elem
                if local == 'kiosk':
                    kiosk = elem
            return show_pr, kiosk

def verify_task(file_path):
    """Verify task completion with progressive scoring. Returns float 0.0-1.0."""
    total_score = 0.0

    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Parse all transition elements
    try:
        transitions = get_transition_elements(file_path, 8)
    except Exception as e:
        print(f"CRITICAL: Cannot parse PPTX as ZIP: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Expected auto-advance timings in ms per slide number
    expected_advTm = {
        1: '6000', 2: '6000',
        3: '12000', 4: '12000', 5: '12000', 6: '12000',
        7: '8000', 8: '8000',
    }

    # Component 1: Cross Fade transition on all 8 slides (0.25 points)
    # Cross Fade = <p:fade thrw="1"> child element in transition
    try:
        fade_count = 0
        for i in range(1, 9):
            tr, fade = transitions.get(i, (None, None))
            if fade is not None and fade.get('thrw') == '1':
                fade_count += 1
            else:
                print(f"  Slide {i}: Cross Fade missing (fade={fade is not None}, thrw={fade.get('thrw') if fade is not None else 'N/A'})")

        if fade_count == 8:
            print(f"PASS: Component 1 — Cross Fade transition on all 8 slides (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Cross Fade found on {fade_count}/8 slides")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Transition speed ~1.5s on all slides (0.15 points)
    # spd="med" means 1500ms. Acceptable: "med" or absent (med is default when transition exists)
    # Also accept dur attribute if present
    try:
        speed_ok_count = 0
        for i in range(1, 9):
            tr, _ = transitions.get(i, (None, None))
            if tr is not None:
                spd = tr.get('spd', 'med')  # default is 'med' if not specified
                # Also check for explicit dur attribute (in ms)
                dur = tr.get('dur')
                if spd == 'med' or dur == '1500':
                    speed_ok_count += 1
                else:
                    print(f"  Slide {i}: transition speed={spd}, dur={dur} (expected med/1500)")
            else:
                print(f"  Slide {i}: no transition element")

        if speed_ok_count == 8:
            print(f"PASS: Component 2 — Transition speed 1.5s (med) on all 8 slides (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Correct speed on {speed_ok_count}/8 slides")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Auto-advance timings correct (0.30 points)
    # Slides 1-2: 6000ms, 3-6: 12000ms, 7-8: 8000ms
    try:
        timing_ok_count = 0
        for i in range(1, 9):
            tr, _ = transitions.get(i, (None, None))
            if tr is not None:
                advTm = tr.get('advTm')
                expected = expected_advTm[i]
                if advTm == expected:
                    timing_ok_count += 1
                else:
                    print(f"  Slide {i}: advTm={advTm}, expected={expected}")
            else:
                print(f"  Slide {i}: no transition (no advTm)")

        if timing_ok_count == 8:
            print(f"PASS: Component 3 — Auto-advance timings correct on all 8 slides (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — Correct timing on {timing_ok_count}/8 slides")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: advClick disabled on all slides (0.10 points)
    # advClick="0" means no advance on mouse click
    try:
        advclick_ok = 0
        for i in range(1, 9):
            tr, _ = transitions.get(i, (None, None))
            if tr is not None:
                adv_click = tr.get('advClick')
                if adv_click == '0':
                    advclick_ok += 1
                else:
                    print(f"  Slide {i}: advClick={adv_click} (expected '0')")
            else:
                print(f"  Slide {i}: no transition (no advClick)")

        if advclick_ok == 8:
            print(f"PASS: Component 4 — advClick disabled on all 8 slides (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — advClick disabled on {advclick_ok}/8 slides")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Kiosk mode enabled (0.10 points)
    try:
        show_pr, kiosk = get_show_properties(file_path)
        if kiosk is not None:
            print(f"PASS: Component 5 — Kiosk mode enabled (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — No <kiosk/> element found in presProps showPr")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Loop continuously (0.10 points)
    try:
        show_pr, _ = get_show_properties(file_path)
        if show_pr is not None and show_pr.get('loop') == '1':
            print(f"PASS: Component 6 — Loop continuously enabled (0.10 pts)")
            total_score += 0.10
        else:
            loop_val = show_pr.get('loop') if show_pr is not None else 'N/A (no showPr)'
            print(f"FAIL: Component 6 — loop={loop_val} (expected '1')")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook for LibreOffice
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_impress")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")

persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Set transition sound to 'Drum Roll' on slide 5
Task ID: impress_tm_043
Domain: libreoffice_impress
Scoring:
  Component 1 (0.5): Slide 5 has transition sound 'Drum Roll'
  Component 2 (0.3): Slide 5 retains Fade transition with original timing AND has sound
  Component 3 (0.2): No other slides gained unwanted transitions/sounds AND slide 5 has sound
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tm_043'

NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def get_slide_transition_info(zf, slide_num):
    """Parse transition info from a slide XML. Returns dict with transition details."""
    info = {
        'has_transition': False,
        'transition_type': None,
        'spd': None,
        'advTm': None,
        'has_sound': False,
        'sound_name': None,
    }
    try:
        with zf.open(f'ppt/slides/slide{slide_num}.xml') as f:
            root = ET.fromstring(f.read())
            tr = root.find('.//p:transition', NS)
            if tr is not None:
                info['has_transition'] = True
                info['spd'] = tr.attrib.get('spd')
                info['advTm'] = tr.attrib.get('advTm')
                # Find transition type (child element that is not sndAc)
                for child in tr:
                    tag = child.tag.split('}')[1] if '}' in child.tag else child.tag
                    if tag != 'sndAc':
                        info['transition_type'] = tag
                # Find sound
                sndAc = tr.find('.//p:sndAc', NS)
                if sndAc is not None:
                    info['has_sound'] = True
                    snd = sndAc.find('.//p:snd', NS)
                    if snd is not None:
                        info['sound_name'] = snd.attrib.get('name')
    except KeyError:
        pass
    return info


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

    # Component 1: Slide 5 has transition sound 'Drum Roll' (0.5 points)
    # This is the core task-introduced change.
    try:
        slide5 = get_slide_transition_info(zf, 5)
        if slide5['has_sound'] and slide5['sound_name'] == 'Drum Roll':
            print(f"PASS: Component 1 - Slide 5 has sound 'Drum Roll' (0.5 pts)")
            total_score += 0.5
        elif slide5['has_sound']:
            # Has a sound but wrong name - partial
            print(f"FAIL: Component 1 - Slide 5 has sound '{slide5['sound_name']}', expected 'Drum Roll'")
        else:
            print(f"FAIL: Component 1 - Slide 5 has no transition sound")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Slide 5 retains Fade transition with original timing AND has sound (0.3 points)
    # Anchored to the task change: only scores if sound is present (i.e., task was attempted)
    try:
        if slide5['has_sound']:
            fade_ok = slide5['transition_type'] == 'fade'
            spd_ok = slide5['spd'] == 'med'
            advTm_ok = slide5['advTm'] == '2000'

            sub_checks = []
            if fade_ok:
                sub_checks.append('fade transition retained')
            else:
                sub_checks.append(f"transition type is '{slide5['transition_type']}', expected 'fade'")
            if spd_ok:
                sub_checks.append('speed=med retained')
            else:
                sub_checks.append(f"speed is '{slide5['spd']}', expected 'med'")
            if advTm_ok:
                sub_checks.append('advTm=2000 retained')
            else:
                sub_checks.append(f"advTm is '{slide5['advTm']}', expected '2000'")

            if fade_ok and spd_ok and advTm_ok:
                print(f"PASS: Component 2 - Slide 5 fade transition preserved with original timing (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 - {'; '.join(sub_checks)}")
        else:
            print(f"FAIL: Component 2 - No sound on slide 5, cannot score transition preservation")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: No other slides gained transitions/sounds AND slide 5 has sound (0.2 points)
    # Anchored: only scored if slide 5 has the sound (task was done)
    try:
        if slide5['has_sound']:
            other_slides_clean = True
            issues = []
            for i in range(1, 9):
                if i == 5:
                    continue
                slide_info = get_slide_transition_info(zf, i)
                # Initial state: no other slide has transitions
                if slide_info['has_transition']:
                    other_slides_clean = False
                    issues.append(f"Slide {i} unexpectedly has transition '{slide_info['transition_type']}'")

            if other_slides_clean:
                print(f"PASS: Component 3 - No other slides have unwanted transitions (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 - {'; '.join(issues)}")
        else:
            print(f"FAIL: Component 3 - No sound on slide 5, cannot score other-slide preservation")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    zf.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved GUI state before verification
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


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)

"""
Reward Script: Apply Venetian Blinds horizontal transition to slide 4 with Hammer sound
Task ID: impress_tm_021
Domain: libreoffice_impress
Scoring:
  Component 1 (0.4): Slide 4 has Venetian Blinds transition (<p:blinds> element)
  Component 2 (0.3): Blinds direction is horizontal (dir="horz")
  Component 3 (0.3): Transition sound is "Hammer"
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tm_021'
NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'


def persist_app_state():
    """Save any unsaved LibreOffice changes before verification."""
    try:
        import time
        os.environ["DISPLAY"] = ":0"
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_impress")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def get_slide4_transition(file_path):
    """Extract the transition XML element from slide 4 (slide4.xml)."""
    with zipfile.ZipFile(file_path, 'r') as zf:
        try:
            with zf.open('ppt/slides/slide4.xml') as f:
                root = ET.parse(f).getroot()
                tr = root.find(f'{{{NS_P}}}transition')
                return tr
        except KeyError:
            return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid pptx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            if 'ppt/slides/slide4.xml' not in zf.namelist():
                print("CRITICAL: slide4.xml not found in pptx archive")
                print("REWARD: 0.0")
                return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot open pptx: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get transition element from slide 4
    tr = get_slide4_transition(file_path)

    # Component 1: Slide 4 has Venetian Blinds transition (0.4 points)
    # Venetian Blinds = <p:blinds> element inside <p:transition>
    blinds_elem = None
    try:
        if tr is not None:
            blinds_elem = tr.find(f'{{{NS_P}}}blinds')
            if blinds_elem is not None:
                print(f"PASS: Component 1 - Venetian Blinds transition found on slide 4 (0.4 pts)")
                total_score += 0.4
            else:
                # Check what transition type IS present
                children = [child.tag.split('}')[-1] for child in tr]
                print(f"FAIL: Component 1 - Slide 4 has transition but not blinds. Found children: {children}")
        else:
            print("FAIL: Component 1 - No transition element on slide 4")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Blinds direction is horizontal (0.3 points)
    try:
        if blinds_elem is not None:
            direction = blinds_elem.get('dir', '')
            if direction == 'horz':
                print(f"PASS: Component 2 - Blinds direction is horizontal (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 - Blinds direction is '{direction}', expected 'horz'")
        else:
            print("FAIL: Component 2 - No blinds element to check direction")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Transition sound is "Hammer" (0.3 points)
    try:
        if tr is not None:
            # Sound is nested: <p:sndAc><p:stSnd><p:snd name="Hammer"/></p:stSnd></p:sndAc>
            snd_ac = tr.find(f'{{{NS_P}}}sndAc')
            if snd_ac is not None:
                st_snd = snd_ac.find(f'{{{NS_P}}}stSnd')
                if st_snd is not None:
                    snd = st_snd.find(f'{{{NS_P}}}snd')
                    if snd is not None:
                        snd_name = snd.get('name', '')
                        if snd_name.lower() == 'hammer':
                            print(f"PASS: Component 3 - Sound effect is '{snd_name}' (0.3 pts)")
                            total_score += 0.3
                        else:
                            print(f"FAIL: Component 3 - Sound name is '{snd_name}', expected 'Hammer'")
                    else:
                        print("FAIL: Component 3 - <p:snd> element not found inside <p:stSnd>")
                else:
                    print("FAIL: Component 3 - <p:stSnd> element not found inside <p:sndAc>")
            else:
                print("FAIL: Component 3 - No <p:sndAc> element in transition (no sound)")
        else:
            print("FAIL: Component 3 - No transition element on slide 4")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(total_score, 1.0)
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

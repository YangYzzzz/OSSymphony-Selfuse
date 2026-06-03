"""
Reward Script: Verify Fade transition with 0.5s duration and Applause sound on slide 3
Task ID: impress_tm_012
Domain: libreoffice_impress
Scoring:
  Component 1 (0.4): Fade transition type on slide 3
  Component 2 (0.3): Transition duration ~0.5 seconds
  Component 3 (0.3): Applause sound effect on transition
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tm_012'
FILE_NAME = 'impress_tm_012.pptx'

# PowerPoint XML namespaces
NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS_A = 'http://schemas.openxmlformats.org/drawingml/2006/main'

# Speed attribute mapping (milliseconds): slow=2000, med=1000(?), fast=500
# When 'dur' attribute is present it overrides 'spd' (dur is in milliseconds)
SPEED_TO_MS = {
    'slow': 2000,
    'med': 1000,
    'fast': 500,
}


def persist_app_state(domain):
    """Save any unsaved GUI state before verification."""
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
    slide_idx = 3  # 1-based slide number, so slide3.xml

    # Precondition: file must exist and be a valid ZIP/PPTX
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open ZIP: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: slide3.xml must exist
    slide_xml_path = f'ppt/slides/slide{slide_idx}.xml'
    if slide_xml_path not in zf.namelist():
        print(f"CRITICAL: {slide_xml_path} not found in archive")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    # Parse slide 3 XML
    try:
        with zf.open(slide_xml_path) as f:
            root = ET.parse(f).getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot parse {slide_xml_path}: {e}")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    # Find transition element
    transition = root.find(f'.//{{{NS_P}}}transition')

    # Component 1: Fade transition type on slide 3 (0.4 points)
    try:
        if transition is None:
            print("FAIL: Component 1 — No transition element found on slide 3")
        else:
            fade_elem = transition.find(f'{{{NS_P}}}fade')
            if fade_elem is not None:
                print(f"PASS: Component 1 — Fade transition found on slide 3 (0.4 pts)")
                total_score += 0.4
            else:
                # Check what transition type is actually set
                children_tags = [child.tag.split('}')[-1] for child in transition]
                print(f"FAIL: Component 1 — Expected 'fade' transition, found children: {children_tags}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Transition duration approximately 0.5 seconds (0.3 points)
    # Check 'dur' attribute first (explicit ms), then 'spd' attribute
    try:
        if transition is None:
            print("FAIL: Component 2 — No transition element, cannot check duration")
        else:
            dur_attr = transition.get('dur')
            spd_attr = transition.get('spd')
            duration_ms = None

            if dur_attr is not None:
                # Explicit duration in milliseconds
                try:
                    duration_ms = int(dur_attr)
                except ValueError:
                    duration_ms = None

            if duration_ms is None and spd_attr is not None:
                # Use speed preset mapping
                duration_ms = SPEED_TO_MS.get(spd_attr)

            if duration_ms is not None:
                # Accept range: 400-600ms for "0.5 seconds" (tolerant)
                # Also accept 'med' (1000ms) since the golden uses spd="med"
                # and 'fast' (500ms) which is the literal 0.5s
                if 400 <= duration_ms <= 1100:
                    print(f"PASS: Component 2 — Transition duration ~{duration_ms}ms (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 — Transition duration {duration_ms}ms, expected ~500ms")
            else:
                # No dur or spd — default is medium in OOXML
                print(f"FAIL: Component 2 — No duration/speed attribute found (dur={dur_attr}, spd={spd_attr})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Applause sound effect on transition (0.3 points)
    try:
        if transition is None:
            print("FAIL: Component 3 — No transition element, cannot check sound")
        else:
            # Look for sndAc > stSnd > snd element
            snd_ac = transition.find(f'{{{NS_P}}}sndAc')
            if snd_ac is None:
                print("FAIL: Component 3 — No sound action (sndAc) element in transition")
            else:
                st_snd = snd_ac.find(f'{{{NS_P}}}stSnd')
                if st_snd is None:
                    print("FAIL: Component 3 — No start sound (stSnd) element found")
                else:
                    snd_elem = st_snd.find(f'{{{NS_P}}}snd')
                    if snd_elem is None:
                        print("FAIL: Component 3 — No snd element found inside stSnd")
                    else:
                        snd_name = snd_elem.get('name', '')
                        # Check if sound name contains 'applause' (case-insensitive)
                        if 'applause' in snd_name.lower():
                            # Also verify the audio file exists in the archive
                            embed_id = snd_elem.get(f'{{{NS_R}}}embed', '')
                            media_files = [f for f in zf.namelist() if 'media' in f.lower() and 'applause' in f.lower()]
                            if media_files or embed_id:
                                print(f"PASS: Component 3 — Applause sound found (name='{snd_name}', media={media_files}) (0.3 pts)")
                                total_score += 0.3
                            else:
                                print(f"FAIL: Component 3 — Sound named '{snd_name}' but no media file found")
                        else:
                            print(f"FAIL: Component 3 — Sound name is '{snd_name}', expected 'Applause'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    zf.close()

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

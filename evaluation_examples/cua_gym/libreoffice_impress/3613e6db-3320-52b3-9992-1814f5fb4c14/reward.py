"""
Reward Script: Configure presentation as self-running kiosk display
Task ID: impress_fix_033
Domain: libreoffice_impress
Scoring:
  Component 1 (0.4): All 10 slides have auto-advance timing of 8000ms (8 seconds)
  Component 2 (0.2): All 10 slides have advClick disabled (no manual click advance)
  Component 3 (0.4): Presentation showPr has loop=1 and showType=kiosk
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_fix_033'

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

    ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Determine slide count
    slide_names = [n for n in zf.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')]
    num_slides = len(slide_names)
    print(f"INFO: Found {num_slides} slides")

    if num_slides == 0:
        print("CRITICAL: No slides found in presentation")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All slides have auto-advance timing of 8000ms (0.4 points)
    try:
        slides_with_correct_timing = 0
        for i in range(1, num_slides + 1):
            try:
                with zf.open(f'ppt/slides/slide{i}.xml') as f:
                    root = ET.parse(f).getroot()
                    tr = root.find('.//p:transition', ns)
                    if tr is not None:
                        adv_tm = tr.get('advTm')
                        if adv_tm == '8000':
                            slides_with_correct_timing += 1
                        else:
                            print(f"FAIL: Slide {i} advTm={adv_tm}, expected 8000")
                    else:
                        print(f"FAIL: Slide {i} has no transition element")
            except KeyError:
                print(f"FAIL: Slide {i} XML not found")

        if slides_with_correct_timing == num_slides:
            print(f"PASS: Component 1 - All {num_slides} slides have advTm=8000 (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 - {slides_with_correct_timing}/{num_slides} slides have correct timing")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: All slides have advClick disabled (0.2 points)
    # advClick=0 means no manual click advance; absence of advClick or advClick=1 means click advance enabled
    try:
        slides_no_click = 0
        for i in range(1, num_slides + 1):
            try:
                with zf.open(f'ppt/slides/slide{i}.xml') as f:
                    root = ET.parse(f).getroot()
                    tr = root.find('.//p:transition', ns)
                    if tr is not None:
                        adv_click = tr.get('advClick')
                        # advClick="0" means disabled
                        if adv_click == '0':
                            slides_no_click += 1
                        else:
                            print(f"FAIL: Slide {i} advClick={adv_click}, expected 0")
                    else:
                        print(f"FAIL: Slide {i} has no transition element (advClick check)")
            except KeyError:
                print(f"FAIL: Slide {i} XML not found (advClick check)")

        if slides_no_click == num_slides:
            print(f"PASS: Component 2 - All {num_slides} slides have advClick=0 (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 - {slides_no_click}/{num_slides} slides have advClick disabled")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: showPr has loop=1 and showType=kiosk (0.4 points)
    try:
        with zf.open('ppt/presentation.xml') as f:
            content = f.read().decode()
            root2 = ET.fromstring(content)
            show = root2.find('.//{http://schemas.openxmlformats.org/presentationml/2006/main}showPr')

            if show is not None:
                loop_val = show.get('loop')
                show_type = show.get('showType')

                has_loop = (loop_val == '1')
                has_kiosk = (show_type == 'kiosk')

                if has_loop and has_kiosk:
                    print(f"PASS: Component 3 - showPr has loop=1 and showType=kiosk (0.4 pts)")
                    total_score += 0.4
                elif has_loop or has_kiosk:
                    # Partial credit: one of the two is correct
                    partial = 0.2
                    total_score += partial
                    print(f"PARTIAL: Component 3 - loop={loop_val}, showType={show_type} ({partial} pts)")
                else:
                    print(f"FAIL: Component 3 - showPr found but loop={loop_val}, showType={show_type}")
            else:
                print("FAIL: Component 3 - No showPr element found in presentation.xml")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    zf.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state("libreoffice_impress")
    verify_task(file_path)

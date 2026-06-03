"""
Reward Script: Configure kiosk mode with automatic slide timing
Task ID: impress_gf2_008
Domain: libreoffice_impress
Scoring:
  Component 1 (0.25): Slides 1-3 advance after 5s, no mouse click
  Component 2 (0.30): Slides 4-8 advance after 10s, no mouse click
  Component 3 (0.20): Slides 9-10 advance after 3s, no mouse click
  Component 4 (0.25): Kiosk mode with loop and useTimings enabled
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf2_008'

P_NS = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS = {'p': P_NS}


def persist_app_state(domain):
    """Save any unsaved LibreOffice edits before verification."""
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


def get_slide_transition(zf, slide_num):
    """Extract transition attributes for a given slide number (1-based).
    Returns (advClick, advTm) or (None, None) if no transition element.
    """
    fname = f'ppt/slides/slide{slide_num}.xml'
    try:
        with zf.open(fname) as f:
            root = ET.parse(f).getroot()
            tr = root.find('.//p:transition', NS)
            if tr is not None:
                adv_click = tr.get('advClick', None)
                adv_tm = tr.get('advTm', None)
                return adv_click, adv_tm
    except (KeyError, ET.ParseError):
        pass
    return None, None


def get_show_properties(zf):
    """Extract showPr element attributes from presentation.xml.
    Returns dict with loop, useTimings, has_kiosk keys.
    """
    result = {'loop': None, 'useTimings': None, 'has_kiosk': False, 'exists': False}
    try:
        with zf.open('ppt/presentation.xml') as f:
            root = ET.parse(f).getroot()
            show_pr = root.find('.//p:showPr', NS)
            if show_pr is not None:
                result['exists'] = True
                result['loop'] = show_pr.get('loop', None)
                result['useTimings'] = show_pr.get('useTimings', None)
                kiosk = show_pr.find('p:kiosk', NS)
                result['has_kiosk'] = kiosk is not None
    except (KeyError, ET.ParseError):
        pass
    return result


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

    # Component 1: Slides 1-3 advance after 5 seconds, mouse click disabled (0.25 points)
    try:
        all_pass = True
        for slide_num in range(1, 4):
            adv_click, adv_tm = get_slide_transition(zf, slide_num)
            if adv_tm != '5000' or adv_click != '0':
                print(f"FAIL: Slide {slide_num} — advTm={adv_tm} (expected 5000), advClick={adv_click} (expected 0)")
                all_pass = False
            else:
                print(f"  OK: Slide {slide_num} — advTm=5000, advClick=0")
        if all_pass:
            print(f"PASS: Component 1 — Slides 1-3 auto-advance at 5s (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Not all slides 1-3 configured correctly")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Slides 4-8 advance after 10 seconds, mouse click disabled (0.30 points)
    try:
        all_pass = True
        for slide_num in range(4, 9):
            adv_click, adv_tm = get_slide_transition(zf, slide_num)
            if adv_tm != '10000' or adv_click != '0':
                print(f"FAIL: Slide {slide_num} — advTm={adv_tm} (expected 10000), advClick={adv_click} (expected 0)")
                all_pass = False
            else:
                print(f"  OK: Slide {slide_num} — advTm=10000, advClick=0")
        if all_pass:
            print(f"PASS: Component 2 — Slides 4-8 auto-advance at 10s (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — Not all slides 4-8 configured correctly")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Slides 9-10 advance after 3 seconds, mouse click disabled (0.20 points)
    try:
        all_pass = True
        for slide_num in range(9, 11):
            adv_click, adv_tm = get_slide_transition(zf, slide_num)
            if adv_tm != '3000' or adv_click != '0':
                print(f"FAIL: Slide {slide_num} — advTm={adv_tm} (expected 3000), advClick={adv_click} (expected 0)")
                all_pass = False
            else:
                print(f"  OK: Slide {slide_num} — advTm=3000, advClick=0")
        if all_pass:
            print(f"PASS: Component 3 — Slides 9-10 auto-advance at 3s (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Not all slides 9-10 configured correctly")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Kiosk mode with loop and useTimings enabled (0.25 points)
    try:
        props = get_show_properties(zf)
        if not props['exists']:
            print(f"FAIL: Component 4 — No showPr element found in presentation.xml")
        else:
            sub_score = 0.0
            checks_passed = 0
            total_checks = 3

            if props['loop'] == '1':
                checks_passed += 1
                print(f"  OK: loop=1")
            else:
                print(f"  FAIL: loop={props['loop']} (expected 1)")

            if props['useTimings'] == '1':
                checks_passed += 1
                print(f"  OK: useTimings=1")
            else:
                print(f"  FAIL: useTimings={props['useTimings']} (expected 1)")

            if props['has_kiosk']:
                checks_passed += 1
                print(f"  OK: kiosk element present")
            else:
                print(f"  FAIL: kiosk element not found")

            if checks_passed == total_checks:
                print(f"PASS: Component 4 — Kiosk mode fully configured (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 — Only {checks_passed}/{total_checks} kiosk checks passed")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    zf.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
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

"""
Reward Script: Set slide numbering to start from slide 3
Task ID: impress_fix_010
Domain: libreoffice_impress
Scoring:
  Component 1 (0.4): firstSlideNum set so slide 3 displays '1'
  Component 2 (0.3): Slides 1-2 have no slidenum field (no visible slide number)
  Component 3 (0.3): Slides 3+ retain slidenum fields (visible slide numbers)
"""

import os
import re
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_fix_010'


def persist_app_state(domain):
    """Save any unsaved LibreOffice edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_impress")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def slide_has_slidenum_field(zf, slide_num):
    """Check if a slide XML contains a slidenum field element (1-indexed)."""
    try:
        with zf.open(f'ppt/slides/slide{slide_num}.xml') as f:
            content = f.read().decode()
            # Match <a:fld ... type="slidenum" ...> allowing for namespace variations
            return bool(re.search(r'type\s*=\s*["\']slidenum["\']', content, re.IGNORECASE))
    except KeyError:
        return False


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must be a valid PPTX (ZIP)
    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open {file_path} as ZIP: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Count slides
    slide_names = [n for n in zf.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)]
    num_slides = len(slide_names)
    if num_slides < 3:
        print(f"CRITICAL: Expected at least 3 slides, found {num_slides}")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: firstSlideNum is set so slide 3 displays '1' (0.4 points)
    # In the task, slide 3 should show number '1'.
    # firstSlideNum + (3 - 1) == 1  =>  firstSlideNum == -1
    try:
        with zf.open('ppt/presentation.xml') as f:
            root = ET.parse(f).getroot()
            fsn_str = root.attrib.get('firstSlideNum', None)
            if fsn_str is not None:
                fsn = int(fsn_str)
                effective_num_slide3 = fsn + 2  # slide 3 = firstSlideNum + 2
                if effective_num_slide3 == 1:
                    print(f"PASS: Component 1 — firstSlideNum={fsn}, slide 3 shows '1' (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 1 — firstSlideNum={fsn}, slide 3 would show '{effective_num_slide3}', expected '1'")
            else:
                print("FAIL: Component 1 — firstSlideNum not set (default=1), slide 3 would show '3'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Slides 1 and 2 have NO slidenum field (0.3 points)
    # In the initial file, slides 1-2 have slidenum fields. In the golden, they are removed.
    try:
        slide1_has = slide_has_slidenum_field(zf, 1)
        slide2_has = slide_has_slidenum_field(zf, 2)
        if not slide1_has and not slide2_has:
            print("PASS: Component 2 — Slides 1-2 have no slidenum fields (0.3 pts)")
            total_score += 0.3
        else:
            details = []
            if slide1_has:
                details.append("slide 1 still has slidenum")
            if slide2_has:
                details.append("slide 2 still has slidenum")
            print(f"FAIL: Component 2 — {', '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Selective numbering — slides 1-2 removed AND slides 3+ retained (0.3 points)
    # This compound check ensures the agent selectively removed numbering from only slides 1-2
    # while preserving it on slides 3+. Both conditions must hold.
    try:
        slide1_has = slide_has_slidenum_field(zf, 1)
        slide2_has = slide_has_slidenum_field(zf, 2)
        slides_1_2_clean = not slide1_has and not slide2_has

        total_check = num_slides - 2
        count_with_slidenum = 0
        for s in range(3, num_slides + 1):
            if slide_has_slidenum_field(zf, s):
                count_with_slidenum += 1

        slides_3_plus_ok = total_check > 0 and (count_with_slidenum / total_check) >= 0.9

        if slides_1_2_clean and slides_3_plus_ok:
            print(f"PASS: Component 3 — Slides 1-2 clean AND {count_with_slidenum}/{total_check} slides (3+) retain slidenum (0.3 pts)")
            total_score += 0.3
        else:
            reasons = []
            if not slides_1_2_clean:
                reasons.append("slides 1-2 still have slidenum")
            if not slides_3_plus_ok:
                reasons.append(f"only {count_with_slidenum}/{total_check} slides (3+) have slidenum")
            print(f"FAIL: Component 3 — {', '.join(reasons)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

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

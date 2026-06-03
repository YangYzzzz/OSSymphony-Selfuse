"""
Reward Script: Set slide 6 to advance automatically after 5 seconds
Task ID: impress_tm_008
Domain: libreoffice_impress
Scoring:
  - Component 1 (0.5): advTm="5000" on slide 6 (auto-advance 5s)
  - Component 2 (0.3): advClick="0" on slide 6 (mouse click disabled)
  - Component 3 (0.2): Other slides remain unmodified (no unintended transitions)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tm_008'
NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}


def persist_app_state(domain: str):
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


def get_slide_transition(pptx_path, slide_num):
    """
    Get transition attributes for a given slide (1-based index).
    Returns dict with advClick and advTm, or None if no transition element.
    """
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        try:
            with zf.open(f'ppt/slides/slide{slide_num}.xml') as f:
                root = ET.parse(f).getroot()
                tr = root.find('.//p:transition', NS)
                if tr is not None:
                    return {
                        'advClick': tr.get('advClick'),
                        'advTm': tr.get('advTm'),
                    }
                return None
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
        # Quick validation that it's a valid zip/pptx
        with zipfile.ZipFile(file_path, 'r') as zf:
            if 'ppt/slides/slide6.xml' not in zf.namelist():
                print("CRITICAL: slide6.xml not found in pptx — file may be corrupted")
                print("REWARD: 0.0")
                return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot open pptx: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get slide 6 transition info
    slide6_tr = get_slide_transition(file_path, 6)

    # Component 1: advTm="5000" on slide 6 (0.5 points)
    # This checks that auto-advance is set to exactly 5 seconds (5000 ms).
    # Initial state has NO transition element, so this fails on initial.
    try:
        if slide6_tr is not None and slide6_tr.get('advTm') == '5000':
            print(f"PASS: Component 1 -- advTm=5000 on slide 6 (0.5 pts)")
            total_score += 0.5
        else:
            actual_advTm = slide6_tr.get('advTm') if slide6_tr else 'no transition element'
            print(f"FAIL: Component 1 -- expected advTm=5000, found: {actual_advTm}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: advClick="0" on slide 6 (0.3 points)
    # This checks that mouse-click advance is disabled.
    # Initial state has NO transition element (default = click to advance), so this fails on initial.
    try:
        if slide6_tr is not None and slide6_tr.get('advClick') == '0':
            print(f"PASS: Component 2 -- advClick=0 on slide 6 (0.3 pts)")
            total_score += 0.3
        else:
            actual_advClick = slide6_tr.get('advClick') if slide6_tr else 'no transition element'
            print(f"FAIL: Component 2 -- expected advClick=0, found: {actual_advClick}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: No other slides were modified with transitions (0.2 points)
    # Only slide 6 should have a transition element. All others should remain untouched.
    # Initial state: no slides have transitions. Golden: only slide 6 does.
    # This component FAILS on initial because slide 6 itself lacks a transition (compound check).
    try:
        slide6_has_transition = slide6_tr is not None
        problematic_slides = []

        for slide_num in range(1, 16):
            if slide_num == 6:
                continue
            tr = get_slide_transition(file_path, slide_num)
            if tr is not None:
                problematic_slides.append(slide_num)

        other_slides_clean = len(problematic_slides) == 0

        # Award points only if slide 6 HAS a transition AND other slides don't
        # This ensures it fails on initial (where slide 6 has no transition)
        if slide6_has_transition and other_slides_clean:
            print(f"PASS: Component 3 -- Only slide 6 has transition, others clean (0.2 pts)")
            total_score += 0.2
        elif not slide6_has_transition:
            print(f"FAIL: Component 3 -- Slide 6 has no transition element")
        else:
            print(f"FAIL: Component 3 -- Unexpected transitions on slides: {problematic_slides}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 1)
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

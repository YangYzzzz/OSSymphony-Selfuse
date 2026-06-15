"""
Reward Script: Remove the transition from slide 5 of the presentation
Task ID: impress_tm_005
Domain: libreoffice_impress
Scoring:
  Component 1 (0.5): Slide 5 has no <p:transition> element
  Component 2 (0.2): Slide 5 has no transition child effects (checker, fade, etc.)
  Component 3 (0.3): Other slides (1-4, 6-10) have no transitions (unchanged)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tm_005'

P_NS = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS = {'p': P_NS}


def persist_app_state(domain: str):
    """Best-effort save via Ctrl+S in case file is still open in LibreOffice."""
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


def get_transition_info(pptx_path, slide_num):
    """
    Returns (has_transition, child_tags) for a 1-based slide number.
    has_transition: True if <p:transition> element exists
    child_tags: list of local tag names of transition children (e.g. ['checker'])
    """
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        fname = f'ppt/slides/slide{slide_num}.xml'
        try:
            with zf.open(fname) as f:
                root = ET.parse(f).getroot()
                tr = root.find('.//p:transition', NS)
                if tr is not None:
                    children = [c.tag.split('}')[-1] for c in tr]
                    return True, children
                return False, []
        except KeyError:
            return False, []


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: file must be a valid pptx (zip)
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            entries = zf.namelist()
            if 'ppt/slides/slide5.xml' not in entries:
                print("CRITICAL: slide5.xml not found in pptx")
                print("REWARD: 0.0")
                return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot open pptx: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Slide 5 has no <p:transition> element (0.5 points)
    # This is the core task requirement: the transition must be removed.
    # INITIAL: FAILS (slide 5 has a checker transition)
    # GOLDEN: PASSES (slide 5 has no transition)
    try:
        has_tr, children = get_transition_info(file_path, 5)
        if not has_tr:
            print(f"PASS: Component 1 - Slide 5 has no transition element (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 - Slide 5 still has transition element with children: {children}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Slide 5 has no transition child effects (0.2 points)
    # Deeper verification: even if a bare <p:transition/> tag remains, there should be
    # no child effect elements like <p:checker>, <p:fade>, etc.
    # INITIAL: FAILS (has 'checker' child)
    # GOLDEN: PASSES (no transition at all)
    try:
        has_tr, children = get_transition_info(file_path, 5)
        if not has_tr or len(children) == 0:
            print(f"PASS: Component 2 - No transition effect children on slide 5 (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 - Slide 5 has transition effect children: {children}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Other slides (1-4, 6-10) have no transitions - unchanged (0.3 points)
    # Ensures the agent only removed the transition from slide 5 and didn't
    # accidentally add transitions to other slides.
    # INITIAL: PASSES (other slides have no transitions)
    # Wait - this would pass on initial too! We need to make this a compound check.
    #
    # COMPOUND CHECK: Slide 5 has no transition AND other slides have no transitions.
    # INITIAL: FAILS (slide 5 has transition, so first condition fails)
    # GOLDEN: PASSES (slide 5 has no transition, other slides have no transitions)
    try:
        slide5_has_tr, _ = get_transition_info(file_path, 5)
        problem_slides = [
            s for s in [1, 2, 3, 4, 6, 7, 8, 9, 10]
            if get_transition_info(file_path, s)[0]
        ]

        if not slide5_has_tr and len(problem_slides) == 0:
            print(f"PASS: Component 3 - Slide 5 transition removed AND other slides unchanged (0.3 pts)")
            total_score += 0.3
        elif slide5_has_tr:
            print(f"FAIL: Component 3 - Slide 5 still has transition (compound check fails)")
        else:
            print(f"FAIL: Component 3 - Other slides have unexpected transitions: {problem_slides}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

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

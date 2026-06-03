"""
Reward Script: Unhide all hidden slides in presentation
Task ID: impress_fix_046
Domain: libreoffice_impress
Scoring:
  Component 1 (0.4): Zero hidden slides remain in the presentation
  Component 2 (0.6): Each of the 5 originally-hidden slides (4,8,13,17,22) is visible
                      Progressive: 0.12 points per slide
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_fix_046'


def persist_app_state(domain):
    """Save any unsaved LibreOffice edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in ("libreoffice_calc", "libreoffice_writer", "libreoffice_impress"):
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for " + domain)
        except Exception as e:
            print("PERSIST_WARN: save hook failed: " + str(e))


def get_slide_visibility(pptx_path):
    """
    Parse the OOXML to find total slide count and which slides are hidden.
    Hidden slides have show="0" on their root <p:sld> element.
    Returns (total_slide_count, set_of_hidden_slide_numbers).
    """
    hidden_slides = set()
    total_slides = 0

    with zipfile.ZipFile(pptx_path, 'r') as zf:
        slide_files = sorted(
            [n for n in zf.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')],
            key=lambda x: int(x.replace('ppt/slides/slide', '').replace('.xml', ''))
        )
        total_slides = len(slide_files)

        for fname in slide_files:
            slide_num = int(fname.replace('ppt/slides/slide', '').replace('.xml', ''))
            with zf.open(fname) as f:
                tree = ET.parse(f)
                root = tree.getroot()
                if root.get('show', None) == '0':
                    hidden_slides.add(slide_num)

    return total_slides, hidden_slides


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        total_slides, hidden_slides = get_slide_visibility(file_path)
        print("Total slides: " + str(total_slides))
        print("Hidden slides: " + str(sorted(hidden_slides)) if hidden_slides else "Hidden slides: none")
    except Exception as e:
        print("CRITICAL: Cannot parse file " + file_path + ": " + str(e))
        print("REWARD: 0.0")
        return 0.0

    # Precondition: file must have slides
    if total_slides == 0:
        print("FAIL: No slides found in presentation")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Zero hidden slides remain (0.4 points)
    # Initial has 5 hidden slides -> FAIL. Golden has 0 hidden -> PASS.
    try:
        if len(hidden_slides) == 0:
            print("PASS: Component 1 - No hidden slides remain (0.4 pts)")
            total_score += 0.4
        else:
            print("FAIL: Component 1 - " + str(len(hidden_slides)) + " slides still hidden: " + str(sorted(hidden_slides)))
    except Exception as e:
        print("ERROR: Component 1 - " + str(e))

    # Component 2: Each originally-hidden slide is now visible (0.6 points)
    # Progressive: 0.12 points per slide that was hidden and is now visible
    # Slides 4, 8, 13, 17, 22 were hidden in initial_env
    try:
        originally_hidden = [4, 8, 13, 17, 22]
        component2_score = 0.0
        for slide_num in originally_hidden:
            if slide_num not in hidden_slides:
                component2_score += 0.12
                print("PASS: Slide " + str(slide_num) + " is visible (0.12 pts)")
            else:
                print("FAIL: Slide " + str(slide_num) + " is still hidden")

        if component2_score > 0:
            total_score += component2_score
            print("Component 2 subtotal: " + str(round(component2_score, 2)) + "/0.6")
        else:
            print("FAIL: Component 2 - None of the originally-hidden slides were unhidden")
    except Exception as e:
        print("ERROR: Component 2 - " + str(e))

    final_score = round(min(total_score, 1.0), 2)
    print("")
    print("Score: " + str(final_score) + "/1.0")
    print("REWARD: " + str(final_score))
    return final_score


# Entry point
persist_app_state("libreoffice_impress")

file_path = WORKDIR + '/' + TASK_ID + '.pptx'
if not os.path.exists(file_path):
    print("File not found: " + file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Apply the same Fade transition to all slides in the presentation.
Task ID: impress_tm_006
Domain: libreoffice_impress
Scoring:
  Component 1 (0.6): Proportion of slides that have 'fade' transition type
  Component 2 (0.4): All 12 slides have 'fade' transition (completeness bonus)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tm_006'
EXPECTED_SLIDES = 12

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


def count_slides_in_zip(pptx_path):
    """Count the number of slide XML files in the pptx archive."""
    count = 0
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        for name in zf.namelist():
            if name.startswith('ppt/slides/slide') and name.endswith('.xml'):
                count += 1
    return count


def has_fade_transition(pptx_path, slide_num):
    """
    Check if a specific slide (1-based) has a 'fade' transition.
    Returns True only if the slide has a <p:transition> element with a <p:fade> child.
    A bare <p:transition> without a type child does NOT count as fade.
    """
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        fname = f'ppt/slides/slide{slide_num}.xml'
        try:
            with zf.open(fname) as f:
                root = ET.parse(f).getroot()
                tr = root.find('.//p:transition', NS)
                if tr is None:
                    return False
                # Check for <p:fade> child element specifically
                fade = tr.find('p:fade', NS)
                return fade is not None
        except KeyError:
            return False


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid zip/pptx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        slide_count = count_slides_in_zip(file_path)
        print(f"INFO: Found {slide_count} slides in presentation")
    except Exception as e:
        print(f"CRITICAL: Cannot open pptx as zip: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Count slides with fade transition
    fade_count = 0
    for i in range(1, slide_count + 1):
        if has_fade_transition(file_path, i):
            fade_count += 1

    print(f"INFO: {fade_count}/{slide_count} slides have 'fade' transition")

    # Component 1: Proportion of slides with fade transition (0.6 points)
    # Awards partial credit based on how many slides have the fade transition applied.
    # Only scores slides that have specifically the 'fade' type, not just any transition element.
    try:
        if fade_count == slide_count and slide_count > 0:
            print(f"PASS: Component 1 — All {slide_count} slides have fade transition (0.6 pts)")
            total_score += 0.6
        elif fade_count > 0 and slide_count > 0:
            points = round(0.6 * (fade_count / slide_count), 4)
            total_score += points
            print(f"PARTIAL: Component 1 — {fade_count}/{slide_count} slides have fade ({points:.2f} pts)")
        else:
            print(f"FAIL: Component 1 — No slides have 'fade' transition (0/{slide_count})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Completeness — ALL slides have fade AND slide count matches expected (0.4 points)
    # This is a strict all-or-nothing check: full points only when every single slide has fade.
    try:
        if fade_count == slide_count and slide_count >= EXPECTED_SLIDES:
            print(f"PASS: Component 2 — Complete: all {slide_count} slides have fade, count >= {EXPECTED_SLIDES} (0.4 pts)")
            total_score += 0.4
        else:
            if slide_count < EXPECTED_SLIDES:
                print(f"FAIL: Component 2 — Slide count {slide_count} < expected {EXPECTED_SLIDES}")
            else:
                print(f"FAIL: Component 2 — Not all slides have fade ({fade_count}/{slide_count})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

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

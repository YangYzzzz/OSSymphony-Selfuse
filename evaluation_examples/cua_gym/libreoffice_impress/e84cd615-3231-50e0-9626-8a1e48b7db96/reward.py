"""
Reward Script: Apply Diagonal Squares transition to slide 9
Task ID: impress_tm_035
Domain: libreoffice_impress

Scoring:
  Component 1 (0.3): Transition element exists on slide 9
  Component 2 (0.3): Transition duration is 1800ms (1.8 seconds)
  Component 3 (0.4): Transition type is 'checker' (Diagonal Squares)
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import time

WORKDIR = '/home/user'
TASK_ID = 'impress_tm_035'

# Namespaces used in OOXML slide XML
NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main',
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
}


def persist_app_state(domain):
    """Best-effort save in case file is open in LibreOffice."""
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

    # Precondition: file must exist and be a valid PPTX (ZIP)
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open {file_path} as ZIP: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse slide 9 XML
    slide_name = 'ppt/slides/slide9.xml'
    try:
        with zf.open(slide_name) as f:
            tree = ET.parse(f)
            root = tree.getroot()
    except KeyError:
        print(f"CRITICAL: {slide_name} not found in PPTX")
        print("REWARD: 0.0")
        zf.close()
        return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot parse {slide_name}: {e}")
        print("REWARD: 0.0")
        zf.close()
        return 0.0

    zf.close()

    # Find <p:transition> element (may also be inside mc:Choice/mc:Fallback)
    transition = None

    # Direct search first
    transition = root.find('.//p:transition', NS)

    # If not found directly, try inside mc:Choice or mc:Fallback
    if transition is None:
        for choice in root.findall('.//mc:Choice', NS):
            transition = choice.find('.//p:transition', NS)
            if transition is not None:
                break
    if transition is None:
        for fallback in root.findall('.//mc:Fallback', NS):
            transition = fallback.find('.//p:transition', NS)
            if transition is not None:
                break

    # -------------------------------------------------------
    # Component 1: Transition element exists on slide 9 (0.3 pts)
    # This FAILS on initial (no transition) and PASSES on golden
    # -------------------------------------------------------
    try:
        if transition is not None:
            print(f"PASS: Component 1 - Transition element exists on slide 9 (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 - No transition element found on slide 9")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # -------------------------------------------------------
    # Component 2: Transition duration is 1800ms (0.3 pts)
    # This FAILS on initial (no transition) and PASSES on golden
    # -------------------------------------------------------
    try:
        if transition is not None:
            # Duration can be in p14:dur attribute or dur attribute
            dur_val = None
            # Check p14:dur first (OOXML 2010 extension)
            p14_dur_key = '{http://schemas.microsoft.com/office/powerpoint/2010/main}dur'
            dur_val = transition.get(p14_dur_key)
            if dur_val is None:
                # Fallback to plain 'dur' attribute
                dur_val = transition.get('dur')

            if dur_val is not None:
                dur_int = int(dur_val)
                if dur_int == 1800:
                    print(f"PASS: Component 2 - Duration is 1800ms (1.8s) (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 - Duration is {dur_int}ms, expected 1800ms")
            else:
                # Check spd attribute as rough indicator
                spd = transition.get('spd')
                print(f"FAIL: Component 2 - No explicit duration attribute found (spd={spd})")
        else:
            print(f"FAIL: Component 2 - No transition element to check duration")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # -------------------------------------------------------
    # Component 3: Transition type is 'checker' (Diagonal Squares) (0.4 pts)
    # This FAILS on initial (no transition) and PASSES on golden
    # -------------------------------------------------------
    try:
        if transition is not None:
            # Look for <p:checker> child element
            checker = transition.find('p:checker', NS)
            if checker is not None:
                dir_val = checker.get('dir', 'not_set')
                print(f"PASS: Component 3 - Checker (Diagonal Squares) transition found, dir={dir_val} (0.4 pts)")
                total_score += 0.4
            else:
                # List actual child elements for debugging
                children = [child.tag for child in transition]
                print(f"FAIL: Component 3 - No <p:checker> child. Found children: {children}")
        else:
            print(f"FAIL: Component 3 - No transition element to check type")
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

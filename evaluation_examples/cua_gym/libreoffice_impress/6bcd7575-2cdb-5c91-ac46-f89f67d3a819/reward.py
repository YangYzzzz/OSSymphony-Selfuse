"""
Reward Script: Apply a Wipe transition from top to bottom on slide 4
Task ID: impress_tm_004
Domain: libreoffice_impress
Scoring:
  Component 1 (0.4): Slide 4 has a wipe transition
  Component 2 (0.35): Wipe direction is 'd' (from top)
  Component 3 (0.25): No other slides have wipe transition
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tm_004'
P_NS = 'http://schemas.openxmlformats.org/presentationml/2006/main'


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice state before verification."""
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
    Verify that slide 4 has a Wipe transition with direction 'from top' (dir='d').
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file exists and is a valid ZIP/PPTX
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open file as ZIP: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: slide4.xml exists
    slide_xml_name = 'ppt/slides/slide4.xml'
    if slide_xml_name not in zf.namelist():
        print(f"CRITICAL: {slide_xml_name} not found in pptx archive")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    try:
        with zf.open(slide_xml_name) as f:
            root = ET.parse(f).getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot parse {slide_xml_name}: {e}")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    # Find all transition elements and locate wipe child across all of them
    transitions = root.findall(f'.//{{{P_NS}}}transition')
    print(f"INFO: Found {len(transitions)} transition element(s) on slide 4")

    # Scan all transition elements for a <p:wipe> child
    wipe_element = None
    for tr in transitions:
        wipes = tr.findall(f'{{{P_NS}}}wipe')
        if wipes:
            wipe_element = wipes[0]
            break

    # Component 1: Slide 4 has a wipe transition (0.4 points)
    # NOTE: Empty <p:transition> elements (no type child) do NOT count —
    # they are just speed/duration metadata, not an actual transition effect.
    try:
        if wipe_element is not None:
            print(f"PASS: Component 1 — Slide 4 has a wipe transition element (0.4 pts)")
            total_score += 0.4
        else:
            all_children = []
            for tr in transitions:
                all_children.extend(
                    [c.tag.split('}')[1] if '}' in c.tag else c.tag for c in tr]
                )
            print(f"FAIL: Component 1 — No wipe transition found. Transition children: {all_children}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Wipe direction is 'd' (from top, wipes downward) (0.35 points)
    try:
        if wipe_element is not None:
            direction = wipe_element.get('dir', None)
            if direction == 'd':
                print(f"PASS: Component 2 — Wipe direction is 'd' (from top) (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 — Expected wipe dir='d', found dir='{direction}'")
        else:
            print("FAIL: Component 2 — No wipe element to check direction")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Slide 4 has wipe AND no other slides have wipe (exclusivity) (0.25 points)
    # This compound check anchors to the task change — it only passes when
    # slide 4 specifically has the wipe transition applied.
    try:
        if wipe_element is not None:
            other_slides_with_wipe = []
            for slide_num in range(1, 8):
                if slide_num == 4:
                    continue
                sname = f'ppt/slides/slide{slide_num}.xml'
                if sname in zf.namelist():
                    with zf.open(sname) as sf:
                        sroot = ET.parse(sf).getroot()
                        for tr2 in sroot.findall(f'.//{{{P_NS}}}transition'):
                            if tr2.findall(f'{{{P_NS}}}wipe'):
                                other_slides_with_wipe.append(slide_num)
            if len(other_slides_with_wipe) == 0:
                print(f"PASS: Component 3 — Slide 4 has wipe and no other slides do (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — Other slides also have wipe transition: {other_slides_with_wipe}")
        else:
            print("FAIL: Component 3 — Slide 4 has no wipe, so exclusivity check fails")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

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

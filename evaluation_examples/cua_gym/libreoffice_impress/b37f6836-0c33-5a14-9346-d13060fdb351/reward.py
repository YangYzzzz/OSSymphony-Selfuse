"""
Reward Script: Add curved motion path animation to airplane icon on slide 2
Task ID: impress_ma_063
Domain: libreoffice_impress
Scoring:
  - Component 1: Animation timing element exists on slide 2 (0.2 pts)
  - Component 2: animMotion targets airplane icon shape (0.25 pts)
  - Component 3: Motion path is curved (cubic bezier) (0.25 pts)
  - Component 4: Duration ~3000ms (0.15 pts)
  - Component 5: onClick trigger (0.15 pts)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ma_063'

NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
}


def get_airplane_shape_id(pptx_path):
    """Find the shape ID of the airplane icon on slide 2 by name."""
    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            with zf.open('ppt/slides/slide2.xml') as f:
                root = ET.fromstring(f.read())
                for el in root.iter():
                    if el.tag.endswith('}cNvPr'):
                        name = el.get('name', '')
                        if 'airplane' in name.lower() or 'plane' in name.lower():
                            return el.get('id')
    except Exception as e:
        print(f"ERROR: Could not find airplane shape ID: {e}")
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
        with zipfile.ZipFile(file_path, 'r') as zf:
            zf.open('ppt/slides/slide2.xml')
    except Exception as e:
        print(f"CRITICAL: Cannot open pptx or slide2.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the airplane icon shape ID
    airplane_spid = get_airplane_shape_id(file_path)
    if airplane_spid:
        print(f"INFO: Airplane icon shape ID = {airplane_spid}")
    else:
        print("WARN: Could not identify airplane icon by name, will check any animMotion")

    # Parse slide 2 XML for timing/animation data
    timing_el = None
    anim_motion_el = None
    anim_motion_target_spid = None
    anim_motion_path = None
    anim_motion_duration = None
    onclick_trigger_found = 0  # 0=not found, 1=found

    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            with zf.open('ppt/slides/slide2.xml') as f:
                root = ET.fromstring(f.read())

                # Find timing element
                timing_el = root.find('.//p:timing', NS)

                if timing_el is not None:
                    # Find animMotion element
                    for am in timing_el.iter():
                        if am.tag.endswith('}animMotion'):
                            anim_motion_el = am
                            anim_motion_path = am.get('path', '')

                            # Get target shape ID from cBhvr/tgtEl/spTgt
                            for child in am.iter():
                                if child.tag.endswith('}spTgt'):
                                    anim_motion_target_spid = child.get('spid')

                            # Get duration from cBhvr/cTn
                            for child in am.iter():
                                if child.tag.endswith('}cTn'):
                                    dur = child.get('dur')
                                    if dur and dur.isdigit():
                                        anim_motion_duration = int(dur)
                                    break

                    # Check for onClick trigger in nextCondLst
                    for cond in timing_el.iter():
                        if cond.tag.endswith('}cond'):
                            if cond.get('evt', '') == 'onClick':
                                onclick_trigger_found = 1

    except Exception as e:
        print(f"ERROR: Failed to parse slide2 XML: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Animation timing element exists on slide 2 (0.2 points)
    try:
        if timing_el is not None:
            # Check it actually contains animation nodes, not just empty timing
            anim_node_count = sum(
                1 for child in timing_el.iter()
                if (child.tag.split('}')[-1] if '}' in child.tag else child.tag)
                in ('animMotion', 'anim', 'animEffect', 'animScale', 'animRot', 'set')
            )
            if anim_node_count > 0:
                print(f"PASS: Component 1 -- Animation timing with animation nodes found on slide 2 (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 -- Timing element found but no animation nodes inside")
        else:
            print(f"FAIL: Component 1 -- No timing element on slide 2")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: animMotion element targets the airplane icon (0.25 points)
    try:
        if anim_motion_el is not None:
            # Check target is the airplane icon
            if airplane_spid and anim_motion_target_spid == airplane_spid:
                print(f"PASS: Component 2 -- animMotion targets shape spid={anim_motion_target_spid} (airplane icon) (0.25 pts)")
                total_score += 0.25
            elif anim_motion_target_spid is not None and airplane_spid is None:
                # Fallback: if we couldn't find airplane by name, accept any target
                print(f"  INFO: Cannot verify exact target, accepting spid={anim_motion_target_spid}")
                print(f"PASS: Component 2 -- animMotion targets shape spid={anim_motion_target_spid} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 -- animMotion targets spid={anim_motion_target_spid}, expected airplane spid={airplane_spid}")
        else:
            print(f"FAIL: Component 2 -- No animMotion element found on slide 2")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Motion path is curved (contains cubic bezier C commands) (0.25 points)
    try:
        if anim_motion_path:
            # A curved/arc path uses C (cubic bezier) commands
            # A straight path would only use L (lineTo) or just M and endpoint
            path_upper = anim_motion_path.upper()
            has_curve = 'C' in path_upper
            if has_curve:
                print(f"PASS: Component 3 -- Motion path contains cubic bezier curves (0.25 pts)")
                print(f"  Path: {anim_motion_path[:120]}")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 -- Motion path has no curves (no C commands)")
                print(f"  Path: {anim_motion_path[:120]}")
        else:
            print(f"FAIL: Component 3 -- No motion path found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Duration is approximately 3000ms (0.15 points)
    try:
        if anim_motion_duration is not None:
            # Allow 20% tolerance: 2400-3600ms
            if 2400 <= anim_motion_duration <= 3600:
                print(f"PASS: Component 4 -- Duration is {anim_motion_duration}ms (within range of 3000ms) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 -- Duration is {anim_motion_duration}ms, expected ~3000ms")
        else:
            print(f"FAIL: Component 4 -- Could not determine animation duration")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Trigger is onClick (0.15 points)
    try:
        if onclick_trigger_found == 1:
            print(f"PASS: Component 5 -- onClick trigger found (0.15 pts)")
            total_score += 0.15
        else:
            # Also check if animation is in mainSeq (which defaults to onClick in PowerPoint)
            main_seq_count = sum(
                1 for child in timing_el.iter()
                if child.tag.endswith('}cTn') and child.get('nodeType') == 'mainSeq'
            ) if timing_el is not None else 0
            if main_seq_count > 0:
                print(f"PASS: Component 5 -- Animation is in mainSeq (implicit onClick trigger) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 -- No onClick trigger found")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook for LibreOffice Impress
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_impress")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
persist_app_state()

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

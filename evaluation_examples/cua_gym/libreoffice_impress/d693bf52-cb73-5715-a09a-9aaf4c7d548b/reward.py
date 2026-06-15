"""
Reward Script: Motion path animation on arrow shape (slide 3)
Task ID: impress_ma_062
Domain: libreoffice_impress
Scoring:
  Component 1 (0.30): Timing/animation element exists on slide 3
  Component 2 (0.25): animMotion targets the arrow shape (Right Arrow 8)
  Component 3 (0.20): Motion path is a straight horizontal line to the right
  Component 4 (0.15): Duration is approximately 2000ms (2 seconds)
  Component 5 (0.10): Trigger is onClick
"""

import os
import re
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ma_062'

# XML namespaces used in PPTX
NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def persist_app_state(domain):
    """Best-effort save of any open LibreOffice document."""
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


def get_arrow_shape_id(pptx_path, slide_idx=2):
    """Find the shape ID of the arrow shape on the given slide (0-based index).
    Returns the spid as a string, or None if not found."""
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        slide_name = f'ppt/slides/slide{slide_idx + 1}.xml'
        try:
            with zf.open(slide_name) as f:
                root = ET.parse(f).getroot()
        except KeyError:
            return None

    # Search for shape named "Right Arrow 8" or any arrow-like shape
    for elem in root.iter():
        if elem.tag.endswith('cNvPr'):
            name = elem.get('name', '')
            if 'arrow' in name.lower():
                return elem.get('id')
    return None


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

    # First, find the arrow shape ID
    arrow_spid = get_arrow_shape_id(file_path, slide_idx=2)
    print(f"INFO: Arrow shape ID on slide 3: {arrow_spid}")

    # Parse slide 3 XML for animation data
    timing_elem = None
    slide_xml_content = None
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            with zf.open('ppt/slides/slide3.xml') as f:
                slide_xml_content = f.read().decode('utf-8')
            root = ET.fromstring(slide_xml_content)
            timing_elem = root.find('.//p:timing', NS)
    except Exception as e:
        print(f"CRITICAL: Cannot parse slide 3 XML: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Timing/animation element exists on slide 3 (0.30 points)
    try:
        if timing_elem is not None:
            # Check that there's actual animation content, not just an empty timing element
            anim_elements = list(timing_elem.iter())
            has_content = len(anim_elements) > 3  # more than just wrapper elements
            if has_content:
                print(f"PASS: Component 1 — Timing element with animation content found on slide 3 (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 1 — Timing element exists but has no meaningful animation content")
        else:
            print(f"FAIL: Component 1 — No timing element found on slide 3")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: animMotion targets the arrow shape (0.25 points)
    anim_motion = None
    try:
        if timing_elem is not None:
            # Find animMotion elements
            for elem in timing_elem.iter():
                if elem.tag.endswith('animMotion'):
                    anim_motion = elem
                    break

            if anim_motion is not None:
                # Check target shape
                tgt_el = None
                for parent in timing_elem.iter():
                    if parent.tag.endswith('animMotion'):
                        # Find the cBhvr/tgtEl/spTgt within the animMotion's parent structure
                        cbhvr = parent.find('{http://schemas.openxmlformats.org/presentationml/2006/main}cBhvr')
                        if cbhvr is None:
                            # Try with wildcard namespace
                            for child in parent:
                                if child.tag.endswith('cBhvr'):
                                    cbhvr = child
                                    break
                        if cbhvr is not None:
                            for child in cbhvr:
                                if child.tag.endswith('tgtEl'):
                                    tgt_el = child
                                    break

                target_spid = None
                if tgt_el is not None:
                    for child in tgt_el:
                        if child.tag.endswith('spTgt'):
                            target_spid = child.get('spid')
                            break

                if target_spid is not None and arrow_spid is not None and target_spid == arrow_spid:
                    print(f"PASS: Component 2 — animMotion targets arrow shape (spid={target_spid}) (0.25 pts)")
                    total_score += 0.25
                elif target_spid is not None:
                    # Check if the target is an arrow by name even if our detection missed it
                    print(f"FAIL: Component 2 — animMotion targets spid={target_spid}, expected arrow spid={arrow_spid}")
                else:
                    print(f"FAIL: Component 2 — animMotion found but no target shape identified")
            else:
                print(f"FAIL: Component 2 — No animMotion element found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Motion path is a straight horizontal line to the right (0.20 points)
    try:
        if anim_motion is not None:
            path_str = anim_motion.get('path', '')
            print(f"INFO: Motion path = '{path_str}'")

            if path_str:
                # A straight horizontal line path should be like "M 0 0 L X 0 E"
                # where X > 0 (moving right). The path uses relative coordinates.
                # Parse path: look for M start and L end with horizontal movement
                # Acceptable patterns: "M 0 0 L <positive_x> 0 E" or similar
                path_parts = path_str.strip().split()

                has_m = 'M' in path_parts
                has_l = 'L' in path_parts
                has_e = path_parts[-1] == 'E' if path_parts else False

                # Check for straight line (M x1 y1 L x2 y2 E)
                is_straight_line = has_m and has_l and has_e

                # Check horizontal: end y should be 0 (or close to 0) and end x > 0
                is_horizontal_right = False
                if is_straight_line:
                    try:
                        l_idx = path_parts.index('L')
                        end_x = float(path_parts[l_idx + 1])
                        end_y = float(path_parts[l_idx + 2])
                        is_horizontal_right = end_x > 0 and abs(end_y) < 0.05
                    except (ValueError, IndexError):
                        pass

                if is_straight_line and is_horizontal_right:
                    print(f"PASS: Component 3 — Straight horizontal line to the right (end_x={end_x}, end_y={end_y}) (0.20 pts)")
                    total_score += 0.20
                elif is_straight_line:
                    print(f"FAIL: Component 3 — Path is a straight line but not horizontal-right")
                else:
                    print(f"FAIL: Component 3 — Path is not a simple straight line: {path_str}")
            else:
                print(f"FAIL: Component 3 — No path attribute on animMotion")
        else:
            print(f"FAIL: Component 3 — No animMotion element found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Duration is approximately 2000ms (0.15 points)
    try:
        if anim_motion is not None:
            # Find the cTn element within animMotion's cBhvr
            duration = None
            for child in anim_motion:
                if child.tag.endswith('cBhvr'):
                    for subchild in child:
                        if subchild.tag.endswith('cTn'):
                            duration = subchild.get('dur')
                            break
                    break

            if duration is not None:
                dur_ms = int(duration)
                # Allow some tolerance: 1500-2500ms (task says 2.0 seconds)
                if 1500 <= dur_ms <= 2500:
                    print(f"PASS: Component 4 — Duration is {dur_ms}ms (within acceptable range of 2000ms) (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 4 — Duration is {dur_ms}ms, expected ~2000ms")
            else:
                print(f"FAIL: Component 4 — Could not find duration attribute")
        else:
            print(f"FAIL: Component 4 — No animMotion element found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Trigger is onClick (0.10 points)
    try:
        if timing_elem is not None:
            # Check for onClick trigger in the sequence
            # The onClick trigger is in nextCondLst/cond with evt="onClick"
            onclick_events = [
                elem for elem in timing_elem.iter()
                if elem.tag.endswith('cond') and elem.get('evt', '') == 'onClick'
            ]

            if len(onclick_events) > 0:
                print(f"PASS: Component 5 — onClick trigger found (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — No onClick trigger found in animation timing")
        else:
            print(f"FAIL: Component 5 — No timing element found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(round(total_score, 2), 1.0)
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

"""
Reward Script: Add a motion path animation to the pointer arrow on slide 7
Task ID: impress_ma_087
Domain: libreoffice_impress
Scoring:
  Component 1: Animation exists on slide 7 (0.2 pts)
  Component 2: Animation targets the arrow shape (0.2 pts)
  Component 3: Motion path is diagonal top-left to bottom-right (0.2 pts)
  Component 4: Duration is ~2.0 seconds (0.2 pts)
  Component 5: Trigger is On Click (0.2 pts)
"""

import os
import re
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ma_087'

# Namespaces used in OOXML
NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_A = 'http://schemas.openxmlformats.org/drawingml/2006/main'


def find_arrow_shape_id(pptx_path, slide_num=7):
    """Find the shape ID of the PointerArrow shape on the given slide."""
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        with zf.open(f'ppt/slides/slide{slide_num}.xml') as f:
            root = ET.fromstring(f.read())
    # Look for cNvPr elements to find the arrow shape
    for el in root.iter():
        tag = el.tag.split('}')[-1] if '}' in el.tag else el.tag
        if tag == 'cNvPr':
            shape_name = el.get('name', '')
            # Match arrow-related shape names (case-insensitive)
            if 'arrow' in shape_name.lower() or 'pointer' in shape_name.lower():
                return el.get('id'), shape_name
    return None, None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file exists and is a valid pptx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            zf.namelist()  # verify it's a valid zip/pptx
    except Exception as e:
        print(f"CRITICAL: Cannot open as PPTX: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the arrow shape ID
    arrow_id, arrow_name = find_arrow_shape_id(file_path, slide_num=7)
    if arrow_id is None:
        print("WARNING: Could not find arrow shape on slide 7 by name. Will check animation targets generically.")

    # Parse slide 7 XML for animation data
    timing_el = None
    slide_xml_content = None
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            with zf.open('ppt/slides/slide7.xml') as f:
                slide_xml_content = f.read()
                root = ET.fromstring(slide_xml_content)
                timing_el = root.find(f'.//{{{NS_P}}}timing')
    except Exception as e:
        print(f"ERROR: Cannot parse slide7.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Animation exists on slide 7 (0.2 pts)
    # The task adds animations to a slide that had none.
    try:
        anim_motion = None
        if timing_el is not None:
            # Look for any animMotion element (motion path animation)
            anim_motion = timing_el.find(f'.//{{{NS_P}}}animMotion')
        if anim_motion is not None:
            print(f"PASS: Component 1 -- Motion path animation found on slide 7 (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- No motion path animation found on slide 7")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Animation targets the arrow shape (0.2 pts)
    try:
        target_spid = None
        if anim_motion is not None:
            # Get the target shape ID from cBhvr/tgtEl/spTgt
            sp_tgt = anim_motion.find(f'.//{{{NS_P}}}spTgt')
            if sp_tgt is not None:
                target_spid = sp_tgt.get('spid')

        if target_spid is not None:
            if arrow_id is not None and target_spid == arrow_id:
                print(f"PASS: Component 2 -- Animation targets PointerArrow (spid={target_spid}, name={arrow_name}) (0.2 pts)")
                total_score += 0.2
            elif arrow_id is None:
                # Could not determine arrow ID by name, but animation has a target
                # Check if the target is an auto_shape (not a text box or placeholder)
                # Accept if it targets any shape on this slide
                print(f"PASS: Component 2 -- Animation targets shape spid={target_spid} (arrow name detection failed, accepting) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 -- Animation targets spid={target_spid}, expected arrow spid={arrow_id} ({arrow_name})")
        else:
            print(f"FAIL: Component 2 -- No animation target shape found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Motion path is diagonal top-left to bottom-right (0.2 pts)
    try:
        if anim_motion is not None:
            path_str = anim_motion.get('path', '')
            # Expected: path like "M 0 0 L <positive_x> <positive_y> E"
            # The motion should move right (positive x) and down (positive y)
            # Parse the path to extract endpoint coordinates
            # Pattern: M <x1> <y1> L <x2> <y2> E  (or more complex paths)
            coords = re.findall(r'L\s+([-\d.]+)\s+([-\d.]+)', path_str)
            if coords:
                # Check the last L command (endpoint of path)
                end_x = float(coords[-1][0])
                end_y = float(coords[-1][1])
                if end_x > 0.1 and end_y > 0.1:
                    print(f"PASS: Component 3 -- Diagonal path detected: endpoint ({end_x}, {end_y}) (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 3 -- Path endpoint ({end_x}, {end_y}) is not clearly diagonal top-left to bottom-right")
            else:
                print(f"FAIL: Component 3 -- Could not parse motion path: {path_str!r}")
        else:
            print(f"FAIL: Component 3 -- No animMotion element to check path")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Duration is approximately 2.0 seconds (0.2 pts)
    try:
        if anim_motion is not None:
            # Duration is on the cTn element inside cBhvr
            cBhvr = anim_motion.find(f'{{{NS_P}}}cBhvr')
            dur_val = None
            if cBhvr is not None:
                cTn = cBhvr.find(f'{{{NS_P}}}cTn')
                if cTn is not None:
                    dur_val = cTn.get('dur')

            if dur_val is not None:
                try:
                    dur_ms = int(dur_val)
                    # Accept 1500-2500ms as approximately 2 seconds
                    if 1500 <= dur_ms <= 2500:
                        print(f"PASS: Component 4 -- Duration is {dur_ms}ms (~{dur_ms/1000:.1f}s) (0.2 pts)")
                        total_score += 0.2
                    else:
                        print(f"FAIL: Component 4 -- Duration is {dur_ms}ms, expected ~2000ms")
                except ValueError:
                    print(f"FAIL: Component 4 -- Duration value not numeric: {dur_val}")
            else:
                print(f"FAIL: Component 4 -- Could not find duration attribute on animation")
        else:
            print(f"FAIL: Component 4 -- No animMotion element to check duration")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Trigger is On Click (0.2 pts)
    try:
        if timing_el is not None:
            # On Click trigger: the animation cTn should have nodeType="clickEffect"
            # Search for the cTn that wraps the animMotion with presetClass="path"
            found_click = False
            for cTn in timing_el.iter(f'{{{NS_P}}}cTn'):
                preset_class = cTn.get('presetClass', '')
                node_type = cTn.get('nodeType', '')
                if preset_class == 'path' and node_type == 'clickEffect':
                    found_click = True
                    break
                # Also check: if nodeType is clickEffect and it contains the animMotion
                if node_type == 'clickEffect':
                    sub_anim = cTn.find(f'.//{{{NS_P}}}animMotion')
                    if sub_anim is not None:
                        found_click = True
                        break

            if found_click:
                print(f"PASS: Component 5 -- Trigger is On Click (clickEffect) (0.2 pts)")
                total_score += 0.2
            else:
                # Also accept mainSeq trigger (which is effectively "on click" in PowerPoint)
                main_seq = timing_el.find(f'.//{{{NS_P}}}seq')
                if main_seq is not None:
                    seq_cTn = main_seq.find(f'{{{NS_P}}}cTn')
                    if seq_cTn is not None and seq_cTn.get('nodeType') == 'mainSeq':
                        # Animations in mainSeq are triggered by click by default
                        print(f"PASS: Component 5 -- Animation in mainSeq (On Click by default) (0.2 pts)")
                        total_score += 0.2
                    else:
                        print(f"FAIL: Component 5 -- Animation not triggered on click")
                else:
                    print(f"FAIL: Component 5 -- No sequence found for trigger detection")
        else:
            print(f"FAIL: Component 5 -- No timing element found")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

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
    verify_task(file_path)

"""
Reward Script: Custom zigzag motion path animation for Ball shape on slide 1
Task ID: impress_ma_064
Domain: libreoffice_impress
Scoring:
  C1 (0.25): Animation exists targeting Ball shape on slide 1
  C2 (0.25): Animation is a motion path (animMotion element)
  C3 (0.25): Path follows a zigzag pattern (alternating Y direction, net rightward X)
  C4 (0.15): Duration is ~4.0 seconds (4000ms)
  C5 (0.10): Trigger is onClick (mainSeq with onClick nextCond)
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import re

WORKDIR = '/home/user'
TASK_ID = 'impress_ma_064'

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
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open pptx as zip: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: slide1.xml must exist
    try:
        slide1_xml = zf.open('ppt/slides/slide1.xml')
        root = ET.parse(slide1_xml).getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot parse slide1.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns_p = 'http://schemas.openxmlformats.org/presentationml/2006/main'

    # Find the Ball shape's spid by looking up cNvPr elements
    content_str = ET.tostring(root, encoding='unicode')
    ball_id = None
    id_name_matches = re.findall(r'cNvPr id="(\d+)" name="([^"]+)"', content_str)
    for sid, name in id_name_matches:
        if name.lower() == 'ball':
            ball_id = sid
            break

    if ball_id is None:
        print("CRITICAL: Ball shape not found on slide 1")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Ball shape found with ID={ball_id}")

    # Find the timing element
    timing = root.find(f'.//{{{ns_p}}}timing')

    # Component 1: Animation exists targeting Ball shape on slide 1 (0.25 points)
    try:
        if timing is None:
            print("FAIL: Component 1 -- No timing/animation element on slide 1")
        else:
            # Check if any animation targets the Ball shape
            timing_str = ET.tostring(timing, encoding='unicode')
            spTgt_pattern = f'spid="{ball_id}"'
            if spTgt_pattern in timing_str:
                print(f"PASS: Component 1 -- Animation targeting Ball (spid={ball_id}) found (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 -- No animation targets Ball shape (spid={ball_id})")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Animation is a motion path (animMotion element) (0.25 points)
    anim_motion = None
    try:
        if timing is not None:
            # Find all animMotion elements and check if one targets Ball
            for am in timing.iter(f'{{{ns_p}}}animMotion'):
                # Check if this animMotion targets Ball
                am_str = ET.tostring(am, encoding='unicode')
                if f'spid="{ball_id}"' in am_str:
                    anim_motion = am
                    break

            if anim_motion is not None:
                path_attr = anim_motion.get('path', '')
                if path_attr:
                    print(f"PASS: Component 2 -- animMotion with path found for Ball (0.25 pts)")
                    print(f"  Path: {path_attr}")
                    total_score += 0.25
                else:
                    print("FAIL: Component 2 -- animMotion found but no path attribute")
            else:
                print("FAIL: Component 2 -- No animMotion element targeting Ball")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Zigzag pattern - path alternates Y direction while moving right (0.25 points)
    try:
        if anim_motion is not None:
            path_attr = anim_motion.get('path', '')
            if path_attr:
                # Parse the path string to extract coordinates
                # Expected format like: "M 0 0 L 0.14 -0.12 L 0.28 0.12 L 0.42 -0.12 L 0.56 0.12 L 0.70 0 E"
                # Extract coordinate pairs from L commands
                coords = re.findall(r'L\s+([-\d.]+)\s+([-\d.]+)', path_attr)

                if len(coords) < 3:
                    print(f"FAIL: Component 3 -- Path has fewer than 3 segments ({len(coords)} L-points), not enough for zigzag")
                else:
                    # Check zigzag properties:
                    # 1. X values should generally increase (left to right)
                    # 2. Y values should alternate direction (up/down)
                    x_vals = [float(c[0]) for c in coords]
                    y_vals = [float(c[1]) for c in coords]

                    # Check X is generally increasing
                    x_increasing = all(x_vals[i] > x_vals[i-1] for i in range(1, len(x_vals)))
                    # Or at minimum, last X > first X (net rightward)
                    x_net_right = x_vals[-1] > x_vals[0] if len(x_vals) > 1 else False

                    # Check Y alternates sign (zigzag up/down)
                    # Y direction changes between consecutive segments
                    y_directions = []
                    prev_y = 0.0  # starting Y from M 0 0
                    for y in y_vals:
                        y_directions.append(y - prev_y)
                        prev_y = y

                    # Count direction changes in Y
                    direction_changes = 0
                    for i in range(1, len(y_directions)):
                        if y_directions[i] * y_directions[i-1] < 0:  # sign change
                            direction_changes += 1

                    zigzag_ok = direction_changes >= 2 and x_net_right

                    if zigzag_ok:
                        print(f"PASS: Component 3 -- Zigzag pattern verified: {direction_changes} Y-direction changes, X net rightward (0.25 pts)")
                        print(f"  X values: {x_vals}")
                        print(f"  Y values: {y_vals}")
                        total_score += 0.25
                    else:
                        print(f"FAIL: Component 3 -- Not a zigzag: direction_changes={direction_changes}, x_net_right={x_net_right}")
                        print(f"  X values: {x_vals}")
                        print(f"  Y values: {y_vals}")
            else:
                print("FAIL: Component 3 -- No path to analyze")
        else:
            print("FAIL: Component 3 -- No animMotion element")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Duration is ~4.0 seconds (4000ms) (0.15 points)
    try:
        if anim_motion is not None:
            # Duration is on the cBhvr > cTn element
            cBhvr = anim_motion.find(f'{{{ns_p}}}cBhvr')
            if cBhvr is not None:
                cTn = cBhvr.find(f'{{{ns_p}}}cTn')
                if cTn is not None:
                    dur = cTn.get('dur', '')
                    if dur:
                        dur_val = int(dur)
                        # Allow some tolerance: 3500-4500ms
                        if 3500 <= dur_val <= 4500:
                            print(f"PASS: Component 4 -- Duration is {dur_val}ms (~4.0s) (0.15 pts)")
                            total_score += 0.15
                        else:
                            print(f"FAIL: Component 4 -- Duration is {dur_val}ms, expected ~4000ms")
                    else:
                        print("FAIL: Component 4 -- No dur attribute on cTn")
                else:
                    print("FAIL: Component 4 -- No cTn element in cBhvr")
            else:
                print("FAIL: Component 4 -- No cBhvr element in animMotion")
        else:
            print("FAIL: Component 4 -- No animMotion element")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Trigger is onClick (0.10 points)
    try:
        if timing is not None:
            timing_str = ET.tostring(timing, encoding='unicode')
            # onClick trigger is indicated by nextCondLst with evt="onClick"
            if 'evt="onClick"' in timing_str:
                print(f"PASS: Component 5 -- onClick trigger found (0.10 pts)")
                total_score += 0.10
            else:
                print("FAIL: Component 5 -- No onClick trigger found in timing")
        else:
            print("FAIL: Component 5 -- No timing element")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    zf.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Motion path animation on car icon (slide 4)
Task ID: impress_ma_077
Domain: libreoffice_impress
Scoring:
  - Component 1 (0.25): animMotion element exists targeting car icon (spid=6)
  - Component 2 (0.25): Motion path is horizontal (left-to-right)
  - Component 3 (0.25): Duration is 3000ms (3 seconds)
  - Component 4 (0.25): Auto-reverse is enabled
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import re

WORKDIR = '/home/user'
TASK_ID = 'impress_ma_077'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            import time
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

    # Precondition: file must exist and be a valid pptx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open pptx {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: slide4.xml must exist
    try:
        with zf.open('ppt/slides/slide4.xml') as f:
            slide4_xml = f.read().decode()
    except Exception as e:
        print(f"CRITICAL: Cannot read slide4.xml: {e}")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    zf.close()

    # Parse slide 4 XML
    ns = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    }

    try:
        root = ET.fromstring(slide4_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot parse slide4.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find all animMotion elements (search full XML namespace-agnostic)
    # Use namespace-agnostic search since namespace prefixes may vary
    anim_motions = root.findall('.//{http://schemas.openxmlformats.org/presentationml/2006/main}animMotion')

    # Component 1: animMotion element exists targeting the car icon shape (0.25 points)
    target_anim = None
    try:
        for am in anim_motions:
            # Find the target shape id within this animMotion's cBhvr/tgtEl/spTgt
            sp_tgt = am.find(
                './/{http://schemas.openxmlformats.org/presentationml/2006/main}spTgt'
            )
            if sp_tgt is not None:
                spid = sp_tgt.get('spid')
                if spid == '6':
                    target_anim = am
                    break

        if target_anim is not None:
            print(f"PASS: Component 1 — animMotion found targeting Car Icon (spid=6) (0.25 pts)")
            total_score += 0.25
        else:
            # Also check if any animMotion targets ANY shape on the slide
            # (task might have used a different shape arrangement)
            if len(anim_motions) > 0:
                # There's an animMotion but not targeting spid=6
                # Check if the shape named "Car Icon" exists with a different id
                car_shapes = root.findall(
                    './/{http://schemas.openxmlformats.org/presentationml/2006/main}cNvPr'
                )
                car_id = None
                for cs in car_shapes:
                    if cs.get('name') and 'car' in cs.get('name', '').lower():
                        car_id = cs.get('id')
                        break

                if car_id:
                    for am in anim_motions:
                        sp_tgt = am.find(
                            './/{http://schemas.openxmlformats.org/presentationml/2006/main}spTgt'
                        )
                        if sp_tgt is not None and sp_tgt.get('spid') == car_id:
                            target_anim = am
                            print(f"PASS: Component 1 — animMotion found targeting car shape (id={car_id}) (0.25 pts)")
                            total_score += 0.25
                            break

                if target_anim is None:
                    print(f"FAIL: Component 1 — animMotion exists but does not target car icon shape")
            else:
                print(f"FAIL: Component 1 — No animMotion element found on slide 4")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If no target animation found, remaining checks cannot pass
    if target_anim is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Motion path is horizontal left-to-right (0.25 points)
    try:
        path_str = target_anim.get('path', '')
        # A horizontal L-to-R path: "M 0 0 L <positive_x> 0 E"
        # The key requirement: Y coordinates stay at 0 (horizontal), X moves positive (left to right)
        # Parse path: expect M x1 y1 L x2 y2 E pattern
        # Normalize whitespace
        path_clean = ' '.join(path_str.split())
        # Match: M <x1> <y1> L <x2> <y2> E
        match = re.match(r'M\s+([\d.e+-]+)\s+([\d.e+-]+)\s+L\s+([\d.e+-]+)\s+([\d.e+-]+)\s+E', path_clean)
        if match:
            x1, y1, x2, y2 = float(match.group(1)), float(match.group(2)), float(match.group(3)), float(match.group(4))
            # Horizontal: y1 == y2 (or very close)
            # Left to right: x2 > x1
            is_horizontal = abs(y2 - y1) < 0.01
            is_left_to_right = x2 > x1
            if is_horizontal and is_left_to_right:
                print(f"PASS: Component 2 — Horizontal L-to-R path: ({x1},{y1}) -> ({x2},{y2}) (0.25 pts)")
                total_score += 0.25
            elif is_horizontal:
                print(f"FAIL: Component 2 — Path is horizontal but NOT left-to-right: ({x1},{y1}) -> ({x2},{y2})")
            elif is_left_to_right:
                print(f"FAIL: Component 2 — Path moves right but NOT horizontal: ({x1},{y1}) -> ({x2},{y2})")
            else:
                print(f"FAIL: Component 2 — Path is neither horizontal nor L-to-R: ({x1},{y1}) -> ({x2},{y2})")
        else:
            # Path might be more complex but still horizontal
            # Check if all Y coordinates in the path are approximately equal
            coords = re.findall(r'[ML]\s+([\d.e+-]+)\s+([\d.e+-]+)', path_clean)
            if coords:
                y_vals = [float(c[1]) for c in coords]
                x_vals = [float(c[0]) for c in coords]
                all_horizontal = all(abs(y - y_vals[0]) < 0.01 for y in y_vals)
                moves_right = x_vals[-1] > x_vals[0]
                if all_horizontal and moves_right:
                    print(f"PASS: Component 2 — Complex horizontal L-to-R path detected (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 2 — Path not horizontal L-to-R. Path: {path_str}")
            else:
                print(f"FAIL: Component 2 — Cannot parse motion path: {path_str}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Duration is 3000ms (3 seconds) (0.25 points)
    try:
        # The cTn element inside cBhvr holds the duration
        cBhvr = target_anim.find(
            '{http://schemas.openxmlformats.org/presentationml/2006/main}cBhvr'
        )
        if cBhvr is not None:
            cTn = cBhvr.find(
                '{http://schemas.openxmlformats.org/presentationml/2006/main}cTn'
            )
            if cTn is not None:
                dur = cTn.get('dur')
                if dur is not None:
                    dur_val = int(dur)
                    if dur_val == 3000:
                        print(f"PASS: Component 3 — Duration is 3000ms (3 seconds) (0.25 pts)")
                        total_score += 0.25
                    else:
                        print(f"FAIL: Component 3 — Duration is {dur_val}ms, expected 3000ms")
                else:
                    print(f"FAIL: Component 3 — No duration attribute on cTn")
            else:
                print(f"FAIL: Component 3 — No cTn element in cBhvr")
        else:
            print(f"FAIL: Component 3 — No cBhvr element in animMotion")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Auto-reverse is enabled (0.25 points)
    try:
        cBhvr = target_anim.find(
            '{http://schemas.openxmlformats.org/presentationml/2006/main}cBhvr'
        )
        if cBhvr is not None:
            cTn = cBhvr.find(
                '{http://schemas.openxmlformats.org/presentationml/2006/main}cTn'
            )
            if cTn is not None:
                auto_rev = cTn.get('autoRev')
                if auto_rev == '1' or auto_rev == 'true':
                    print(f"PASS: Component 4 — Auto-reverse is enabled (autoRev={auto_rev}) (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 4 — autoRev={auto_rev}, expected '1'")
            else:
                print(f"FAIL: Component 4 — No cTn element in cBhvr")
        else:
            print(f"FAIL: Component 4 — No cBhvr element in animMotion")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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

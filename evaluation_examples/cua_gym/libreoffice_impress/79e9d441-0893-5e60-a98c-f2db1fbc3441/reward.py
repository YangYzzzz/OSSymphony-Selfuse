"""
Reward Script: Apply horizontal linear gradient background to slides 1-5
Task ID: impress_el_086
Domain: libreoffice_impress
Scoring:
  Component 1 (0.40): Slides 1-5 have gradient fill type
  Component 2 (0.30): Gradient stop colors are #0D47A1 and #1565C0
  Component 3 (0.15): Gradient direction is horizontal (angle=0)
  Component 4 (0.15): Slides 6-10 remain without gradient (white/solid)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_el_086'

NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
}


def parse_slide_background(zf, slide_num):
    """Parse background info from a slide XML. Returns dict with fill details."""
    info = {'fill_type': None, 'gradient_stops': [], 'gradient_angle': None}
    fname = f'ppt/slides/slide{slide_num}.xml'
    try:
        with zf.open(fname) as f:
            root = ET.parse(f).getroot()
    except KeyError:
        return info

    bg = root.find('.//p:bg', NS)
    if bg is None:
        return info

    bgPr = bg.find('p:bgPr', NS)
    if bgPr is None:
        return info

    # Check for gradient fill
    grad_fill = bgPr.find('a:gradFill', NS)
    if grad_fill is not None:
        info['fill_type'] = 'gradient'
        gs_lst = grad_fill.find('a:gsLst', NS)
        if gs_lst is not None:
            for gs in gs_lst.findall('a:gs', NS):
                pos = gs.get('pos')
                clr_elem = gs.find('a:srgbClr', NS)
                color_val = clr_elem.get('val') if clr_elem is not None else None
                info['gradient_stops'].append({'pos': pos, 'color': color_val})
        lin = grad_fill.find('a:lin', NS)
        if lin is not None:
            info['gradient_angle'] = lin.get('ang')
        return info

    # Check for solid fill
    solid_fill = bgPr.find('a:solidFill', NS)
    if solid_fill is not None:
        info['fill_type'] = 'solid'
        clr_elem = solid_fill.find('a:srgbClr', NS)
        if clr_elem is not None:
            info['solid_color'] = clr_elem.get('val')
        return info

    return info


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

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse all slide backgrounds
    slides_info = {}
    for i in range(1, 11):
        slides_info[i] = parse_slide_background(zf, i)

    # Component 1: Slides 1-5 have gradient fill type (0.40 points)
    # Each slide contributes 0.08 points
    try:
        gradient_count = 0
        for slide_num in range(1, 6):
            info = slides_info[slide_num]
            if info['fill_type'] == 'gradient':
                gradient_count += 1
                print(f"  Slide {slide_num}: gradient fill detected")
            else:
                print(f"  Slide {slide_num}: expected gradient, found {info['fill_type']}")
        comp1_score = (gradient_count / 5) * 0.40
        if gradient_count == 5:
            print(f"PASS: Component 1 -- All 5 slides have gradient fill ({comp1_score:.2f} pts)")
        else:
            print(f"PARTIAL: Component 1 -- {gradient_count}/5 slides have gradient fill ({comp1_score:.2f} pts)")
        total_score += comp1_score
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Gradient stop colors are correct (0.30 points)
    # Expected: stop at pos 0 -> #0D47A1, stop at pos 100000 -> #1565C0
    try:
        correct_colors_count = 0
        for slide_num in range(1, 6):
            info = slides_info[slide_num]
            if info['fill_type'] != 'gradient' or len(info['gradient_stops']) < 2:
                print(f"  Slide {slide_num}: no gradient stops to check colors")
                continue
            stops = info['gradient_stops']
            # Find the two stops
            start_color = None
            end_color = None
            for stop in stops:
                if stop['pos'] == '0':
                    start_color = stop['color']
                elif stop['pos'] == '100000':
                    end_color = stop['color']
            if (start_color and start_color.upper() == '0D47A1' and
                    end_color and end_color.upper() == '1565C0'):
                correct_colors_count += 1
                print(f"  Slide {slide_num}: colors correct (0D47A1 -> 1565C0)")
            else:
                print(f"  Slide {slide_num}: expected 0D47A1->1565C0, found {start_color}->{end_color}")
        comp2_score = (correct_colors_count / 5) * 0.30
        if correct_colors_count == 5:
            print(f"PASS: Component 2 -- All 5 slides have correct gradient colors ({comp2_score:.2f} pts)")
        else:
            print(f"PARTIAL: Component 2 -- {correct_colors_count}/5 slides have correct colors ({comp2_score:.2f} pts)")
        total_score += comp2_score
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Gradient direction is horizontal, angle=0 (0.15 points)
    try:
        correct_angle_count = 0
        for slide_num in range(1, 6):
            info = slides_info[slide_num]
            if info['fill_type'] != 'gradient':
                print(f"  Slide {slide_num}: no gradient to check angle")
                continue
            angle = info['gradient_angle']
            if angle == '0':
                correct_angle_count += 1
                print(f"  Slide {slide_num}: horizontal gradient (angle=0)")
            else:
                print(f"  Slide {slide_num}: expected angle 0, found {angle}")
        comp3_score = (correct_angle_count / 5) * 0.15
        if correct_angle_count == 5:
            print(f"PASS: Component 3 -- All 5 slides have horizontal gradient ({comp3_score:.2f} pts)")
        else:
            print(f"PARTIAL: Component 3 -- {correct_angle_count}/5 slides have correct angle ({comp3_score:.2f} pts)")
        total_score += comp3_score
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Slides 6-10 do NOT have gradient fill AND slides 1-5 DO have gradient (0.15 points)
    # This is a compound check: only awards points if the gradient was selectively applied
    # (i.e., slides 1-5 changed to gradient while 6-10 stayed non-gradient)
    # This prevents awarding points on initial_env where all slides are solid white.
    try:
        non_gradient_count = 0
        for slide_num in range(6, 11):
            info = slides_info[slide_num]
            if info['fill_type'] != 'gradient':
                non_gradient_count += 1
                print(f"  Slide {slide_num}: no gradient (fill={info['fill_type']})")
            else:
                print(f"  Slide {slide_num}: should not have gradient but does")
        # Only award points if gradient_count > 0 (from Component 1) AND all 6-10 are non-gradient
        # This ensures this component only passes when the task change was selectively applied
        if gradient_count > 0 and non_gradient_count == 5:
            comp4_score = 0.15
            print(f"PASS: Component 4 -- Slides 6-10 remain without gradient while 1-5 have gradient ({comp4_score:.2f} pts)")
        elif gradient_count > 0:
            comp4_score = (non_gradient_count / 5) * 0.15
            print(f"PARTIAL: Component 4 -- {non_gradient_count}/5 slides correctly lack gradient ({comp4_score:.2f} pts)")
        else:
            comp4_score = 0.0
            print(f"FAIL: Component 4 -- No gradient applied to slides 1-5, so selective application not verified (0.00 pts)")
        total_score += comp4_score
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    zf.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice changes
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_impress")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

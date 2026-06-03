"""
Reward Script: Set a gradient background (light to dark blue) on all slides
Task ID: osworld_impress_all_slides_background_005
Domain: libreoffice_impress
Scoring:
  Component 1: All 6 slides have gradient fill (not white solid) in bgPr — 0.5 pts
  Component 2: Gradient colors are in the blue spectrum — 0.3 pts
  Component 3: At least one stop is a light blue and another is a dark/pure blue — 0.2 pts
Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_impress_all_slides_background_005'

# Namespaces used in pptx XML
NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
NS = {
    'p': NS_P,
    'a': NS_A,
}


def hex_to_rgb(hex_str):
    """Convert 6-char hex string to (r, g, b) tuple."""
    h = hex_str.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def is_blue_dominant(hex_str):
    """Return True if the color has blue as its dominant channel."""
    r, g, b = hex_to_rgb(hex_str)
    return b > r and b > g


def is_light_blue(hex_str):
    """Return True if color is in light blue range (high brightness, blue dominant)."""
    r, g, b = hex_to_rgb(hex_str)
    # Light blue: blue dominant, all channels relatively high
    return b > r and b > g and (r + g + b) > 400


def is_dark_blue(hex_str):
    """Return True if color is in dark blue range (low brightness, blue dominant)."""
    r, g, b = hex_to_rgb(hex_str)
    # Dark blue: blue dominant (or pure blue), low overall brightness
    return b >= r and b >= g and (r + g + b) < 400


def get_slide_bgpr_fill(pptx_path, slide_idx):
    """
    Extract the background fill element (bgPr child) from a slide XML.
    Returns the XML element or None if no bgPr fill.
    slide_idx is 0-based.
    """
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        slide_file = f'ppt/slides/slide{slide_idx + 1}.xml'
        try:
            with zf.open(slide_file) as f:
                root = ET.parse(f).getroot()
                # bgPr is inside p:bg
                bgPr = root.find('.//p:bgPr', NS)
                return bgPr
        except KeyError:
            return None


def verify_task(file_path):
    """
    Verify that all 6 slides have a blue gradient background.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Pre-condition: file must exist and be a valid PPTX
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        if not zipfile.is_zipfile(file_path):
            print(f"CRITICAL: File is not a valid PPTX (zip): {file_path}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot validate file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Determine number of slides
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            slide_files = sorted(
                [n for n in zf.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')]
            )
        num_slides = len(slide_files)
        print(f"INFO: Detected {num_slides} slides")
    except Exception as e:
        print(f"CRITICAL: Cannot read slides from file: {e}")
        print("REWARD: 0.0")
        return 0.0

    if num_slides < 6:
        print(f"FAIL: Expected at least 6 slides, found {num_slides}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All 6 slides must have gradFill (not solidFill) in bgPr (0.5 points)
    # Initial env has solidFill FFFFFF per slide; golden env replaces with gradFill
    try:
        slides_with_gradient = 0
        slides_with_solid_white = 0
        slides_missing_bgpr = 0
        slide_details = []

        for slide_idx in range(6):
            bgPr = get_slide_bgpr_fill(file_path, slide_idx)
            if bgPr is None:
                slides_missing_bgpr += 1
                slide_details.append(f"  Slide {slide_idx+1}: no bgPr (inherited from master)")
            else:
                # Check for gradFill vs solidFill
                grad_fill = bgPr.find('a:gradFill', NS)
                solid_fill = bgPr.find('a:solidFill', NS)
                if grad_fill is not None:
                    slides_with_gradient += 1
                    slide_details.append(f"  Slide {slide_idx+1}: gradFill present")
                elif solid_fill is not None:
                    # Check if it's white
                    srgb = solid_fill.find('.//a:srgbClr', NS)
                    if srgb is not None and srgb.get('val', '').upper() == 'FFFFFF':
                        slides_with_solid_white += 1
                        slide_details.append(f"  Slide {slide_idx+1}: solidFill WHITE (not changed)")
                    else:
                        val = srgb.get('val', 'unknown') if srgb is not None else 'unknown'
                        slide_details.append(f"  Slide {slide_idx+1}: solidFill {val} (not gradient)")
                else:
                    slide_details.append(f"  Slide {slide_idx+1}: bgPr present but unknown fill type")

        print("Component 1: Checking gradient fill on all 6 slides")
        for d in slide_details:
            print(d)

        if slides_with_gradient == 6:
            print(f"PASS: Component 1 — All 6 slides have gradient fill (0.5 pts)")
            total_score += 0.5
        elif slides_with_gradient > 0:
            partial = round(0.5 * (slides_with_gradient / 6), 2)
            print(f"PARTIAL: Component 1 — {slides_with_gradient}/6 slides have gradient fill ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No slides have gradient fill (0.0 pts)")
            print(f"  Slides with solid white: {slides_with_solid_white}, missing bgPr: {slides_missing_bgpr}")

    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Gradient colors must be in the blue spectrum on all slides (0.3 points)
    # Both gradient stops must be blue-dominant colors
    try:
        slides_with_blue_gradient = 0
        blue_details = []

        for slide_idx in range(6):
            bgPr = get_slide_bgpr_fill(file_path, slide_idx)
            if bgPr is None:
                blue_details.append(f"  Slide {slide_idx+1}: no bgPr, skipping blue check")
                continue

            grad_fill = bgPr.find('a:gradFill', NS)
            if grad_fill is None:
                blue_details.append(f"  Slide {slide_idx+1}: no gradFill, cannot check blue")
                continue

            gsLst = grad_fill.find('a:gsLst', NS)
            if gsLst is None:
                blue_details.append(f"  Slide {slide_idx+1}: no gradient stops defined")
                continue

            stops = gsLst.findall('a:gs', NS)
            stop_colors = []
            non_blue_count = 0
            for stop in stops:
                srgb = stop.find('a:srgbClr', NS)
                if srgb is not None:
                    color_val = srgb.get('val', '')
                    stop_colors.append(color_val)
                    if not is_blue_dominant(color_val):
                        non_blue_count += 1
                else:
                    # Could be schemeClr - can't easily verify blue from scheme
                    stop_colors.append('(schemeClr)')

            if non_blue_count == 0 and len(stop_colors) >= 2:
                slides_with_blue_gradient += 1
                blue_details.append(f"  Slide {slide_idx+1}: blue gradient stops: {stop_colors}")
            else:
                blue_details.append(f"  Slide {slide_idx+1}: NOT blue - stops: {stop_colors}")

        print("\nComponent 2: Checking gradient colors are in blue spectrum")
        for d in blue_details:
            print(d)

        if slides_with_blue_gradient == 6:
            print(f"PASS: Component 2 — All 6 slides have blue gradient colors (0.3 pts)")
            total_score += 0.3
        elif slides_with_blue_gradient > 0:
            partial = round(0.3 * (slides_with_blue_gradient / 6), 2)
            print(f"PARTIAL: Component 2 — {slides_with_blue_gradient}/6 slides have blue gradient ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No slides have blue gradient colors (0.0 pts)")

    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Gradient must span from light blue to dark blue (0.2 points)
    # Stop at pos=0 should be light blue; stop at pos=100000 should be dark blue
    try:
        slides_light_to_dark = 0
        range_details = []

        for slide_idx in range(6):
            bgPr = get_slide_bgpr_fill(file_path, slide_idx)
            if bgPr is None:
                range_details.append(f"  Slide {slide_idx+1}: no bgPr, skipping range check")
                continue

            grad_fill = bgPr.find('a:gradFill', NS)
            if grad_fill is None:
                range_details.append(f"  Slide {slide_idx+1}: no gradFill, cannot check range")
                continue

            gsLst = grad_fill.find('a:gsLst', NS)
            if gsLst is None:
                range_details.append(f"  Slide {slide_idx+1}: no gradient stops")
                continue

            stops = gsLst.findall('a:gs', NS)
            # Get first and last stops by position
            stop_map = {}
            for stop in stops:
                pos = int(stop.get('pos', '0'))
                srgb = stop.find('a:srgbClr', NS)
                if srgb is not None:
                    stop_map[pos] = srgb.get('val', '')

            if not stop_map or len(stop_map) < 2:
                range_details.append(f"  Slide {slide_idx+1}: insufficient stops: {stop_map}")
                continue

            min_pos = min(stop_map.keys())
            max_pos = max(stop_map.keys())
            first_color = stop_map[min_pos]
            last_color = stop_map[max_pos]

            # Check: first stop is lighter (higher brightness) than last stop
            first_rgb = hex_to_rgb(first_color)
            last_rgb = hex_to_rgb(last_color)
            first_brightness = sum(first_rgb)
            last_brightness = sum(last_rgb)

            first_is_lighter = first_brightness > last_brightness
            both_blue = is_blue_dominant(first_color) and is_blue_dominant(last_color)

            if first_is_lighter and both_blue:
                slides_light_to_dark += 1
                range_details.append(
                    f"  Slide {slide_idx+1}: light-to-dark blue PASS "
                    f"(start={first_color} brightness={first_brightness}, "
                    f"end={last_color} brightness={last_brightness})"
                )
            else:
                range_details.append(
                    f"  Slide {slide_idx+1}: FAIL "
                    f"(start={first_color} brightness={first_brightness}, "
                    f"end={last_color} brightness={last_brightness}, "
                    f"first_lighter={first_is_lighter}, both_blue={both_blue})"
                )

        print("\nComponent 3: Checking gradient spans light-to-dark blue range")
        for d in range_details:
            print(d)

        if slides_light_to_dark == 6:
            print(f"PASS: Component 3 — All 6 slides have light-to-dark blue gradient (0.2 pts)")
            total_score += 0.2
        elif slides_light_to_dark > 0:
            partial = round(0.2 * (slides_light_to_dark / 6), 2)
            print(f"PARTIAL: Component 3 — {slides_light_to_dark}/6 slides have light-to-dark range ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No slides have correct light-to-dark range (0.0 pts)")

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: run against the canonical task artifact path
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

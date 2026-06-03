"""
Reward Script: Configure Master Slide with custom theme colors, fonts, gradient background, and save as .otp
Task ID: impress_gf5_024
Domain: libreoffice_impress
Scoring:
  Component 1 (0.30): Theme accent colors (Accent1=#FF6B35, Accent2=#2E4057, Accent3=#048A81)
  Component 2 (0.25): Font scheme (Raleway headings, Open Sans body)
  Component 3 (0.25): Gradient background on master slide (#2D2D2D to #000000)
  Component 4 (0.20): .otp file exists
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf5_024'

# Expected accent colors (uppercase hex without #)
EXPECTED_ACCENTS = {
    'accent1': 'FF6B35',
    'accent2': '2E4057',
    'accent3': '048A81',
}

# Expected fonts
EXPECTED_MAJOR_FONT = 'Raleway'
EXPECTED_MINOR_FONT = 'Open Sans'

# Expected gradient stops
EXPECTED_GRAD_START = '2D2D2D'
EXPECTED_GRAD_END = '000000'


def extract_accent_colors(pptx_path):
    """Extract accent1-3 color values from theme XML."""
    # Namespace can vary; search without namespace prefix
    colors = {}
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        theme_files = [f for f in zf.namelist() if 'theme/theme' in f and f.endswith('.xml')]
        if not theme_files:
            return colors
        data = zf.read(theme_files[0]).decode('utf-8')
        root = ET.fromstring(data)

        # Find clrScheme - handle any namespace
        for elem in root.iter():
            tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
            if tag in ('accent1', 'accent2', 'accent3'):
                for child in elem:
                    child_tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                    if child_tag == 'srgbClr':
                        colors[tag] = child.get('val', '').upper()
    return colors


def extract_font_scheme(pptx_path):
    """Extract major and minor font latin typefaces from theme XML."""
    major = None
    minor = None
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        theme_files = [f for f in zf.namelist() if 'theme/theme' in f and f.endswith('.xml')]
        if not theme_files:
            return major, minor
        data = zf.read(theme_files[0]).decode('utf-8')
        root = ET.fromstring(data)

        # Walk to find majorFont/minorFont -> latin typeface
        in_major = False
        in_minor = False
        for elem in root.iter():
            tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
            if tag == 'majorFont':
                in_major = True
                in_minor = False
            elif tag == 'minorFont':
                in_minor = True
                in_major = False
            elif tag == 'latin':
                typeface = elem.get('typeface', '')
                if in_major and major is None:
                    major = typeface
                elif in_minor and minor is None:
                    minor = typeface
            elif tag in ('fontScheme', 'themeElements'):
                # Reset when leaving context
                pass
    return major, minor


def check_gradient_background(pptx_path):
    """Check if slide master has gradient background with expected colors."""
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        master_files = [f for f in zf.namelist()
                        if 'slideMasters/slideMaster' in f and f.endswith('.xml')
                        and '_rels' not in f]
        if not master_files:
            return False, "No slide master found"

        data = zf.read(master_files[0]).decode('utf-8')
        root = ET.fromstring(data)

        # Look for gradFill within bg element
        grad_stops = []
        for elem in root.iter():
            tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
            if tag == 'gradFill':
                # Found gradient fill - now find gradient stops
                for gs in elem.iter():
                    gs_tag = gs.tag.split('}')[-1] if '}' in gs.tag else gs.tag
                    if gs_tag == 'gs':
                        pos = gs.get('pos', '')
                        for color_child in gs:
                            ct = color_child.tag.split('}')[-1] if '}' in color_child.tag else color_child.tag
                            if ct == 'srgbClr':
                                grad_stops.append((pos, color_child.get('val', '').upper()))
                break  # Only check first gradFill

        if not grad_stops:
            return False, "No gradient stops found in slide master"

        # Check that we have the expected gradient colors
        found_start = False
        found_end = False
        for pos, val in grad_stops:
            if val == EXPECTED_GRAD_START.upper():
                found_start = True
            if val == EXPECTED_GRAD_END.upper():
                found_end = True

        if found_start and found_end:
            return True, f"Gradient stops: {grad_stops}"
        else:
            return False, f"Expected {EXPECTED_GRAD_START}->{EXPECTED_GRAD_END}, found stops: {grad_stops}"


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

    # Component 1: Theme accent colors (0.30 points)
    # Accent 1=#FF6B35, Accent 2=#2E4057, Accent 3=#048A81
    try:
        colors = extract_accent_colors(file_path)
        matched = 0
        for accent_key, expected_val in EXPECTED_ACCENTS.items():
            actual = colors.get(accent_key, 'N/A')
            if actual == expected_val.upper():
                matched += 1
                print(f"  PASS: {accent_key} = #{actual}")
            else:
                print(f"  FAIL: {accent_key} expected #{expected_val}, found #{actual}")

        if matched == 3:
            print(f"PASS: Component 1 - All 3 accent colors correct (0.30 pts)")
            total_score += 0.30
        elif matched > 0:
            partial = round(0.30 * matched / 3, 2)
            print(f"PARTIAL: Component 1 - {matched}/3 accent colors correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 - No accent colors match")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Font scheme (0.25 points)
    # Major (headings) = Raleway, Minor (body) = Open Sans
    try:
        major, minor = extract_font_scheme(file_path)
        major_ok = (major == EXPECTED_MAJOR_FONT) if major else False
        minor_ok = (minor == EXPECTED_MINOR_FONT) if minor else False

        if major_ok and minor_ok:
            print(f"PASS: Component 2 - Font scheme correct: major={major}, minor={minor} (0.25 pts)")
            total_score += 0.25
        elif major_ok or minor_ok:
            partial = 0.125
            print(f"PARTIAL: Component 2 - major={major} ({'OK' if major_ok else 'FAIL'}), minor={minor} ({'OK' if minor_ok else 'FAIL'}) ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - Expected major={EXPECTED_MAJOR_FONT}, minor={EXPECTED_MINOR_FONT}; found major={major}, minor={minor}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Gradient background on master slide (0.25 points)
    # #2D2D2D at top to #000000 at bottom
    try:
        grad_ok, grad_detail = check_gradient_background(file_path)
        if grad_ok:
            print(f"PASS: Component 3 - Gradient background verified: {grad_detail} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 - {grad_detail}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: .otp file exists (0.20 points)
    try:
        otp_path = os.path.join(WORKDIR, f'{TASK_ID}.otp')
        if os.path.exists(otp_path) and os.path.getsize(otp_path) > 0:
            size = os.path.getsize(otp_path)
            print(f"PASS: Component 4 - .otp file exists ({size} bytes) (0.20 pts)")
            total_score += 0.20
        else:
            if os.path.exists(otp_path):
                print(f"FAIL: Component 4 - .otp file exists but is empty")
            else:
                print(f"FAIL: Component 4 - .otp file not found at {otp_path}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(round(total_score, 2), 1.0)
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

"""
Reward Script: Footnote separator configuration in LibreOffice Writer
Task ID: writer_bs_022
Domain: libreoffice_writer
Scoring:
  - Component 1: Separator rel-width ~33% (5cm on 15.24cm text) AND left-aligned (0.30 pts)
  - Component 2: Spacing above separator = 0.5cm (0.35 pts)
  - Component 3: Spacing below separator = 0.5cm (0.35 pts)

Verification approach: Parse the .odt (ODF) file's styles.xml to read
the style:footnote-sep element attributes directly. This avoids needing
a running LibreOffice instance or UNO API connection.
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_022'
FILE_PATH = os.path.join(WORKDIR, f'{TASK_ID}.odt')

STYLE_NS = 'urn:oasis:names:tc:opendocument:xmlns:style:1.0'


def parse_cm(value_str):
    """Parse a cm value string like '0.501cm' into a float."""
    if value_str is None:
        return None
    match = re.match(r'([0-9.]+)\s*cm', value_str.strip())
    if match:
        return float(match.group(1))
    return None


def parse_pct(value_str):
    """Parse a percentage string like '33%' into an integer."""
    if value_str is None:
        return None
    match = re.match(r'(\d+)\s*%', value_str.strip())
    if match:
        return int(match.group(1))
    return None


def get_footnote_sep_attrs(file_path):
    """Extract footnote-sep attributes from the ODF styles.xml."""
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            styles_xml = z.read('styles.xml').decode('utf-8')
    except Exception as e:
        print(f"ERROR: Cannot read styles.xml from {file_path}: {e}")
        return None

    root = ET.fromstring(styles_xml)

    # Find the style:footnote-sep element
    tag_name = f'{{{STYLE_NS}}}footnote-sep'
    for elem in root.iter(tag_name):
        attrs = {}
        for k, v in elem.attrib.items():
            # Strip namespace from attribute names for easier access
            local = k.split('}')[-1] if '}' in k else k
            attrs[local] = v
        return attrs

    print("WARNING: No style:footnote-sep element found in styles.xml")
    return None


def verify_task(file_path):
    """
    Verify footnote separator configuration with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid .odt
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    attrs = get_footnote_sep_attrs(file_path)
    if attrs is None:
        print("CRITICAL: Could not extract footnote separator attributes")
        print("REWARD: 0.0")
        return 0.0

    print(f"Footnote separator attributes: {attrs}")

    # Component 1: Separator line ~5cm (rel-width ~33%) AND left-aligned (0.30 points)
    # Task requires 5cm line. Text width is 15.24cm, so 5cm = ~32.8%.
    # The closest integer percentage is 33% (= 5.03cm). Accept 30-36% as valid range.
    # Alignment must be "left".
    # NOTE: Default rel-width is 25% and default adjustment is "left".
    # We only score if rel-width has CHANGED from the 25% default.
    try:
        rel_width = parse_pct(attrs.get('rel-width'))
        adjustment = attrs.get('adjustment', '')

        if rel_width is not None:
            print(f"  rel-width = {rel_width}% (expected ~33%, default is 25%)")
            print(f"  adjustment = {adjustment} (expected 'left')")

            # Must be different from default 25% AND in acceptable range for 5cm
            if 30 <= rel_width <= 36 and adjustment == 'left':
                print(f"PASS: Component 1 -- rel-width={rel_width}% (~5cm) and left-aligned (0.30 pts)")
                total_score += 0.30
            elif rel_width == 25:
                print(f"FAIL: Component 1 -- rel-width={rel_width}% is still default (25%), not changed to ~33%")
            else:
                print(f"FAIL: Component 1 -- rel-width={rel_width}% or adjustment={adjustment} out of range")
        else:
            print(f"FAIL: Component 1 -- rel-width not found or unparseable: {attrs.get('rel-width')}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Spacing above separator = 0.5cm (0.35 points)
    # ODF attribute: distance-before-sep
    # Default is 0.101cm. Task requires 0.5cm.
    # Accept 0.45-0.55cm range for tolerance.
    try:
        dist_before = parse_cm(attrs.get('distance-before-sep'))
        if dist_before is not None:
            print(f"  distance-before-sep = {dist_before}cm (expected ~0.5cm, default is 0.101cm)")

            if 0.45 <= dist_before <= 0.55:
                print(f"PASS: Component 2 -- spacing above = {dist_before}cm (~0.5cm) (0.35 pts)")
                total_score += 0.35
            elif abs(dist_before - 0.101) < 0.01:
                print(f"FAIL: Component 2 -- spacing above = {dist_before}cm is still default (~0.1cm)")
            else:
                print(f"FAIL: Component 2 -- spacing above = {dist_before}cm, expected ~0.5cm")
        else:
            print(f"FAIL: Component 2 -- distance-before-sep not found: {attrs.get('distance-before-sep')}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Spacing below separator = 0.5cm (0.35 points)
    # ODF attribute: distance-after-sep
    # Default is 0.101cm. Task requires 0.5cm.
    # Accept 0.45-0.55cm range for tolerance.
    try:
        dist_after = parse_cm(attrs.get('distance-after-sep'))
        if dist_after is not None:
            print(f"  distance-after-sep = {dist_after}cm (expected ~0.5cm, default is 0.101cm)")

            if 0.45 <= dist_after <= 0.55:
                print(f"PASS: Component 3 -- spacing below = {dist_after}cm (~0.5cm) (0.35 pts)")
                total_score += 0.35
            elif abs(dist_after - 0.101) < 0.01:
                print(f"FAIL: Component 3 -- spacing below = {dist_after}cm is still default (~0.1cm)")
            else:
                print(f"FAIL: Component 3 -- spacing below = {dist_after}cm, expected ~0.5cm")
        else:
            print(f"FAIL: Component 3 -- distance-after-sep not found: {attrs.get('distance-after-sep')}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification (save any unsaved changes)
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Main execution
persist_app_state()

if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

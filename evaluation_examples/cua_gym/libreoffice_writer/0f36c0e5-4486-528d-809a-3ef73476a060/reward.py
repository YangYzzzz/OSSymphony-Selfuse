"""
Reward Script: Set up envelope printing with face-up feed direction and flap at the left
Task ID: writer_lec_051
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5 pts): FromAbove == true (face-up feed direction)
  Component 2 (0.5 pts): Alignment == 0 (flap at the left)
"""

import os
import xml.etree.ElementTree as ET

TASK_ID = 'writer_lec_051'
REGISTRY_PATH = '/home/user/.config/libreoffice/4/user/registrymodifications.xcu'


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


def parse_envelope_print_settings(registry_path):
    """
    Parse the LibreOffice registrymodifications.xcu to extract
    envelope print settings from /org.openoffice.Office.Writer/Envelope/Print.

    Returns a dict with keys: FromAbove, Alignment, Right, Down (as strings).
    """
    settings = {}

    if not os.path.exists(registry_path):
        print(f"CRITICAL: Registry file not found: {registry_path}")
        return settings

    try:
        tree = ET.parse(registry_path)
        root = tree.getroot()
    except ET.ParseError:
        # Fallback: parse line-by-line since the file may not be well-formed XML
        # or may use namespaces that confuse ElementTree
        print("INFO: ET.parse failed, falling back to text parsing")
        return parse_envelope_settings_text(registry_path)

    # The registrymodifications.xcu uses oor namespace
    # Try namespace-aware parsing
    ns = {
        'oor': 'http://openoffice.org/2001/registry',
        'xs': 'http://www.w3.org/2001/XMLSchema',
    }

    for item in root.iter():
        path_attr = item.get('{http://openoffice.org/2001/registry}path', '')
        if not path_attr:
            path_attr = item.get('oor:path', '')

        if 'Envelope/Print' in path_attr:
            for prop in item.iter():
                name_attr = prop.get('{http://openoffice.org/2001/registry}name', '')
                if not name_attr:
                    name_attr = prop.get('oor:name', '')

                if name_attr in ('FromAbove', 'Alignment', 'Right', 'Down'):
                    for val_elem in prop.iter():
                        if val_elem.tag.endswith('value') or val_elem.tag == 'value':
                            if val_elem.text is not None:
                                settings[name_attr] = val_elem.text.strip()

    if not settings:
        # Fallback to text-based parsing
        print("INFO: XML parsing found no envelope settings, falling back to text parsing")
        return parse_envelope_settings_text(registry_path)

    return settings


def parse_envelope_settings_text(registry_path):
    """
    Fallback text-based parser for registrymodifications.xcu.
    Reads the file as text and extracts envelope print settings via string matching.
    """
    settings = {}

    try:
        with open(registry_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR: Cannot read registry file: {e}")
        return settings

    import re

    # Pattern: <item oor:path="...Envelope/Print"><prop oor:name="XXX" ...><value>YYY</value></prop></item>
    # Each item is on one line in registrymodifications.xcu
    pattern = r'oor:path="/org\.openoffice\.Office\.Writer/Envelope/Print".*?oor:name="(\w+)".*?<value>(.*?)</value>'

    for match in re.finditer(pattern, content):
        name = match.group(1)
        value = match.group(2)
        settings[name] = value

    return settings


def verify_task():
    """
    Verify envelope print settings:
    - FromAbove should be 'true' (face-up feed direction)
    - Alignment should be '0' (flap at the left)

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Parse envelope print settings from LibreOffice registry
    settings = parse_envelope_print_settings(REGISTRY_PATH)

    if not settings:
        print("CRITICAL: No envelope print settings found in registry")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Parsed envelope print settings: {settings}")

    # Component 1: FromAbove == true (face-up feed direction) (0.5 points)
    # Task requires face-up feed direction. In initial_env this is 'false' (face-down).
    try:
        from_above = settings.get('FromAbove', None)
        if from_above is not None and from_above.lower() == 'true':
            print(f"PASS: Component 1 -- FromAbove is 'true' (face-up) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 -- Expected FromAbove='true' (face-up), found: '{from_above}'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Alignment == 0 (flap at the left) (0.5 points)
    # Task requires flap at the left. In initial_env this is '5' (different orientation).
    # Alignment=0 corresponds to flap-at-left in the LibreOffice envelope feed direction grid.
    try:
        alignment = settings.get('Alignment', None)
        if alignment is not None and str(alignment).strip() == '0':
            print(f"PASS: Component 2 -- Alignment is '0' (flap at the left) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 -- Expected Alignment='0' (flap at left), found: '{alignment}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification
persist_app_state("libreoffice_writer")

# Run verification
verify_task()

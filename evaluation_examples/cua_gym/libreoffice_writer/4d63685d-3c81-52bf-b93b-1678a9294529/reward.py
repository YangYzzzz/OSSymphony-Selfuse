"""
Reward Script: Configure tracked changes display settings
Task ID: writer_lec_078
Domain: libreoffice_writer
Scoring:
  Component 1: Insertion color is blue (0.25)
  Component 2: Insertion attribute is double underline (0.25)
  Component 3: Deletion color is red (0.25)
  Component 4: Deletion attribute is strikethrough (0.25)
"""

import os
import xml.etree.ElementTree as ET

REGISTRY_PATH = '/home/user/.config/libreoffice/4/user/registrymodifications.xcu'
TASK_ID = 'writer_lec_078'

# Expected values for tracked changes display settings
# Insertions: blue color (0x0000FF = 255), double underline (attribute 4)
# Deletions: red color (0xFF0000 = 16711680), strikethrough (attribute 5)
EXPECTED_INSERT_COLOR = 255          # Blue (0x0000FF)
EXPECTED_INSERT_ATTRIBUTE = 4        # Double underline
EXPECTED_DELETE_COLOR = 16711680     # Red (0xFF0000)
EXPECTED_DELETE_ATTRIBUTE = 5        # Strikethrough


def parse_revision_settings(registry_path):
    """
    Parse LibreOffice registrymodifications.xcu to extract
    tracked changes (Revision/TextDisplay) settings.
    Returns a dict with keys like 'Insert/Color', 'Insert/Attribute', etc.
    """
    settings = {}
    try:
        tree = ET.parse(registry_path)
        root = tree.getroot()
        oor_ns = 'http://openoffice.org/2001/registry'

        for item in root:
            path = item.attrib.get(f'{{{oor_ns}}}path', '')
            # Look for Revision/TextDisplay/Insert and Delete paths
            if '/Revision/TextDisplay/Insert' in path or '/Revision/TextDisplay/Delete' in path:
                # Extract the category (Insert or Delete)
                if '/Insert' in path:
                    category = 'Insert'
                elif '/Delete' in path:
                    category = 'Delete'
                else:
                    continue

                # Find prop element and extract name and value
                for prop in item:
                    prop_name = prop.attrib.get(f'{{{oor_ns}}}name', '')
                    value_elem = prop.find('{urn:oasis:names:tc:opendocument:xmlns:common:1.0}value')
                    if value_elem is None:
                        # Try without namespace
                        for child in prop:
                            if child.tag.endswith('value') or child.tag == 'value':
                                value_elem = child
                                break
                    if value_elem is not None and value_elem.text is not None:
                        key = f'{category}/{prop_name}'
                        settings[key] = value_elem.text.strip()
    except Exception as e:
        print(f"ERROR: Failed to parse registry: {e}")

    return settings


def verify_task():
    """
    Verify tracked changes display settings with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Check if registry file exists (precondition gate, not scored)
    if not os.path.exists(REGISTRY_PATH):
        print(f"CRITICAL: Registry file not found: {REGISTRY_PATH}")
        print("REWARD: 0.0")
        return 0.0

    settings = parse_revision_settings(REGISTRY_PATH)
    print(f"Parsed revision settings: {settings}")

    # Component 1: Insertion color is blue (0.25 points)
    try:
        insert_color = settings.get('Insert/Color')
        if insert_color is not None and int(insert_color) == EXPECTED_INSERT_COLOR:
            print(f"PASS: Component 1 -- Insertion color is blue ({insert_color}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 -- Expected insertion color {EXPECTED_INSERT_COLOR}, found: {insert_color}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Insertion attribute is double underline (0.25 points)
    try:
        insert_attr = settings.get('Insert/Attribute')
        if insert_attr is not None and int(insert_attr) == EXPECTED_INSERT_ATTRIBUTE:
            print(f"PASS: Component 2 -- Insertion attribute is double underline ({insert_attr}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- Expected insertion attribute {EXPECTED_INSERT_ATTRIBUTE}, found: {insert_attr}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Deletion color is red (0.25 points)
    try:
        delete_color = settings.get('Delete/Color')
        if delete_color is not None and int(delete_color) == EXPECTED_DELETE_COLOR:
            print(f"PASS: Component 3 -- Deletion color is red ({delete_color}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- Expected deletion color {EXPECTED_DELETE_COLOR}, found: {delete_color}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Deletion attribute is strikethrough (0.25 points)
    try:
        delete_attr = settings.get('Delete/Attribute')
        if delete_attr is not None and int(delete_attr) == EXPECTED_DELETE_ATTRIBUTE:
            print(f"PASS: Component 4 -- Deletion attribute is strikethrough ({delete_attr}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 -- Expected deletion attribute {EXPECTED_DELETE_ATTRIBUTE}, found: {delete_attr}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

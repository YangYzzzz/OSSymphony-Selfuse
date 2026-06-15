"""
Reward Script: Change tracked insertion color to blue and deletion color to red
Task ID: writer_rm_015
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): Insertion color is blue (decimal 255 = 0x0000FF)
  Component 2 (0.5): Deletion color is red (decimal 16711680 = 0xFF0000)
"""

import os
import re

TASK_ID = 'writer_rm_015'
REGISTRY_PATH = '/home/user/.config/libreoffice/4/user/registrymodifications.xcu'

# Expected color values (LibreOffice stores colors as signed 32-bit integers)
# Blue = 0x0000FF = 255
# Red  = 0xFF0000 = 16711680
# "By author" / auto = -1
BLUE_DECIMAL = 255
RED_DECIMAL = 16711680


def parse_registry_color(xcu_content, oor_path, prop_name):
    """
    Parse a color value from registrymodifications.xcu.
    Returns the integer value if found, or None.

    Handles two XML patterns:
      Pattern A: <item oor:path="..."><prop oor:name="Color" ...><value>NNN</value></prop></item>
      Pattern B: Multiline variants
    """
    # Build regex to match the specific path + property
    # Escape dots and slashes in path for regex
    escaped_path = re.escape(oor_path)
    escaped_prop = re.escape(prop_name)

    pattern = (
        r'<item\s+oor:path="' + escaped_path + r'">'
        r'\s*<prop\s+oor:name="' + escaped_prop + r'"[^>]*>'
        r'\s*<value>([^<]+)</value>'
    )

    match = re.search(pattern, xcu_content)
    if match:
        try:
            return int(match.group(1).strip())
        except ValueError:
            return None
    return None


def verify_task():
    """
    Verify that tracked changes colors are set correctly in LibreOffice Writer config.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: registry file must exist
    if not os.path.exists(REGISTRY_PATH):
        print(f"CRITICAL: Registry file not found: {REGISTRY_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
            xcu_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read registry file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Tracked insertion color is blue (0.5 points)
    # Path: /org.openoffice.Office.Writer/Revision/TextDisplay/Insert, Property: Color
    # Expected: 255 (blue). Initial state: -1 (auto/by author)
    try:
        insert_color = parse_registry_color(
            xcu_content,
            "/org.openoffice.Office.Writer/Revision/TextDisplay/Insert",
            "Color"
        )
        if insert_color is not None and insert_color == BLUE_DECIMAL:
            print(f"PASS: Component 1 -- Insertion color is blue (value: {insert_color}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 -- Expected insertion color {BLUE_DECIMAL} (blue), found: {insert_color}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Tracked deletion color is red (0.5 points)
    # Path: /org.openoffice.Office.Writer/Revision/TextDisplay/Delete, Property: Color
    # Expected: 16711680 (red). Initial state: -1 (auto/by author)
    try:
        delete_color = parse_registry_color(
            xcu_content,
            "/org.openoffice.Office.Writer/Revision/TextDisplay/Delete",
            "Color"
        )
        if delete_color is not None and delete_color == RED_DECIMAL:
            print(f"PASS: Component 2 -- Deletion color is red (value: {delete_color}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 -- Expected deletion color {RED_DECIMAL} (red), found: {delete_color}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

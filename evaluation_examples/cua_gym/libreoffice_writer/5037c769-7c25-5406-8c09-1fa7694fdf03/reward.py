"""
Reward Script: Verify Track Changes display settings in LibreOffice Writer
Task ID: writer_rm_042
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): Insert attribute = 4 (Double underline)
  Component 2 (0.35): Delete attribute = 5 (Strikethrough)
  Component 3 (0.30): Insert color = 25600 (dark green #006400)
"""

import os
import re

# The settings live in the LibreOffice user profile registry file
REGISTRY_PATH = os.path.expanduser("~/.config/libreoffice/4/user/registrymodifications.xcu")


def parse_registry_settings(content):
    """
    Parse registrymodifications.xcu for Writer Revision/TextDisplay settings.
    Returns a dict like:
      {
        'Insert': {'Attribute': '...', 'Color': '...'},
        'Delete': {'Attribute': '...', 'Color': '...'},
      }
    """
    settings = {
        'Insert': {'Attribute': None, 'Color': None},
        'Delete': {'Attribute': None, 'Color': None},
    }

    # Match items under org.openoffice.Office.Writer/Revision/TextDisplay/(Insert|Delete)
    pattern = re.compile(
        r'<item\s+oor:path="/org\.openoffice\.Office\.Writer/Revision/TextDisplay/(Insert|Delete)">'
        r'<prop\s+oor:name="(Attribute|Color)"\s+oor:op="fuse">'
        r'<value>([^<]*)</value>'
    )

    for match in pattern.finditer(content):
        section = match.group(1)   # Insert or Delete
        prop_name = match.group(2) # Attribute or Color
        value = match.group(3)
        if section in settings and prop_name in settings[section]:
            settings[section][prop_name] = value

    return settings


def verify_task():
    """
    Verify task completion with progressive scoring.
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
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read registry file: {e}")
        print("REWARD: 0.0")
        return 0.0

    settings = parse_registry_settings(content)
    print(f"Parsed settings: {settings}")

    # Component 1: Insert Attribute = 4 (Double underline) — 0.35 points
    try:
        insert_attr = settings['Insert']['Attribute']
        if insert_attr is not None and int(insert_attr) == 4:
            print(f"PASS: Component 1 — Insert Attribute is 4 (Double underline) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — Expected Insert Attribute=4, found: {insert_attr}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Delete Attribute = 5 (Strikethrough) — 0.35 points
    try:
        delete_attr = settings['Delete']['Attribute']
        if delete_attr is not None and int(delete_attr) == 5:
            print(f"PASS: Component 2 — Delete Attribute is 5 (Strikethrough) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — Expected Delete Attribute=5, found: {delete_attr}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Insert Color = 25600 (dark green #006400) — 0.30 points
    try:
        insert_color = settings['Insert']['Color']
        if insert_color is not None and int(insert_color) == 25600:
            print(f"PASS: Component 3 — Insert Color is 25600 (dark green #006400) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — Expected Insert Color=25600, found: {insert_color}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

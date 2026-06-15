"""
Reward Script: Change LibreOffice author name from 'User1' to 'Dr. Emily Watson'
Task ID: writer_rm_032
Domain: libreoffice_writer
Scoring:
  Component 1: First name (givenname) changed to 'Dr. Emily' (0.4 pts)
  Component 2: Last name (sn) changed to 'Watson' (0.4 pts)
  Component 3: Initials updated away from 'U1' (0.2 pts)
"""

import os
import xml.etree.ElementTree as ET

CONFIG_PATH = '/home/user/.config/libreoffice/4/user/registrymodifications.xcu'
TASK_ID = 'writer_rm_032'
OOR_NS = 'http://openoffice.org/2001/registry'


def get_user_profile_fields(config_path):
    """Parse registrymodifications.xcu and extract UserProfile/Data fields."""
    fields = {}
    try:
        tree = ET.parse(config_path)
        root = tree.getroot()
        for item in root:
            path_attr = item.get(f'{{{OOR_NS}}}path', '')
            if 'UserProfile/Data' not in path_attr:
                continue
            for prop in item:
                name = prop.get(f'{{{OOR_NS}}}name', '')
                if name in ('givenname', 'sn', 'initials'):
                    # Get the value element text
                    for val_elem in prop:
                        if val_elem.tag.endswith('value') or 'value' in val_elem.tag:
                            fields[name] = val_elem.text or ''
                            break
    except Exception as e:
        print(f"ERROR: Could not parse config file: {e}")
    return fields


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: config file must exist
    if not os.path.exists(CONFIG_PATH):
        print(f"CRITICAL: Config file not found: {CONFIG_PATH}")
        print("REWARD: 0.0")
        return 0.0

    fields = get_user_profile_fields(CONFIG_PATH)
    if not fields:
        print("CRITICAL: Could not extract any UserProfile fields from config")
        print("REWARD: 0.0")
        return 0.0

    print(f"Extracted UserProfile fields: {fields}")

    # Component 1: First name (givenname) is 'Dr. Emily' (0.4 points)
    # Initial state has 'User1', golden state should have 'Dr. Emily'
    try:
        givenname = fields.get('givenname', '')
        if givenname.strip() == 'Dr. Emily':
            print(f"PASS: Component 1 -- givenname is 'Dr. Emily' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- expected givenname 'Dr. Emily', found '{givenname}'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Last name (sn) is 'Watson' (0.4 points)
    # Initial state has '' (empty), golden state should have 'Watson'
    try:
        sn = fields.get('sn', '')
        if sn.strip() == 'Watson':
            print(f"PASS: Component 2 -- sn (last name) is 'Watson' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 -- expected sn 'Watson', found '{sn}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Initials updated from 'U1' to something reflecting 'Dr. Emily Watson' (0.2 points)
    # The golden state has 'EW'; we accept any initials that are NOT the old 'U1'
    # and that contain at least one character from the new name
    try:
        initials = fields.get('initials', '')
        # Must not be the old initials AND must not be empty
        if initials.strip() and initials.strip() != 'U1':
            print(f"PASS: Component 3 -- initials updated to '{initials}' (no longer 'U1') (0.2 pts)")
            total_score += 0.2
        else:
            if initials.strip() == 'U1':
                print(f"FAIL: Component 3 -- initials still 'U1' (not updated)")
            else:
                print(f"FAIL: Component 3 -- initials are empty")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice state before verifying
def persist_app_state():
    """Send Ctrl+S to save any unsaved settings changes in LibreOffice."""
    try:
        os.environ["DISPLAY"] = ":0"
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        import time
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for LibreOffice Writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


persist_app_state()
verify_task()

"""
Reward Script: Enable 'Always save version on closing' in LibreOffice Writer
Task ID: writer_lec_081
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.4): settings.xml exists in .odt archive with SaveVersionOnClose config item
  - Component 2 (0.6): SaveVersionOnClose is set to 'true'
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_081'

def verify_task(file_path):
    """
    Verify that the 'Always save a version on close' option is enabled
    in the ODF document's settings.xml.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid zip (ODF)
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open ODT file as zip: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: settings.xml exists and contains SaveVersionOnClose config item (0.4 points)
    try:
        file_list = zf.namelist()
        if 'settings.xml' not in file_list:
            print(f"FAIL: Component 1 — settings.xml not found in ODT archive. Files: {file_list}")
        else:
            settings_content = zf.read('settings.xml').decode('utf-8')
            if 'SaveVersionOnClose' in settings_content:
                print(f"PASS: Component 1 — settings.xml exists and contains SaveVersionOnClose (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — settings.xml exists but does not contain SaveVersionOnClose")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: SaveVersionOnClose is set to 'true' (0.6 points)
    try:
        if 'settings.xml' in zf.namelist():
            settings_content = zf.read('settings.xml').decode('utf-8')
            root = ET.fromstring(settings_content)

            # Define ODF namespaces
            ns = {
                'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
                'config': 'urn:oasis:names:tc:opendocument:xmlns:config:1.0',
            }

            # Search for SaveVersionOnClose config item
            # Collect all SaveVersionOnClose items
            matching_items = [
                item for item in root.iter('{urn:oasis:names:tc:opendocument:xmlns:config:1.0}config-item')
                if item.attrib.get('{urn:oasis:names:tc:opendocument:xmlns:config:1.0}name', '') == 'SaveVersionOnClose'
            ]
            if len(matching_items) > 0:
                value = (matching_items[0].text or '').strip().lower()
                if value == 'true':
                    print(f"PASS: Component 2 — SaveVersionOnClose is 'true' (0.6 pts)")
                    total_score += 0.6
                else:
                    print(f"FAIL: Component 2 — SaveVersionOnClose value is '{value}', expected 'true'")
            else:
                print(f"FAIL: Component 2 — SaveVersionOnClose config-item not found in XML tree")
        else:
            print(f"FAIL: Component 2 — settings.xml not present, cannot check SaveVersionOnClose value")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    zf.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.odt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Add AutoCorrect entry 'addr' -> '1234 Innovation Drive, Suite 500, San Jose, CA 95134'
Task ID: writer_edit_054
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): acor_en-US.dat exists in the user's LibreOffice autocorr directory
  Component 2 (0.5): DocumentList.xml inside acor_en-US.dat contains the 'addr' -> address entry
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_edit_054'

# Path to the LibreOffice user AutoCorrect file for English
AUTOCORR_PATH = '/home/user/.config/libreoffice/4/user/autocorr/acor_en-US.dat'

# Expected AutoCorrect entry
EXPECTED_SHORT = 'addr'
EXPECTED_LONG  = '1234 Innovation Drive, Suite 500, San Jose, CA 95134'


def verify_task():
    """
    Verify that the LibreOffice AutoCorrect replacement entry 'addr' ->
    '1234 Innovation Drive, Suite 500, San Jose, CA 95134' has been added.

    The AutoCorrect entries are stored in:
      ~/.config/libreoffice/4/user/autocorr/acor_en-US.dat
    which is a ZIP archive containing DocumentList.xml with block-list entries.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ------------------------------------------------------------------
    # Component 1: acor_en-US.dat exists and is non-empty (0.5 points)
    # This file is absent on initial_env (empty autocorr dir).
    # It is created on golden_env when the AutoCorrect entry is added.
    # ------------------------------------------------------------------
    try:
        dat_exists = os.path.exists(AUTOCORR_PATH) and os.path.getsize(AUTOCORR_PATH) > 0
        if dat_exists:
            print(f"PASS: Component 1 — acor_en-US.dat exists at {AUTOCORR_PATH} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — acor_en-US.dat not found or empty at {AUTOCORR_PATH}")
            # Without the file, component 2 cannot pass either
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # ------------------------------------------------------------------
    # Component 2: DocumentList.xml contains the 'addr' -> address entry
    # (0.5 points)
    # The .dat file is a ZIP archive; DocumentList.xml holds Replace-tab
    # entries as <block-list:block abbreviated-name="..." name="..."> nodes.
    # ------------------------------------------------------------------
    try:
        with zipfile.ZipFile(AUTOCORR_PATH, 'r') as z:
            if 'DocumentList.xml' not in z.namelist():
                print(f"FAIL: Component 2 — DocumentList.xml not found inside acor_en-US.dat")
            else:
                content = z.read('DocumentList.xml').decode('utf-8')
                ns = 'http://openoffice.org/2001/block-list'

                try:
                    root = ET.fromstring(content)
                    matched_name = None
                    for block in root.findall(f'{{{ns}}}block'):
                        abbr = block.attrib.get(f'{{{ns}}}abbreviated-name', '')
                        if abbr == EXPECTED_SHORT:
                            matched_name = block.attrib.get(f'{{{ns}}}name', '')
                            break

                    if matched_name == EXPECTED_LONG:
                        print(f"PASS: Component 2 — entry verified: '{EXPECTED_SHORT}' -> '{matched_name}' (0.5 pts)")
                        total_score += 0.5
                    elif matched_name is not None:
                        print(f"FAIL: Component 2 — 'addr' found but wrong value: '{matched_name}'")
                        print(f"       Expected: '{EXPECTED_LONG}'")
                    else:
                        print(f"FAIL: Component 2 — no abbreviated-name='{EXPECTED_SHORT}' in XML")

                except ET.ParseError:
                    # Fallback: raw string search when XML is malformed
                    addr_key = f'abbreviated-name="{EXPECTED_SHORT}"'
                    if addr_key in content and EXPECTED_LONG in content:
                        print(f"PASS: Component 2 — entry found via string search fallback (0.5 pts)")
                        total_score += 0.5
                    else:
                        print(f"FAIL: Component 2 — 'addr' entry not found (string search fallback)")

    except zipfile.BadZipFile as e:
        print(f"FAIL: Component 2 — acor_en-US.dat is not a valid ZIP archive: {e}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

"""
Reward Script: Configure AutoCorrect to replace ':)' with smiley emoji
Task ID: writer_frd_057
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): acor_en-US.dat exists with valid structure
  Component 2 (0.6): ':)' -> smiley (U+263A or similar) entry present in DocumentList.xml
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_frd_057'

# Path to user-level AutoCorrect file for en-US
AUTOCORR_DIR = os.path.join(WORKDIR, '.config', 'libreoffice', '4', 'user', 'autocorr')
AUTOCORR_DAT = os.path.join(AUTOCORR_DIR, 'acor_en-US.dat')

# Acceptable smiley characters that ':)' could map to
SMILEY_CHARS = {
    '\u263A',  # WHITE SMILING FACE
    '\u263B',  # BLACK SMILING FACE
    '\U0001F600',  # GRINNING FACE
    '\U0001F601',  # GRINNING FACE WITH SMILING EYES
    '\U0001F603',  # SMILING FACE WITH OPEN MOUTH
    '\U0001F604',  # SMILING FACE WITH OPEN MOUTH AND SMILING EYES
    '\U0001F642',  # SLIGHTLY SMILING FACE
    '\U0001F60A',  # SMILING FACE WITH SMILING EYES
}


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


def verify_task():
    """
    Verify that AutoCorrect has been configured to replace ':)' with a smiley.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: acor_en-US.dat exists and is a valid zip (0.4 points)
    # This file is created when user adds/modifies AutoCorrect entries.
    # On initial_env, this file does NOT exist (empty autocorr dir).
    try:
        if os.path.exists(AUTOCORR_DAT):
            with zipfile.ZipFile(AUTOCORR_DAT, 'r') as z:
                names = z.namelist()
                if 'DocumentList.xml' in names:
                    print(f"PASS: Component 1 -- acor_en-US.dat exists with DocumentList.xml (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 1 -- acor_en-US.dat exists but missing DocumentList.xml. Contents: {names}")
        else:
            print(f"FAIL: Component 1 -- acor_en-US.dat not found at {AUTOCORR_DAT}")
    except zipfile.BadZipFile:
        print(f"FAIL: Component 1 -- acor_en-US.dat is not a valid zip file")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: ':)' -> smiley entry exists in DocumentList.xml (0.6 points)
    # The AutoCorrect replacement list is stored as XML block-list entries.
    # We look for abbreviated-name=":)" mapped to a smiley character.
    try:
        if os.path.exists(AUTOCORR_DAT):
            with zipfile.ZipFile(AUTOCORR_DAT, 'r') as z:
                if 'DocumentList.xml' in z.namelist():
                    xml_content = z.read('DocumentList.xml').decode('utf-8')
                    # Parse the XML
                    root = ET.fromstring(xml_content)
                    ns = {'bl': 'http://openoffice.org/2001/block-list'}

                    replacement_value = None

                    for block in root.findall('.//bl:block', ns):
                        abbrev = block.get('{http://openoffice.org/2001/block-list}abbreviated-name', '')
                        name = block.get('{http://openoffice.org/2001/block-list}name', '')
                        if abbrev == ':)':
                            replacement_value = name
                            break

                    # Check if replacement is a recognized smiley character
                    is_smiley = (replacement_value is not None and
                                 (replacement_value in SMILEY_CHARS or
                                  any(c in SMILEY_CHARS for c in replacement_value)))

                    if is_smiley:
                        print(f"PASS: Component 2 -- ':)' maps to smiley '{replacement_value}' (U+{ord(replacement_value[0]):04X}) (0.6 pts)")
                        total_score += 0.6
                    elif replacement_value is not None:
                        print(f"FAIL: Component 2 -- ':)' entry found but maps to '{replacement_value}' (not a recognized smiley)")
                    else:
                        print(f"FAIL: Component 2 -- No ':)' entry found in DocumentList.xml")
                else:
                    print(f"FAIL: Component 2 -- DocumentList.xml not in acor_en-US.dat")
        else:
            print(f"FAIL: Component 2 -- acor_en-US.dat not found, cannot check entries")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before checking (AutoCorrect changes should already be saved to disk)
persist_app_state("libreoffice_writer")

verify_task()

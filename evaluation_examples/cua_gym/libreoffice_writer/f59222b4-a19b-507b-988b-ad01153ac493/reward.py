"""
Reward Script: Disable AutoCorrect 'Capitalize first letter of every sentence'
Task ID: writer_edit_026
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6): CapitalizeFirstSentence is explicitly set to 'false' in
                      registrymodifications.xcu under /org.openoffice.Office.Writer/AutoFunction/Text
  Component 2 (0.4): Document file code_samples.docx still exists and is a valid docx
                     (guarded: only awarded when Component 1 passes)
"""

import os
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_edit_026'
CONFIG_PATH = '/home/user/.config/libreoffice/4/user/registrymodifications.xcu'
DOC_PATH = '/home/user/Desktop/code_samples.docx'


def check_capitalize_disabled(config_path):
    """
    Parse the LibreOffice registrymodifications.xcu file and check whether
    the CapitalizeFirstSentence property is explicitly set to 'false'.

    Returns:
        (bool, str): (is_disabled, diagnostic_message)
    """
    ns_oor = 'http://openoffice.org/2001/registry'
    target_path = '/org.openoffice.Office.Writer/AutoFunction/Text'

    tree = ET.parse(config_path)
    root = tree.getroot()

    for item in root.iter():
        item_path = item.get(f'{{{ns_oor}}}path', '')
        if item_path == target_path:
            for prop in item.iter():
                prop_name = prop.get(f'{{{ns_oor}}}name', '')
                if prop_name == 'CapitalizeFirstSentence':
                    value_el = prop.find('value')
                    if value_el is not None and value_el.text:
                        val = value_el.text.strip().lower()
                        if val == 'false':
                            return True, f"CapitalizeFirstSentence='false' found at '{target_path}'"
                        else:
                            return False, f"CapitalizeFirstSentence='{val}' found (expected 'false')"
                    else:
                        return False, "CapitalizeFirstSentence prop found but has no value element"
            # target_path item found but no CapitalizeFirstSentence property
            return False, f"Item at '{target_path}' found but no CapitalizeFirstSentence property"

    # No entry at all: setting is at default (true = enabled)
    return False, f"No entry at '{target_path}' — CapitalizeFirstSentence still at default (true/enabled)"


def verify_task():
    """
    Verify that the AutoCorrect 'Capitalize first letter of every sentence' option
    has been disabled in LibreOffice Writer settings.

    The setting is stored in registrymodifications.xcu at path:
      /org.openoffice.Office.Writer/AutoFunction/Text
    as property 'CapitalizeFirstSentence' with value 'false'.

    When this setting is NOT present in the file, the default is 'true' (enabled).
    The task requires it to be explicitly set to 'false' (disabled).

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: registry config file must exist to proceed
    if not os.path.exists(CONFIG_PATH):
        print(f"CRITICAL: LibreOffice registry config not found: {CONFIG_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: CapitalizeFirstSentence is explicitly set to false (0.6 points)
    # FAILS on initial_env (no entry — default = true, feature is enabled)
    # PASSES on golden_env (entry present with value 'false', feature is disabled)
    try:
        disabled, msg = check_capitalize_disabled(CONFIG_PATH)
        if disabled:
            print(f"PASS: Component 1 — {msg} (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — {msg}")
    except ET.ParseError as e:
        print(f"ERROR: Component 1 — Could not parse {CONFIG_PATH}: {e}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Document file exists and is a valid docx (0.4 points)
    # Guards: only awarded when Component 1 already passed, so initial_env
    # (where Component 1 fails) can never reach this branch and score 0.4.
    # This verifies the agent did not corrupt or delete the document.
    if total_score > 0.0:
        try:
            if os.path.exists(DOC_PATH):
                with open(DOC_PATH, 'rb') as f:
                    magic = f.read(4)
                # DOCX files are zip archives starting with PK magic bytes
                file_size = os.path.getsize(DOC_PATH)
                is_valid_docx = magic[:2] == b'PK'
                if is_valid_docx:
                    print(f"PASS: Component 2 — document {DOC_PATH} is intact "
                          f"(size: {file_size} bytes, valid zip/docx) (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 2 — {DOC_PATH} exists but is not a valid docx "
                          f"(bad magic bytes: {magic.hex()})")
            else:
                print(f"FAIL: Component 2 — document not found at {DOC_PATH}")
        except Exception as e:
            print(f"ERROR: Component 2 — {e}")
    else:
        print("SKIP: Component 2 (document integrity) — not evaluated because Component 1 failed")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

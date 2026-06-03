"""
Reward Script: Enable Word Completion and set min word length to 5
Task ID: writer_edit_044
Domain: libreoffice_writer
Scoring:
  Component 1: WordCompletion IsActive == true (0.6 points)
  Component 2: WordCompletion MinWordLen == 5 (0.4 points)
  Total: 1.0

Verification reads LibreOffice user configuration file
(/home/user/.config/libreoffice/4/user/registrymodifications.xcu)
and checks for the WordCompletion XML entries.
"""

import os
import xml.etree.ElementTree as ET

TASK_ID = 'writer_edit_044'
LO_CONFIG_PATH = '/home/user/.config/libreoffice/4/user/registrymodifications.xcu'
WORD_COMPLETION_PATH = '/org.openoffice.Office.Writer/AutoFunction/Text/WordCompletion'


def extract_word_completion_settings(config_path):
    """
    Parse the LibreOffice XCU registry file and extract
    WordCompletion settings.

    Returns: dict with 'IsActive' and 'MinWordLen' keys,
             or None if parsing fails.
    """
    tree = ET.parse(config_path)
    root = tree.getroot()

    oor_ns = 'http://openoffice.org/2001/registry'
    path_attr = f'{{{oor_ns}}}path'
    name_attr = f'{{{oor_ns}}}name'

    settings = {}

    for elem in root.iter():
        tag_local = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag

        if tag_local == 'item':
            item_path = elem.get(path_attr, '')
            if item_path == WORD_COMPLETION_PATH:
                for prop in elem.iter():
                    prop_local = prop.tag.split('}')[-1] if '}' in prop.tag else prop.tag
                    if prop_local == 'prop':
                        prop_name = prop.get(name_attr, '')
                        if prop_name in ('IsActive', 'MinWordLen'):
                            for val_elem in prop:
                                val_local = val_elem.tag.split('}')[-1] if '}' in val_elem.tag else val_elem.tag
                                if val_local == 'value':
                                    settings[prop_name] = val_elem.text

    return settings


def verify_task():
    """
    Verify that LibreOffice Word Completion has been enabled and the
    minimum word length has been set to 5 characters.

    Checks the LibreOffice user registry modifications file for:
      - IsActive == true  (Word Completion enabled)
      - MinWordLen == 5   (minimum word length is 5)

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: config file must exist
    if not os.path.exists(LO_CONFIG_PATH):
        print(f"CRITICAL: LibreOffice config file not found at {LO_CONFIG_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Parse the XCU registry file
    try:
        settings = extract_word_completion_settings(LO_CONFIG_PATH)
    except ET.ParseError as e:
        print(f"CRITICAL: Cannot parse config file {LO_CONFIG_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"CRITICAL: Unexpected error reading config: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Word Completion IsActive == true (0.6 points)
    # Verifies that 'Enable word completion' checkbox is checked.
    # This is absent or false in initial_env and 'true' in golden_env.
    try:
        is_active_raw = settings.get('IsActive')
        if is_active_raw is not None and is_active_raw.strip().lower() == 'true':
            print(f"PASS: Component 1 — Word Completion IsActive == true (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — Word Completion IsActive expected 'true', found: {is_active_raw!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Word Completion MinWordLen == 5 (0.4 points)
    # Verifies that 'Min. word length' is set to 5 characters.
    # This is absent in initial_env and explicitly 5 in golden_env.
    try:
        min_len_raw = settings.get('MinWordLen')
        if min_len_raw is not None:
            min_len = int(min_len_raw.strip())
            if min_len == 5:
                print(f"PASS: Component 2 — Word Completion MinWordLen == 5 (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — Word Completion MinWordLen expected 5, found {min_len}")
        else:
            print(f"FAIL: Component 2 — Word Completion MinWordLen setting not found in config")
    except ValueError:
        print(f"FAIL: Component 2 — MinWordLen value '{min_len_raw}' is not a valid integer")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: verify the LibreOffice config on the VM
if not os.path.exists(LO_CONFIG_PATH):
    print(f"Config file not found: {LO_CONFIG_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()

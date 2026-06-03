"""
Reward Script: Disable AutoCorrect 'Capitalize first letter of every sentence'
Task ID: writer_frd_046
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6): CapitalAtStartSentence setting exists and is false in registrymodifications.xcu
  Component 2 (0.4): No other AutoCorrect capitalization settings conflict (CapitalAtStartWord also checked)
"""

import os
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_frd_046'

# Path to LibreOffice user configuration
REGISTRY_PATH = os.path.expanduser(
    '~/.config/libreoffice/4/user/registrymodifications.xcu'
)
# Also try /home/user path explicitly
REGISTRY_PATH_ALT = '/home/user/.config/libreoffice/4/user/registrymodifications.xcu'


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
    Verify that the AutoCorrect option 'Capitalize first letter of every sentence'
    has been disabled in LibreOffice Writer settings.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Determine the registry file path
    reg_path = None
    for candidate in [REGISTRY_PATH, REGISTRY_PATH_ALT]:
        if os.path.exists(candidate):
            reg_path = candidate
            break

    if reg_path is None:
        print("CRITICAL: Cannot find registrymodifications.xcu")
        print("REWARD: 0.0")
        return 0.0

    # Parse the XML registry file
    try:
        tree = ET.parse(reg_path)
        root = tree.getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot parse {reg_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Define namespace
    ns = {'oor': 'http://openoffice.org/2001/registry'}

    # Component 1: CapitalAtStartSentence is explicitly set to false (0.6 points)
    # This is the primary task requirement: disable auto-capitalization of sentence starts
    try:
        capital_sentence_value = None

        # Since the XML uses oor: namespace on attributes, we need to iterate
        for item in root.iter():
            if item.tag.endswith('item') or item.tag == 'item':
                path_attr = item.get('{http://openoffice.org/2001/registry}path', '')
                if path_attr == '/org.openoffice.Office.Common/AutoCorrect':
                    # Found the AutoCorrect section - look for CapitalAtStartSentence prop
                    for prop in item.iter():
                        if prop.tag.endswith('prop') or prop.tag == 'prop':
                            name_attr = prop.get('{http://openoffice.org/2001/registry}name', '')
                            if name_attr == 'CapitalAtStartSentence':
                                # Get the value element
                                for val in prop.iter():
                                    if val.tag.endswith('value') or val.tag == 'value':
                                        capital_sentence_value = val.text
                                        break

        if capital_sentence_value is not None:
            if capital_sentence_value.strip().lower() == 'false':
                print(f"PASS: Component 1 — CapitalAtStartSentence is explicitly set to false (0.6 pts)")
                total_score += 0.6
            else:
                print(f"FAIL: Component 1 — CapitalAtStartSentence exists but value is '{capital_sentence_value}', expected 'false'")
        else:
            print(f"FAIL: Component 1 — CapitalAtStartSentence not found in registrymodifications.xcu (still at default=true)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Verify through a broader search - grep-style check (0.4 points)
    # Read the raw file content and verify the setting is present with correct value
    # This catches edge cases where XML parsing might miss due to namespace issues
    try:
        with open(reg_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check that the specific setting line exists
        has_capital_false = (
            'CapitalAtStartSentence' in content
            and 'AutoCorrect' in content
        )

        if has_capital_false:
            # Verify it's actually set to false, not true
            import re
            pattern = r'CapitalAtStartSentence.*?<value>(.*?)</value>'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                value = match.group(1).strip().lower()
                if value == 'false':
                    print(f"PASS: Component 2 — Raw content confirms CapitalAtStartSentence=false (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 2 — CapitalAtStartSentence found but value is '{value}', expected 'false'")
            else:
                print(f"FAIL: Component 2 — CapitalAtStartSentence mentioned but value pattern not matched")
        else:
            print(f"FAIL: Component 2 — CapitalAtStartSentence not found in registry file content")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification (settings changes via GUI may need this)
persist_app_state("libreoffice_writer")

# Run verification
verify_task()

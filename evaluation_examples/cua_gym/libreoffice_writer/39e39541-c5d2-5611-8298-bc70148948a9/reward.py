"""
Reward Script: Set default language for spell checking to English (US)
Task ID: writer_legal_078
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Normal style language set to en-US
  Component 2 (0.3): docDefaults language set to en-US
  Component 3 (0.3): DefaultParagraphFont style language set to en-US
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_078'

WML_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WML_NS}


def get_lang_val(element, ns=NS):
    """Extract w:lang w:val from an rPr element."""
    if element is None:
        return None
    lang = element.find('w:lang', ns)
    if lang is None:
        return None
    return lang.get(f'{{{WML_NS}}}val')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with zipfile.ZipFile(file_path) as z:
            if 'word/styles.xml' not in z.namelist():
                print("CRITICAL: No word/styles.xml found in docx")
                print("REWARD: 0.0")
                return 0.0
            styles_xml = z.read('word/styles.xml')
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        root = ET.fromstring(styles_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot parse styles.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Normal style language set to en-US (0.4 points)
    # In initial_env this is 'zxx'; in golden_env it should be 'en-US'
    try:
        normal_lang = None
        for style in root.findall('.//w:style', NS):
            style_id = style.get(f'{{{WML_NS}}}styleId')
            if style_id == 'Normal':
                rpr = style.find('w:rPr', NS)
                normal_lang = get_lang_val(rpr)
                break

        if normal_lang is not None and normal_lang.lower() == 'en-us':
            print(f"PASS: Component 1 -- Normal style lang is '{normal_lang}' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- Normal style lang is '{normal_lang}', expected 'en-US'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: docDefaults language set to en-US (0.3 points)
    # In initial_env this is 'zxx'; in golden_env it should be 'en-US'
    try:
        doc_defaults = root.find('.//w:docDefaults', NS)
        rpr_default = None
        if doc_defaults is not None:
            rpr_default = doc_defaults.find('.//w:rPrDefault/w:rPr', NS)
        defaults_lang = get_lang_val(rpr_default)

        if defaults_lang is not None and defaults_lang.lower() == 'en-us':
            print(f"PASS: Component 2 -- docDefaults lang is '{defaults_lang}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- docDefaults lang is '{defaults_lang}', expected 'en-US'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: DefaultParagraphFont style language set to en-US (0.3 points)
    # In initial_env this style may not have a lang element or it is 'zxx';
    # in golden_env it should be 'en-US'
    try:
        dpf_lang = None
        for style in root.findall('.//w:style', NS):
            style_id = style.get(f'{{{WML_NS}}}styleId')
            if style_id == 'DefaultParagraphFont':
                rpr = style.find('w:rPr', NS)
                dpf_lang = get_lang_val(rpr)
                break

        if dpf_lang is not None and dpf_lang.lower() == 'en-us':
            print(f"PASS: Component 3 -- DefaultParagraphFont lang is '{dpf_lang}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 -- DefaultParagraphFont lang is '{dpf_lang}', expected 'en-US'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved GUI state before verification
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

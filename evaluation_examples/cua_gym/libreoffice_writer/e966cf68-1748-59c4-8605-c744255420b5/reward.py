"""
Reward Script: Insert footnote on first mention of 'REST API'
Task ID: writer_tech_014
Domain: libreoffice_writer
Scoring:
  Component 1: Footnote reference exists in document body (0.3 pts)
  Component 2: Footnote reference is in paragraph containing 'REST API' (0.3 pts)
  Component 3: Footnote text contains the correct expansion (0.4 pts)
"""

import os
import zipfile
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_014'

EXPECTED_FOOTNOTE_TEXT = 'Representational State Transfer Application Programming Interface'

WML_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WML_NS}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid docx (zip)
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open docx as zip: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ---- Parse document.xml for footnote references in body ----
    try:
        doc_xml = zf.read('word/document.xml')
        doc_root = etree.fromstring(doc_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot parse document.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    body = doc_root.find(f'{{{WML_NS}}}body')
    if body is None:
        print("CRITICAL: No body element in document.xml")
        print("REWARD: 0.0")
        return 0.0

    # Find all footnote references in the body
    footnote_refs = body.findall(f'.//{{{WML_NS}}}footnoteReference')

    # Component 1: At least one footnote reference exists in body (0.3 pts)
    # This FAILS on initial (no footnotes) and PASSES on golden (has footnote)
    try:
        if len(footnote_refs) > 0:
            print(f"PASS: Component 1 -- Footnote reference(s) found in body: {len(footnote_refs)} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 -- No footnote references found in document body")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Footnote reference is in a paragraph containing 'REST API' (0.3 pts)
    # This verifies the footnote is placed at the correct location (near first 'REST API' mention)
    try:
        # Iterate paragraphs in body to find one with both 'REST API' text and a footnoteReference
        paragraphs = body.findall(f'.//{{{WML_NS}}}p')
        matching_paras = [
            p for p in paragraphs
            if 'REST API' in ''.join((t.text or '') for t in p.findall(f'.//{{{WML_NS}}}t'))
            and len(p.findall(f'.//{{{WML_NS}}}footnoteReference')) > 0
        ]

        if len(matching_paras) > 0:
            print(f"PASS: Component 2 -- Footnote reference is in paragraph containing 'REST API' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- No footnote reference found in a paragraph containing 'REST API'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Footnote text matches expected expansion (0.4 pts)
    # Parse word/footnotes.xml and check the text of the user-added footnote
    try:
        if 'word/footnotes.xml' not in zf.namelist():
            print(f"FAIL: Component 3 -- word/footnotes.xml not found in docx archive")
        else:
            fn_xml = zf.read('word/footnotes.xml')
            fn_root = etree.fromstring(fn_xml)
            footnotes = fn_root.findall(f'{{{WML_NS}}}footnote')

            # Filter to "normal" footnotes (skip separator/continuationSeparator which have id -1, 0)
            normal_footnotes = []
            for fn in footnotes:
                fn_type = fn.get(f'{{{WML_NS}}}type')
                if fn_type is None:  # normal footnotes have no type attribute, or type="normal"
                    normal_footnotes.append(fn)
                elif fn_type == 'normal':
                    normal_footnotes.append(fn)

            if len(normal_footnotes) == 0:
                print(f"FAIL: Component 3 -- No normal footnotes found in footnotes.xml")
            else:
                # Check if any normal footnote contains the expected text
                expected_normalized = ' '.join(EXPECTED_FOOTNOTE_TEXT.split()).lower()
                matching_fns = [
                    fn for fn in normal_footnotes
                    if expected_normalized in ' '.join(
                        ''.join((t.text or '') for t in fn.findall(f'.//{{{WML_NS}}}t')).split()
                    ).lower()
                ]

                if len(matching_fns) > 0:
                    fn_text = ''.join((t.text or '') for t in matching_fns[0].findall(f'.//{{{WML_NS}}}t')).strip()
                    print(f"PASS: Component 3 -- Footnote text matches: '{fn_text}' (0.4 pts)")
                    total_score += 0.4
                else:
                    # Show what we found for debugging
                    for fn in normal_footnotes:
                        text_elements = fn.findall(f'.//{{{WML_NS}}}t')
                        fn_text = ''.join(t.text or '' for t in text_elements).strip()
                        print(f"FAIL: Component 3 -- Expected footnote containing '{EXPECTED_FOOTNOTE_TEXT}', found: '{fn_text}'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    zf.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice edits before verification
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

"""
Reward Script: Show tracked changes in "Final" view mode without accepting them
Task ID: writer_rm_022
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): revisionView element exists with markup="0" in settings.xml
  Component 2 (0.3): revisionView markup="0" AND tracked changes still preserved (>=20 ins+del)
  Component 3 (0.2): revisionView markup="0" AND trackRevisions element still present
"""

import os
import zipfile
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_022'
WML_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WML_NS}


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice changes before verification."""
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
        z = zipfile.ZipFile(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open file as zip: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: settings.xml must exist
    if 'word/settings.xml' not in z.namelist():
        print("CRITICAL: word/settings.xml not found in docx")
        print("REWARD: 0.0")
        return 0.0

    try:
        settings_xml = z.read('word/settings.xml')
        settings_root = etree.fromstring(settings_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot parse settings.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse document.xml for tracked change counts
    doc_xml_data = None
    doc_root = None
    try:
        doc_xml_data = z.read('word/document.xml')
        doc_root = etree.fromstring(doc_xml_data)
    except Exception as e:
        print(f"WARNING: Cannot parse document.xml: {e}")

    # Find revisionView element
    revision_views = settings_root.findall(f'.//{{{WML_NS}}}revisionView')
    has_revision_view = len(revision_views) > 0
    markup_val = None
    if has_revision_view:
        markup_val = revision_views[0].get(f'{{{WML_NS}}}markup')

    # Component 1: revisionView element exists with markup="0" (0.5 points)
    # This is the core check: "Show Final" mode sets revisionView markup="0"
    try:
        if has_revision_view and markup_val == '0':
            print(f"PASS: Component 1 - revisionView exists with markup='0' (0.5 pts)")
            total_score += 0.5
        else:
            if not has_revision_view:
                print(f"FAIL: Component 1 - No revisionView element found in settings.xml")
            else:
                print(f"FAIL: Component 1 - revisionView markup='{markup_val}', expected '0'")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: revisionView markup="0" AND tracked changes still preserved (0.3 points)
    # Ensures the changes were NOT accepted (task says "without actually accepting them")
    try:
        if has_revision_view and markup_val == '0' and doc_root is not None:
            ins_count = len(doc_root.findall(f'.//{{{WML_NS}}}ins'))
            del_count = len(doc_root.findall(f'.//{{{WML_NS}}}del'))
            total_changes = ins_count + del_count
            if total_changes >= 20:
                print(f"PASS: Component 2 - markup='0' AND {total_changes} tracked changes preserved (ins={ins_count}, del={del_count}) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 - Only {total_changes} tracked changes remain (expected >=20). Changes may have been accepted instead of just hidden.")
        else:
            if not (has_revision_view and markup_val == '0'):
                print(f"FAIL: Component 2 - revisionView check failed (prerequisite for this component)")
            else:
                print(f"FAIL: Component 2 - Could not parse document.xml to count tracked changes")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: revisionView markup="0" AND trackRevisions still enabled (0.2 points)
    # Ensures track changes feature wasn't disabled
    try:
        if has_revision_view and markup_val == '0':
            track_revisions = settings_root.findall(f'.//{{{WML_NS}}}trackRevisions')
            if len(track_revisions) > 0:
                # Check that it's not explicitly set to false via w:val="false" or w:val="0"
                val_attr = track_revisions[0].get(f'{{{WML_NS}}}val')
                if val_attr in ('false', '0'):
                    print(f"FAIL: Component 3 - trackRevisions is explicitly disabled (val='{val_attr}')")
                else:
                    print(f"PASS: Component 3 - markup='0' AND trackRevisions is present/enabled (0.2 pts)")
                    total_score += 0.2
            else:
                print(f"FAIL: Component 3 - trackRevisions element not found in settings.xml")
        else:
            print(f"FAIL: Component 3 - revisionView check failed (prerequisite for this component)")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    z.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist unsaved state before verification
persist_app_state("libreoffice_writer")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

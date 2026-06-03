"""
Reward Script: Hide tracked changes display in Writer document
Task ID: writer_rm_010
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6): revisionView markup attribute set to '0' (Show Changes off)
  Component 2 (0.4): Tracked changes still exist internally (not accepted/rejected)
"""

import os
import zipfile
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_010'

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


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
        print(f"CRITICAL: Cannot open docx as zip: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: revisionView markup='0' — Show Changes is disabled (0.6 points)
    try:
        if 'word/settings.xml' not in z.namelist():
            print("FAIL: Component 1 — word/settings.xml not found in docx")
        else:
            settings_xml = z.read('word/settings.xml')
            root = etree.fromstring(settings_xml)

            # Find the revisionView element
            rev_view = root.find(f'.//{{{W_NS}}}revisionView')
            if rev_view is None:
                # If revisionView element is absent, LibreOffice treats it as
                # "show all" by default, so absence means markup is ON (initial state).
                print("FAIL: Component 1 — revisionView element not found (defaults to markup visible)")
            else:
                markup_val = rev_view.get(f'{{{W_NS}}}markup')
                if markup_val == '0':
                    print(f"PASS: Component 1 — revisionView markup='0' (Show Changes disabled) (0.6 pts)")
                    total_score += 0.6
                else:
                    print(f"FAIL: Component 1 — revisionView markup='{markup_val}', expected '0'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Tracked changes still exist internally (0.4 points)
    # The task says to hide changes, NOT accept/reject them.
    # So the document must still contain <w:ins> and/or <w:del> elements.
    try:
        if 'word/document.xml' not in z.namelist():
            print("FAIL: Component 2 — word/document.xml not found")
        else:
            doc_xml = z.read('word/document.xml')
            doc_root = etree.fromstring(doc_xml)

            ins_elements = doc_root.findall(f'.//{{{W_NS}}}ins')
            del_elements = doc_root.findall(f'.//{{{W_NS}}}del')
            total_changes = len(ins_elements) + len(del_elements)

            if total_changes >= 6:
                # Only award points if Component 1 passed (markup is hidden)
                # This ensures initial_env scores 0 since markup='1' there
                if total_score >= 0.5:
                    print(f"PASS: Component 2 — {total_changes} tracked changes preserved internally ({len(ins_elements)} ins, {len(del_elements)} del) (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 2 — tracked changes exist ({total_changes}) but markup is still visible (Component 1 failed)")
            else:
                print(f"FAIL: Component 2 — expected >=6 tracked changes, found {total_changes} (changes may have been accepted/rejected)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    z.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

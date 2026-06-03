"""
Reward Script: Accept all tracked changes and enable track changes
Task ID: writer_rm_088
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6): All tracked changes accepted (no revision marks remain)
  Component 2 (0.4): Track changes recording is enabled in document settings
"""

import os
import zipfile
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_088'

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W_NS}


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
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

    # Precondition: file must be loadable as a valid docx (zip with word/document.xml)
    try:
        zf = zipfile.ZipFile(file_path)
        doc_xml = zf.read('word/document.xml')
        doc_tree = etree.fromstring(doc_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All tracked changes accepted — no revision marks remain (0.6 points)
    # Check for w:ins, w:del, w:rPrChange, w:pPrChange, w:sectPrChange,
    # w:tblPrChange, w:trPrChange, w:tcPrChange elements in the document body.
    # In the initial state there are 30 tracked changes; after accepting all, there should be 0.
    try:
        ins_count = len(doc_tree.findall('.//' + f'{{{W_NS}}}ins'))
        del_count = len(doc_tree.findall('.//' + f'{{{W_NS}}}del'))
        rpr_count = len(doc_tree.findall('.//' + f'{{{W_NS}}}rPrChange'))
        ppr_count = len(doc_tree.findall('.//' + f'{{{W_NS}}}pPrChange'))
        sec_count = len(doc_tree.findall('.//' + f'{{{W_NS}}}sectPrChange'))
        tbl_count = len(doc_tree.findall('.//' + f'{{{W_NS}}}tblPrChange'))
        tr_count = len(doc_tree.findall('.//' + f'{{{W_NS}}}trPrChange'))
        tc_count = len(doc_tree.findall('.//' + f'{{{W_NS}}}tcPrChange'))
        total_revisions = (ins_count + del_count + rpr_count + ppr_count +
                           sec_count + tbl_count + tr_count + tc_count)

        if total_revisions == 0:
            print(f"PASS: Component 1 — No tracked changes remain (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — {total_revisions} tracked changes still present "
                  f"(ins={ins_count}, del={del_count}, rPr={rpr_count}, pPr={ppr_count})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Track changes recording is enabled (0.4 points)
    # The w:trackChanges element must be present in word/settings.xml.
    # In the initial state, this element is absent (recording OFF).
    # In the golden state, it should be present (recording ON).
    try:
        if 'word/settings.xml' in zf.namelist():
            settings_xml = zf.read('word/settings.xml')
            settings_tree = etree.fromstring(settings_xml)
            track_changes_elems = settings_tree.findall('.//' + f'{{{W_NS}}}trackChanges')
            if len(track_changes_elems) > 0:
                print(f"PASS: Component 2 — trackChanges element found in settings.xml (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — trackChanges element NOT found in settings.xml")
        else:
            print(f"FAIL: Component 2 — word/settings.xml not found in docx archive")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    zf.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Insert a bookmark named 'troubleshooting' at the beginning of the Troubleshooting section heading.
Task ID: writer_tech_018
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Bookmark named 'troubleshooting' exists in the document
  Component 2 (0.3): Bookmark is inside the Troubleshooting heading paragraph (Heading 1)
  Component 3 (0.3): Bookmark is positioned at the beginning of the paragraph (before text runs)
"""

import os
from docx import Document
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_018'
WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WNS}


def persist_app_state(domain: str):
    """Attempt to save any unsaved changes in LibreOffice."""
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

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    body = doc.element.body

    # Component 1: Bookmark named 'troubleshooting' exists in document (0.4 points)
    try:
        all_bookmarks = body.findall('.//w:bookmarkStart', NS)
        bookmark_names = []
        for bm in all_bookmarks:
            name = bm.get(f'{{{WNS}}}name')
            if name:
                bookmark_names.append(name)

        if 'troubleshooting' in bookmark_names:
            print(f"PASS: Component 1 — Bookmark 'troubleshooting' exists in document (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Bookmark 'troubleshooting' not found. Found bookmarks: {bookmark_names}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Bookmark is inside the Troubleshooting heading paragraph (0.3 points)
    try:
        troubleshooting_para = None
        for para in doc.paragraphs:
            if 'Troubleshooting' in para.text and para.style.name == 'Heading 1':
                troubleshooting_para = para
                break

        if troubleshooting_para is None:
            print(f"FAIL: Component 2 — No 'Troubleshooting' heading (Heading 1) found in document")
        else:
            para_bookmarks = troubleshooting_para._element.findall('.//w:bookmarkStart', NS)
            para_bm_names = [bm.get(f'{{{WNS}}}name') for bm in para_bookmarks]

            if 'troubleshooting' in para_bm_names:
                print(f"PASS: Component 2 — Bookmark 'troubleshooting' is inside the Troubleshooting heading paragraph (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Bookmark 'troubleshooting' not in Troubleshooting heading. Para bookmarks: {para_bm_names}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Bookmark is at the beginning of the paragraph (before first run) (0.3 points)
    try:
        if troubleshooting_para is not None:
            children = list(troubleshooting_para._element)
            # Find the index of bookmarkStart named 'troubleshooting'
            bm_index = None
            first_run_index = None
            for ci, child in enumerate(children):
                tag = etree.QName(child).localname
                if tag == 'bookmarkStart':
                    name = child.get(f'{{{WNS}}}name')
                    if name == 'troubleshooting' and bm_index is None:
                        bm_index = ci
                if tag == 'r' and first_run_index is None:
                    first_run_index = ci

            if bm_index is not None and first_run_index is not None and bm_index < first_run_index:
                print(f"PASS: Component 3 — Bookmark is at beginning of paragraph (index {bm_index} before first run at {first_run_index}) (0.3 pts)")
                total_score += 0.3
            elif bm_index is not None and first_run_index is None:
                # No runs but bookmark exists - still at beginning
                print(f"PASS: Component 3 — Bookmark is in paragraph with no runs (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Bookmark not at beginning. bm_index={bm_index}, first_run_index={first_run_index}")
        else:
            print(f"FAIL: Component 3 — Cannot check position, Troubleshooting heading not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

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

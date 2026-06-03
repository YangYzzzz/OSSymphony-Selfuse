"""
Reward Script: Reject all tracked changes and remove all comments from a contract document.
Task ID: osworld_writer_comment_track_changes_003
Domain: libreoffice_writer

Scoring Rubric:
  Component 1: All tracked changes rejected (0 w:ins and 0 w:del elements) — 0.5 pts
  Component 2: All comments removed (comments part absent or empty)         — 0.5 pts
  Total: 1.0

Context: Document started with 5 tracked changes (3 insertions, 2 deletions) and 3 comments.
Rejecting tracked changes reverts the document to its original text (without insertions accepted).
Removing all comments clears the comments part entirely.
"""

import os
import re
from docx import Document
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_comment_track_changes_003'


def persist_app_state():
    """Send Ctrl+S to ensure any open LibreOffice instance saves the document."""
    try:
        import time
        os.environ["DISPLAY"] = ":0"
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that all tracked changes have been rejected and all comments removed.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document — failure is a hard gate
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Namespace constant
    W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

    # Component 1: All tracked changes rejected (0.5 points)
    # A rejected change means all w:ins and w:del elements are absent from the document body.
    # Initial state: 3 w:ins elements + 2 w:del elements (5 total).
    # Golden state:  0 w:ins elements and 0 w:del elements.
    try:
        body = doc.element.body
        ins_elements = body.findall('.//{%s}ins' % W_NS)
        del_elements = body.findall('.//{%s}del' % W_NS)
        ins_count = len(ins_elements)
        del_count = len(del_elements)

        if ins_count == 0 and del_count == 0:
            print(f"PASS: Component 1 — No tracked changes found (ins={ins_count}, del={del_count}). All 5 changes rejected. (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Expected 0 tracked changes, found ins={ins_count}, del={del_count}.")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check tracked changes: {e}")

    # Component 2: All comments removed (0.5 points)
    # Initial state: 3 comments in the comments part.
    # Golden state:  no comments part, or comments part with 0 comment elements.
    try:
        part = doc.part
        comments_part = None
        for rel in part.rels.values():
            if 'comments' in rel.reltype.lower():
                comments_part = rel.target_part
                break

        if comments_part is None:
            # No comments relationship — all comments fully removed
            print("PASS: Component 2 — No comments part found. All 3 comments removed. (0.5 pts)")
            total_score += 0.5
        else:
            # Comments part exists — count remaining comment elements
            root = etree.fromstring(comments_part.blob)
            comments = root.findall('{%s}comment' % W_NS)
            if len(comments) == 0:
                print("PASS: Component 2 — Comments part present but empty (0 comments). All 3 comments removed. (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 2 — Expected 0 comments, found {len(comments)} comment(s) still in document.")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check comments: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point — run on the VM with the canonical file path
file_path = f'{WORKDIR}/{TASK_ID}.docx'

persist_app_state()

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

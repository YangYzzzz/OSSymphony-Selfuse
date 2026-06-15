"""
Reward Script: Compare document with saved version to show tracked changes
Task ID: writer_lec_074
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Tracked changes element exists with changed regions
  Component 2 (0.3): Both insertions and deletions are present
  Component 3 (0.3): Multiple change regions (>=4) indicating real comparison
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_074'

# Namespace map for ODF XML
NS = {
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'dc': 'http://purl.org/dc/elements/1.1/',
}


def persist_app_state(domain: str):
    """Save any unsaved changes in LibreOffice Writer before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that tracked changes (from version comparison) are present in the document.
    The task requires the user to compare the current document with a saved version
    via File > Versions > Compare, which inserts tracked changes (insertions/deletions)
    into the document content.xml.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load and parse the ODT content.xml
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            content_xml = z.read('content.xml').decode('utf-8')
        root = ET.fromstring(content_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot load or parse {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Tracked changes element exists with changed regions (0.4 points)
    # The version comparison operation creates a <text:tracked-changes> element
    # containing <text:changed-region> entries. The initial file has NONE of these.
    try:
        tracked_changes = root.findall('.//text:tracked-changes', NS)
        changed_regions = root.findall('.//text:changed-region', NS)
        num_regions = len(changed_regions)

        if len(tracked_changes) > 0 and num_regions > 0:
            print(f"PASS: Component 1 — tracked-changes present with {num_regions} changed regions (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — tracked-changes elements: {len(tracked_changes)}, changed regions: {num_regions}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Both insertions and deletions are present (0.3 points)
    # A real version comparison produces BOTH insertion and deletion markers,
    # reflecting text that was added and text that was removed since the saved version.
    try:
        insertions = root.findall('.//text:insertion', NS)
        deletions = root.findall('.//text:deletion', NS)
        num_ins = len(insertions)
        num_del = len(deletions)

        if num_ins > 0 and num_del > 0:
            print(f"PASS: Component 2 — {num_ins} insertions and {num_del} deletions found (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — insertions: {num_ins}, deletions: {num_del} (need both > 0)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Multiple change regions (>=4) indicating real comparison (0.3 points)
    # A genuine version comparison of a document with "several paragraphs modified"
    # should produce multiple tracked change regions, not just 1-2.
    try:
        # Re-use the count from Component 1
        if num_regions >= 4:
            print(f"PASS: Component 3 — {num_regions} change regions (>= 4 threshold) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — only {num_regions} change regions (need >= 4)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.odt'

# Persist app state before verification (document may have unsaved changes)
persist_app_state("libreoffice_writer")

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

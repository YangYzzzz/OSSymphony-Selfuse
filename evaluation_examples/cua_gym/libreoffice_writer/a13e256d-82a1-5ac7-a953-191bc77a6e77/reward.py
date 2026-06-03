"""
Reward Script: Continue numbering of second list from first list
Task ID: writer_lec_006
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6): Second list items share same numId as first list items
  Component 2 (0.4): Only one unique numId across all numbered list paragraphs
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_006'


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice edits before verification."""
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

    The task asks: make the second numbered list continue numbering from the first.
    Initial state: two separate numbering sequences (different numId values).
    Golden state: both lists share the same numId, so the second continues from the first.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
    except ImportError:
        print("CRITICAL: python-docx not available")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

    # Identify the two list groups by their position relative to headings/normal text.
    # Structure: heading, normal, heading, list1 (5 items), normal, heading, list2 (3 items), normal
    # We find the "Supplementary Tasks" heading and split lists before/after it.

    paragraphs = doc.paragraphs
    first_list_numids = []
    second_list_numids = []
    found_supplementary = False

    for para in paragraphs:
        # Detect the divider heading
        if 'Supplementary Tasks' in para.text:
            found_supplementary = True
            continue

        # Check if paragraph has numbering
        numPr = para._element.find('.//w:numPr', ns)
        if numPr is not None:
            numId_elem = numPr.find('w:numId', ns)
            if numId_elem is not None:
                numId_val = numId_elem.get(f'{{{W_NS}}}val')
                if numId_val and numId_val != '0':
                    if not found_supplementary:
                        first_list_numids.append(numId_val)
                    else:
                        second_list_numids.append(numId_val)

    print(f"INFO: First list numIds: {first_list_numids}")
    print(f"INFO: Second list numIds: {second_list_numids}")

    # Precondition: both lists must exist
    if not first_list_numids:
        print("FAIL: No first list found in document")
        print("REWARD: 0.0")
        return 0.0

    if not second_list_numids:
        print("FAIL: No second list found after 'Supplementary Tasks' heading")
        print("REWARD: 0.0")
        return 0.0

    first_list_numid = first_list_numids[0]  # The numId used by the first list

    # Component 1: Second list items share the same numId as first list items (0.6 points)
    # In the initial state, the second list uses a DIFFERENT numId (e.g., 21 vs 20).
    # In the golden state, the second list uses the SAME numId as the first (e.g., 20).
    try:
        second_uses_first_numid = all(nid == first_list_numid for nid in second_list_numids)
        if second_uses_first_numid:
            print(f"PASS: Component 1 — All second list items use numId={first_list_numid}, matching first list (0.6 pts)")
            total_score += 0.6
        else:
            mismatched = [nid for nid in second_list_numids if nid != first_list_numid]
            print(f"FAIL: Component 1 — Second list items have numId(s) {set(mismatched)}, expected {first_list_numid}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Only one unique numId across ALL numbered paragraphs (0.4 points)
    # In the initial state, there are two unique numIds (two separate sequences).
    # In the golden state, there is only one unique numId (one continuous sequence).
    try:
        all_numids = set(first_list_numids + second_list_numids)
        if len(all_numids) == 1:
            print(f"PASS: Component 2 — Single numId {all_numids.pop()} across all list items (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — Multiple numIds found: {all_numids} (expected 1 unique numId)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification
persist_app_state("libreoffice_writer")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Accept the first tracked change in a LibreOffice Writer document
Task ID: writer_rm_019
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): First tracked change accepted — 'select' is normal text, 'click' deletion removed in para 3
  Component 2 (0.3): Total tracked changes reduced from 7 to 6 (both inserts and deletes)
  Component 3 (0.2): Remaining 6 tracked changes are intact
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_019'


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
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
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    body = doc.element.body

    # Gather all tracked inserts and deletes across the document
    all_inserts = body.findall('.//w:ins', ns)
    all_deletes = body.findall('.//w:del', ns)
    num_inserts = len(all_inserts)
    num_deletes = len(all_deletes)

    print(f"INFO: Found {num_inserts} tracked inserts, {num_deletes} tracked deletes")

    # Component 1: First tracked change accepted (0.5 points)
    # In paragraph 3 (0-indexed), the insert 'select' should now be normal text
    # (not inside <w:ins>), and the delete 'click' should be gone (no <w:del>).
    try:
        para3 = doc.paragraphs[3]
        para3_el = para3._element

        # Check for remaining tracked inserts with 'select' in paragraph 3
        para3_inserts = para3_el.findall('.//w:ins', ns)
        select_still_tracked = False
        for ins in para3_inserts:
            ins_texts = ins.findall('.//w:r/w:t', ns)
            ins_text = ''.join(t.text or '' for t in ins_texts)
            if 'select' in ins_text.lower():
                select_still_tracked = True
                break

        # Check for remaining tracked deletes with 'click' in paragraph 3
        para3_deletes = para3_el.findall('.//w:del', ns)
        click_still_tracked = False
        for dl in para3_deletes:
            del_texts = dl.findall('.//w:r/w:delText', ns)
            del_text = ''.join(t.text or '' for t in del_texts)
            if 'click' in del_text.lower():
                click_still_tracked = True
                break

        # 'select' should appear in the paragraph text as normal text
        select_in_text = 'select' in para3.text.lower()

        if not select_still_tracked and not click_still_tracked and select_in_text:
            print(f"PASS: Component 1 — First tracked change accepted: 'select' is normal text, 'click' deletion removed (0.5 pts)")
            total_score += 0.5
        else:
            reasons = []
            if select_still_tracked:
                reasons.append("'select' still inside <w:ins>")
            if click_still_tracked:
                reasons.append("'click' still inside <w:del>")
            if not select_in_text:
                reasons.append("'select' not found in paragraph text")
            print(f"FAIL: Component 1 — {'; '.join(reasons)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Total tracked changes reduced to 6 each (0.3 points)
    # Initial has 7 inserts + 7 deletes. After accepting one change, should be 6 + 6.
    try:
        if num_inserts == 6 and num_deletes == 6:
            print(f"PASS: Component 2 — Tracked changes reduced to 6 inserts + 6 deletes (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected 6 inserts + 6 deletes, found {num_inserts} inserts + {num_deletes} deletes")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Remaining 6 tracked changes intact AND first change is gone (0.2 points)
    # This is a compound check: the 6 other changes must still be tracked, AND the
    # first change ('select'/'click') must NOT be tracked anymore.
    # This ensures the component only passes on golden (where the first was accepted)
    # and fails on initial (where all 7 are still tracked).
    try:
        expected_inserts = {'comprehensive', 'actionable', 'concurrently', 'robust', 'direct', 'detailed'}
        expected_deletes = {'consolidated', 'manageable', 'simultaneously', 'powerful', 'programmatic', 'granular'}

        found_inserts = set()
        first_change_insert_present = False
        for ins in all_inserts:
            ins_texts = ins.findall('.//w:r/w:t', ns)
            ins_text = ''.join(t.text or '' for t in ins_texts).strip().lower()
            if ins_text in expected_inserts:
                found_inserts.add(ins_text)
            if ins_text == 'select':
                first_change_insert_present = True

        found_deletes = set()
        first_change_delete_present = False
        for dl in all_deletes:
            del_texts = dl.findall('.//w:r/w:delText', ns)
            del_text = ''.join(t.text or '' for t in del_texts).strip().lower()
            if del_text in expected_deletes:
                found_deletes.add(del_text)
            if del_text == 'click':
                first_change_delete_present = True

        missing_inserts = expected_inserts - found_inserts
        missing_deletes = expected_deletes - found_deletes

        # Must have all 6 remaining AND the first change must be gone
        if not missing_inserts and not missing_deletes and not first_change_insert_present and not first_change_delete_present:
            print(f"PASS: Component 3 — All 6 remaining tracked changes intact, first change accepted (0.2 pts)")
            total_score += 0.2
        else:
            details = []
            if missing_inserts:
                details.append(f"missing inserts: {missing_inserts}")
            if missing_deletes:
                details.append(f"missing deletes: {missing_deletes}")
            if first_change_insert_present:
                details.append("'select' insert still tracked (first change not yet accepted)")
            if first_change_delete_present:
                details.append("'click' delete still tracked (first change not yet accepted)")
            print(f"FAIL: Component 3 — {'; '.join(details)}")
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

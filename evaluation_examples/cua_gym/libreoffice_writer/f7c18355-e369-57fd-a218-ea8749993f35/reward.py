"""
Reward Script: Merge review changes from two reviewers into base document
Task ID: writer_rm_046
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.25): Report_Base.docx contains tracked changes from Reviewer A
  - Component 2 (0.25): Report_Base.docx contains tracked changes from Reviewer B
  - Component 3 (0.25): Reviewer A has substantial tracked changes (>=10 revision elements)
  - Component 4 (0.25): Reviewer B has substantial tracked changes (>=4 revision elements)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_046'


def persist_app_state(domain):
    """Save any open LibreOffice documents before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_writer", "libreoffice_calc", "libreoffice_impress"}:
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

    We verify that Report_Base.docx now contains tracked changes (revisions)
    from both Reviewer A and Reviewer B, indicating that merges were performed.

    The initial state has 0 tracked changes in Report_Base.docx.
    The golden state has tracked changes from both reviewers merged in.
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

    # Collect all revision elements
    ins_elements = body.findall('.//w:ins', ns)
    del_elements = body.findall('.//w:del', ns)
    rpr_change = body.findall('.//w:rPrChange', ns)
    ppr_change = body.findall('.//w:pPrChange', ns)

    all_revisions = ins_elements + del_elements + rpr_change + ppr_change

    # Count revisions per author
    from collections import Counter
    author_counts = Counter()
    for el in all_revisions:
        author = el.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}author')
        if author:
            author_counts[author] += 1

    total_revisions = sum(author_counts.values())
    reviewer_a_count = author_counts.get('Reviewer A', 0)
    reviewer_b_count = author_counts.get('Reviewer B', 0)

    print(f"INFO: Total revision elements in Report_Base.docx: {total_revisions}")
    print(f"INFO: Reviewer A revisions: {reviewer_a_count}")
    print(f"INFO: Reviewer B revisions: {reviewer_b_count}")
    print(f"INFO: All authors: {dict(author_counts)}")

    # Component 1: Reviewer A has at least 1 tracked change in Report_Base (0.25 points)
    # Initial state: Report_Base has 0 tracked changes, so this fails on initial
    try:
        if reviewer_a_count > 0:
            print(f"PASS: Component 1 - Reviewer A has {reviewer_a_count} revision elements in Report_Base (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 - No tracked changes from Reviewer A found in Report_Base")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Reviewer B has at least 1 tracked change in Report_Base (0.25 points)
    # Initial state: Report_Base has 0 tracked changes, so this fails on initial
    try:
        if reviewer_b_count > 0:
            print(f"PASS: Component 2 - Reviewer B has {reviewer_b_count} revision elements in Report_Base (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 - No tracked changes from Reviewer B found in Report_Base")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Reviewer A has substantial changes (>=10 revision elements) (0.25 points)
    # ReviewA.docx has 16 revision elements; we expect most/all to be merged
    try:
        if reviewer_a_count >= 10:
            print(f"PASS: Component 3 - Reviewer A has {reviewer_a_count} revision elements (>=10 expected) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 - Reviewer A has only {reviewer_a_count} revision elements (expected >=10)")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Reviewer B has substantial changes (>=4 revision elements) (0.25 points)
    # ReviewB.docx has 6 revision elements; we expect most/all to be merged
    try:
        if reviewer_b_count >= 4:
            print(f"PASS: Component 4 - Reviewer B has {reviewer_b_count} revision elements (>=4 expected) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 - Reviewer B has only {reviewer_b_count} revision elements (expected >=4)")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/Report_Base.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

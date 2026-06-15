"""
Reward Script: Accept all tracked changes in the document to finalize the text.
Task ID: writer_struct_015
Domain: libreoffice_writer
Scoring:
  Component 1: No tracked insertions (w:ins elements) in document XML  — 0.40 pts
  Component 2: No tracked deletions (w:del elements) in document XML   — 0.30 pts
  Component 3: Inserted text is present in final document content       — 0.30 pts
Total: 1.0
"""

import os

# python-docx is required; install via: pip3 install python-docx
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_struct_015'
FILE_PATH = f'{WORKDIR}/Desktop/edited_manuscript.docx'

# Ground truth: these phrases were originally marked as insertions in tracked changes.
# After accepting all changes, they must be present in the final text.
EXPECTED_INSERTED_PHRASES = [
    'and consolidating',
    'Hebbian',
    'gradual',
]

# Ground truth: these phrases were originally marked as deletions in tracked changes.
# After accepting all changes, they must NOT appear in the final text.
EXPECTED_DELETED_PHRASES = [
    'relatively',
    'it is generally accepted that',
    'simply',
]


def verify_task(file_path):
    """
    Verify that all tracked changes have been accepted in the document.
    Returns a float between 0.0 and 1.0.

    The task requires:
      - Edit > Track Changes > Accept All Changes was used
      - No w:ins or w:del XML elements remain in the document body
      - All inserted text is retained; all deleted text is removed
    """
    total_score = 0.0

    # Precondition gate: ensure the file exists and is loadable
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    body_xml = doc.element.body.xml

    # Component 1: No tracked insertions remain (0.40 points)
    # w:ins elements mark text added via track changes; after Accept All, none should remain.
    try:
        ins_count = body_xml.count('<w:ins ')
        if ins_count == 0:
            print(f"PASS: Component 1 — No tracked insertions (w:ins) found (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 1 — Found {ins_count} w:ins element(s); expected 0 after accepting all changes")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: No tracked deletions remain (0.30 points)
    # w:del elements mark text deleted via track changes; after Accept All, none should remain.
    try:
        del_count = body_xml.count('<w:del ')
        if del_count == 0:
            print(f"PASS: Component 2 — No tracked deletions (w:del) found (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — Found {del_count} w:del element(s); expected 0 after accepting all changes")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Inserted text is present and deleted text is absent (0.30 points)
    # This verifies that Accept All (not Reject All) was performed:
    #   - inserted phrases must appear in the final text
    #   - deleted phrases must not appear in the final text
    try:
        full_text = ' '.join(p.text for p in doc.paragraphs)

        # Check all inserted phrases are present
        inserted_present = all(phrase in full_text for phrase in EXPECTED_INSERTED_PHRASES)
        missing_inserted = [p for p in EXPECTED_INSERTED_PHRASES if p not in full_text]

        # Check all deleted phrases are absent
        deleted_absent = all(phrase not in full_text for phrase in EXPECTED_DELETED_PHRASES)
        unexpected_deleted = [p for p in EXPECTED_DELETED_PHRASES if p in full_text]

        if inserted_present and deleted_absent:
            print(f"PASS: Component 3 — All inserted text present and all deleted text absent (0.30 pts)")
            total_score += 0.30
        else:
            if missing_inserted:
                print(f"FAIL: Component 3 — Missing inserted text: {missing_inserted}")
            if unexpected_deleted:
                print(f"FAIL: Component 3 — Deleted text still present: {unexpected_deleted}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

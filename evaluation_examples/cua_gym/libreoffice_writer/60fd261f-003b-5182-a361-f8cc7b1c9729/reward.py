"""
Reward Script: Insert three bookmarks in the document
Task ID: writer_struct_044
Domain: libreoffice_writer
Scoring:
  Component 1: Exactly 3 bookmarks present in the document (0.30 pts)
  Component 2: 'intro_bookmark' is placed within the 'Introduction' heading paragraph (0.25 pts)
  Component 3: 'methods_bookmark' is placed within the 'Methods' heading paragraph (0.25 pts)
  Component 4: 'conclusion_bookmark' is placed within the 'Conclusion' heading paragraph (0.20 pts)
  Total: 1.0
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_struct_044'
FILE_NAME = 'biology_paper.docx'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document — precondition gate
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # Collect all bookmarkStart elements and their names
    try:
        bookmark_starts = doc.element.body.findall('.//w:bookmarkStart', ns)
        bookmark_names = [bm.get(qn('w:name')) for bm in bookmark_starts]
        # Filter out internal Word bookmarks (those starting with '_')
        user_bookmarks = [n for n in bookmark_names if n and not n.startswith('_')]
    except Exception as e:
        print(f"ERROR: Failed to read bookmarks: {e}")
        user_bookmarks = []

    # Component 1: Exactly 3 user-defined bookmarks present (0.30 points)
    try:
        expected_bookmark_names = {'intro_bookmark', 'methods_bookmark', 'conclusion_bookmark'}
        found_set = set(user_bookmarks)
        if len(user_bookmarks) == 3 and found_set == expected_bookmark_names:
            print(f"PASS: Component 1 — Exactly 3 expected bookmarks present: {sorted(found_set)} (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Expected exactly 3 bookmarks {sorted(expected_bookmark_names)}, found {len(user_bookmarks)}: {sorted(found_set)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Helper: map each bookmark name to the text of its containing paragraph
    def get_bookmark_para_text(bm_name):
        """Return the text of the paragraph containing the bookmarkStart with the given name."""
        for bm in doc.element.body.findall('.//w:bookmarkStart', ns):
            if bm.get(qn('w:name')) == bm_name:
                # Walk up to the enclosing <w:p>
                parent = bm.getparent()
                while parent is not None and parent.tag != qn('w:p'):
                    parent = parent.getparent()
                if parent is not None:
                    texts = parent.findall('.//w:t', ns)
                    return ''.join(t.text or '' for t in texts)
        return None

    # Component 2: 'intro_bookmark' is in the 'Introduction' paragraph (0.25 points)
    try:
        para_text = get_bookmark_para_text('intro_bookmark')
        if para_text is not None and 'Introduction' in para_text:
            print(f"PASS: Component 2 — 'intro_bookmark' found in paragraph: {para_text!r} (0.25 pts)")
            total_score += 0.25
        elif para_text is not None:
            print(f"FAIL: Component 2 — 'intro_bookmark' found but in wrong paragraph: {para_text!r}, expected 'Introduction'")
        else:
            print("FAIL: Component 2 — 'intro_bookmark' not found in document")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'methods_bookmark' is in the 'Methods' paragraph (0.25 points)
    try:
        para_text = get_bookmark_para_text('methods_bookmark')
        if para_text is not None and 'Methods' in para_text:
            print(f"PASS: Component 3 — 'methods_bookmark' found in paragraph: {para_text!r} (0.25 pts)")
            total_score += 0.25
        elif para_text is not None:
            print(f"FAIL: Component 3 — 'methods_bookmark' found but in wrong paragraph: {para_text!r}, expected 'Methods'")
        else:
            print("FAIL: Component 3 — 'methods_bookmark' not found in document")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 'conclusion_bookmark' is in the 'Conclusion' paragraph (0.20 points)
    try:
        para_text = get_bookmark_para_text('conclusion_bookmark')
        if para_text is not None and 'Conclusion' in para_text:
            print(f"PASS: Component 4 — 'conclusion_bookmark' found in paragraph: {para_text!r} (0.20 pts)")
            total_score += 0.20
        elif para_text is not None:
            print(f"FAIL: Component 4 — 'conclusion_bookmark' found but in wrong paragraph: {para_text!r}, expected 'Conclusion'")
        else:
            print("FAIL: Component 4 — 'conclusion_bookmark' not found in document")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
file_path = os.path.join(WORKDIR, FILE_NAME)
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

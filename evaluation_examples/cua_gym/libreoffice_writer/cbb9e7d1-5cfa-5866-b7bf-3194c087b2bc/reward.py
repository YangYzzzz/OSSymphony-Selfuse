"""
Reward Script: Insert two comments on document headings
Task ID: writer_struct_052
Domain: libreoffice_writer
Scoring:
  Component 1: Comment on 'Introduction' with correct text (0.4 pts)
  Component 2: Comment on 'Conclusion' with correct text (0.4 pts)
  Component 3: Both comments anchored to correct headings (0.2 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_struct_052'

FILE_PATH = os.path.join(WORKDIR, 'sociology_paper.docx')

# Expected comment texts (exact strings from task_config.json)
COMMENT_INTRO_TEXT = 'Add a thesis statement in the opening paragraph.'
COMMENT_CONCLUSION_TEXT = 'Strengthen the concluding argument with quantitative evidence from Section 4.'

NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def get_comments(doc):
    """Extract all comments from the document. Returns list of (id, text) tuples."""
    try:
        comments_part = doc.part.part_related_by(
            'http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments'
        )
        root = comments_part._element
        comment_elements = root.findall('.//{%s}comment' % NS)
        result = []
        for c in comment_elements:
            cid = c.get('{%s}id' % NS, '')
            text_els = c.findall('.//{%s}t' % NS)
            text = ''.join(t.text or '' for t in text_els)
            result.append((cid, text))
        return result
    except Exception:
        return []


def get_comment_anchors(doc):
    """Find which paragraph texts have commentRangeStart elements.
    Returns dict: comment_id -> paragraph_text"""
    anchors = {}
    for para in doc.paragraphs:
        starts = para._element.findall('.//{%s}commentRangeStart' % NS)
        for s in starts:
            cid = s.get('{%s}id' % NS, '')
            anchors[cid] = para.text.strip()
    return anchors


def find_comment_id_by_text(comments, target_text):
    """Return comment ID for the first comment matching target_text, or None."""
    for cid, text in comments:
        if text.strip() == target_text:
            return cid
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document — precondition gate
    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Retrieve all comments from the document
    comments = get_comments(doc)
    if not comments:
        print("FAIL: No comments found in the document (comments part missing or empty)")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    print(f"INFO: Found {len(comments)} comment(s) in document")
    for cid, text in comments:
        print(f"  Comment ID={cid}: {repr(text)}")

    # Retrieve comment anchors (which paragraphs each comment is attached to)
    anchors = get_comment_anchors(doc)
    print(f"INFO: Comment anchors: {anchors}")

    # Component 1: Comment on 'Introduction' with correct text (0.4 points)
    # This FAILS on initial_env (no comments) and PASSES on golden_env
    try:
        intro_id = find_comment_id_by_text(comments, COMMENT_INTRO_TEXT)
        if intro_id is not None:
            print(f"PASS: Component 1 — Comment with Introduction text found (ID={intro_id}, 0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Expected comment text {repr(COMMENT_INTRO_TEXT)} not found")
            print(f"  Existing comment texts: {[t for _, t in comments]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        intro_id = None

    # Component 2: Comment on 'Conclusion' with correct text (0.4 points)
    # This FAILS on initial_env (no comments) and PASSES on golden_env
    try:
        conclusion_id = find_comment_id_by_text(comments, COMMENT_CONCLUSION_TEXT)
        if conclusion_id is not None:
            print(f"PASS: Component 2 — Comment with Conclusion text found (ID={conclusion_id}, 0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — Expected comment text {repr(COMMENT_CONCLUSION_TEXT)} not found")
            print(f"  Existing comment texts: {[t for _, t in comments]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")
        conclusion_id = None

    # Component 3: Comments anchored to correct headings (0.2 points)
    # Verifies the intro comment anchors to 'Introduction' and the
    # conclusion comment anchors to 'Conclusion'.
    # This FAILS on initial_env (no comments, no anchors) and PASSES on golden_env
    try:
        intro_anchor = anchors.get(intro_id, '') if intro_id is not None else ''
        conclusion_anchor = anchors.get(conclusion_id, '') if conclusion_id is not None else ''

        intro_anchored = 'Introduction' in intro_anchor
        conclusion_anchored = 'Conclusion' in conclusion_anchor

        if not intro_anchored:
            print(f"FAIL: Component 3a — Intro comment not anchored to 'Introduction' heading. Anchor={repr(intro_anchor)}")
        else:
            print(f"PASS: Component 3a — Introduction comment anchored to: {repr(intro_anchor)}")

        if not conclusion_anchored:
            print(f"FAIL: Component 3b — Conclusion comment not anchored to 'Conclusion' heading. Anchor={repr(conclusion_anchor)}")
        else:
            print(f"PASS: Component 3b — Conclusion comment anchored to: {repr(conclusion_anchor)}")

        if intro_anchored and conclusion_anchored:
            print(f"PASS: Component 3 — Both comments anchored to correct headings (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Not all comments anchored to correct headings")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

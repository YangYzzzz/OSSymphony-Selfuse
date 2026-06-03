"""
Reward Script: Delete the second comment ('Revise this paragraph') from manuscript_review.docx
Task ID: writer_struct_057
Domain: libreoffice_writer
Scoring:
  Component 1: Comment 'Revise this paragraph' is absent (0.5 pts)
  Component 2: Exactly 2 comments remain AND both 'Good introduction' and
               'Strong evidence presented' are still present (compound check, 0.3 pts)
               — This is a compound check anchored to the task change
  Component 3: No unexpected comments were added or altered — comment id ordering consistent
               with expected outcome (ids 1 and 3 remain, id 2 removed) (0.2 pts)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_struct_057'
FILE_PATH = f'{WORKDIR}/manuscript_review.docx'

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

# Expected comments after task completion (comment id -> text)
EXPECTED_REMAINING_COMMENTS = {'Good introduction', 'Strong evidence presented'}
DELETED_COMMENT = 'Revise this paragraph'
EXPECTED_COUNT = 2


def get_comments_with_ids(docx_path):
    """
    Extract all comments from the docx comments.xml part.
    Returns a list of (comment_id, comment_text) tuples.
    """
    with zipfile.ZipFile(docx_path, 'r') as z:
        if 'word/comments.xml' not in z.namelist():
            return []
        with z.open('word/comments.xml') as f:
            xml_content = f.read()

    root = ET.fromstring(xml_content)
    comments = []
    for comment_elem in root.findall('w:comment', NS):
        comment_id = comment_elem.get(f'{{{NS["w"]}}}id')
        texts = []
        for t_elem in comment_elem.findall('.//w:t', NS):
            if t_elem.text:
                texts.append(t_elem.text)
        comment_text = ''.join(texts).strip()
        comments.append((comment_id, comment_text))
    return comments


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Task: Delete the second comment ('Revise this paragraph') from manuscript_review.docx.
    After task: only 'Good introduction' and 'Strong evidence presented' should remain.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be a valid docx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        comment_entries = get_comments_with_ids(file_path)
        comment_texts = [text for _, text in comment_entries]
        comment_ids = [cid for cid, _ in comment_entries]
        print(f"INFO: Found {len(comment_entries)} comment(s):")
        for cid, text in comment_entries:
            print(f"  id={cid}: '{text}'")
    except Exception as e:
        print(f"CRITICAL: Cannot read comments from {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Compute revise_present once, used in both Component 1 and Component 2
    revise_present = any(DELETED_COMMENT in c for c in comment_texts)

    # Component 1: Comment 'Revise this paragraph' must be absent (0.5 points)
    # This comment exists in initial_env and should be deleted in golden_env.
    # FAILS on initial_env (comment is present), PASSES on golden_env (comment is absent).
    try:
        if not revise_present:
            print(f"PASS: Component 1 — '{DELETED_COMMENT}' comment is absent (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — '{DELETED_COMMENT}' still present; must be deleted")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Exactly 2 comments remain AND 'Revise this paragraph' is absent
    #              AND both expected comments are present (compound check, 0.3 points)
    # This is a compound check: it requires the deletion to have occurred (no 'Revise this paragraph')
    # AND verifies that the two remaining comments are exactly the expected ones.
    # FAILS on initial_env (count is 3, not 2), PASSES on golden_env (count is 2 and correct).
    try:
        num_comments = len(comment_texts)
        has_good_intro = any('Good introduction' in c for c in comment_texts)
        has_strong_evidence = any('Strong evidence presented' in c for c in comment_texts)
        # This compound check requires count == 2 AND correct comments present AND deleted comment absent
        if num_comments == EXPECTED_COUNT and has_good_intro and has_strong_evidence and not revise_present:
            print(f"PASS: Component 2 — Exactly 2 comments remain and both expected comments present (0.3 pts)")
            total_score += 0.3
        else:
            if num_comments != EXPECTED_COUNT:
                print(f"FAIL: Component 2 — Expected exactly {EXPECTED_COUNT} comments, found {num_comments}")
            elif not has_good_intro:
                print("FAIL: Component 2 — 'Good introduction' comment missing")
            elif not has_strong_evidence:
                print("FAIL: Component 2 — 'Strong evidence presented' comment missing")
            else:
                print(f"FAIL: Component 2 — Compound check failed (deleted comment still present)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The comment with text 'Revise this paragraph' (originally id='2') is absent,
    #              and the surviving comments have ids '1' and '3' as expected (0.2 points)
    # This verifies only the specific second comment was removed, not all comments.
    # FAILS on initial_env (id '2' is present), PASSES on golden_env (ids 1 and 3 survive).
    try:
        # Check that id='2' is not among the remaining comment ids
        has_id_2 = '2' in comment_ids
        has_id_1 = '1' in comment_ids
        has_id_3 = '3' in comment_ids
        if not has_id_2 and has_id_1 and has_id_3:
            print(f"PASS: Component 3 — Comment id=2 removed, ids 1 and 3 still present (0.2 pts)")
            total_score += 0.2
        else:
            if has_id_2:
                print("FAIL: Component 3 — Comment id=2 ('Revise this paragraph') still present")
            if not has_id_1:
                print("FAIL: Component 3 — Comment id=1 ('Good introduction') missing")
            if not has_id_3:
                print("FAIL: Component 3 — Comment id=3 ('Strong evidence presented') missing")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

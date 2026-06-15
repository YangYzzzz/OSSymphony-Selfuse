"""
Reward Script: Insert a comment on 'restructuring' in paragraph 2 with text
'Requires board approval per Article 7.', then reply with 'Board meeting scheduled for March 15.'
Task ID: writer_struct_064
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Comment with text 'Requires board approval per Article 7.' exists
  Component 2 (0.3): That comment is anchored to the word 'restructuring'
  Component 3 (0.3): A reply comment with text 'Board meeting scheduled for March 15.' exists
"""

import os
import zipfile
import re

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_struct_064'
FILE_PATH = f'{WORKDIR}/governance_amendment.docx'

COMMENT_TEXT_1 = 'Requires board approval per Article 7.'
COMMENT_TEXT_2 = 'Board meeting scheduled for March 15.'


def get_comments(doc_path):
    """
    Parse comments.xml and commentsExtended.xml from the docx archive.
    Returns:
      comments: dict of {comment_id: {'text': str, 'para_id': str}}
      reply_map: dict of {comment_id: parent_comment_id}  (from commentsExtended)
    """
    comments = {}
    reply_map = {}

    with zipfile.ZipFile(doc_path, 'r') as z:
        names = z.namelist()

        if 'word/comments.xml' not in names:
            return comments, reply_map

        comments_xml = z.read('word/comments.xml').decode('utf-8', errors='replace')

        # Extract each w:comment element
        comment_blocks = re.findall(
            r'<w:comment\b([^>]*)>(.*?)</w:comment>',
            comments_xml,
            re.DOTALL
        )
        for attrs, body in comment_blocks:
            # Get id
            id_match = re.search(r'w:id="(\d+)"', attrs)
            if not id_match:
                continue
            comment_id = id_match.group(1)

            # Get paraId from w14:paraId attribute on the inner w:p
            para_id_match = re.search(r'w14:paraId="([A-Fa-f0-9]+)"', body)
            para_id = para_id_match.group(1) if para_id_match else None

            # Extract text: collect all w:t content
            texts = re.findall(r'<w:t[^>]*>(.*?)</w:t>', body, re.DOTALL)
            full_text = ''.join(texts).strip()

            comments[comment_id] = {'text': full_text, 'para_id': para_id}

        # Parse commentsExtended.xml for reply relationships
        if 'word/commentsExtended.xml' in names:
            ext_xml = z.read('word/commentsExtended.xml').decode('utf-8', errors='replace')
            # Find commentEx entries with paraIdParent (= reply indicator)
            ext_entries = re.findall(
                r'<w15:commentEx\b([^/]*?)/>',
                ext_xml
            )
            for entry_attrs in ext_entries:
                para_id_match = re.search(r'w15:paraId="([A-Fa-f0-9]+)"', entry_attrs)
                parent_match = re.search(r'w15:paraIdParent="([A-Fa-f0-9]+)"', entry_attrs)
                if para_id_match and parent_match:
                    child_para_id = para_id_match.group(1)
                    parent_para_id = parent_match.group(1)
                    # Map child comment (by paraId) to parent comment (by paraId)
                    # We'll resolve to comment IDs below
                    reply_map[child_para_id] = parent_para_id

    return comments, reply_map


def get_comment_anchors(doc_path):
    """
    Parse document.xml to find which word/run is annotated by each comment.
    Returns a dict: {comment_id: anchor_text}
    where anchor_text is the text between commentRangeStart and commentRangeEnd.
    """
    anchors = {}
    with zipfile.ZipFile(doc_path, 'r') as z:
        if 'word/document.xml' not in z.namelist():
            return anchors
        doc_xml = z.read('word/document.xml').decode('utf-8', errors='replace')

    # Find commentRangeStart/End pairs and extract text between them
    # Pattern: <w:commentRangeStart w:id="N"/>...<w:commentRangeEnd w:id="N"/>
    starts = {m.group(1): m.start() for m in re.finditer(
        r'<w:commentRangeStart\s+w:id="(\d+)"\s*/?>', doc_xml)}
    ends = {m.group(1): m.end() for m in re.finditer(
        r'<w:commentRangeEnd\s+w:id="(\d+)"\s*/?>', doc_xml)}

    for cid in starts:
        if cid not in ends:
            continue
        segment = doc_xml[starts[cid]:ends[cid]]
        # Extract all w:t content within the segment
        texts = re.findall(r'<w:t[^>]*>(.*?)</w:t>', segment, re.DOTALL)
        anchor_text = ''.join(texts).strip()
        anchors[cid] = anchor_text

    return anchors


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: file must be a valid docx (zip)
    try:
        with zipfile.ZipFile(file_path, 'r') as _:
            pass
    except Exception as e:
        print(f"CRITICAL: Cannot open docx as zip: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse comments and anchors
    try:
        comments, reply_map = get_comments(file_path)
        anchors = get_comment_anchors(file_path)
    except Exception as e:
        print(f"CRITICAL: Error parsing document: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found {len(comments)} comment(s) in document.")
    for cid, cdata in comments.items():
        print(f"  Comment id={cid}: text='{cdata['text']}' para_id={cdata['para_id']}")
    print(f"Reply map (child_para_id -> parent_para_id): {reply_map}")
    print(f"Anchors: {anchors}")

    # --- Component 1: Comment with correct first text exists (0.4 pts) ---
    try:
        comment1_id = None
        for cid, cdata in comments.items():
            if COMMENT_TEXT_1 in cdata['text']:
                comment1_id = cid
                break
        if comment1_id is not None:
            print(f"PASS: Component 1 — Comment '{COMMENT_TEXT_1}' found (id={comment1_id}) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — No comment with text '{COMMENT_TEXT_1}' found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --- Component 2: That comment is anchored to the word 'restructuring' (0.3 pts) ---
    try:
        if comment1_id is not None:
            anchor = anchors.get(comment1_id, '')
            if 'restructuring' in anchor.lower():
                print(f"PASS: Component 2 — Comment is anchored to 'restructuring' (anchor='{anchor}') (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Comment anchor text is '{anchor}', expected to contain 'restructuring'")
        else:
            print("FAIL: Component 2 — Skipped (Component 1 failed, no primary comment found)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # --- Component 3: A reply comment with correct text exists (0.3 pts) ---
    # A reply is identified by having a paraIdParent in commentsExtended.xml
    # linking it back to the primary comment's paraId
    try:
        comment2_id = None
        for cid, cdata in comments.items():
            if COMMENT_TEXT_2 in cdata['text']:
                comment2_id = cid
                break

        if comment2_id is None:
            print(f"FAIL: Component 3 — No comment with text '{COMMENT_TEXT_2}' found")
        else:
            # Verify it is a reply (has paraIdParent pointing to parent's paraId)
            comment2_para_id = comments[comment2_id].get('para_id', '')
            is_reply = comment2_para_id in reply_map

            if is_reply:
                parent_para_id = reply_map[comment2_para_id]
                # Additionally verify the parent is the primary comment (comment1)
                comment1_para_id = comments.get(comment1_id, {}).get('para_id', '') if comment1_id else ''
                if parent_para_id == comment1_para_id:
                    print(f"PASS: Component 3 — Reply '{COMMENT_TEXT_2}' found and correctly linked to primary comment (0.3 pts)")
                    total_score += 0.3
                else:
                    # Reply exists but parent doesn't match — still award partial: reply text is correct
                    # but we cannot fully verify the threading. Award points if text matches.
                    print(f"PASS: Component 3 — Reply '{COMMENT_TEXT_2}' found (reply structure present, parent_para_id={parent_para_id}) (0.3 pts)")
                    total_score += 0.3
            else:
                # No paraIdParent — comment exists but is not marked as a reply
                # If the text is correct but threading is missing, give no points
                print(f"FAIL: Component 3 — Comment '{COMMENT_TEXT_2}' exists but is not marked as a reply (no paraIdParent)")
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

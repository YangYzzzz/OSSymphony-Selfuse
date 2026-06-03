"""
Reward Script: Delete a specific comment from a LibreOffice Writer document
Task ID: writer_rm_008
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Comment count reduced from 3 to 2
  Component 2 (0.35): The specific 'This section needs more data' comment is absent
  Component 3 (0.25): The two remaining comments are preserved intact
"""

import os
import zipfile
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_008'

WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WNS}


def persist_app_state(domain: str):
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


def parse_comments(file_path):
    """Extract comments from the docx comments.xml part."""
    comments = []
    with zipfile.ZipFile(file_path) as z:
        if 'word/comments.xml' not in z.namelist():
            return comments
        xml_data = z.read('word/comments.xml')
        root = etree.fromstring(xml_data)
        for comment_el in root.findall('.//w:comment', NS):
            cid = comment_el.get(f'{{{WNS}}}id')
            author = comment_el.get(f'{{{WNS}}}author')
            # Extract all text from the comment
            texts = []
            for t_el in comment_el.findall('.//w:t', NS):
                if t_el.text:
                    texts.append(t_el.text)
            text = ''.join(texts)
            comments.append({
                'id': cid,
                'author': author,
                'text': text,
            })
    return comments


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file exists and is a valid docx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        comments = parse_comments(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse comments from {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(comments)} comments in document")
    for c in comments:
        print(f"  - id={c['id']}, author='{c['author']}', text='{c['text']}'")

    # Component 1: Comment count is exactly 2 (reduced from 3) — 0.4 points
    try:
        if len(comments) == 2:
            print(f"PASS: Component 1 — Comment count is 2 (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Expected 2 comments, found {len(comments)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The deleted comment 'This section needs more data' is absent — 0.35 points
    try:
        deleted_comment_texts = [c['text'] for c in comments if 'needs more data' in c['text'].lower()]
        if len(deleted_comment_texts) == 0:
            print(f"PASS: Component 2 — 'This section needs more data' comment not found (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — Found deleted comment text: {deleted_comment_texts}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Exactly 2 comments remain AND both are the correct ones — 0.25 points
    # This is a compound check: count==2 AND 'Great opening summary' AND 'discuss these projections'
    # It only passes on golden (where the deletion happened), not on initial (which has 3 comments).
    try:
        comment_texts = {c['text'].strip() for c in comments}

        has_sarah = 'Great opening summary' in comment_texts
        has_david = any('discuss these projections' in t for t in comment_texts)
        count_is_two = len(comments) == 2

        if count_is_two and has_sarah and has_david:
            print(f"PASS: Component 3 — Exactly 2 comments remain and both are correct (0.25 pts)")
            total_score += 0.25
        else:
            reasons = []
            if not count_is_two:
                reasons.append(f"comment count is {len(comments)}, not 2")
            if not has_sarah:
                reasons.append("missing 'Great opening summary' by Sarah Lee")
            if not has_david:
                reasons.append("missing 'Let's discuss these projections' by David Chen")
            print(f"FAIL: Component 3 — {'; '.join(reasons)}")
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

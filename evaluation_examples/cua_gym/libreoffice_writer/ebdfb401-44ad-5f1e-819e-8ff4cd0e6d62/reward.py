"""
Reward Script: Add a comment on the non-compete clause noting California enforceability concerns
Task ID: writer_legal_033
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): Document contains at least one comment
  Component 2 (0.3): Comment is anchored to text containing the non-compete duration clause
  Component 3 (0.4): Comment text mentions California enforceability and recommends 12 months
"""

import os
import re
import time
import lxml.etree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_033'
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W_NS}


def persist_app_state(domain):
    """Save any unsaved changes in LibreOffice Writer."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def get_comments(doc):
    """Extract comments from the docx document via its relationships."""
    comments = []
    for rel in doc.part.rels.values():
        if 'comment' in rel.reltype.lower():
            comments_part = rel.target_part
            tree = ET.fromstring(comments_part.blob)
            for c in tree.findall('.//w:comment', NS):
                cid = c.get(f'{{{W_NS}}}id')
                texts = []
                for t in c.iter(f'{{{W_NS}}}t'):
                    if t.text:
                        texts.append(t.text)
                full_text = ''.join(texts)
                comments.append({'id': cid, 'text': full_text})
    return comments


def get_commented_text(doc, comment_id):
    """Get the document text that a comment is anchored to (between commentRangeStart and commentRangeEnd)."""
    body = doc.element.body
    body_xml = ET.tostring(body, encoding='unicode')

    # Find the paragraph containing the commentRangeStart for this comment_id
    # Walk paragraphs and check if they contain commentRangeStart with matching id
    for para in doc.paragraphs:
        el = para._element
        starts = el.findall(f'.//{{{W_NS}}}commentRangeStart')
        for s in starts:
            if s.get(f'{{{W_NS}}}id') == str(comment_id):
                return para.text
    return ""


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

    # Component 1: Document contains at least one comment (0.3 points)
    # This FAILS on initial (no comments) and PASSES on golden (1 comment)
    try:
        comments = get_comments(doc)
        if len(comments) > 0:
            print(f"PASS: Component 1 — Document has {len(comments)} comment(s) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No comments found in document")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Comment is anchored to text containing the non-compete duration clause (0.3 points)
    # The comment should be on text related to "non-compete period shall extend for twenty-four (24) months"
    try:
        if len(comments) > 0:
            anchored_correctly = False
            for comment in comments:
                anchor_text = get_commented_text(doc, comment['id'])
                if anchor_text and 'non-compete' in anchor_text.lower() and 'twenty-four' in anchor_text.lower():
                    anchored_correctly = True
                    print(f"PASS: Component 2 — Comment anchored to non-compete clause text (0.3 pts)")
                    print(f"  Anchor text excerpt: '{anchor_text[:100]}...'")
                    total_score += 0.3
                    break
            if not anchored_correctly:
                # Check if any comment is at least in a paragraph mentioning 24 months
                for comment in comments:
                    anchor_text = get_commented_text(doc, comment['id'])
                    if anchor_text and ('24' in anchor_text or 'twenty-four' in anchor_text.lower()):
                        anchored_correctly = True
                        print(f"PASS: Component 2 — Comment anchored to paragraph with 24-month reference (0.3 pts)")
                        total_score += 0.3
                        break
                if not anchored_correctly:
                    print(f"FAIL: Component 2 — Comment not anchored to the non-compete duration clause")
                    for comment in comments:
                        anchor_text = get_commented_text(doc, comment['id'])
                        print(f"  Comment {comment['id']} anchor text: '{anchor_text[:100] if anchor_text else 'N/A'}'")
        else:
            print(f"FAIL: Component 2 — No comments to check anchoring")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Comment text mentions California enforceability and recommends 12 months (0.4 points)
    # Expected: "This duration may be unenforceable in California under Business and Professions Code Section 16600.
    #            Recommend reducing to twelve (12) months."
    try:
        if len(comments) > 0:
            best_match_score = 0.0
            best_comment_text = ""
            for comment in comments:
                ct = comment['text'].lower()
                match_score = 0.0

                # Sub-check a: mentions California (0.15)
                if 'california' in ct:
                    match_score += 0.15

                # Sub-check b: mentions enforceability concern (0.1)
                if 'unenforceable' in ct or 'enforceab' in ct or 'enforceable' in ct:
                    match_score += 0.1

                # Sub-check c: recommends 12 months reduction (0.15)
                if ('12' in ct or 'twelve' in ct) and ('month' in ct or 'reduce' in ct or 'recommend' in ct):
                    match_score += 0.15

                if match_score > best_match_score:
                    best_match_score = match_score
                    best_comment_text = comment['text']

            if best_match_score > 0:
                total_score += best_match_score
                print(f"PASS: Component 3 — Comment text matches expectations ({best_match_score} pts)")
                print(f"  Comment text: '{best_comment_text}'")
                if best_match_score < 0.4:
                    print(f"  Note: Partial match — full score requires California + enforceability + 12 months")
            else:
                print(f"FAIL: Component 3 — Comment text does not mention California enforceability or 12-month recommendation")
                for comment in comments:
                    print(f"  Comment text: '{comment['text'][:200]}'")
        else:
            print(f"FAIL: Component 3 — No comments to check text content")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
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

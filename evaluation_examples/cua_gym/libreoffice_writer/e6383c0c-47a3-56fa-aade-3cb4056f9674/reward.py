"""
Reward Script: Verify a tracked change comment spanning paragraphs 6 and 7
Task ID: writer_lec_093
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): Comment exists in document
  Component 2 (0.3): Comment text matches expected value
  Component 3 (0.4): Comment range spans paragraphs 6 and 7
"""

import os
import zipfile
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_093'
EXPECTED_COMMENT_TEXT = 'Needs legal review before publication'
WML_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WML_NS}


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice changes before verification."""
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
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the docx as a zip to access comments.xml and document.xml directly
    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse comments.xml if it exists
    comments = []  # list of (id, text)
    try:
        if 'word/comments.xml' in zf.namelist():
            comments_xml = zf.read('word/comments.xml')
            comments_root = etree.fromstring(comments_xml)
            for comment_el in comments_root.findall('.//w:comment', NS):
                cid = comment_el.get(f'{{{WML_NS}}}id')
                # Gather all text nodes within the comment
                text_parts = []
                for t in comment_el.findall('.//w:t', NS):
                    if t.text:
                        text_parts.append(t.text)
                comment_text = ''.join(text_parts)
                comments.append((cid, comment_text))
            print(f"INFO: Found {len(comments)} comment(s) in comments.xml")
        else:
            print("INFO: No word/comments.xml found in the document")
    except Exception as e:
        print(f"ERROR: Failed to parse comments.xml: {e}")

    # Parse document.xml for comment ranges
    doc_xml = None
    body = None
    paragraphs = []
    try:
        doc_xml = zf.read('word/document.xml')
        doc_root = etree.fromstring(doc_xml)
        body = doc_root.find('.//w:body', NS)
        if body is not None:
            paragraphs = body.findall('w:p', NS)
            print(f"INFO: Document has {len(paragraphs)} top-level paragraphs")
    except Exception as e:
        print(f"ERROR: Failed to parse document.xml: {e}")

    zf.close()

    # Component 1: At least one comment exists in the document (0.3 points)
    try:
        if len(comments) >= 1:
            print(f"PASS: Component 1 -- Comment exists ({len(comments)} comment(s) found) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 -- No comments found in document")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Comment text matches expected value (0.3 points)
    try:
        text_match_found = False
        for cid, ctext in comments:
            if ctext.strip().lower() == EXPECTED_COMMENT_TEXT.lower():
                text_match_found = True
                print(f"PASS: Component 2 -- Comment text matches: '{ctext}' (0.3 pts)")
                total_score += 0.3
                break
        if not text_match_found:
            actual_texts = [ctext for _, ctext in comments]
            print(f"FAIL: Component 2 -- Expected comment text '{EXPECTED_COMMENT_TEXT}', found: {actual_texts}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Comment range spans paragraphs 6 and 7 (0-indexed) (0.4 points)
    # The commentRangeStart should be in paragraph 6, commentRangeEnd in paragraph 7
    try:
        if body is None or len(paragraphs) == 0:
            print("FAIL: Component 3 -- Could not parse document body")
        else:
            # Find which paragraphs contain commentRangeStart and commentRangeEnd
            start_para_indices = []
            end_para_indices = []
            for i, p in enumerate(paragraphs):
                if p.findall('w:commentRangeStart', NS):
                    start_para_indices.append(i)
                if p.findall('w:commentRangeEnd', NS):
                    end_para_indices.append(i)

            print(f"INFO: commentRangeStart in paragraphs: {start_para_indices}")
            print(f"INFO: commentRangeEnd in paragraphs: {end_para_indices}")

            # Check that the comment spans across at least two paragraphs
            # and covers paragraph 6 and 7 specifically
            spans_two_paras = False
            if start_para_indices and end_para_indices:
                start_idx = min(start_para_indices)
                end_idx = max(end_para_indices)
                if end_idx > start_idx:
                    # Comment spans multiple paragraphs
                    # Verify it covers paragraphs 6 and 7 (the legal paragraphs)
                    if start_idx <= 6 and end_idx >= 7:
                        spans_two_paras = True

            if spans_two_paras:
                print(f"PASS: Component 3 -- Comment spans paragraphs {start_idx}-{end_idx}, covering paras 6 and 7 (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 3 -- Comment does not span paragraphs 6 and 7 as required")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 1)
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

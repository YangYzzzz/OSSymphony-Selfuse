"""
Reward Script: Add a text comment on the Q3 projected revenue paragraph
Task ID: writer_biz_036
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): comments.xml exists with at least one comment
  Component 2 (0.3): Comment text matches expected content
  Component 3 (0.3): Comment is anchored in document.xml (commentRangeStart/End/Reference)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_biz_036'
WML_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WML_NS}

EXPECTED_COMMENT_KEYWORDS = ['figures', 'verified', 'finance']


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        zf = zipfile.ZipFile(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: comments.xml exists and contains at least one comment (0.4 points)
    try:
        if 'word/comments.xml' not in zf.namelist():
            print("FAIL: Component 1 -- word/comments.xml not found in archive")
        else:
            tree = ET.parse(zf.open('word/comments.xml'))
            root = tree.getroot()
            comments = root.findall('.//w:comment', NS)
            if len(comments) >= 1:
                print(f"PASS: Component 1 -- comments.xml has {len(comments)} comment(s) (0.4 pts)")
                total_score += 0.4
            else:
                print("FAIL: Component 1 -- comments.xml exists but contains no comments")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Comment text matches expected content (0.3 points)
    # Expected: "These figures need to be verified by the finance team."
    try:
        if 'word/comments.xml' in zf.namelist():
            tree = ET.parse(zf.open('word/comments.xml'))
            root = tree.getroot()
            comments = root.findall('.//w:comment', NS)
            matching_comments = [
                ''.join(t.text or '' for t in c.findall('.//w:t', NS)).strip()
                for c in comments
                if all(kw in ''.join(t.text or '' for t in c.findall('.//w:t', NS)).strip().lower() for kw in EXPECTED_COMMENT_KEYWORDS)
            ]
            if len(matching_comments) >= 1:
                print(f"PASS: Component 2 -- Comment text contains expected keywords: '{matching_comments[0]}' (0.3 pts)")
                total_score += 0.3
            else:
                all_texts = [
                    ''.join(t.text or '' for t in c.findall('.//w:t', NS)).strip()
                    for c in comments
                ]
                print(f"FAIL: Component 2 -- No comment matches expected keywords {EXPECTED_COMMENT_KEYWORDS}. Found: {all_texts}")
        else:
            print("FAIL: Component 2 -- No comments.xml to check")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Comment is anchored in document body (0.3 points)
    # There should be commentRangeStart, commentRangeEnd, and commentReference in document.xml
    try:
        doc_tree = ET.parse(zf.open('word/document.xml'))
        doc_root = doc_tree.getroot()
        range_starts = doc_root.findall(f'.//{{{WML_NS}}}commentRangeStart')
        range_ends = doc_root.findall(f'.//{{{WML_NS}}}commentRangeEnd')
        references = doc_root.findall(f'.//{{{WML_NS}}}commentReference')

        if len(range_starts) >= 1 and len(range_ends) >= 1 and len(references) >= 1:
            print(f"PASS: Component 3 -- Comment anchored in document (starts={len(range_starts)}, ends={len(range_ends)}, refs={len(references)}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 -- Missing comment anchoring (starts={len(range_starts)}, ends={len(range_ends)}, refs={len(references)})")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    zf.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

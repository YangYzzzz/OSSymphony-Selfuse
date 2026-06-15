"""
Reward Script: Merge three reviewer comment documents into thesis chapter
Task ID: writer_acad_094
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): Tracked changes exist from multiple authors (insertions + deletions)
  Component 2 (0.3): Comments exist from multiple reviewers
  Component 3 (0.2): All three specific reviewer authors are represented
  Component 4 (0.2): Sufficient quantity of tracked changes and comments
"""

import os
import re
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'writer_acad_094'

EXPECTED_AUTHORS = {'Dr. James Thornton', 'Prof. Mei-Ling Chen', 'Dr. Aisha Patel'}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document
    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse XML namespace for tracked changes
    ns_uri = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    ns = {'w': ns_uri}
    body = doc.element.body

    # Gather all insertion elements and their authors
    ins_elements = body.findall('.//w:ins', ns)
    del_elements = body.findall('.//w:del', ns)

    ins_authors = set()
    for el in ins_elements:
        author = el.get(f'{{{ns_uri}}}author')
        if author:
            ins_authors.add(author)

    del_authors = set()
    for el in del_elements:
        author = el.get(f'{{{ns_uri}}}author')
        if author:
            del_authors.add(author)

    tracked_change_authors = ins_authors | del_authors
    total_ins = len(ins_elements)
    total_del = len(del_elements)

    print(f"INFO: Found {total_ins} insertions from {ins_authors}")
    print(f"INFO: Found {total_del} deletions from {del_authors}")

    # Gather comments from word/comments.xml
    comment_authors = set()
    comment_count = 0
    try:
        with zipfile.ZipFile(file_path) as z:
            if 'word/comments.xml' in z.namelist():
                content = z.read('word/comments.xml').decode()
                for m in re.finditer(r'<w:comment [^>]*w:author="([^"]+)"', content):
                    comment_authors.add(m.group(1))
                comment_count = len(re.findall(r'<w:comment ', content))
    except Exception as e:
        print(f"WARN: Could not read comments XML: {e}")

    print(f"INFO: Found {comment_count} comments from {comment_authors}")

    # Also check comment range markers in body
    comment_ranges = body.findall('.//w:commentRangeStart', ns)
    print(f"INFO: Found {len(comment_ranges)} comment range markers in body")

    # Component 1: Tracked changes exist from multiple authors (0.3 points)
    # Initial doc has 0 tracked changes; golden has 9 insertions + 3 deletions from 3 authors
    try:
        if total_ins >= 3 and total_del >= 1 and len(tracked_change_authors) >= 2:
            print(f"PASS: Component 1 -- Tracked changes from multiple authors ({total_ins} ins, {total_del} del, authors: {tracked_change_authors}) (0.3 pts)")
            total_score += 0.3
        elif total_ins >= 1 or total_del >= 1:
            # Partial: some tracked changes but not from multiple authors
            print(f"PARTIAL: Component 1 -- Some tracked changes but insufficient (ins={total_ins}, del={total_del}, authors={len(tracked_change_authors)})")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 -- No tracked changes found (expected insertions and deletions from multiple authors)")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Comments exist from multiple reviewers (0.3 points)
    # Initial doc has 0 comments; golden has 10 comments from 3 authors
    try:
        if comment_count >= 5 and len(comment_authors) >= 2:
            print(f"PASS: Component 2 -- Comments from multiple reviewers ({comment_count} comments, authors: {comment_authors}) (0.3 pts)")
            total_score += 0.3
        elif comment_count >= 1:
            # Partial: some comments but not enough diversity
            print(f"PARTIAL: Component 2 -- Some comments but insufficient ({comment_count} comments, {len(comment_authors)} authors)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 2 -- No comments found (expected comments from multiple reviewers)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: All three specific reviewer authors are represented (0.2 points)
    # Check that all 3 expected authors appear in tracked changes OR comments
    try:
        all_authors = tracked_change_authors | comment_authors
        matching_authors = EXPECTED_AUTHORS & all_authors
        if len(matching_authors) >= 3:
            print(f"PASS: Component 3 -- All 3 reviewers represented ({matching_authors}) (0.2 pts)")
            total_score += 0.2
        elif len(matching_authors) >= 2:
            print(f"PARTIAL: Component 3 -- Only {len(matching_authors)}/3 reviewers found ({matching_authors})")
            total_score += 0.1
        else:
            print(f"FAIL: Component 3 -- Only {len(matching_authors)}/3 expected reviewers found (expected: {EXPECTED_AUTHORS}, found: {all_authors})")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Sufficient quantity of tracked changes and comments (0.2 points)
    # Golden has exactly 9 insertions, 3 deletions, 10 comments
    try:
        sufficient_ins = total_ins >= 6
        sufficient_del = total_del >= 2
        sufficient_comments = comment_count >= 7
        if sufficient_ins and sufficient_del and sufficient_comments:
            print(f"PASS: Component 4 -- Sufficient quantities (ins={total_ins}>=6, del={total_del}>=2, comments={comment_count}>=7) (0.2 pts)")
            total_score += 0.2
        elif (total_ins >= 3) and (comment_count >= 3):
            print(f"PARTIAL: Component 4 -- Partial quantities (ins={total_ins}, del={total_del}, comments={comment_count})")
            total_score += 0.1
        else:
            print(f"FAIL: Component 4 -- Insufficient quantities (ins={total_ins}, del={total_del}, comments={comment_count})")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

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

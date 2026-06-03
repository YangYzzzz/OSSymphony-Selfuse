"""
Reward Script: Insert page breaks before Chapter 2 and Chapter 3 headings
Task ID: writer_page_039
Domain: libreoffice_writer
Scoring:
  Component 1: 'Chapter 2: The Journey' heading has page_break_before=True  (0.5 pts)
  Component 2: 'Chapter 3: The Return' heading has page_break_before=True   (0.5 pts)
  Total: 1.0
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_page_039'
FILE_PATH = f'{WORKDIR}/Desktop/short_story_collection.docx'


def verify_task(file_path):
    """
    Verify that page breaks have been inserted before Chapter 2 and Chapter 3 headings.
    Task requires: page_break_before=True on the 'Chapter 2: The Journey' and
    'Chapter 3: The Return' heading paragraphs.
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

    # Build a map: heading text -> paragraph_format.page_break_before
    heading_map = {}
    for para in doc.paragraphs:
        if para.style.name.startswith('Heading'):
            text = para.text.strip()
            heading_map[text] = para.paragraph_format.page_break_before

    print(f"Detected headings and page_break_before flags: {heading_map}")

    # Component 1: 'Chapter 2: The Journey' heading has page_break_before=True (0.5 points)
    # This should FAIL on initial_env (pb=None) and PASS on golden_env (pb=True)
    try:
        ch2_key = None
        for k in heading_map:
            if 'Chapter 2' in k:
                ch2_key = k
                break

        if ch2_key is None:
            print("FAIL: Component 1 — Heading 'Chapter 2' not found in document")
        else:
            pb_ch2 = heading_map[ch2_key]
            if pb_ch2 is True:
                print(f"PASS: Component 1 — '{ch2_key}' has page_break_before=True (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 1 — '{ch2_key}' page_break_before={pb_ch2}, expected True")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'Chapter 3: The Return' heading has page_break_before=True (0.5 points)
    # This should FAIL on initial_env (pb=None) and PASS on golden_env (pb=True)
    try:
        ch3_key = None
        for k in heading_map:
            if 'Chapter 3' in k:
                ch3_key = k
                break

        if ch3_key is None:
            print("FAIL: Component 2 — Heading 'Chapter 3' not found in document")
        else:
            pb_ch3 = heading_map[ch3_key]
            if pb_ch3 is True:
                print(f"PASS: Component 2 — '{ch3_key}' has page_break_before=True (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 2 — '{ch3_key}' page_break_before={pb_ch3}, expected True")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

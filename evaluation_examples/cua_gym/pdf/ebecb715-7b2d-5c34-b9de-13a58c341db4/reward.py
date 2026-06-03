"""
Reward Script: PDF metadata removal and producer update
Task ID: pdf_legal_059
Domain: pdf
Scoring:
  - Component 1 (0.15): Output file exists at correct path
  - Component 2 (0.25): Producer set to 'Law Office Document System'
  - Component 3 (0.15): Author is empty/blank
  - Component 4 (0.15): Creator is empty/blank
  - Component 5 (0.15): Title and Subject are empty/blank
  - Component 6 (0.15): Keywords is empty/blank AND file has content (not corrupted)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_059'

OUTPUT_PATH = os.path.join(WORKDIR, 'legal', 'court_submission_clean.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: output file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
        meta = doc.metadata
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file exists and is a valid PDF with pages (0.15 points)
    # This differentiates from initial_env where clean file does NOT exist
    try:
        page_count = doc.page_count
        if page_count > 0:
            print(f"PASS: Component 1 -- Output file exists with {page_count} page(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Output file has 0 pages")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Producer is 'Law Office Document System' (0.25 points)
    try:
        producer = meta.get('producer', '') or ''
        if producer.strip() == 'Law Office Document System':
            print(f"PASS: Component 2 -- Producer is 'Law Office Document System' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- Expected producer 'Law Office Document System', found: {repr(producer)}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Author is empty/blank (0.15 points)
    try:
        author = meta.get('author', '') or ''
        if author.strip() == '':
            print(f"PASS: Component 3 -- Author is empty (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 -- Expected empty author, found: {repr(author)}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Creator is empty/blank (0.15 points)
    try:
        creator = meta.get('creator', '') or ''
        if creator.strip() == '':
            print(f"PASS: Component 4 -- Creator is empty (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 -- Expected empty creator, found: {repr(creator)}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Title and Subject are both empty/blank (0.15 points)
    try:
        title = meta.get('title', '') or ''
        subject = meta.get('subject', '') or ''
        if title.strip() == '' and subject.strip() == '':
            print(f"PASS: Component 5 -- Title and Subject are empty (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 -- Expected empty title/subject, found title={repr(title)}, subject={repr(subject)}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: Keywords is empty/blank (0.15 points)
    try:
        keywords = meta.get('keywords', '') or ''
        if keywords.strip() == '':
            print(f"PASS: Component 6 -- Keywords is empty (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 -- Expected empty keywords, found: {repr(keywords)}")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)

"""
Reward Script: Verify squiggly underline annotations on PDF page 3
Task ID: pdf_fm_044
Domain: pdf
Scoring:
  - Component 1 (0.3): Exactly 3 Squiggly annotations on page 3 (0-indexed page 2)
  - Component 2 (0.25): Squiggly annotation covers "irregardless of the outcome"
  - Component 3 (0.25): Squiggly annotation covers "could of been"
  - Component 4 (0.2): Squiggly annotation covers "alot of evidence"
"""

import os
import pymupdf  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_044'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'essay_draft.pdf')

# The three phrases that must have squiggly underline annotations on page 3 (0-indexed: 2)
TARGET_PAGE = 2
TARGET_PHRASES = [
    "irregardless of the outcome",
    "could of been",
    "alot of evidence",
]


def check_squiggly_covers_phrase(page, annots_squiggly, phrase):
    """Check if any Squiggly annotation overlaps with the given phrase text on the page."""
    text_rects = page.search_for(phrase)
    if not text_rects:
        print(f"  Text '{phrase}' not found on page {TARGET_PAGE}")
        return False
    for annot in annots_squiggly:
        annot_rect = annot.rect
        for text_rect in text_rects:
            if annot_rect.intersects(text_rect):
                return True
    return False


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: PDF must have at least 3 pages
    if len(doc) < 3:
        print(f"FAIL: PDF has only {len(doc)} pages, need at least 3")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    page = doc[TARGET_PAGE]

    # Collect all annotations on the target page
    all_annots = list(page.annots()) if page.annots() else []
    # Filter to only Squiggly type (type code 10)
    squiggly_annots = [a for a in all_annots if a.type[0] == 10]

    # Component 1: Exactly 3 Squiggly annotations on page 3 (0.3 points)
    try:
        count = len(squiggly_annots)
        if count == 3:
            print(f"PASS: Component 1 — Exactly 3 Squiggly annotations on page 3 (found {count}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Expected 3 Squiggly annotations on page 3, found {count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Squiggly annotation covers "irregardless of the outcome" (0.25 points)
    try:
        phrase = TARGET_PHRASES[0]
        if check_squiggly_covers_phrase(page, squiggly_annots, phrase):
            print(f"PASS: Component 2 — Squiggly covers '{phrase}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — No Squiggly annotation covers '{phrase}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Squiggly annotation covers "could of been" (0.25 points)
    try:
        phrase = TARGET_PHRASES[1]
        if check_squiggly_covers_phrase(page, squiggly_annots, phrase):
            print(f"PASS: Component 3 — Squiggly covers '{phrase}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — No Squiggly annotation covers '{phrase}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Squiggly annotation covers "alot of evidence" (0.2 points)
    try:
        phrase = TARGET_PHRASES[2]
        if check_squiggly_covers_phrase(page, squiggly_annots, phrase):
            print(f"PASS: Component 4 — Squiggly covers '{phrase}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — No Squiggly annotation covers '{phrase}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

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

"""
Reward Script: Redact all email addresses from corporate governance PDF
Task ID: pdf_legal_041
Domain: pdf
Scoring:
  - Component 1 (0.20): Output file exists at expected path
  - Component 2 (0.45): Zero email addresses remain in redacted PDF text
  - Component 3 (0.15): Page count preserved (25 pages)
  - Component 4 (0.20): Redaction marks (black rectangles/drawings) present
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_041'

OUTPUT_PATH = os.path.join(WORKDIR, 'legal', 'corp', 'governance_docs_redacted.pdf')
ORIGINAL_PATH = os.path.join(WORKDIR, 'legal', 'corp', 'governance_docs.pdf')

EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
EXPECTED_PAGES = 25
EXPECTED_EMAIL_COUNT = 18


def verify_task():
    """
    Verify email redaction task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists at correct path (0.20 points)
    # This is a task-introduced change: the redacted file does not exist before the task.
    try:
        if os.path.exists(OUTPUT_PATH) and os.path.getsize(OUTPUT_PATH) > 0:
            print(f"PASS: Component 1 — Output file exists at {OUTPUT_PATH} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Output file not found or empty at {OUTPUT_PATH}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load the redacted PDF
    try:
        import pymupdf
        doc = pymupdf.open(OUTPUT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot load redacted PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Zero email addresses in the redacted PDF (0.45 points)
    # The original has 18 emails; after redaction there should be 0.
    # Progressive: partial credit based on how many were removed.
    try:
        emails_found = []
        for i in range(len(doc)):
            text = doc[i].get_text('text')
            found = EMAIL_PATTERN.findall(text)
            if found:
                emails_found.extend(found)
            # Also check via dict extraction to catch hidden text
            blocks = doc[i].get_text('dict')['blocks']
            for block in blocks:
                if 'lines' in block:
                    for line in block['lines']:
                        for span in line['spans']:
                            found2 = EMAIL_PATTERN.findall(span['text'])
                            if found2:
                                # Deduplicate with text extraction
                                for e in found2:
                                    if e not in emails_found:
                                        emails_found.append(e)

        num_remaining = len(emails_found)
        if num_remaining == 0:
            print(f"PASS: Component 2 — Zero email addresses remain in redacted PDF (0.45 pts)")
            total_score += 0.45
        else:
            # Partial credit: proportional to emails removed
            fraction_removed = max(0, (EXPECTED_EMAIL_COUNT - num_remaining)) / EXPECTED_EMAIL_COUNT
            partial = round(0.45 * fraction_removed, 3)
            print(f"PARTIAL: Component 2 — {num_remaining} emails still present (removed {EXPECTED_EMAIL_COUNT - num_remaining}/{EXPECTED_EMAIL_COUNT}), awarding {partial} pts")
            print(f"  Remaining emails: {emails_found[:5]}...")
            total_score += partial
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Page count preserved at 25 pages (0.15 points)
    try:
        page_count = len(doc)
        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 3 — Page count is {page_count} (expected {EXPECTED_PAGES}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — Page count is {page_count}, expected {EXPECTED_PAGES}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Redaction marks present (black rectangles/drawings) (0.20 points)
    # The golden file has black rectangles drawn over email locations.
    # We check that there are drawings on at least some pages that had emails.
    try:
        pages_with_drawings = 0
        total_black_rects = 0
        for i in range(len(doc)):
            page = doc[i]
            drawings = page.get_drawings()
            # Count filled black rectangles (redaction marks)
            for d in drawings:
                fill = d.get('fill')
                if fill is not None and isinstance(fill, tuple):
                    # Black fill: all components close to 0
                    if all(c <= 0.05 for c in fill):
                        total_black_rects += 1
            if drawings:
                pages_with_drawings += 1

        if total_black_rects >= 1:
            print(f"PASS: Component 4 — Found {total_black_rects} redaction marks across {pages_with_drawings} pages (0.20 pts)")
            total_score += 0.20
        else:
            # Check for redaction annotations as alternative
            annot_count = 0
            for i in range(len(doc)):
                annots = list(doc[i].annots()) if doc[i].annots() else []
                annot_count += len(annots)
            if annot_count > 0:
                print(f"PASS: Component 4 — Found {annot_count} redaction annotations (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — No redaction marks or annotations found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()

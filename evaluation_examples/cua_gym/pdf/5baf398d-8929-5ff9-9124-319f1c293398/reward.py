"""
Reward Script: PDF Processing Pipeline - Merge, page numbers, watermark, metadata, password protection
Task ID: pdf_fm_095
Domain: pdf
Scoring:
  Component 1 (0.20): Page count == 43 (merged correctly from report 25pp + appendix_a 10pp + appendix_b 8pp)
  Component 2 (0.25): Page numbers "Page X of 43" at bottom center on all pages
  Component 3 (0.20): "FINAL VERSION" watermark on page 1 only
  Component 4 (0.20): Metadata title='Project Atlas Final Report', author='Team Alpha'
  Component 5 (0.15): Password-protected with 'Atlas2025!'
"""

import os
import pymupdf  # PyMuPDF (fitz)

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_095'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'project_atlas_final.pdf')
PASSWORD = 'Atlas2025!'


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

    # Try to open the file - it may be encrypted
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # If encrypted, authenticate first so we can inspect content
    is_encrypted = doc.is_encrypted
    auth_ok = False
    if is_encrypted:
        auth_result = doc.authenticate(PASSWORD)
        auth_ok = auth_result > 0
        if not auth_ok:
            print(f"CRITICAL: Cannot authenticate with password '{PASSWORD}'")
            doc.close()
            # We can still give partial credit for encryption existing
            # but we can't verify content, so very limited
            print("REWARD: 0.0")
            return 0.0

    # Component 1: Page count == 43 (0.20 points)
    # Task merges report(25) + appendix_a(10) + appendix_b(8) = 43 pages
    try:
        page_count = doc.page_count
        if page_count == 43:
            print(f"PASS: Component 1 — Page count is 43 (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Expected 43 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Page numbers "Page X of 43" on all pages (0.25 points)
    # Check a sample of pages for "Page X of 43" text
    try:
        pages_with_correct_numbering = 0
        total_pages = doc.page_count
        # Check all pages
        for i in range(total_pages):
            page_text = doc[i].get_text("text")
            expected_label = f"Page {i + 1} of {total_pages}"
            if expected_label in page_text:
                pages_with_correct_numbering += 1

        if total_pages > 0:
            ratio = pages_with_correct_numbering / total_pages
        else:
            ratio = 0.0

        if ratio >= 0.95:
            # All or nearly all pages have correct numbering
            print(f"PASS: Component 2 — {pages_with_correct_numbering}/{total_pages} pages have correct numbering (0.25 pts)")
            total_score += 0.25
        elif ratio >= 0.5:
            # Partial credit: more than half have it
            partial = round(0.25 * ratio, 3)
            print(f"PARTIAL: Component 2 — {pages_with_correct_numbering}/{total_pages} pages have correct numbering ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {pages_with_correct_numbering}/{total_pages} pages have correct 'Page X of {total_pages}' numbering")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: "FINAL VERSION" watermark on page 1 only (0.20 points)
    try:
        page0_text = doc[0].get_text("text")
        has_watermark_p1 = "FINAL VERSION" in page0_text

        # Check that other pages do NOT have the watermark
        watermark_on_other_pages = False
        for i in range(1, min(doc.page_count, 10)):  # Check first 10 pages after page 1
            other_text = doc[i].get_text("text")
            if "FINAL VERSION" in other_text:
                watermark_on_other_pages = True
                break

        if has_watermark_p1 and not watermark_on_other_pages:
            print(f"PASS: Component 3 — 'FINAL VERSION' watermark on page 1 only (0.20 pts)")
            total_score += 0.20
        elif has_watermark_p1 and watermark_on_other_pages:
            # Watermark exists on page 1 but also on others - partial credit
            print(f"PARTIAL: Component 3 — 'FINAL VERSION' found on page 1 but also on other pages (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — 'FINAL VERSION' not found on page 1")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Metadata - title and author (0.20 points)
    try:
        meta = doc.metadata
        title_ok = False
        author_ok = False

        actual_title = (meta.get("title", "") or "").strip()
        actual_author = (meta.get("author", "") or "").strip()

        if actual_title.lower() == "project atlas final report":
            title_ok = True
        if actual_author.lower() == "team alpha":
            author_ok = True

        if title_ok and author_ok:
            print(f"PASS: Component 4 — Metadata title='{actual_title}', author='{actual_author}' (0.20 pts)")
            total_score += 0.20
        elif title_ok or author_ok:
            partial = 0.10
            print(f"PARTIAL: Component 4 — title_ok={title_ok} ('{actual_title}'), author_ok={author_ok} ('{actual_author}') ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Expected title='Project Atlas Final Report', author='Team Alpha'; found title='{actual_title}', author='{actual_author}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Password protection with 'Atlas2025!' (0.15 points)
    # We already checked encryption at the top; now we verify it scores correctly
    try:
        if is_encrypted and auth_ok:
            print(f"PASS: Component 5 — File is password-protected and 'Atlas2025!' works (0.15 pts)")
            total_score += 0.15
        elif is_encrypted and not auth_ok:
            print(f"PARTIAL: Component 5 — File is encrypted but 'Atlas2025!' did not authenticate (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 5 — File is not encrypted")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

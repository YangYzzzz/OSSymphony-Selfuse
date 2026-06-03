"""
Reward Script: OCR scanned deposition transcript to make it searchable
Task ID: pdf_legal_011
Domain: pdf
Scoring:
  Component 1 (0.3): Output PDF has 30 pages with text layer on all pages
  Component 2 (0.3): Extracted text contains meaningful English legal content
  Component 3 (0.2): Sufficient text volume across all pages (OCR quality)
  Component 4 (0.2): Original images preserved on all pages
"""

import os
import sys

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_011'

# Paths
OUTPUT_PATH = os.path.join(WORKDIR, 'legal', 'scanned_deposition_searchable.pdf')
ORIGINAL_PATH = os.path.join(WORKDIR, 'legal', 'scanned_deposition.pdf')


def verify_task():
    """
    Verify that the scanned deposition PDF has been OCR'd into a searchable PDF.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: output file must exist (no points, just a precondition)
    if not os.path.exists(OUTPUT_PATH):
        print(f"CRITICAL: Output file not found: {OUTPUT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("CRITICAL: PyMuPDF (fitz) not available")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = fitz.open(OUTPUT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open output PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = len(doc)

    # Component 1: Output PDF has 30 pages with text layer on all pages (0.3 pts)
    try:
        pages_with_text = 0
        for i in range(page_count):
            text = doc[i].get_text().strip()
            if len(text) > 10:
                pages_with_text += 1

        if page_count == 30 and pages_with_text == 30:
            print(f"PASS: Component 1 — All 30 pages have text layer ({pages_with_text}/30) (0.3 pts)")
            total_score += 0.3
        elif page_count == 30 and pages_with_text >= 25:
            partial = 0.3 * (pages_with_text / 30)
            print(f"PARTIAL: Component 1 — {pages_with_text}/30 pages have text (partial: {partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — Expected 30 pages with text, got {pages_with_text}/{page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Extracted text contains meaningful English legal content (0.3 pts)
    # The deposition is a legal document; OCR should produce recognizable legal terms
    try:
        # Sample pages 0, 1, 14, 29 for legal keywords
        legal_keywords = [
            'court', 'plaintiff', 'defendant', 'deposition', 'witness',
            'attorney', 'counsel', 'case', 'record', 'testimony',
            'objection', 'question', 'answer', 'page', 'exhibit'
        ]
        # Gather text from sampled pages
        sample_pages = [0, 1, 14, 29]
        combined_text = ""
        for pg in sample_pages:
            if pg < page_count:
                combined_text += doc[pg].get_text().lower()

        keyword_hits = sum(1 for kw in legal_keywords if kw in combined_text)

        if keyword_hits >= 8:
            print(f"PASS: Component 2 — {keyword_hits}/{len(legal_keywords)} legal keywords found in sample pages (0.3 pts)")
            total_score += 0.3
        elif keyword_hits >= 4:
            partial = 0.3 * (keyword_hits / 8)
            print(f"PARTIAL: Component 2 — {keyword_hits}/{len(legal_keywords)} legal keywords (partial: {partial:.2f} pts)")
            total_score += min(partial, 0.3)
        else:
            print(f"FAIL: Component 2 — Only {keyword_hits}/{len(legal_keywords)} legal keywords found (need >= 8)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Sufficient text volume across all pages (OCR quality) (0.2 pts)
    # Each page of a deposition transcript should have substantial text
    try:
        total_text_len = 0
        pages_with_sufficient_text = 0
        min_text_per_page = 50  # at least 50 chars per page for meaningful OCR

        for i in range(page_count):
            text = doc[i].get_text().strip()
            total_text_len += len(text)
            if len(text) >= min_text_per_page:
                pages_with_sufficient_text += 1

        # A 30-page deposition should have at least ~15000 chars total
        if pages_with_sufficient_text >= 28 and total_text_len >= 15000:
            print(f"PASS: Component 3 — {pages_with_sufficient_text}/30 pages with sufficient text, total {total_text_len} chars (0.2 pts)")
            total_score += 0.2
        elif pages_with_sufficient_text >= 20 and total_text_len >= 8000:
            partial = 0.2 * min(pages_with_sufficient_text / 28, total_text_len / 15000)
            print(f"PARTIAL: Component 3 — {pages_with_sufficient_text}/30 pages, total {total_text_len} chars (partial: {partial:.2f} pts)")
            total_score += min(partial, 0.2)
        else:
            print(f"FAIL: Component 3 — {pages_with_sufficient_text}/30 pages with sufficient text, total {total_text_len} chars")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Original images preserved on all pages (0.2 pts)
    # The searchable PDF should still contain the original scanned images
    try:
        pages_with_images = 0
        for i in range(page_count):
            images = doc[i].get_images()
            if len(images) > 0:
                pages_with_images += 1

        if pages_with_images == 30:
            print(f"PASS: Component 4 — All 30 pages retain images ({pages_with_images}/30) (0.2 pts)")
            total_score += 0.2
        elif pages_with_images >= 25:
            partial = 0.2 * (pages_with_images / 30)
            print(f"PARTIAL: Component 4 — {pages_with_images}/30 pages retain images (partial: {partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Only {pages_with_images}/30 pages retain images")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

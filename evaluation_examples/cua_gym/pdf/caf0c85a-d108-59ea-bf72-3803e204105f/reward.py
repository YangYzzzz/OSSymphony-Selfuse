"""
Reward Script: Verify PDF wrapping — header + body + footer merge for each doc in wrap_batch/.
Task ID: pdf_adv_182
Domain: pdf

Task: Merge ~/Documents/header_page.pdf (1 page) at the beginning and
      ~/Documents/footer_page.pdf (1 page) at the end of each of the 3 PDFs in
      ~/Documents/wrap_batch/. Save results in ~/Documents/wrap_batch/wrapped/.

Scoring Rubric (total = 1.0):
  Component 1 (0.10): wrapped/ directory exists
  Component 2 (0.10): wrapped/doc1.pdf exists with exactly 6 pages
  Component 3 (0.10): wrapped/doc2.pdf exists with exactly 8 pages
  Component 4 (0.10): wrapped/doc3.pdf exists with exactly 5 pages
  Component 5 (0.15): wrapped/doc1.pdf — first page matches header, last page matches footer
  Component 6 (0.15): wrapped/doc2.pdf — first page matches header, last page matches footer
  Component 7 (0.15): wrapped/doc3.pdf — first page matches header, last page matches footer
  Component 8 (0.15): Inner pages preserved — body content of each wrapped doc matches original
"""

import os
import sys

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

DOCUMENTS_DIR = '/home/user/Documents'
WRAP_BATCH_DIR = '/home/user/Documents/wrap_batch'
WRAPPED_DIR = '/home/user/Documents/wrap_batch/wrapped'
HEADER_PDF = '/home/user/Documents/header_page.pdf'
FOOTER_PDF = '/home/user/Documents/footer_page.pdf'

# Expected page counts for wrapped docs
EXPECTED = {
    'doc1.pdf': {'wrapped_pages': 6, 'body_pages': 4},
    'doc2.pdf': {'wrapped_pages': 8, 'body_pages': 6},
    'doc3.pdf': {'wrapped_pages': 5, 'body_pages': 3},
}


def render_page_text(pdf_path: str, page_index: int) -> str:
    """Extract text from a specific page of a PDF."""
    try:
        doc = pymupdf.open(pdf_path)
        if page_index >= doc.page_count:
            doc.close()
            return ""
        text = doc[page_index].get_text("text")
        doc.close()
        return text.strip()
    except Exception as e:
        print(f"ERROR extracting text from {pdf_path} page {page_index}: {e}")
        return ""


def render_page_image(pdf_path: str, page_index: int, dpi: int = 72):
    """Render a page to a pixmap (for visual comparison)."""
    try:
        doc = pymupdf.open(pdf_path)
        if page_index >= doc.page_count:
            doc.close()
            return None
        mat = pymupdf.Matrix(dpi / 72, dpi / 72)
        pix = doc[page_index].get_pixmap(matrix=mat)
        doc.close()
        return pix
    except Exception:
        return None


def compare_pages_text(path_a: str, page_a: int, path_b: str, page_b: int) -> float:
    """
    Compare two pages by text content similarity.
    Returns 0.0-1.0 similarity score.
    """
    text_a = render_page_text(path_a, page_a)
    text_b = render_page_text(path_b, page_b)

    if not text_a and not text_b:
        # Both pages have no text — try pixel comparison
        pix_a = render_page_image(path_a, page_a)
        pix_b = render_page_image(path_b, page_b)
        if pix_a is None or pix_b is None:
            return 0.0
        if pix_a.width != pix_b.width or pix_a.height != pix_b.height:
            return 0.5
        # Compare sample pixels
        matches = 0
        total = min(len(pix_a.samples), len(pix_b.samples))
        for i in range(0, total, max(1, total // 1000)):
            if pix_a.samples[i] == pix_b.samples[i]:
                matches += 1
        return matches / (total // max(1, total // 1000))

    if not text_a or not text_b:
        return 0.0

    # Text-based similarity: check token overlap
    tokens_a = set(text_a.lower().split())
    tokens_b = set(text_b.lower().split())
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = tokens_a & tokens_b
    union = tokens_a | tokens_b
    jaccard = len(intersection) / len(union) if union else 0.0
    return jaccard


def pages_are_similar(path_a: str, page_a: int, path_b: str, page_b: int, threshold: float = 0.6) -> bool:
    """Return True if two pages are similar enough to be considered the same content."""
    score = compare_pages_text(path_a, page_a, path_b, page_b)
    return score >= threshold


def check_wrapped_doc(doc_name: str, total_score: list) -> float:
    """
    Check a single wrapped document.
    Returns the score earned for this document (page count + header/footer match + body check).
    """
    src_path = f'{WRAP_BATCH_DIR}/{doc_name}'
    dst_path = f'{WRAPPED_DIR}/{doc_name}'
    exp = EXPECTED[doc_name]
    expected_pages = exp['wrapped_pages']
    body_pages = exp['body_pages']
    doc_score = 0.0

    # --- Page count check (0.10 per doc) ---
    try:
        dst_doc = pymupdf.open(dst_path)
        actual_pages = dst_doc.page_count
        dst_doc.close()

        if actual_pages == expected_pages:
            print(f"PASS: {doc_name} has {actual_pages} pages (expected {expected_pages})")
            doc_score += 0.10
        else:
            print(f"FAIL: {doc_name} has {actual_pages} pages, expected {expected_pages}")
            # Still continue with partial checks if page count is close
    except Exception as e:
        print(f"ERROR: Cannot open wrapped/{doc_name}: {e}")
        return 0.0

    # --- Header/footer page check (0.15 per doc) ---
    # Header must be page 0, footer must be last page
    hf_score = 0.0
    try:
        # Check header (page 0 of wrapped == page 0 of header_page.pdf)
        header_match = pages_are_similar(dst_path, 0, HEADER_PDF, 0, threshold=0.5)
        footer_match = pages_are_similar(dst_path, expected_pages - 1, FOOTER_PDF, 0, threshold=0.5)

        if header_match:
            print(f"PASS: {doc_name} first page matches header_page.pdf")
            hf_score += 0.075
        else:
            print(f"FAIL: {doc_name} first page does NOT match header_page.pdf")

        if footer_match:
            print(f"PASS: {doc_name} last page matches footer_page.pdf")
            hf_score += 0.075
        else:
            print(f"FAIL: {doc_name} last page does NOT match footer_page.pdf")

    except Exception as e:
        print(f"ERROR: Header/footer check for {doc_name}: {e}")

    doc_score += hf_score

    return doc_score


def check_body_preservation(doc_name: str) -> float:
    """
    Check that the middle pages of a wrapped doc match the original body doc.
    Returns 0.0-0.05 score.
    """
    src_path = f'{WRAP_BATCH_DIR}/{doc_name}'
    dst_path = f'{WRAPPED_DIR}/{doc_name}'
    exp = EXPECTED[doc_name]
    body_pages = exp['body_pages']
    expected_pages = exp['wrapped_pages']

    if not os.path.exists(src_path) or not os.path.exists(dst_path):
        return 0.0

    try:
        dst_doc = pymupdf.open(dst_path)
        actual_pages = dst_doc.page_count
        dst_doc.close()
        if actual_pages != expected_pages:
            return 0.0

        # Check all body pages (pages 1 through body_pages, i.e. indices 1..body_pages)
        match_count = 0
        for i in range(body_pages):
            src_page = i
            dst_page = i + 1  # offset by 1 for the header
            if pages_are_similar(src_path, src_page, dst_path, dst_page, threshold=0.6):
                match_count += 1

        match_ratio = match_count / body_pages if body_pages > 0 else 0.0
        score = 0.05 * match_ratio
        if match_ratio >= 0.8:
            print(f"PASS: {doc_name} body pages preserved ({match_count}/{body_pages} pages match)")
        else:
            print(f"FAIL: {doc_name} body pages not well preserved ({match_count}/{body_pages} pages match)")
        return score
    except Exception as e:
        print(f"ERROR: Body preservation check for {doc_name}: {e}")
        return 0.0


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: wrapped/ directory exists (0.10)
    try:
        if os.path.isdir(WRAPPED_DIR):
            print(f"PASS: wrapped/ directory exists at {WRAPPED_DIR}")
            total_score += 0.10
        else:
            print(f"FAIL: wrapped/ directory does not exist at {WRAPPED_DIR}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score:.2f}")
            return total_score
    except Exception as e:
        print(f"ERROR: checking wrapped/ directory: {e}")
        print(f"REWARD: 0.00")
        return 0.0

    # Check all three files exist before detailed checks
    missing_files = []
    for doc_name in EXPECTED:
        dst_path = f'{WRAPPED_DIR}/{doc_name}'
        if not os.path.exists(dst_path):
            print(f"FAIL: wrapped/{doc_name} does not exist")
            missing_files.append(doc_name)
        else:
            print(f"INFO: wrapped/{doc_name} found")

    if missing_files:
        # Still count directory existing (0.10 already awarded)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score:.2f}")
        return total_score

    # Verify source header/footer files exist (precondition gate)
    if not os.path.exists(HEADER_PDF):
        print(f"ERROR: header_page.pdf not found at {HEADER_PDF}")
        print(f"REWARD: 0.00")
        return 0.0
    if not os.path.exists(FOOTER_PDF):
        print(f"ERROR: footer_page.pdf not found at {FOOTER_PDF}")
        print(f"REWARD: 0.00")
        return 0.0

    # Components 2–7: Per-document checks (page count + header/footer)
    # Each doc contributes 0.10 (page count) + 0.15 (header/footer) = 0.25
    # Total across 3 docs: 0.75

    for doc_name in ['doc1.pdf', 'doc2.pdf', 'doc3.pdf']:
        doc_score = check_wrapped_doc(doc_name, [total_score])
        total_score += doc_score

    # Component 8: Body content preservation (0.15 total, 0.05 per doc)
    body_score = 0.0
    for doc_name in ['doc1.pdf', 'doc2.pdf', 'doc3.pdf']:
        body_score += check_body_preservation(doc_name)
    total_score += body_score

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task()

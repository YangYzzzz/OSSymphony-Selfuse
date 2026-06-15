"""
Reward Script: Extract pages containing 'adjustment' from journal entries PDF
Task ID: pdf_fin_062
Domain: pdf
Scoring:
  - Component 1 (0.3): Output PDF has exactly 6 pages
  - Component 2 (0.3): All 6 pages contain the word 'adjustment'
  - Component 3 (0.4): Content of output pages matches corresponding source pages (5,12,13,21,28,35)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_062'

SOURCE_FILE = os.path.join(WORKDIR, 'finance', 'journal_entries_2024.pdf')
OUTPUT_FILE = os.path.join(WORKDIR, 'finance', 'adjustment_entries.pdf')

# Expected source page numbers (1-indexed) that contain 'adjustment'
EXPECTED_SOURCE_PAGES = [5, 12, 13, 21, 28, 35]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: output file must exist
    if not os.path.exists(OUTPUT_FILE):
        print(f"CRITICAL: Output file not found: {OUTPUT_FILE}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import fitz
    except ImportError:
        print("CRITICAL: PyMuPDF (fitz) not available")
        print("REWARD: 0.0")
        return 0.0

    try:
        out_doc = fitz.open(OUTPUT_FILE)
    except Exception as e:
        print(f"CRITICAL: Cannot open output PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output PDF has exactly 6 pages (0.3 points)
    try:
        page_count = len(out_doc)
        if page_count == 6:
            print(f"PASS: Component 1 — Output has exactly 6 pages (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Expected 6 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Every page contains the word 'adjustment' (0.3 points)
    try:
        pages_with_adj = 0
        for i in range(len(out_doc)):
            text = out_doc[i].get_text().lower()
            if 'adjustment' in text:
                pages_with_adj += 1
            else:
                print(f"  Page {i+1}: missing 'adjustment'")

        if pages_with_adj == len(out_doc) and len(out_doc) > 0:
            print(f"PASS: Component 2 — All {pages_with_adj} pages contain 'adjustment' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — {pages_with_adj}/{len(out_doc)} pages contain 'adjustment'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Content matches corresponding source pages (0.4 points)
    # Each of the 6 pages should match the text from the expected source page
    try:
        if not os.path.exists(SOURCE_FILE):
            print(f"FAIL: Component 3 — Source file not found: {SOURCE_FILE}")
        else:
            src_doc = fitz.open(SOURCE_FILE)
            matched_pages = 0
            total_expected = len(EXPECTED_SOURCE_PAGES)

            for i, src_page_num in enumerate(EXPECTED_SOURCE_PAGES):
                if i >= len(out_doc):
                    print(f"  Output page {i+1}: missing (output has fewer pages)")
                    continue

                src_idx = src_page_num - 1  # convert to 0-indexed
                if src_idx >= len(src_doc):
                    print(f"  Source page {src_page_num}: out of range")
                    continue

                src_text = src_doc[src_idx].get_text().strip()
                out_text = out_doc[i].get_text().strip()

                if src_text == out_text:
                    matched_pages += 1
                else:
                    # Check partial match (at least 80% of source text present)
                    if len(src_text) > 0 and len(out_text) > 0:
                        # Check if key content overlaps
                        src_lines = set(src_text.split('\n'))
                        out_lines = set(out_text.split('\n'))
                        overlap = len(src_lines & out_lines) / max(len(src_lines), 1)
                        if overlap >= 0.8:
                            matched_pages += 1
                            print(f"  Output page {i+1} vs Source page {src_page_num}: partial match ({overlap:.0%})")
                        else:
                            print(f"  Output page {i+1} vs Source page {src_page_num}: content mismatch (overlap={overlap:.0%})")
                    else:
                        print(f"  Output page {i+1} vs Source page {src_page_num}: content mismatch")

            src_doc.close()

            if matched_pages == total_expected:
                print(f"PASS: Component 3 — All {matched_pages}/{total_expected} pages match source content (0.4 pts)")
                total_score += 0.4
            elif matched_pages > 0:
                partial = 0.4 * (matched_pages / total_expected)
                print(f"PARTIAL: Component 3 — {matched_pages}/{total_expected} pages match ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — 0/{total_expected} pages match source content")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    out_doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_FILE):
    print(f"File not found: {OUTPUT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task()

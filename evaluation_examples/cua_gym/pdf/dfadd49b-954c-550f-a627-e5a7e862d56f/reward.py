"""
Reward Script: Merge quarterly PDFs, add cover page, bookmarks, page numbers, metadata
Task ID: pdf_pw_049
Domain: pdf
Scoring:
  Component 1: File exists with 51 pages (0.2)
  Component 2: Cover page has title and subtitle (0.2)
  Component 3: Bookmarks/TOC match expected entries (0.2)
  Component 4: Page numbers on pages 2-51, none on cover (0.2)
  Component 5: Metadata title and author correct (0.2)
"""

import os
import fitz  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_049'
FILE_PATH = os.path.join(WORKDIR, 'finance', 'annual_financial_2025.pdf')

EXPECTED_PAGE_COUNT = 51
EXPECTED_TOC = [
    [1, 'Q1 Report', 2],
    [1, 'Q2 Report', 14],
    [1, 'Q3 Report', 28],
    [1, 'Q4 Report', 39],
]
EXPECTED_TITLE = 'Annual Financial Report 2025'
EXPECTED_SUBTITLE = 'Fiscal Year Summary'
EXPECTED_META_TITLE = 'Annual Financial Report 2025'
EXPECTED_META_AUTHOR = 'Finance Department'


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

    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Page count is 51 (1 cover + 50 content pages) — 0.2 points
    try:
        pc = doc.page_count
        if pc == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 1 — Page count is {pc} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_PAGE_COUNT} pages, found {pc}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Cover page (page 0) contains title and subtitle — 0.2 points
    try:
        cover_text = doc[0].get_text()
        has_title = EXPECTED_TITLE in cover_text
        has_subtitle = EXPECTED_SUBTITLE in cover_text
        if has_title and has_subtitle:
            print(f"PASS: Component 2 — Cover page has title and subtitle (0.2 pts)")
            total_score += 0.2
        else:
            missing = []
            if not has_title:
                missing.append(f"title '{EXPECTED_TITLE}'")
            if not has_subtitle:
                missing.append(f"subtitle '{EXPECTED_SUBTITLE}'")
            print(f"FAIL: Component 2 — Cover page missing: {', '.join(missing)}")
            # Partial: one of two present
            if has_title or has_subtitle:
                total_score += 0.1
                print(f"  Partial credit: 0.1 pts for one element present")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Bookmarks/TOC match expected entries — 0.2 points
    try:
        toc = doc.get_toc()
        # Check each expected bookmark
        matched = 0
        for expected_entry in EXPECTED_TOC:
            for actual_entry in toc:
                if (actual_entry[0] == expected_entry[0] and
                    actual_entry[1] == expected_entry[1] and
                    actual_entry[2] == expected_entry[2]):
                    matched += 1
                    break
        if matched == len(EXPECTED_TOC):
            print(f"PASS: Component 3 — All {matched} bookmarks correct (0.2 pts)")
            total_score += 0.2
        elif matched > 0:
            partial = round(0.2 * matched / len(EXPECTED_TOC), 2)
            print(f"FAIL: Component 3 — {matched}/{len(EXPECTED_TOC)} bookmarks matched (partial: {partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No matching bookmarks found. TOC: {toc}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Page numbers on pages 2-51 (indices 1-50), none on cover (index 0) — 0.2 points
    try:
        # Check cover has NO page number
        cover_text = doc[0].get_text().strip()
        cover_lines = cover_text.split('\n')
        # Page number would typically be a standalone number at the end
        cover_has_page_num = any(line.strip() == '1' for line in cover_lines)

        # Check a sample of content pages for page numbers
        # Pages 2-51 in document (indices 1-50) should have numbers 2-51
        pages_with_numbers = 0
        sample_indices = [1, 2, 10, 25, 40, 49, 50]  # sample pages
        sample_indices = [i for i in sample_indices if i < doc.page_count]
        for idx in sample_indices:
            page_text = doc[idx].get_text().strip()
            lines = page_text.split('\n')
            expected_num = str(idx + 1)  # page index 1 -> number 2, etc.
            # Check last few lines for the page number
            has_page_num = any(line.strip() == expected_num for line in lines[-5:])
            if has_page_num:
                pages_with_numbers += 1

        no_cover_num = not cover_has_page_num
        pages_ratio = pages_with_numbers / len(sample_indices) if sample_indices else 0

        if no_cover_num and pages_ratio >= 0.8:
            print(f"PASS: Component 4 — No page number on cover, {pages_with_numbers}/{len(sample_indices)} sampled pages have numbers (0.2 pts)")
            total_score += 0.2
        elif pages_ratio >= 0.5:
            partial = round(0.2 * pages_ratio, 2)
            if cover_has_page_num:
                partial = max(partial - 0.05, 0)
            print(f"FAIL: Component 4 — Partial: cover_num={cover_has_page_num}, pages_with_num={pages_with_numbers}/{len(sample_indices)} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — cover_has_num={cover_has_page_num}, pages_with_num={pages_with_numbers}/{len(sample_indices)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Metadata title and author — 0.2 points
    try:
        meta = doc.metadata
        meta_title = meta.get('title', '') or ''
        meta_author = meta.get('author', '') or ''
        title_ok = meta_title.strip() == EXPECTED_META_TITLE
        author_ok = meta_author.strip() == EXPECTED_META_AUTHOR
        if title_ok and author_ok:
            print(f"PASS: Component 5 — Metadata title='{meta_title}', author='{meta_author}' (0.2 pts)")
            total_score += 0.2
        else:
            partial = 0.0
            if title_ok:
                partial += 0.1
            if author_ok:
                partial += 0.1
            print(f"FAIL: Component 5 — title='{meta_title}' (ok={title_ok}), author='{meta_author}' (ok={author_ok}) ({partial} pts)")
            total_score += partial
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

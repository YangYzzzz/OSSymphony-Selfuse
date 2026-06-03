"""
Reward Script: Merge quarterly financial reports with unified header/footer
Task ID: pdf_fin_051
Domain: pdf
Scoring:
  Component 1 (0.25): Merged file exists with 60 pages
  Component 2 (0.25): Content from all 4 quarters preserved in correct order
  Component 3 (0.25): Header "FY2024 Financial Report - NexGen Industries" on every page
  Component 4 (0.25): Footer "Confidential | Page X" with correct page numbering on every page
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_051'
MERGED_PATH = os.path.join(WORKDIR, 'finance', 'fy2024_full_report.pdf')
QUARTERLY_DIR = os.path.join(WORKDIR, 'finance', 'quarterly')

EXPECTED_HEADER = 'FY2024 Financial Report - NexGen Industries'
EXPECTED_TOTAL_PAGES = 60


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid PDF
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Merged file has exactly 60 pages (0.25 points)
    try:
        page_count = doc.page_count
        if page_count == EXPECTED_TOTAL_PAGES:
            print(f"PASS: Component 1 — Page count is {page_count} (expected {EXPECTED_TOTAL_PAGES}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Page count is {page_count}, expected {EXPECTED_TOTAL_PAGES}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Content from all 4 quarters preserved in order (0.25 points)
    # Check that Q1 content appears before Q2, Q2 before Q3, Q3 before Q4
    try:
        quarter_markers = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024']
        first_occurrence_page = {}

        for pg_idx in range(doc.page_count):
            page = doc[pg_idx]
            text = page.get_text('text')
            for marker in quarter_markers:
                if marker in text and marker not in first_occurrence_page:
                    first_occurrence_page[marker] = pg_idx

        all_found = all(m in first_occurrence_page for m in quarter_markers)
        if all_found:
            pages = [first_occurrence_page[m] for m in quarter_markers]
            in_order = all(pages[i] < pages[i+1] for i in range(len(pages) - 1))
            if in_order:
                print(f"PASS: Component 2 — All quarters found in order: {dict(zip(quarter_markers, [p+1 for p in pages]))} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — Quarters not in order: {dict(zip(quarter_markers, [p+1 for p in pages]))}")
        else:
            missing = [m for m in quarter_markers if m not in first_occurrence_page]
            print(f"FAIL: Component 2 — Missing quarter markers: {missing}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Header on every page (0.25 points)
    # Header "FY2024 Financial Report - NexGen Industries" should appear in the top region (y < 50) of every page
    try:
        pages_with_header = 0
        pages_missing_header = []

        for pg_idx in range(doc.page_count):
            page = doc[pg_idx]
            blocks = page.get_text('blocks')
            # Check text blocks in top region (y0 < 50 points from top)
            top_text_blocks = [b for b in blocks if b[1] < 50 and b[6] == 0]
            top_text = ' '.join(b[4].strip() for b in top_text_blocks)

            if EXPECTED_HEADER in top_text:
                pages_with_header += 1
            else:
                pages_missing_header.append(pg_idx + 1)

        if pages_with_header == doc.page_count:
            print(f"PASS: Component 3 — Header found on all {doc.page_count} pages (0.25 pts)")
            total_score += 0.25
        else:
            # Partial: proportional credit if most pages have the header
            ratio = pages_with_header / doc.page_count
            partial = round(0.25 * ratio, 3)
            total_score += partial
            sample_missing = pages_missing_header[:5]
            print(f"PARTIAL: Component 3 — Header on {pages_with_header}/{doc.page_count} pages ({partial} pts). Missing on pages: {sample_missing}{'...' if len(pages_missing_header) > 5 else ''}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Footer with correct page numbers on every page (0.25 points)
    # Footer "Confidential | Page X" where X = 1..60, in bottom region (y1 > page_height - 50)
    try:
        pages_with_correct_footer = 0
        pages_bad_footer = []

        for pg_idx in range(doc.page_count):
            page = doc[pg_idx]
            page_height = page.rect.height
            blocks = page.get_text('blocks')
            # Check text blocks in bottom region
            bot_text_blocks = [b for b in blocks if b[3] > page_height - 50 and b[6] == 0]
            bot_text = ' '.join(b[4].strip() for b in bot_text_blocks)

            expected_footer = f'Confidential | Page {pg_idx + 1}'
            if expected_footer in bot_text:
                pages_with_correct_footer += 1
            else:
                pages_bad_footer.append((pg_idx + 1, bot_text[:80]))

        if pages_with_correct_footer == doc.page_count:
            print(f"PASS: Component 4 — Correct footer on all {doc.page_count} pages (0.25 pts)")
            total_score += 0.25
        else:
            ratio = pages_with_correct_footer / doc.page_count
            partial = round(0.25 * ratio, 3)
            total_score += partial
            sample_bad = pages_bad_footer[:5]
            print(f"PARTIAL: Component 4 — Correct footer on {pages_with_correct_footer}/{doc.page_count} pages ({partial} pts). Bad footers: {sample_bad}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
if not os.path.exists(MERGED_PATH):
    print(f"File not found: {MERGED_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(MERGED_PATH)

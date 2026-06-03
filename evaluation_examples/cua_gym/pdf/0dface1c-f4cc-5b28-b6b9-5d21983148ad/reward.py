"""
Reward Script: Add line numbers to every page of a 12-page PDF
Task ID: pdf_res_032
Domain: pdf
Scoring:
  Component 1 (0.2): Output PDF exists and has 12 pages
  Component 2 (0.4): Line numbers present in left margin on every page
  Component 3 (0.2): Correct every-5th-line numbering pattern (5, 10, 15, ...)
  Component 4 (0.2): Original PDF preserved and output has valid structure
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_032'
OUTPUT_PATH = os.path.join(WORKDIR, 'papers', 'submission_draft_lined.pdf')
ORIGINAL_PATH = os.path.join(WORKDIR, 'papers', 'submission_draft.pdf')
EXPECTED_PAGES = 12
LEFT_MARGIN_THRESHOLD = 72  # points; line numbers should be to the left of main content


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: output file must exist
    if not os.path.exists(OUTPUT_PATH):
        print(f"CRITICAL: Output file not found: {OUTPUT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import fitz
        doc = fitz.open(OUTPUT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open output PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = len(doc)

    # Component 1: Output PDF has 12 pages (0.2 points)
    try:
        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 1 — Output PDF has {page_count} pages (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_PAGES} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Line numbers present in left margin on every page (0.4 points)
    # For each page, check that there are numeric words in the left margin area (x0 < threshold).
    # Award partial credit proportional to how many pages have line numbers.
    try:
        pages_with_line_nums = 0
        for pg_num in range(page_count):
            page = doc[pg_num]
            words = page.get_text('words')
            # Find numeric-only words in the left margin
            left_margin_nums = [w[4] for w in words if w[0] < LEFT_MARGIN_THRESHOLD and w[4].isdigit()]
            if len(left_margin_nums) >= 1:
                pages_with_line_nums += 1

        if page_count > 0:
            ratio = pages_with_line_nums / page_count
        else:
            ratio = 0.0

        comp2_score = 0.4 * ratio
        if pages_with_line_nums == page_count and page_count == EXPECTED_PAGES:
            print(f"PASS: Component 2 — All {page_count} pages have line numbers in left margin (0.4 pts)")
            total_score += 0.4
        elif pages_with_line_nums > 0:
            print(f"PARTIAL: Component 2 — {pages_with_line_nums}/{page_count} pages have line numbers ({comp2_score:.2f} pts)")
            total_score += comp2_score
        else:
            print(f"FAIL: Component 2 — No pages have line numbers in the left margin")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct every-5th-line numbering pattern (0.2 points)
    # Line numbers should be multiples of 5 (5, 10, 15, 20, ...).
    # Check all pages: each page's left-margin numbers should all be multiples of 5.
    try:
        pages_correct_pattern = 0
        for pg_num in range(page_count):
            page = doc[pg_num]
            words = page.get_text('words')
            left_margin_nums = [int(w[4]) for w in words if w[0] < LEFT_MARGIN_THRESHOLD and w[4].isdigit()]
            if len(left_margin_nums) == 0:
                continue
            # Check: all numbers are multiples of 5
            all_multiples_of_5 = all(n % 5 == 0 for n in left_margin_nums)
            # Check: numbers are in ascending order
            is_ascending = left_margin_nums == sorted(left_margin_nums)
            # Check: first number is 5
            starts_at_5 = left_margin_nums[0] == 5
            if all_multiples_of_5 and is_ascending and starts_at_5:
                pages_correct_pattern += 1
            else:
                print(f"  Page {pg_num}: pattern issue — nums={left_margin_nums}, mult5={all_multiples_of_5}, asc={is_ascending}, start5={starts_at_5}")

        if page_count > 0:
            ratio = pages_correct_pattern / page_count
        else:
            ratio = 0.0

        comp3_score = 0.2 * ratio
        if pages_correct_pattern == page_count and page_count == EXPECTED_PAGES:
            print(f"PASS: Component 3 — All {page_count} pages have correct 5th-line numbering pattern (0.2 pts)")
            total_score += 0.2
        elif pages_correct_pattern > 0:
            print(f"PARTIAL: Component 3 — {pages_correct_pattern}/{page_count} pages with correct pattern ({comp3_score:.2f} pts)")
            total_score += comp3_score
        else:
            print(f"FAIL: Component 3 — No pages have the correct numbering pattern")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    # Component 4: Original PDF preserved AND output has line numbers (0.2 points)
    # This combines preservation check with a task-change anchor.
    # The original must still exist, AND the output must have more content (line numbers added).
    try:
        original_exists = os.path.exists(ORIGINAL_PATH)
        if not original_exists:
            print(f"FAIL: Component 4 — Original PDF missing at {ORIGINAL_PATH}")
        else:
            # Verify original is a valid PDF and has expected page count
            try:
                import fitz as fitz2
                orig_doc = fitz2.open(ORIGINAL_PATH)
                orig_pages = len(orig_doc)
                # Check that original does NOT have line numbers in left margin
                orig_page0_words = orig_doc[0].get_text('words')
                orig_left_nums = [w[4] for w in orig_page0_words if w[0] < LEFT_MARGIN_THRESHOLD and w[4].isdigit()]
                orig_doc.close()

                # Output file should be larger than original (line numbers add content)
                output_size = os.path.getsize(OUTPUT_PATH)
                original_size = os.path.getsize(ORIGINAL_PATH)

                if orig_pages == EXPECTED_PAGES and output_size > original_size and len(orig_left_nums) == 0:
                    print(f"PASS: Component 4 — Original preserved ({orig_pages} pages, {original_size} bytes), output larger ({output_size} bytes) with added line numbers (0.2 pts)")
                    total_score += 0.2
                elif orig_pages == EXPECTED_PAGES and output_size > original_size:
                    print(f"PARTIAL: Component 4 — Original preserved but may have been modified")
                    total_score += 0.1
                else:
                    print(f"FAIL: Component 4 — Original pages={orig_pages}, output_size={output_size} vs original_size={original_size}")
            except Exception as e:
                print(f"FAIL: Component 4 — Cannot verify original: {e}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

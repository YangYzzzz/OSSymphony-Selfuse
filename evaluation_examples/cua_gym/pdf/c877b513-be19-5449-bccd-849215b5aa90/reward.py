"""
Reward Script: Create a two-column PDF with Summary and Key Metrics
Task ID: pdf_cr_014
Domain: pdf
Scoring:
  Component 1 (0.15): PDF exists, is valid, has 1 page, A4 portrait
  Component 2 (0.20): 'Summary' title present in left column region (x < 300)
  Component 3 (0.20): 'Key Metrics' title present in right column region (x >= 300)
  Component 4 (0.15): Left column contains Q4 summary body text
  Component 5 (0.15): Right column contains metric bullet items
  Component 6 (0.15): Two-column layout — content in both left and right halves
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_014'
FILE_PATH = os.path.join(WORKDIR, 'Desktop', 'two_column.pdf')

# A4 dimensions in points (tolerance of ~5 pts for rounding)
A4_WIDTH = 595
A4_HEIGHT = 842
SIZE_TOLERANCE = 10

# Column boundary: midpoint of A4 width ~297.5
COLUMN_BOUNDARY = 300


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
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PDF has 1 page, A4 portrait (0.15 points)
    try:
        page_count = doc.page_count
        if page_count < 1:
            print(f"FAIL: Component 1 — PDF has no pages")
        else:
            page = doc[0]
            w, h = page.rect.width, page.rect.height
            is_a4 = (abs(w - A4_WIDTH) <= SIZE_TOLERANCE and abs(h - A4_HEIGHT) <= SIZE_TOLERANCE)
            is_portrait = h > w
            if page_count == 1 and is_a4 and is_portrait:
                print(f"PASS: Component 1 — 1 page, A4 portrait ({w:.0f}x{h:.0f}) (0.15 pts)")
                total_score += 0.15
            else:
                reasons = []
                if page_count != 1:
                    reasons.append(f"page_count={page_count}")
                if not is_a4:
                    reasons.append(f"size={w:.0f}x{h:.0f}, expected ~595x842")
                if not is_portrait:
                    reasons.append("not portrait")
                print(f"FAIL: Component 1 — {', '.join(reasons)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Extract all text spans with positions from page 0
    try:
        page = doc[0]
        blocks = page.get_text('dict')['blocks']
        spans = []
        for b in blocks:
            if 'lines' in b:
                for line in b['lines']:
                    for span in line['spans']:
                        spans.append(span)
    except Exception as e:
        print(f"CRITICAL: Cannot extract text from PDF: {e}")
        doc.close()
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Helper: get spans in a horizontal region
    def spans_in_region(x_min, x_max):
        return [s for s in spans if x_min <= s['origin'][0] < x_max]

    left_spans = spans_in_region(0, COLUMN_BOUNDARY)
    right_spans = spans_in_region(COLUMN_BOUNDARY, A4_WIDTH + 50)

    left_texts = [s['text'] for s in left_spans]
    right_texts = [s['text'] for s in right_spans]

    left_full = ' '.join(left_texts).lower()
    right_full = ' '.join(right_texts).lower()

    # Component 2: 'Summary' title in left column (0.20 points)
    try:
        summary_in_left = any(
            'summary' in s['text'].lower() and s['size'] >= 14
            for s in left_spans
        )
        if summary_in_left:
            print(f"PASS: Component 2 — 'Summary' title found in left column (0.20 pts)")
            total_score += 0.20
        else:
            # Check if Summary is anywhere
            summary_anywhere = any('summary' in s['text'].lower() for s in spans)
            if summary_anywhere:
                print(f"FAIL: Component 2 — 'Summary' found but not in left column or not title-sized")
            else:
                print(f"FAIL: Component 2 — 'Summary' title not found anywhere")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'Key Metrics' title in right column (0.20 points)
    try:
        key_metrics_in_right = any(
            'key metrics' in s['text'].lower() and s['size'] >= 14
            for s in right_spans
        )
        if key_metrics_in_right:
            print(f"PASS: Component 3 — 'Key Metrics' title found in right column (0.20 pts)")
            total_score += 0.20
        else:
            key_metrics_anywhere = any('key metrics' in s['text'].lower() for s in spans)
            if key_metrics_anywhere:
                print(f"FAIL: Component 3 — 'Key Metrics' found but not in right column or not title-sized")
            else:
                print(f"FAIL: Component 3 — 'Key Metrics' title not found anywhere")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Left column body text contains Q4 summary content (0.15 points)
    try:
        has_q4 = 'q4' in left_full
        has_satisfaction = 'satisfaction' in left_full
        has_revenue_word = 'revenue' in left_full or 'record' in left_full
        body_checks = sum([has_q4, has_satisfaction, has_revenue_word])
        if body_checks >= 2:
            print(f"PASS: Component 4 — Left column body text has Q4 summary content (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Left column body missing expected content (q4={has_q4}, satisfaction={has_satisfaction}, revenue/record={has_revenue_word})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Right column contains metric bullet items (0.15 points)
    try:
        has_revenue_metric = 'revenue' in right_full and '4.2m' in right_full
        has_growth = 'growth' in right_full and '23%' in right_full
        has_customers = 'customers' in right_full or '1,250' in right_full or '1250' in right_full
        has_nps = 'nps' in right_full or 'score' in right_full
        metric_checks = sum([has_revenue_metric, has_growth, has_customers, has_nps])
        if metric_checks >= 3:
            print(f"PASS: Component 5 — Right column has metric items ({metric_checks}/4 matched) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — Right column missing metrics (rev={has_revenue_metric}, growth={has_growth}, cust={has_customers}, nps={has_nps})")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Two-column layout — substantive content in both halves (0.15 points)
    try:
        left_content_count = len([s for s in left_spans if len(s['text'].strip()) > 3])
        right_content_count = len([s for s in right_spans if len(s['text'].strip()) > 3])
        if left_content_count >= 3 and right_content_count >= 3:
            print(f"PASS: Component 6 — Two-column layout verified (left={left_content_count}, right={right_content_count} content spans) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 — Insufficient two-column content (left={left_content_count}, right={right_content_count})")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

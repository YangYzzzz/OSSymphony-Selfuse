"""
Reward Script: Add SUPERSEDED watermark and replacement notice to accounting policy PDF
Task ID: pdf_fin_077
Domain: pdf
Scoring:
  Component 1: SUPERSEDED watermark on all 18 pages (0.35 pts)
  Component 2: Watermark style — orange color, ~65pt font (0.25 pts)
  Component 3: Replacement notice text on page 1 (0.25 pts)
  Component 4: Notice style — red color, ~11pt, positioned at top (0.15 pts)
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_077'
OUTPUT_FILE = os.path.join(WORKDIR, 'finance', 'accounting_policy_v2_superseded.pdf')


def get_spans_matching(page, search_text):
    """Get all text spans on a page that contain search_text."""
    data = page.get_text('dict')
    matches = []
    for block in data['blocks']:
        if block['type'] != 0:
            continue
        for line in block['lines']:
            for span in line['spans']:
                if search_text in span['text']:
                    matches.append(span)
    return matches


def color_int_to_rgb(c):
    """Convert PyMuPDF integer color to (R, G, B) 0-255 tuple."""
    return ((c >> 16) & 0xFF, (c >> 8) & 0xFF, c & 0xFF)


def color_close(actual_rgb, expected_rgb, tolerance=40):
    """Check if two RGB tuples are within tolerance."""
    return all(abs(a - e) <= tolerance for a, e in zip(actual_rgb, expected_rgb))


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file exists and is a valid PDF
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = len(doc)
    if page_count != 18:
        print(f"WARNING: Expected 18 pages, found {page_count}")

    # Component 1: SUPERSEDED watermark text present on ALL pages (0.35 points)
    try:
        pages_with_watermark = 0
        for i in range(len(doc)):
            page = doc[i]
            text = page.get_text('text')
            if 'SUPERSEDED' in text:
                pages_with_watermark += 1

        if pages_with_watermark == len(doc) and len(doc) >= 18:
            print(f"PASS: Component 1 — SUPERSEDED watermark found on all {pages_with_watermark}/{len(doc)} pages (0.35 pts)")
            total_score += 0.35
        elif pages_with_watermark > 0:
            # Partial credit: proportional to pages covered
            partial = 0.35 * (pages_with_watermark / max(len(doc), 18))
            print(f"PARTIAL: Component 1 — SUPERSEDED watermark found on {pages_with_watermark}/{len(doc)} pages ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — SUPERSEDED watermark not found on any page")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Watermark style — orange color (~255,128,0), ~65pt size (0.25 points)
    try:
        # Check watermark style on a sample of pages (first, middle, last)
        sample_pages = [0, len(doc) // 2, len(doc) - 1]
        style_pass_count = 0
        for pi in sample_pages:
            if pi >= len(doc):
                continue
            spans = get_spans_matching(doc[pi], 'SUPERSEDED')
            if not spans:
                continue
            span = spans[0]
            rgb = color_int_to_rgb(span['color'])
            size = span['size']
            # Orange is roughly (255, 128, 0) with tolerance
            is_orange = color_close(rgb, (255, 128, 0), tolerance=50)
            # Size should be around 65pt
            size_ok = abs(size - 65.0) < 10.0
            if is_orange and size_ok:
                style_pass_count += 1
            else:
                print(f"  Page {pi}: color={rgb}, size={size:.1f}, orange={is_orange}, size_ok={size_ok}")

        if style_pass_count == len(sample_pages):
            print(f"PASS: Component 2 — Watermark style correct (orange, ~65pt) on all sampled pages (0.25 pts)")
            total_score += 0.25
        elif style_pass_count > 0:
            partial = 0.25 * (style_pass_count / len(sample_pages))
            print(f"PARTIAL: Component 2 — Watermark style correct on {style_pass_count}/{len(sample_pages)} sampled pages ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Watermark style incorrect on all sampled pages")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Replacement notice text on page 1 (0.25 points)
    try:
        page0 = doc[0]
        page0_text = page0.get_text('text')
        notice_keywords = ['replaced', 'Policy v3.0', 'January 1, 2025']
        found_keywords = [kw for kw in notice_keywords if kw in page0_text]

        if len(found_keywords) == len(notice_keywords):
            print(f"PASS: Component 3 — Replacement notice text found on page 1 with all keywords (0.25 pts)")
            total_score += 0.25
        elif len(found_keywords) > 0:
            partial = 0.25 * (len(found_keywords) / len(notice_keywords))
            print(f"PARTIAL: Component 3 — Found {len(found_keywords)}/{len(notice_keywords)} notice keywords ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Replacement notice text not found on page 1")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Notice style — red color (~255,0,0), ~11pt, at top of page (0.15 points)
    try:
        page0 = doc[0]
        # Find spans containing part of the notice
        notice_spans = get_spans_matching(page0, 'replaced')
        if not notice_spans:
            # Try alternative search
            notice_spans = get_spans_matching(page0, 'Policy v3')

        if notice_spans:
            span = notice_spans[0]
            rgb = color_int_to_rgb(span['color'])
            size = span['size']
            bbox_y = span['bbox'][1]  # y0 position (top-left origin)
            page_height = page0.rect.height

            is_red = color_close(rgb, (255, 0, 0), tolerance=40)
            size_ok = abs(size - 11.0) < 3.0
            is_at_top = bbox_y < (page_height * 0.15)  # within top 15% of page

            checks_passed = sum([is_red, size_ok, is_at_top])
            if checks_passed == 3:
                print(f"PASS: Component 4 — Notice style correct: red ({rgb}), {size:.1f}pt, at top y={bbox_y:.1f} (0.15 pts)")
                total_score += 0.15
            elif checks_passed > 0:
                partial = 0.15 * (checks_passed / 3)
                print(f"PARTIAL: Component 4 — Notice style {checks_passed}/3 checks: red={is_red} (rgb={rgb}), size_ok={size_ok} ({size:.1f}pt), top={is_at_top} (y={bbox_y:.1f}) ({partial:.3f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — Notice style all wrong: rgb={rgb}, size={size:.1f}, y={bbox_y:.1f}")
        else:
            print(f"FAIL: Component 4 — Could not find notice text spans to check style")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_FILE):
    print(f"File not found: {OUTPUT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_FILE)

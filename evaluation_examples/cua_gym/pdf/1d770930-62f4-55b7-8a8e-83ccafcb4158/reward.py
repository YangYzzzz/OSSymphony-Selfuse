"""
Reward Script: Scale US Letter PDF to A4 with centered content
Task ID: pdf_fm_079
Domain: pdf
Scoring:
  Component 1 (0.3): Output file exists with correct page count (8 pages)
  Component 2 (0.4): All pages have A4 dimensions (595.28 x 841.89 pts, tolerance ±2)
  Component 3 (0.3): Pages contain text content (original content preserved)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_079'

# A4 dimensions in points (72 pts/inch)
A4_WIDTH = 595.28
A4_HEIGHT = 841.89
TOLERANCE = 2.0  # points tolerance for dimension check

def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    output_path = os.path.join(WORKDIR, 'Documents', 'us_letter_a4.pdf')
    source_path = os.path.join(WORKDIR, 'Documents', 'us_letter.pdf')

    # Precondition: output file must exist
    if not os.path.exists(output_path):
        print(f"CRITICAL: Output file not found: {output_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import fitz
        doc = fitz.open(output_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load output PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file has 8 pages matching the source (0.3 points)
    try:
        page_count = doc.page_count
        if page_count == 8:
            print(f"PASS: Component 1 — Output has {page_count} pages (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Expected 8 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All pages have A4 dimensions (0.4 points)
    # Award partial credit: 0.4 * (pages_with_a4 / total_pages)
    try:
        a4_count = 0
        for i in range(doc.page_count):
            page = doc[i]
            r = page.rect
            width_ok = abs(r.width - A4_WIDTH) <= TOLERANCE
            height_ok = abs(r.height - A4_HEIGHT) <= TOLERANCE
            if width_ok and height_ok:
                a4_count += 1
            else:
                print(f"FAIL: Page {i} dimensions: {r.width:.2f}x{r.height:.2f} (expected ~{A4_WIDTH}x{A4_HEIGHT})")

        if doc.page_count > 0:
            ratio = a4_count / doc.page_count
            points = round(0.4 * ratio, 4)
            if a4_count == doc.page_count:
                print(f"PASS: Component 2 — All {a4_count} pages have A4 dimensions (0.4 pts)")
                total_score += points
            elif a4_count > 0:
                print(f"PARTIAL: Component 2 — {a4_count}/{doc.page_count} pages have A4 dimensions ({points} pts)")
                total_score += points
            else:
                print(f"FAIL: Component 2 — No pages have A4 dimensions")
        else:
            print(f"FAIL: Component 2 — No pages in document")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Pages contain text content (original content preserved) (0.3 points)
    # Check that pages are not blank — text from original should be present
    try:
        # Get reference text from original source if available
        source_texts = []
        if os.path.exists(source_path):
            src_doc = fitz.open(source_path)
            for i in range(src_doc.page_count):
                source_texts.append(src_doc[i].get_text().strip())
            src_doc.close()

        pages_with_content = 0
        pages_matching_source = 0
        for i in range(doc.page_count):
            page = doc[i]
            text = page.get_text().strip()
            if len(text) > 10:
                pages_with_content += 1
                # If we have source texts, check that content is similar
                if i < len(source_texts) and source_texts[i]:
                    # Check that at least some key words from source appear in output
                    source_words = set(source_texts[i].split()[:20])
                    output_words = set(text.split()[:20])
                    overlap = len(source_words & output_words)
                    if overlap >= len(source_words) * 0.3:
                        pages_matching_source += 1

        if source_texts and any(t for t in source_texts):
            # We have source reference — use matching check
            if doc.page_count > 0 and pages_matching_source == doc.page_count:
                print(f"PASS: Component 3 — All {pages_matching_source} pages preserve source content (0.3 pts)")
                total_score += 0.3
            elif doc.page_count > 0 and pages_matching_source > 0:
                points = round(0.3 * pages_matching_source / doc.page_count, 4)
                print(f"PARTIAL: Component 3 — {pages_matching_source}/{doc.page_count} pages match source content ({points} pts)")
                total_score += points
            else:
                print(f"FAIL: Component 3 — No pages match source content")
        else:
            # No source reference — just check pages have content
            if doc.page_count > 0 and pages_with_content == doc.page_count:
                print(f"PASS: Component 3 — All {pages_with_content} pages have text content (0.3 pts)")
                total_score += 0.3
            elif doc.page_count > 0 and pages_with_content > 0:
                points = round(0.3 * pages_with_content / doc.page_count, 4)
                print(f"PARTIAL: Component 3 — {pages_with_content}/{doc.page_count} pages have content ({points} pts)")
                total_score += points
            else:
                print(f"FAIL: Component 3 — No pages have content")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

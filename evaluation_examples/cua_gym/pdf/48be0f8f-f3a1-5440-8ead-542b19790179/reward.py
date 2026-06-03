"""
Reward Script: Highlight author names in references section of NLP survey PDF
Task ID: pdf_res_021
Domain: pdf
Scoring:
  Component 1 (0.15): Output file exists at correct path
  Component 2 (0.35): Green highlight annotations present on all 4 reference pages (12-15)
  Component 3 (0.30): Sufficient number of highlights on each reference page (>=5 per page)
  Component 4 (0.20): No highlight annotations on non-reference pages (pages 1-11)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_021'
OUTPUT_FILE = os.path.join(WORKDIR, 'papers', 'nlp_survey_refs_highlighted.pdf')

# Pages 12-15 in 1-indexed = pages 11-14 in 0-indexed
REF_PAGES = [11, 12, 13, 14]
GREEN_COLOR = (0.0, 1.0, 0.0)
COLOR_TOLERANCE = 0.15
MIN_HIGHLIGHTS_PER_PAGE = 5


def is_green(stroke_color):
    """Check if a stroke color is green within tolerance."""
    if stroke_color is None:
        return False
    if len(stroke_color) < 3:
        return False
    r, g, b = stroke_color[0], stroke_color[1], stroke_color[2]
    return (abs(r - GREEN_COLOR[0]) < COLOR_TOLERANCE and
            abs(g - GREEN_COLOR[1]) < COLOR_TOLERANCE and
            abs(b - GREEN_COLOR[2]) < COLOR_TOLERANCE)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists at correct path (0.15 points)
    try:
        if os.path.exists(OUTPUT_FILE):
            file_size = os.path.getsize(OUTPUT_FILE)
            if file_size > 1000:
                print(f"PASS: Component 1 — Output file exists ({file_size} bytes) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — Output file too small ({file_size} bytes)")
        else:
            print(f"FAIL: Component 1 — Output file not found: {OUTPUT_FILE}")
            # No file means nothing else to check
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Load the PDF
    try:
        import fitz
        doc = fitz.open(OUTPUT_FILE)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {OUTPUT_FILE}: {e}")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Green highlight annotations on all 4 reference pages (0.35 points)
    # Each page contributes 0.35/4 = 0.0875 points
    try:
        pages_with_green_highlights = 0
        for pg_idx in REF_PAGES:
            if pg_idx >= doc.page_count:
                print(f"FAIL: Component 2 — Page {pg_idx} does not exist (doc has {doc.page_count} pages)")
                continue
            page = doc[pg_idx]
            annots = list(page.annots()) if page.annots() else []
            green_highlights = [a for a in annots if a.type[1] == "Highlight" and is_green(a.colors.get("stroke"))]
            if len(green_highlights) > 0:
                pages_with_green_highlights += 1
                print(f"  Page {pg_idx} (1-indexed: {pg_idx+1}): {len(green_highlights)} green highlights found")
            else:
                print(f"  Page {pg_idx} (1-indexed: {pg_idx+1}): No green highlights found")

        if pages_with_green_highlights == 4:
            print(f"PASS: Component 2 — All 4 reference pages have green highlights (0.35 pts)")
            total_score += 0.35
        elif pages_with_green_highlights > 0:
            partial = 0.35 * (pages_with_green_highlights / 4)
            print(f"PARTIAL: Component 2 — {pages_with_green_highlights}/4 reference pages have green highlights ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No reference pages have green highlights")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Sufficient number of highlights per reference page (0.30 points)
    # Each page contributes 0.30/4 = 0.075 points
    try:
        pages_with_sufficient = 0
        for pg_idx in REF_PAGES:
            if pg_idx >= doc.page_count:
                continue
            page = doc[pg_idx]
            annots = list(page.annots()) if page.annots() else []
            green_highlights = [a for a in annots if a.type[1] == "Highlight" and is_green(a.colors.get("stroke"))]
            if len(green_highlights) >= MIN_HIGHLIGHTS_PER_PAGE:
                pages_with_sufficient += 1
                print(f"  Page {pg_idx} (1-indexed: {pg_idx+1}): {len(green_highlights)} >= {MIN_HIGHLIGHTS_PER_PAGE} highlights")
            else:
                print(f"  Page {pg_idx} (1-indexed: {pg_idx+1}): Only {len(green_highlights)} highlights (need >= {MIN_HIGHLIGHTS_PER_PAGE})")

        if pages_with_sufficient == 4:
            print(f"PASS: Component 3 — All reference pages have sufficient highlights (0.30 pts)")
            total_score += 0.30
        elif pages_with_sufficient > 0:
            partial = 0.30 * (pages_with_sufficient / 4)
            print(f"PARTIAL: Component 3 — {pages_with_sufficient}/4 pages have sufficient highlights ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No pages have sufficient highlights")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: No highlight annotations on non-reference pages (0.20 points)
    # This verifies precision — highlights should only be in the references section
    try:
        non_ref_pages_with_highlights = 0
        for pg_idx in range(doc.page_count):
            if pg_idx in REF_PAGES:
                continue
            page = doc[pg_idx]
            annots = list(page.annots()) if page.annots() else []
            highlights = [a for a in annots if a.type[1] == "Highlight"]
            if len(highlights) > 0:
                non_ref_pages_with_highlights += 1
                print(f"  Page {pg_idx} (non-ref): {len(highlights)} unexpected highlights")

        if non_ref_pages_with_highlights == 0:
            print(f"PASS: Component 4 — No highlights on non-reference pages (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — {non_ref_pages_with_highlights} non-reference pages have highlights")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

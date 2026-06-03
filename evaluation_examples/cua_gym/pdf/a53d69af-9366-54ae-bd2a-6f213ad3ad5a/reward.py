"""
Reward Script: Add yellow highlight annotations over every occurrence of 'revenue'
Task ID: pdf_ro_003
Domain: pdf
Scoring:
  Component 1 (0.3): Highlight annotations exist (count >= 18)
  Component 2 (0.3): Highlight count matches revenue text count exactly
  Component 3 (0.2): All highlights are yellow (stroke color ~[1,1,0])
  Component 4 (0.2): Highlights overlap actual 'revenue' text positions
"""

import os
import pymupdf  # PyMuPDF (fitz)

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_003'
OUTPUT_FILE = f'{WORKDIR}/finance/quarterly_highlighted.pdf'
SOURCE_FILE = f'{WORKDIR}/finance/quarterly.pdf'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: output file must exist
    if not os.path.exists(OUTPUT_FILE):
        print(f"CRITICAL: Output file not found: {OUTPUT_FILE}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(OUTPUT_FILE)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {OUTPUT_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Gather data: count highlights and revenue occurrences across all pages
    all_highlights = []
    all_revenue_rects = []
    total_revenue_count = 0

    try:
        for page_num in range(len(doc)):
            page = doc[page_num]

            # Count revenue occurrences (case-insensitive)
            revenue_instances = page.search_for("revenue", flags=1)
            total_revenue_count += len(revenue_instances)
            for rect in revenue_instances:
                all_revenue_rects.append((page_num, rect))

            # Gather highlight annotations
            annot_iter = page.annots()
            if annot_iter:
                for annot in annot_iter:
                    if annot.type[1] == "Highlight":
                        stroke = annot.colors.get("stroke")
                        all_highlights.append({
                            "page": page_num,
                            "rect": annot.rect,
                            "stroke": stroke,
                        })
    except Exception as e:
        print(f"ERROR: Failed to gather annotation data: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    highlight_count = len(all_highlights)
    print(f"INFO: Found {highlight_count} highlight annotations, {total_revenue_count} revenue occurrences")

    # Component 1: Highlight annotations exist — at least 80% of revenue occurrences (0.3 points)
    # This checks that the task was substantially attempted.
    try:
        min_expected = max(1, int(total_revenue_count * 0.8))
        if highlight_count >= min_expected:
            print(f"PASS: Component 1 — {highlight_count} highlights >= {min_expected} minimum (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — {highlight_count} highlights < {min_expected} minimum")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Highlight count matches revenue occurrence count exactly (0.3 points)
    # This verifies completeness — every 'revenue' should have a highlight.
    try:
        if highlight_count == total_revenue_count:
            print(f"PASS: Component 2 — highlight count ({highlight_count}) matches revenue count ({total_revenue_count}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — highlight count ({highlight_count}) != revenue count ({total_revenue_count})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All highlights are yellow — stroke color approximately (1.0, 1.0, 0.0) (0.2 points)
    try:
        if highlight_count == 0:
            print(f"FAIL: Component 3 — no highlights to check color")
        else:
            yellow_count = 0
            for h in all_highlights:
                stroke = h["stroke"]
                if stroke and len(stroke) >= 3:
                    # Check if color is approximately yellow (R~1, G~1, B~0)
                    if abs(stroke[0] - 1.0) < 0.1 and abs(stroke[1] - 1.0) < 0.1 and stroke[2] < 0.15:
                        yellow_count += 1
            if yellow_count == highlight_count:
                print(f"PASS: Component 3 — all {yellow_count} highlights are yellow (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — {yellow_count}/{highlight_count} highlights are yellow")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Highlights overlap actual 'revenue' text positions (0.2 points)
    # For each page, check that every highlight intersects with at least one 'revenue' rect.
    try:
        if highlight_count == 0:
            print(f"FAIL: Component 4 — no highlights to check overlap")
        else:
            overlapping = 0
            for h in all_highlights:
                h_page = h["page"]
                h_rect = h["rect"]
                # Check if this highlight overlaps any revenue rect on the same page
                for (rev_page, rev_rect) in all_revenue_rects:
                    if rev_page == h_page and h_rect.intersects(rev_rect):
                        overlapping += 1
                        break
            if overlapping == highlight_count:
                print(f"PASS: Component 4 — all {overlapping} highlights overlap 'revenue' text (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 — {overlapping}/{highlight_count} highlights overlap 'revenue' text")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

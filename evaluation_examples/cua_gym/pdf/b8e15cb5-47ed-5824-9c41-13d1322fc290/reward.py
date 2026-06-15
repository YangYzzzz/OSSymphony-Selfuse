"""
Reward Script: Tile A3 poster onto 4 A4 pages
Task ID: pdf_gf2_033
Domain: pdf
Scoring:
  - Component 1: Output file has exactly 4 pages (0.25)
  - Component 2: All 4 pages are A4 size (595x842 pts, tolerance 5) (0.25)
  - Component 3: Top-left quadrant page contains expected content (0.15)
  - Component 4: Top-right quadrant page contains expected content (0.15)
  - Component 5: Bottom-left quadrant page contains expected content (0.10)
  - Component 6: Bottom-right quadrant page contains expected content (0.10)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_033'

# A4 dimensions in points
A4_WIDTH = 595.0
A4_HEIGHT = 842.0
SIZE_TOLERANCE = 5.0  # points


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output has exactly 4 pages (0.25 points)
    try:
        page_count = doc.page_count
        if page_count == 4:
            print(f"PASS: Component 1 — page count is 4 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — expected 4 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 4 pages are A4 size ~595x842 pts (0.25 points)
    try:
        if doc.page_count >= 4:
            non_a4_pages = [
                i for i in range(4)
                if abs(doc[i].rect.width - A4_WIDTH) > SIZE_TOLERANCE
                or abs(doc[i].rect.height - A4_HEIGHT) > SIZE_TOLERANCE
            ]
            if len(non_a4_pages) == 0:
                print(f"PASS: Component 2 — all 4 pages are A4 size (0.25 pts)")
                total_score += 0.25
            else:
                for i in non_a4_pages:
                    p = doc[i]
                    print(f"FAIL: Component 2 — Page {i} size ({p.rect.width:.1f}x{p.rect.height:.1f}) not A4 ({A4_WIDTH}x{A4_HEIGHT})")
        else:
            print(f"FAIL: Component 2 — fewer than 4 pages, cannot check sizes")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # For content checks, we verify that text from different quadrants of the
    # original A3 poster appears on the correct tiled pages.
    # The original poster title "Annual Research Symposium 2025" spans the top.
    # Top-left should have the beginning of the title, top-right should have the end.
    # Bottom pages should have different content sections.

    # Component 3: Page 0 (top-left quadrant) contains beginning of title and intro section (0.15 pts)
    try:
        if doc.page_count >= 1:
            text_p0 = doc[0].get_text("text")
            # Top-left should contain start of title (truncated) and "Introduction"
            has_title_start = "Annual Research" in text_p0
            has_intro = "Introduction" in text_p0
            if has_title_start and has_intro:
                print(f"PASS: Component 3 — Page 0 has top-left quadrant content: title start + Introduction (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — Page 0 missing expected top-left content. "
                      f"has_title_start={has_title_start}, has_intro={has_intro}")
        else:
            print(f"FAIL: Component 3 — no pages")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Page 1 (top-right quadrant) contains results table data (0.15 pts)
    try:
        if doc.page_count >= 2:
            text_p1 = doc[1].get_text("text")
            # Top-right quadrant should have "Results" and benchmark data like "GLUE" or "SQuAD"
            has_results = "Results" in text_p1
            has_benchmark = "GLUE" in text_p1 or "SQuAD" in text_p1
            if has_results and has_benchmark:
                print(f"PASS: Component 4 — Page 1 has top-right quadrant content: Results + benchmarks (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — Page 1 missing expected top-right content. "
                      f"has_results={has_results}, has_benchmark={has_benchmark}")
        else:
            print(f"FAIL: Component 4 — fewer than 2 pages")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Page 2 (bottom-left quadrant) contains analysis/discussion section (0.10 pts)
    try:
        if doc.page_count >= 3:
            text_p2 = doc[2].get_text("text")
            # Bottom-left should have "Analysis" or "Discussion"
            has_analysis = "Analysis" in text_p2 or "Discussion" in text_p2
            if has_analysis:
                print(f"PASS: Component 5 — Page 2 has bottom-left quadrant content: Analysis/Discussion (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — Page 2 missing expected bottom-left content. "
                      f"has_analysis={has_analysis}. Text preview: {text_p2[:100]}")
        else:
            print(f"FAIL: Component 5 — fewer than 3 pages")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Page 3 (bottom-right quadrant) contains conclusion section (0.10 pts)
    try:
        if doc.page_count >= 4:
            text_p3 = doc[3].get_text("text")
            # Bottom-right should have "Conclusion"
            has_conclusion = "Conclusion" in text_p3
            if has_conclusion:
                print(f"PASS: Component 6 — Page 3 has bottom-right quadrant content: Conclusion (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 — Page 3 missing expected bottom-right content. "
                      f"has_conclusion={has_conclusion}. Text preview: {text_p3[:100]}")
        else:
            print(f"FAIL: Component 6 — fewer than 4 pages")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/Documents/poster_tiled.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Underline every instance of 'p < 0.05' in stats_analysis.pdf
Task ID: pdf_res_003
Domain: pdf
Scoring:
  Component 1: Page count preserved at 12 (0.15 pts)
  Component 2: Total underline annotation count == 9 (0.35 pts)
  Component 3: Correct page distribution of underline annotations (0.25 pts)
  Component 4: Underline annotations overlap with 'p < 0.05' text positions (0.25 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_003'
OUTPUT_FILE = os.path.join(WORKDIR, 'papers', 'stats_analysis_underlined.pdf')
SOURCE_FILE = os.path.join(WORKDIR, 'papers', 'stats_analysis.pdf')


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
        doc = fitz.open(OUTPUT_FILE)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {OUTPUT_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Page count preserved at 12 (0.15 points)
    # The task should not alter the page count of the document.
    try:
        page_count = doc.page_count
        if page_count == 12:
            print(f"PASS: Component 1 — Page count is 12 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected 12 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Total underline annotation count == 9 (0.35 points)
    # The task requires underlining 9 instances of 'p < 0.05'.
    # Award partial credit: 0.35 * (found / 9), capped at 9.
    try:
        total_underlines = 0
        for i in range(doc.page_count):
            page = doc[i]
            annots = list(page.annots()) if page.annots() else []
            underlines = [a for a in annots if a.type[1] == 'Underline']
            total_underlines += len(underlines)

        if total_underlines == 9:
            print(f"PASS: Component 2 — Found exactly 9 underline annotations (0.35 pts)")
            total_score += 0.35
        elif total_underlines > 0:
            partial = 0.35 * min(total_underlines, 9) / 9
            print(f"PARTIAL: Component 2 — Found {total_underlines} underline annotations, expected 9 ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No underline annotations found, expected 9")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct page distribution of underline annotations (0.25 points)
    # Expected distribution (0-indexed pages): {4: 2, 5: 2, 6: 2, 7: 1, 8: 1, 9: 1}
    try:
        expected_distribution = {4: 2, 5: 2, 6: 2, 7: 1, 8: 1, 9: 1}
        actual_distribution = {}
        for i in range(doc.page_count):
            page = doc[i]
            annots = list(page.annots()) if page.annots() else []
            underlines = [a for a in annots if a.type[1] == 'Underline']
            if underlines:
                actual_distribution[i] = len(underlines)

        matching_pages = 0
        total_expected_pages = len(expected_distribution)
        for pg, count in expected_distribution.items():
            if actual_distribution.get(pg) == count:
                matching_pages += 1

        if matching_pages == total_expected_pages:
            print(f"PASS: Component 3 — All 6 pages have correct underline distribution (0.25 pts)")
            total_score += 0.25
        elif matching_pages > 0:
            partial = 0.25 * matching_pages / total_expected_pages
            print(f"PARTIAL: Component 3 — {matching_pages}/{total_expected_pages} pages match expected distribution ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No pages match expected distribution. Actual: {actual_distribution}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Underline annotations overlap with 'p < 0.05' text positions (0.25 points)
    # Each underline annotation should be positioned over an actual 'p < 0.05' text instance.
    try:
        overlapping = 0
        total_text_instances = 0
        for i in range(doc.page_count):
            page = doc[i]
            text_instances = page.search_for('p < 0.05')
            total_text_instances += len(text_instances)

            annots = list(page.annots()) if page.annots() else []
            underlines = [a for a in annots if a.type[1] == 'Underline']

            for inst in text_instances:
                # Check if any underline annotation intersects this text instance
                for annot in underlines:
                    if annot.rect.intersects(inst):
                        overlapping += 1
                        break

        if total_text_instances > 0 and overlapping == total_text_instances:
            print(f"PASS: Component 4 — All {overlapping} text instances have overlapping underline annotations (0.25 pts)")
            total_score += 0.25
        elif overlapping > 0:
            partial = 0.25 * overlapping / max(total_text_instances, 1)
            print(f"PARTIAL: Component 4 — {overlapping}/{total_text_instances} text instances have overlapping underlines ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No underline annotations overlap with 'p < 0.05' text positions")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

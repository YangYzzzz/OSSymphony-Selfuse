"""
Reward Script: Complete document preparation on prepared_thesis.pdf
Task ID: pdf_adv_200
Domain: pdf

Scoring rubric (total: 1.0):
  Component 1: Title metadata = 'Advanced Machine Learning for Climate Modeling'  (0.15)
  Component 2: Author metadata = 'Dr. Emily Watson'                               (0.10)
  Component 3: All 7 bookmarks present at correct pages                           (0.25)
  Component 4: Page numbers present on all pages (bottom center region)           (0.25)
  Component 5: DRAFT watermark present on all pages (diagonal, light gray)        (0.25)
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user/Documents'
TASK_ID = 'pdf_adv_200'
RESULT_PATH = f'{WORKDIR}/prepared_thesis.pdf'

EXPECTED_BOOKMARKS = [
    (1, "Abstract", 1),
    (1, "Introduction", 3),
    (1, "Literature Review", 8),
    (1, "Methodology", 15),
    (1, "Results", 25),
    (1, "Conclusion", 40),
    (1, "References", 45),
]


def verify_task(file_path: str) -> float:
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: file must exist and be a valid PDF
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

    # Verify page count (gate — wrong page count means something is fundamentally broken)
    if doc.page_count != 50:
        print(f"CRITICAL: Expected 50 pages, got {doc.page_count}. Aborting.")
        doc.close()
        print("REWARD: 0.0")
        return 0.0
    print(f"Gate: 50 pages confirmed")

    meta = doc.metadata

    # -------------------------------------------------------------------------
    # Component 1: Title metadata (0.15 points)
    # -------------------------------------------------------------------------
    try:
        actual_title = (meta.get('title') or '').strip()
        expected_title = 'Advanced Machine Learning for Climate Modeling'
        if actual_title.lower() == expected_title.lower():
            print(f"PASS Component 1: Title metadata correct — '{actual_title}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL Component 1: Title wrong. Expected '{expected_title}', got '{actual_title}'")
    except Exception as e:
        print(f"ERROR Component 1: {e}")

    # -------------------------------------------------------------------------
    # Component 2: Author metadata (0.10 points)
    # -------------------------------------------------------------------------
    try:
        actual_author = (meta.get('author') or '').strip()
        expected_author = 'Dr. Emily Watson'
        if actual_author.lower() == expected_author.lower():
            print(f"PASS Component 2: Author metadata correct — '{actual_author}' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL Component 2: Author wrong. Expected '{expected_author}', got '{actual_author}'")
    except Exception as e:
        print(f"ERROR Component 2: {e}")

    # -------------------------------------------------------------------------
    # Component 3: Bookmarks / TOC (0.25 points)
    # 0.25 if all 7 bookmarks exactly correct; partial credit per bookmark (0.25/7 each)
    # -------------------------------------------------------------------------
    try:
        toc = doc.get_toc()
        if len(toc) == 0:
            print(f"FAIL Component 3: No bookmarks found (expected 7)")
        else:
            correct_bm = 0
            for i, (exp_level, exp_title, exp_page) in enumerate(EXPECTED_BOOKMARKS):
                if i < len(toc):
                    act_level, act_title, act_page = toc[i][0], toc[i][1], toc[i][2]
                    if (act_level == exp_level and
                            act_title.strip() == exp_title and
                            act_page == exp_page):
                        correct_bm += 1
                    else:
                        print(f"  Bookmark {i+1} mismatch: expected ({exp_level},'{exp_title}',p{exp_page}), "
                              f"got ({act_level},'{act_title}',p{act_page})")
                else:
                    print(f"  Bookmark {i+1} missing: expected ({exp_level},'{exp_title}',p{exp_page})")

            bm_score = (correct_bm / 7) * 0.25
            total_score += bm_score
            if correct_bm == 7:
                print(f"PASS Component 3: All 7 bookmarks correct (0.25 pts)")
            else:
                print(f"PARTIAL Component 3: {correct_bm}/7 bookmarks correct "
                      f"({bm_score:.4f} pts) — total toc entries: {len(toc)}")
    except Exception as e:
        print(f"ERROR Component 3: {e}")

    # -------------------------------------------------------------------------
    # Component 4: Page numbers present on all pages (0.25 points)
    # Strategy: check that each page contains its 1-indexed page number as text
    # AND the number appears in the bottom 15% of the page (bottom center region)
    # -------------------------------------------------------------------------
    try:
        pages_with_number = 0
        pages_centered = 0
        sample_pages = list(range(50))  # Check all 50 pages

        for pi in sample_pages:
            page = doc[pi]
            expected_num = str(pi + 1)
            page_h = page.rect.height
            page_w = page.rect.width

            # Find text instances matching the page number
            instances = page.search_for(expected_num)
            if instances:
                pages_with_number += 1
                # Check if any instance is in the bottom 15% and horizontally centered
                for inst in instances:
                    center_x = (inst.x0 + inst.x1) / 2
                    center_y = (inst.y0 + inst.y1) / 2
                    in_bottom = center_y > page_h * 0.80
                    in_center_x = page_w * 0.30 < center_x < page_w * 0.70
                    if in_bottom and in_center_x:
                        pages_centered += 1
                        break

        # Require that all pages have a page number; check centering on most
        coverage_ratio = pages_with_number / 50
        center_ratio = pages_centered / 50

        if pages_with_number == 50 and pages_centered >= 45:
            print(f"PASS Component 4: Page numbers on all 50 pages, centered on {pages_centered}/50 (0.25 pts)")
            total_score += 0.25
        elif pages_with_number >= 45 and pages_centered >= 40:
            partial = 0.20
            print(f"PARTIAL Component 4: Page numbers on {pages_with_number}/50 pages, "
                  f"centered on {pages_centered}/50 ({partial} pts)")
            total_score += partial
        elif pages_with_number >= 30:
            partial = 0.10
            print(f"PARTIAL Component 4: Page numbers on {pages_with_number}/50 pages ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL Component 4: Page numbers found on only {pages_with_number}/50 pages")
    except Exception as e:
        print(f"ERROR Component 4: {e}")

    # -------------------------------------------------------------------------
    # Component 5: DRAFT watermark present on all pages (0.25 points)
    # Strategy: check that each page's text contains "DRAFT"
    # AND optionally verify watermark color is light gray
    # -------------------------------------------------------------------------
    try:
        pages_with_draft = 0
        pages_with_gray = 0

        for pi in range(50):
            page = doc[pi]
            page_text = page.get_text("text")
            if "DRAFT" in page_text:
                pages_with_draft += 1

                # Optional: check color is light gray via text dict
                try:
                    text_data = page.get_text("dict")
                    for block in text_data.get("blocks", []):
                        if block.get("type") != 0:
                            continue
                        for line in block.get("lines", []):
                            for span in line.get("spans", []):
                                if "DRAFT" in span.get("text", ""):
                                    color_int = span.get("color", 0)
                                    r = (color_int >> 16) & 0xFF
                                    g = (color_int >> 8) & 0xFF
                                    b = color_int & 0xFF
                                    # Light gray: all channels > 150 and close together
                                    if r > 150 and g > 150 and b > 150:
                                        pages_with_gray += 1
                                    break
                except Exception:
                    pass

        if pages_with_draft == 50:
            print(f"PASS Component 5: DRAFT watermark found on all 50 pages (0.25 pts)")
            total_score += 0.25
        elif pages_with_draft >= 45:
            partial = 0.20
            print(f"PARTIAL Component 5: DRAFT watermark on {pages_with_draft}/50 pages ({partial} pts)")
            total_score += partial
        elif pages_with_draft >= 30:
            partial = 0.10
            print(f"PARTIAL Component 5: DRAFT watermark on {pages_with_draft}/50 pages ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL Component 5: DRAFT watermark found on only {pages_with_draft}/50 pages")

        if pages_with_gray > 0:
            print(f"  Info: Light gray color verified on {pages_with_gray} pages with DRAFT text")
    except Exception as e:
        print(f"ERROR Component 5: {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore breakdown:")
    print(f"  Component 1 (title metadata):   up to 0.15")
    print(f"  Component 2 (author metadata):  up to 0.10")
    print(f"  Component 3 (7 bookmarks):      up to 0.25")
    print(f"  Component 4 (page numbers):     up to 0.25")
    print(f"  Component 5 (DRAFT watermark):  up to 0.25")
    print(f"Total: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: verify the prepared_thesis.pdf
if not os.path.exists(RESULT_PATH):
    print(f"File not found: {RESULT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(RESULT_PATH)

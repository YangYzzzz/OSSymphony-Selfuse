"""
Reward Script: Rotate all pages of report.pdf 90 degrees clockwise and save as report_rotated.pdf
Task ID: pdf_gf3_001
Domain: pdf
Scoring:
  Component 1: report_rotated.pdf exists and is a valid PDF (0.1 pts)
  Component 2: Rotated PDF has exactly 8 pages (0.15 pts)
  Component 3: All 8 pages have rotation == 90 (0.35 pts)
  Component 4: Page dimensions are swapped to landscape (0.2 pts)
  Component 5: Original report.pdf is unchanged (rotation=0, 8 pages) (0.2 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_001'

ROTATED_PATH = os.path.join(WORKDIR, 'documents', 'report_rotated.pdf')
ORIGINAL_PATH = os.path.join(WORKDIR, 'documents', 'report.pdf')

# Expected original dimensions (portrait A4)
ORIG_WIDTH = 595.0
ORIG_HEIGHT = 842.0
DIM_TOLERANCE = 5.0  # points


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: rotated file must exist
    if not os.path.exists(ROTATED_PATH):
        print(f"CRITICAL: Rotated file not found: {ROTATED_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Try to load the rotated PDF — gate all further checks
    try:
        import fitz
        rotated_doc = fitz.open(ROTATED_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot load rotated PDF {ROTATED_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Rotated PDF is valid and loadable (0.1 pts)
    # This checks the file is not corrupted — only passes if we got past the gate above
    # AND the file has at least 1 page (not an empty PDF)
    try:
        if rotated_doc.page_count > 0:
            print(f"PASS: Component 1 — report_rotated.pdf is a valid PDF with {rotated_doc.page_count} pages (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — report_rotated.pdf has 0 pages")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Rotated PDF has exactly 8 pages (0.15 pts)
    try:
        page_count = rotated_doc.page_count
        if page_count == 8:
            print(f"PASS: Component 2 — Rotated PDF has exactly 8 pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Expected 8 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 8 pages have rotation == 90 degrees (0.35 pts)
    # This is the core task requirement — each page must be rotated 90 CW
    try:
        pages_rotated = 0
        for i in range(rotated_doc.page_count):
            page = rotated_doc[i]
            if page.rotation == 90:
                pages_rotated += 1
            else:
                print(f"  Page {i}: rotation={page.rotation}, expected 90")

        if pages_rotated == rotated_doc.page_count and rotated_doc.page_count == 8:
            print(f"PASS: Component 3 — All 8 pages have rotation=90 (0.35 pts)")
            total_score += 0.35
        elif pages_rotated > 0:
            # Partial credit: proportional to pages rotated correctly
            partial = 0.35 * (pages_rotated / 8)
            print(f"PARTIAL: Component 3 — {pages_rotated}/8 pages rotated correctly ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No pages have rotation=90")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Page dimensions are swapped (landscape after rotation) (0.2 pts)
    # After 90-degree rotation, width and height should swap:
    #   original portrait (595 x 842) -> rotated landscape (842 x 595)
    try:
        pages_correct_dims = 0
        for i in range(rotated_doc.page_count):
            page = rotated_doc[i]
            w, h = page.rect.width, page.rect.height
            # After rotation: width should be ~842, height should be ~595
            if (abs(w - ORIG_HEIGHT) <= DIM_TOLERANCE and
                    abs(h - ORIG_WIDTH) <= DIM_TOLERANCE):
                pages_correct_dims += 1
            else:
                print(f"  Page {i}: dims={w:.1f}x{h:.1f}, expected ~{ORIG_HEIGHT:.1f}x{ORIG_WIDTH:.1f}")

        if pages_correct_dims == 8:
            print(f"PASS: Component 4 — All 8 pages have swapped dimensions (0.2 pts)")
            total_score += 0.2
        elif pages_correct_dims > 0:
            partial = 0.2 * (pages_correct_dims / 8)
            print(f"PARTIAL: Component 4 — {pages_correct_dims}/8 pages have correct dimensions ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No pages have swapped dimensions")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    rotated_doc.close()

    # Component 5: Original report.pdf is unchanged (0.2 pts)
    # Verify original file still has rotation=0 and 8 pages with portrait dims
    try:
        if not os.path.exists(ORIGINAL_PATH):
            print(f"FAIL: Component 5 — Original report.pdf not found (deleted?)")
        else:
            import fitz as fitz2
            orig_doc = fitz2.open(ORIGINAL_PATH)
            issues = []

            if orig_doc.page_count != 8:
                issues.append(f"page count={orig_doc.page_count}, expected 8")

            for i in range(orig_doc.page_count):
                page = orig_doc[i]
                if page.rotation != 0:
                    issues.append(f"page {i} rotation={page.rotation}, expected 0")
                    break
                w, h = page.rect.width, page.rect.height
                if not (abs(w - ORIG_WIDTH) <= DIM_TOLERANCE and abs(h - ORIG_HEIGHT) <= DIM_TOLERANCE):
                    issues.append(f"page {i} dims={w:.1f}x{h:.1f}, expected ~{ORIG_WIDTH:.1f}x{ORIG_HEIGHT:.1f}")
                    break

            orig_doc.close()

            if len(issues) == 0:
                print(f"PASS: Component 5 — Original report.pdf unchanged (8 pages, rotation=0, portrait) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 5 — Original report.pdf was modified: {'; '.join(issues)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

"""
Reward Script: Add colored rectangle annotations around equations in a math PDF
Task ID: pdf_res_029
Domain: pdf
Scoring:
  Component 1: Output file created at correct path (0.1 points)
  Component 2: Rectangle annotations exist across pages 3-8 with >= 10 total (0.35 points)
  Component 3: Annotations have yellow color (stroke = [1,1,0]) (0.25 points)
  Component 4: Annotations span at least 4 of the 6 target pages (3-8) (0.3 points)
"""

import os
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    try:
        import pymupdf as fitz
    except ImportError:
        print("CRITICAL: Neither fitz nor pymupdf available")
        print("REWARD: 0.0")
        sys.exit(0)

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_029'
OUTPUT_PATH = os.path.join(WORKDIR, 'papers', 'math_paper_equations_marked.pdf')

# Pages 3-8 in 1-indexed = pages 2-7 in 0-indexed
TARGET_PAGES_0INDEXED = list(range(2, 8))  # [2, 3, 4, 5, 6, 7]
MIN_TOTAL_ANNOTS = 10
MIN_PAGES_WITH_ANNOTS = 4


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists at the correct path (0.1 points)
    # This is a task-introduced change: initial_env has no output file.
    try:
        if os.path.exists(OUTPUT_PATH) and os.path.getsize(OUTPUT_PATH) > 0:
            print(f"PASS: Component 1 — Output file exists at {OUTPUT_PATH} (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — Output file not found or empty at {OUTPUT_PATH}")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"REWARD: {total_score}")
        return total_score

    # Load the output PDF
    try:
        doc = fitz.open(OUTPUT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {OUTPUT_PATH}: {e}")
        print(f"REWARD: {total_score}")
        return total_score

    # Collect all annotations on target pages (0-indexed pages 2-7)
    page_annot_counts = {}  # page_idx -> list of annots
    all_annots_on_target = []

    try:
        for page_idx in TARGET_PAGES_0INDEXED:
            if page_idx >= doc.page_count:
                continue
            page = doc[page_idx]
            annots = []
            if page.annots():
                for annot in page.annots():
                    # "Square" is the PDF annotation type for rectangles
                    if annot.type[1] in ("Square", "Rectangle"):
                        annots.append({
                            "type": annot.type[1],
                            "rect": tuple(annot.rect),
                            "stroke": annot.colors.get("stroke"),
                            "fill": annot.colors.get("fill"),
                        })
            if annots:
                page_annot_counts[page_idx] = annots
                all_annots_on_target.extend(annots)
    except Exception as e:
        print(f"ERROR: Failed to collect annotations: {e}")

    total_rect_annots = len(all_annots_on_target)
    pages_with_annots = len(page_annot_counts)

    print(f"INFO: Found {total_rect_annots} rectangle annotations across {pages_with_annots} target pages")
    for pidx, annots in sorted(page_annot_counts.items()):
        print(f"  Page {pidx + 1} (0-indexed {pidx}): {len(annots)} rect annotations")

    # Component 2: At least 10 rectangle annotations across pages 3-8 (0.35 points)
    # Progressive: partial credit for fewer annotations
    try:
        if total_rect_annots >= MIN_TOTAL_ANNOTS:
            print(f"PASS: Component 2 — {total_rect_annots} rectangle annotations (>= {MIN_TOTAL_ANNOTS}) (0.35 pts)")
            total_score += 0.35
        elif total_rect_annots >= 5:
            partial = 0.35 * (total_rect_annots / MIN_TOTAL_ANNOTS)
            partial = round(min(partial, 0.35), 2)
            print(f"PARTIAL: Component 2 — {total_rect_annots} annotations (need >= {MIN_TOTAL_ANNOTS}) ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {total_rect_annots} rectangle annotations (need >= {MIN_TOTAL_ANNOTS})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Annotations have yellow color (stroke = [1.0, 1.0, 0.0]) (0.25 points)
    try:
        if total_rect_annots == 0:
            print(f"FAIL: Component 3 — No annotations to check color")
        else:
            yellow_count = 0
            for annot_info in all_annots_on_target:
                stroke = annot_info.get("stroke")
                if stroke is not None:
                    # Check if stroke color is yellow (1.0, 1.0, 0.0) with tolerance
                    if (len(stroke) >= 3
                            and abs(stroke[0] - 1.0) < 0.1
                            and abs(stroke[1] - 1.0) < 0.1
                            and abs(stroke[2] - 0.0) < 0.1):
                        yellow_count += 1

            yellow_ratio = yellow_count / total_rect_annots
            if yellow_ratio >= 0.8:
                print(f"PASS: Component 3 — {yellow_count}/{total_rect_annots} annotations are yellow ({yellow_ratio:.0%}) (0.25 pts)")
                total_score += 0.25
            elif yellow_ratio >= 0.5:
                partial = round(0.25 * yellow_ratio, 2)
                print(f"PARTIAL: Component 3 — {yellow_count}/{total_rect_annots} yellow ({yellow_ratio:.0%}) ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — Only {yellow_count}/{total_rect_annots} annotations are yellow")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Annotations span at least 4 of the 6 target pages (0.3 points)
    try:
        if pages_with_annots >= MIN_PAGES_WITH_ANNOTS:
            print(f"PASS: Component 4 — Annotations on {pages_with_annots} pages (>= {MIN_PAGES_WITH_ANNOTS}) (0.3 pts)")
            total_score += 0.3
        elif pages_with_annots >= 2:
            partial = round(0.3 * (pages_with_annots / MIN_PAGES_WITH_ANNOTS), 2)
            print(f"PARTIAL: Component 4 — Annotations on {pages_with_annots} pages (need >= {MIN_PAGES_WITH_ANNOTS}) ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Annotations on only {pages_with_annots} target pages")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()

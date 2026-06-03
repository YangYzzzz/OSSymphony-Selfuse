"""
Reward Script: Verify ink annotations on pages 3 and 4 of a PDF
Task ID: pdf_res_055
Domain: pdf
Scoring:
  - Component 1: Output file exists and is valid 7-page PDF (0.15)
  - Component 2: Ink annotations on page 3 (0-indexed page 2) (0.25)
  - Component 3: Ink annotations on page 4 (0-indexed page 3) (0.25)
  - Component 4: All ink annotations are blue (0.20)
  - Component 5: Annotations positioned at left margin (0.15)
"""

import os
import fitz  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_055'

OUTPUT_PATH = os.path.join(WORKDIR, 'papers', 'review_copy_marked.pdf')
# Left margin threshold: annotations should have x-coordinates < 100 pts
LEFT_MARGIN_THRESHOLD = 100.0


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists and is a valid 7-page PDF (0.15 points)
    try:
        doc = fitz.open(file_path)
        page_count = doc.page_count
        if page_count == 7:
            print(f"PASS: Component 1 - Valid PDF with {page_count} pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - Expected 7 pages, found {page_count}")
            doc.close()
            # Still continue to check other components
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Helper: collect ink annotations per page
    ink_annots_by_page = {}
    for page_idx in range(doc.page_count):
        page = doc[page_idx]
        ink_annots = []
        if page.annots():
            for annot in page.annots():
                if annot.type[0] == 15:  # Ink annotation type code
                    ink_annots.append({
                        "rect": tuple(annot.rect),
                        "stroke": annot.colors.get("stroke"),
                    })
        ink_annots_by_page[page_idx] = ink_annots

    # Component 2: Ink annotations on page 3 (0-indexed page 2) (0.25 points)
    try:
        page2_inks = ink_annots_by_page.get(2, [])
        if len(page2_inks) >= 1:
            print(f"PASS: Component 2 - Found {len(page2_inks)} ink annotation(s) on page 3 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 - No ink annotations found on page 3 (0-indexed page 2)")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Ink annotations on page 4 (0-indexed page 3) (0.25 points)
    try:
        page3_inks = ink_annots_by_page.get(3, [])
        if len(page3_inks) >= 1:
            print(f"PASS: Component 3 - Found {len(page3_inks)} ink annotation(s) on page 4 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 - No ink annotations found on page 4 (0-indexed page 3)")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: All ink annotations on pages 3 & 4 are blue (0.20 points)
    try:
        all_inks = page2_inks + page3_inks
        if len(all_inks) == 0:
            print(f"FAIL: Component 4 - No ink annotations to check color")
        else:
            # Check each annotation has blue stroke color (0, 0, 1) with tolerance
            non_blue = [ink for ink in all_inks
                        if ink["stroke"] is None
                        or ink["stroke"][0] >= 0.1
                        or ink["stroke"][1] >= 0.1
                        or ink["stroke"][2] <= 0.8]
            if len(non_blue) == 0:
                print(f"PASS: Component 4 - All {len(all_inks)} ink annotations are blue (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 - {len(non_blue)} ink annotation(s) are not blue")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Annotations positioned at left margin (0.15 points)
    try:
        all_inks = page2_inks + page3_inks
        if len(all_inks) == 0:
            print(f"FAIL: Component 5 - No ink annotations to check position")
        else:
            # Check all annotations have x1 (right edge) within left margin threshold
            beyond_margin = [ink for ink in all_inks if ink["rect"][2] > LEFT_MARGIN_THRESHOLD]
            if len(beyond_margin) == 0:
                print(f"PASS: Component 5 - All ink annotations are within left margin (x < {LEFT_MARGIN_THRESHOLD}) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 - {len(beyond_margin)} annotation(s) extend beyond left margin")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)

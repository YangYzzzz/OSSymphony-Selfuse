"""
Reward Script: Add blue highlight annotation over 'Midterm Exam: March 15' on page 8
Task ID: pdf_basic_098
Domain: pdf (Evince / PyMuPDF verification)

Scoring Rubric:
  Component 1: A Highlight annotation exists on page 8 (index 7) — 0.4 pts
  Component 2: The Highlight annotation intersects the 'Midterm Exam: March 15' text — 0.4 pts
  Component 3: The Highlight annotation is blue (stroke color close to (0, 0, 1)) — 0.2 pts
  Total: 1.0 pts

Task requires:
  - The text 'Midterm Exam: March 15' appears on page 8 of ~/Desktop/course_syllabus.pdf
  - Agent should add a blue highlight annotation over this text
  - File should be saved after annotation is added
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_basic_098'
TARGET_PAGE = 7  # page 8, 0-indexed
TARGET_TEXT = 'Midterm Exam: March 15'
PDF_FILE = os.path.join(WORKDIR, 'Desktop', 'course_syllabus.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the PDF — critical precondition gate
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: verify the file has at least 8 pages
    try:
        if doc.page_count < 8:
            print(f"CRITICAL: Expected at least 8 pages, found {doc.page_count}")
            doc.close()
            print("REWARD: 0.0")
            return 0.0
        print(f"INFO: PDF has {doc.page_count} pages — OK")
    except Exception as e:
        print(f"CRITICAL: Cannot read page count: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Get page 8 (0-indexed = 7)
    try:
        page = doc[TARGET_PAGE]
    except Exception as e:
        print(f"CRITICAL: Cannot access page {TARGET_PAGE + 1}: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Locate the target text on page 8
    target_text_rects = []
    try:
        target_text_rects = page.search_for(TARGET_TEXT)
        if not target_text_rects:
            print(f"INFO: Text '{TARGET_TEXT}' not found on page {TARGET_PAGE + 1} (search returned empty)")
        else:
            print(f"INFO: Found '{TARGET_TEXT}' at {target_text_rects[0]} on page {TARGET_PAGE + 1}")
    except Exception as e:
        print(f"WARN: Could not search for target text: {e}")

    # Collect all annotations on page 8
    page_annots = []
    try:
        page_annots = list(page.annots())
    except Exception as e:
        print(f"WARN: Could not read annotations from page {TARGET_PAGE + 1}: {e}")

    # -------------------------------------------------------------------------
    # Component 1: A Highlight annotation exists on page 8 (0.4 pts)
    # This FAILS on initial_env (no annotations) and PASSES on golden_env.
    # -------------------------------------------------------------------------
    highlight_annots = []
    try:
        highlight_annots = [a for a in page_annots if a.type[1] == 'Highlight']
        if highlight_annots:
            print(f"PASS: Component 1 — Found {len(highlight_annots)} Highlight annotation(s) on page 8 (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — No Highlight annotations found on page 8. "
                  f"All annots: {[a.type[1] for a in page_annots]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: The Highlight annotation intersects 'Midterm Exam: March 15' text (0.4 pts)
    # This FAILS on initial_env (no annotations) and PASSES on golden_env.
    # -------------------------------------------------------------------------
    try:
        if not highlight_annots:
            print(f"FAIL: Component 2 — No Highlight annotations to check for text intersection")
        elif not target_text_rects:
            # Fallback: check if the annotation rect is in a reasonable location on the page
            # Based on exploration: text appears near y=119-136 on page 8
            # Use a generous region check
            any_in_region = False
            for annot in highlight_annots:
                arect = annot.rect
                # Text 'Midterm Exam: March 15' is in the top area of page 8
                # From exploration: Rect(72.0, 119.2, 213.4, 135.7)
                # Allow generous ±50pt tolerance
                if (arect.x0 < 280 and arect.y0 < 200 and arect.y1 > 100):
                    any_in_region = True
                    break
            if any_in_region:
                print(f"PASS: Component 2 — Highlight annotation is in region consistent with "
                      f"'Midterm Exam: March 15' text area (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — Highlight annotation rects {[tuple(a.rect) for a in highlight_annots]} "
                      f"do not appear to cover the expected text region")
        else:
            # Check if any highlight intersects with the text location
            text_rect = target_text_rects[0]
            # Use a slightly expanded text rect for tolerance
            expanded_text = pymupdf.Rect(
                text_rect.x0 - 10, text_rect.y0 - 10,
                text_rect.x1 + 10, text_rect.y1 + 10
            )
            intersects = False
            for annot in highlight_annots:
                if annot.rect.intersects(expanded_text):
                    intersects = True
                    print(f"PASS: Component 2 — Highlight at {annot.rect} intersects text "
                          f"'{TARGET_TEXT}' at {text_rect} (0.4 pts)")
                    break
            if intersects:
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — None of the {len(highlight_annots)} highlight annotation(s) "
                      f"intersect '{TARGET_TEXT}' at {text_rect}. "
                      f"Annotation rects: {[tuple(a.rect) for a in highlight_annots]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: The Highlight annotation is blue (0.2 pts)
    # Blue means stroke color close to (0.0, 0.0, 1.0) in PyMuPDF float notation.
    # This FAILS on initial_env (no annotations) and PASSES on golden_env.
    # -------------------------------------------------------------------------
    try:
        if not highlight_annots:
            print(f"FAIL: Component 3 — No Highlight annotations to check for blue color")
        else:
            blue_found = False
            for annot in highlight_annots:
                stroke = annot.colors.get('stroke')
                fill = annot.colors.get('fill')
                # Check stroke color for blue — allow tolerance of 0.15 per channel
                # Blue = (0, 0, 1) in float RGB
                color_to_check = stroke if stroke else fill
                if color_to_check and len(color_to_check) >= 3:
                    r, g, b = color_to_check[0], color_to_check[1], color_to_check[2]
                    is_blue = (b > 0.5 and r < 0.5 and g < 0.5)
                    if is_blue:
                        blue_found = True
                        print(f"PASS: Component 3 — Highlight annotation is blue "
                              f"(stroke={color_to_check}) (0.2 pts)")
                        break
                    else:
                        print(f"INFO: Component 3 — Annotation color {color_to_check} is not blue "
                              f"(expected blue ~ (0, 0, 1))")
                else:
                    # No stroke color set — some tools set color differently
                    # Check if the annotation's appearance stream is blue-ish
                    print(f"INFO: Component 3 — Annotation has no explicit stroke color: "
                          f"colors={annot.colors}")
            if blue_found:
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — No blue Highlight annotation found on page 8. "
                      f"Annotation colors: {[a.colors for a in highlight_annots]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path on the VM
if not os.path.exists(PDF_FILE):
    print(f"File not found: {PDF_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(PDF_FILE)

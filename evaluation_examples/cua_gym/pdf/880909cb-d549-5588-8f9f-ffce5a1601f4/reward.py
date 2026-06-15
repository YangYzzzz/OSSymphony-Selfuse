"""
Reward Script: Add rectangular annotation around 'Emergency Exit' on page 2 with red border
Task ID: pdf_fm_027
Domain: pdf
Scoring:
  Component 1 (0.4): Square/Rectangle annotation exists on page 2 (0-indexed page 1)
  Component 2 (0.3): Annotation has red border (stroke color)
  Component 3 (0.3): Annotation overlaps the 'Emergency Exit' text area
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_027'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'blueprint.pdf')

# Page 2 in the task instruction = page index 1 (0-indexed)
TARGET_PAGE = 1


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

    # Precondition: PDF must have at least 2 pages
    if doc.page_count < 2:
        print(f"FAIL: PDF has only {doc.page_count} pages, need at least 2")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    page = doc[TARGET_PAGE]

    # Collect all annotations on the target page
    annots = []
    if page.annots():
        for annot in page.annots():
            annots.append(annot)

    # Filter for rectangular/square annotations
    # PyMuPDF type codes: 4 = Square, 5 = Circle, 6 = Polygon, etc.
    # "Square" in PyMuPDF corresponds to a rectangle annotation
    rect_annots = [a for a in annots if a.type[0] in (4,)]  # Square type

    # Component 1: A Square/Rectangle annotation exists on page 2 (0.4 points)
    try:
        if len(rect_annots) >= 1:
            print(f"PASS: Component 1 — Found {len(rect_annots)} rectangular annotation(s) on page 2 (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — No rectangular annotations found on page 2. Found {len(annots)} total annotations with types: {[a.type for a in annots]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The annotation has a red border (0.3 points)
    try:
        red_rect_annots = []
        for annot in rect_annots:
            stroke = annot.colors.get("stroke")
            if stroke is not None and len(stroke) >= 3:
                r, g, b = stroke[0], stroke[1], stroke[2]
                # Red means high R, low G, low B (tolerance 0.15)
                if r > 0.7 and g < 0.3 and b < 0.3:
                    red_rect_annots.append(annot)
                    print(f"  Found red-bordered rect annot: stroke=({r:.2f}, {g:.2f}, {b:.2f})")

        if len(red_rect_annots) >= 1:
            print(f"PASS: Component 2 — Found {len(red_rect_annots)} rectangular annotation(s) with red border (0.3 pts)")
            total_score += 0.3
        else:
            # Show what colors were found
            for annot in rect_annots:
                stroke = annot.colors.get("stroke")
                print(f"  Rect annot stroke color: {stroke}")
            print(f"FAIL: Component 2 — No rectangular annotations with red border found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The annotation overlaps the 'Emergency Exit' text area (0.3 points)
    try:
        # Find 'Emergency Exit' text on the page
        text_instances = page.search_for("Emergency Exit")
        if not text_instances:
            print(f"FAIL: Component 3 — 'Emergency Exit' text not found on page 2")
        else:
            # Compute bounding box of all text instances
            text_x0 = min(r.x0 for r in text_instances)
            text_y0 = min(r.y0 for r in text_instances)
            text_x1 = max(r.x1 for r in text_instances)
            text_y1 = max(r.y1 for r in text_instances)
            text_bbox = pymupdf.Rect(text_x0, text_y0, text_x1, text_y1)
            print(f"  'Emergency Exit' text bounding box: {tuple(text_bbox)}")

            # Check if any red rectangular annotation overlaps the text area
            # Use all rect_annots (not just red ones) since Component 2 independently scores color
            overlapping = False
            for annot in rect_annots:
                annot_rect = annot.rect
                if annot_rect.intersects(text_bbox):
                    overlapping = True
                    print(f"  Annotation rect {tuple(annot_rect)} overlaps text bbox")
                    break

            if overlapping:
                print(f"PASS: Component 3 — Rectangular annotation overlaps 'Emergency Exit' text area (0.3 pts)")
                total_score += 0.3
            else:
                for annot in rect_annots:
                    print(f"  Annotation rect: {tuple(annot.rect)} does NOT overlap text bbox {tuple(text_bbox)}")
                print(f"FAIL: Component 3 — No rectangular annotation overlaps the 'Emergency Exit' text area")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

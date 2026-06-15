"""
Reward Script: Add red borders around images in PDF
Task ID: pdf_gf2_045
Domain: pdf
Scoring:
  - Component 1 (0.3): Red rectangle drawings exist, count matches image count (11)
  - Component 2 (0.3): Red borders spatially align with image bounding rects
  - Component 3 (0.2): Border properties correct (2pt width, red color, no fill)
  - Component 4 (0.2): Original content preserved (page count, image count)
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_045'

# Paths
RESULT_PATH = f'{WORKDIR}/Documents/image_report_bordered.pdf'
ORIGINAL_PATH = f'{WORKDIR}/Documents/image_report.pdf'

# Expected values from task context
EXPECTED_PAGES = 6
EXPECTED_TOTAL_IMAGES = 11


def rects_overlap(r1, r2, tolerance=5.0):
    """Check if two rects substantially overlap (within tolerance in points)."""
    return (abs(r1.x0 - r2.x0) <= tolerance and
            abs(r1.y0 - r2.y0) <= tolerance and
            abs(r1.x1 - r2.x1) <= tolerance and
            abs(r1.y1 - r2.y1) <= tolerance)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: output file must exist
    if not os.path.exists(RESULT_PATH):
        print(f"CRITICAL: Output file not found: {RESULT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(RESULT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open result PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all image rects and red rect drawings across pages
    all_image_rects = []  # list of (page_idx, Rect)
    all_red_drawings = []  # list of (page_idx, drawing_dict)
    total_images = 0

    for i in range(doc.page_count):
        page = doc[i]
        images = page.get_images()
        total_images += len(images)

        # Get image bounding rects
        for img in images:
            xref = img[0]
            rects = page.get_image_rects(xref)
            for r in rects:
                all_image_rects.append((i, r))

        # Get red rectangle drawings
        drawings = page.get_drawings()
        for d in drawings:
            color = d.get('color')
            items = d.get('items', [])
            item_types = [it[0] for it in items]
            # Check if this is a red rectangle (not other pre-existing drawings)
            if (color and len(color) >= 3 and
                    abs(color[0] - 1.0) < 0.1 and abs(color[1]) < 0.1 and abs(color[2]) < 0.1 and
                    're' in item_types):
                all_red_drawings.append((i, d))

    # Component 1: Red rectangle drawings exist, count matches image count (0.3 pts)
    try:
        red_count = len(all_red_drawings)
        if red_count >= EXPECTED_TOTAL_IMAGES:
            print(f"PASS: Component 1 - Found {red_count} red rectangles for {EXPECTED_TOTAL_IMAGES} images (0.3 pts)")
            total_score += 0.3
        elif red_count > 0:
            # Partial credit: proportion of borders found
            ratio = red_count / EXPECTED_TOTAL_IMAGES
            pts = round(0.3 * ratio, 2)
            print(f"PARTIAL: Component 1 - Found {red_count}/{EXPECTED_TOTAL_IMAGES} red rectangles ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 1 - No red rectangles found (expected {EXPECTED_TOTAL_IMAGES})")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Red borders spatially align with image bounding rects (0.3 pts)
    try:
        matched = 0
        for (pg_idx, img_rect) in all_image_rects:
            # Find a red drawing on the same page that overlaps this image rect
            for (draw_pg, draw) in all_red_drawings:
                if draw_pg != pg_idx:
                    continue
                draw_rect = draw.get('rect')
                if draw_rect and rects_overlap(pymupdf.Rect(draw_rect), pymupdf.Rect(img_rect), tolerance=5.0):
                    matched += 1
                    break

        if matched >= EXPECTED_TOTAL_IMAGES:
            print(f"PASS: Component 2 - All {matched} borders align with image rects (0.3 pts)")
            total_score += 0.3
        elif matched > 0:
            ratio = matched / EXPECTED_TOTAL_IMAGES
            pts = round(0.3 * ratio, 2)
            print(f"PARTIAL: Component 2 - {matched}/{EXPECTED_TOTAL_IMAGES} borders align ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 2 - No borders align with image rects")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Border properties correct - 2pt width, red, no fill (0.2 pts)
    try:
        correct_props = 0
        for (pg_idx, d) in all_red_drawings:
            color = d.get('color', ())
            width = d.get('width', 0)
            fill = d.get('fill')
            # Check: width ~2pt, red color, no fill
            width_ok = abs(width - 2.0) < 0.5
            color_ok = (len(color) >= 3 and abs(color[0] - 1.0) < 0.05 and
                        abs(color[1]) < 0.05 and abs(color[2]) < 0.05)
            fill_ok = fill is None
            if width_ok and color_ok and fill_ok:
                correct_props += 1

        if len(all_red_drawings) > 0 and correct_props == len(all_red_drawings):
            print(f"PASS: Component 3 - All {correct_props} borders have correct properties (2pt, red, no fill) (0.2 pts)")
            total_score += 0.2
        elif correct_props > 0:
            ratio = correct_props / max(len(all_red_drawings), 1)
            pts = round(0.2 * ratio, 2)
            print(f"PARTIAL: Component 3 - {correct_props}/{len(all_red_drawings)} borders have correct properties ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 3 - No borders with correct properties")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Original content preserved (page count, image count) (0.2 pts)
    try:
        page_ok = doc.page_count == EXPECTED_PAGES
        img_ok = total_images == EXPECTED_TOTAL_IMAGES

        if page_ok and img_ok:
            print(f"PASS: Component 4 - Content preserved: {doc.page_count} pages, {total_images} images (0.2 pts)")
            total_score += 0.2
        else:
            details = []
            if not page_ok:
                details.append(f"pages: expected {EXPECTED_PAGES}, found {doc.page_count}")
            if not img_ok:
                details.append(f"images: expected {EXPECTED_TOTAL_IMAGES}, found {total_images}")
            print(f"FAIL: Component 4 - Content changed: {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

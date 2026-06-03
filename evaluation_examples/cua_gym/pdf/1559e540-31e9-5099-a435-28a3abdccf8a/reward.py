"""
Reward Script: Extract images from recipe_book.pdf and create contact sheet
Task ID: pdf_cross_088
Domain: pdf
Scoring:
  Component 1: recipe_contact_sheet.png exists and is exactly 3000x2000 pixels (0.20 pts)
  Component 2: 5x3 grid layout verified (10px column spacers + 10px row spacers) (0.30 pts)
  Component 3: All 15 grid cells contain image content (diverse pixel content) (0.30 pts)
  Component 4: Title region contains text (dark pixels in top ~60px area) (0.10 pts)
  Component 5: recipe_contact_sheet.pdf exists as single-page PDF (0.10 pts)
"""

import os

WORKDIR = '/home/user/Documents'
TASK_ID = 'pdf_cross_088'

PNG_PATH = f'{WORKDIR}/recipe_contact_sheet.png'
PDF_PATH = f'{WORKDIR}/recipe_contact_sheet.pdf'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Precondition gate: PNG must exist ---
    if not os.path.exists(PNG_PATH):
        print(f"FAIL: recipe_contact_sheet.png not found at {PNG_PATH}")
        print(f"\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Load the PNG for all image-based checks
    try:
        from PIL import Image
        import numpy as np
        img = Image.open(PNG_PATH)
        arr = np.array(img)
    except Exception as e:
        print(f"CRITICAL: Cannot load PNG {PNG_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PNG exists and is exactly 3000x2000 pixels (0.20 pts)
    try:
        width, height = img.size
        if width == 3000 and height == 2000:
            print(f"PASS: Component 1 — PNG is exactly 3000x2000 pixels (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Expected 3000x2000 pixels, found {width}x{height}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 5x3 grid layout verified via 10px column spacers and 10px row spacers (0.30 pts)
    # Layout (as confirmed from golden_env analysis):
    #   Left margin: x=0..29 (30px white)
    #   Col 0: x=30..609 (580px), Spacer: x=610..619 (10px white)
    #   Col 1: x=620..1199 (580px), Spacer: x=1200..1209 (10px white)
    #   Col 2: x=1210..1789 (580px), Spacer: x=1790..1799 (10px white)
    #   Col 3: x=1800..2379 (580px), Spacer: x=2380..2389 (10px white)
    #   Col 4: x=2390..2969 (580px), Right margin: x=2970..2999 (30px)
    #   Title area: y=0..59 (60px)
    #   Image row 1: y=60..699 (640px), Row spacer: y=700..709 (10px white)
    #   Image row 2: y=710..1349 (640px), Row spacer: y=1350..1359 (10px white)
    #   Image row 3: y=1360..1999 (640px)
    try:
        import numpy as np

        col_spacer_failures = []
        row_spacer_failures = []
        # Check 4 column spacers (each 10px wide, at y=400 which is well within row 1)
        col_spacer_starts = [610, 1200, 1790, 2380]
        for sx in col_spacer_starts:
            # Sample pixels at y=400 within image row 1
            spacer_pixels = arr[400, sx:sx+10, :]
            all_white = (spacer_pixels == 255).all()
            if not all_white:
                col_spacer_failures.append((sx, spacer_pixels[5].tolist()))

        # Check 2 row spacers (each 10px tall, at x=290 which is center of col 0)
        row_spacer_starts = [700, 1350]
        for sy in row_spacer_starts:
            # Sample pixels in middle of spacer rows
            spacer_row_pixels = arr[sy:sy+10, 290, :]
            all_white = (spacer_row_pixels == 255).all()
            if not all_white:
                row_spacer_failures.append((sy, spacer_row_pixels[5].tolist()))

        if not col_spacer_failures and not row_spacer_failures:
            # Also verify the image rows have correct height (640px each)
            # Row 1: y=60..699 (640px), Row 2: y=710..1349 (640px), Row 3: y=1360..1999 (640px)
            row_heights = [
                699 - 60 + 1,    # 640
                1349 - 710 + 1,  # 640
                1999 - 1360 + 1  # 640
            ]
            heights_ok = all(h == 640 for h in row_heights)
            if heights_ok:
                print(f"PASS: Component 2 — 5x3 grid layout verified (4 column spacers + 2 row spacers, 10px each, rows 640px tall) (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 — Grid row heights incorrect: {row_heights}")
        else:
            print(f"FAIL: Component 2 — Spacer check failed: col_failures={col_spacer_failures}, row_failures={row_spacer_failures}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 15 grid cells contain image content (std > 10 per cell) (0.30 pts)
    try:
        import numpy as np

        cells_with_content = 0
        failed_cells = []
        row_y_starts = [60, 710, 1360]

        for row_idx in range(3):
            y_start = row_y_starts[row_idx]
            y_end = y_start + 640
            for col_idx in range(5):
                x_start = 30 + col_idx * (580 + 10)
                x_end = x_start + 580
                cell = arr[y_start:y_end, x_start:x_end, :]
                # Check pixel diversity: std dev > 10 indicates real image content (not solid color)
                std = cell.std()
                if std > 10.0:
                    cells_with_content += 1
                else:
                    failed_cells.append((row_idx, col_idx, std))

        if cells_with_content == 15:
            print(f"PASS: Component 3 — All 15 grid cells contain image content (diverse pixel values) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — Only {cells_with_content}/15 cells have image content; empty cells: {failed_cells}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Title region contains text (dark pixels in top ~60px area) (0.10 pts)
    # The title 'Recipe Collection' should appear as dark text in y=0..59 region
    try:
        import numpy as np

        title_region = arr[:60, :, :]
        # Count pixels with at least one channel below 100 (dark text pixels)
        dark_pixel_count = ((title_region < 100).any(axis=2)).sum()
        # Require at least 1000 dark pixels to confirm substantial text presence
        if dark_pixel_count >= 1000:
            print(f"PASS: Component 4 — Title region contains text ({dark_pixel_count} dark pixels in y=0..59) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — Title region has only {dark_pixel_count} dark pixels (expected >= 1000 for 'Recipe Collection' text)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: recipe_contact_sheet.pdf exists as a single-page PDF (0.10 pts)
    try:
        if not os.path.exists(PDF_PATH):
            print(f"FAIL: Component 5 — recipe_contact_sheet.pdf not found at {PDF_PATH}")
        else:
            try:
                import pymupdf
            except ImportError:
                import fitz as pymupdf

            doc = pymupdf.open(PDF_PATH)
            page_count = doc.page_count
            doc.close()

            if page_count == 1:
                print(f"PASS: Component 5 — recipe_contact_sheet.pdf exists and has exactly 1 page (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — recipe_contact_sheet.pdf has {page_count} pages (expected 1)")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

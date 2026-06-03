"""
Reward Script: Convert first 3 PDF pages to 300 DPI PNG images
Task ID: pdf_res_085
Domain: pdf
Scoring:
  Component 1 (0.3): Three correctly named PNG files exist in slides/
  Component 2 (0.4): Images have correct dimensions for 300 DPI rendering
  Component 3 (0.3): DPI metadata is approximately 300
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_085'
PDF_PATH = os.path.join(WORKDIR, 'papers', 'presentation_slides.pdf')
SLIDES_DIR = os.path.join(WORKDIR, 'papers', 'slides')
EXPECTED_FILES = ['slide_1.png', 'slide_2.png', 'slide_3.png']


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: source PDF must exist
    if not os.path.exists(PDF_PATH):
        print(f"CRITICAL: Source PDF not found at {PDF_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Get expected dimensions from the source PDF
    try:
        import fitz
        doc = fitz.open(PDF_PATH)
        page_dims = []
        for i in range(min(3, len(doc))):
            page = doc[i]
            r = page.rect
            # At 300 DPI: pixels = points * 300 / 72
            expected_w = round(r.width * 300 / 72)
            expected_h = round(r.height * 300 / 72)
            page_dims.append((expected_w, expected_h))
        doc.close()
        print(f"PDF page dimensions (300 DPI): {page_dims}")
    except Exception as e:
        print(f"CRITICAL: Cannot read source PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Three correctly named PNG files exist in slides/ (0.3 points)
    # This checks task-introduced changes: the slides dir and files don't exist in initial_env
    try:
        if not os.path.isdir(SLIDES_DIR):
            print(f"FAIL: Component 1 - slides directory does not exist at {SLIDES_DIR}")
        else:
            found_count = 0
            for fname in EXPECTED_FILES:
                fpath = os.path.join(SLIDES_DIR, fname)
                if os.path.isfile(fpath) and os.path.getsize(fpath) > 0:
                    found_count += 1
                else:
                    print(f"FAIL: Component 1 - {fname} missing or empty")

            if found_count == 3:
                print(f"PASS: Component 1 - All 3 PNG files exist in slides/ (0.3 pts)")
                total_score += 0.3
            elif found_count > 0:
                partial = round(0.3 * found_count / 3, 2)
                print(f"PARTIAL: Component 1 - {found_count}/3 files found ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 1 - No expected PNG files found in slides/")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Images have correct pixel dimensions for 300 DPI (0.4 points)
    # Expected: each image matches the PDF page rendered at 300 DPI
    try:
        from PIL import Image
        dim_pass = 0
        for i, fname in enumerate(EXPECTED_FILES):
            fpath = os.path.join(SLIDES_DIR, fname)
            if not os.path.isfile(fpath):
                print(f"FAIL: Component 2 - {fname} not found, cannot check dimensions")
                continue
            img = Image.open(fpath)
            actual_w, actual_h = img.size
            expected_w, expected_h = page_dims[i]
            # Allow small tolerance (2 pixels) for rounding differences
            if abs(actual_w - expected_w) <= 2 and abs(actual_h - expected_h) <= 2:
                print(f"PASS: Component 2 - {fname} dimensions {actual_w}x{actual_h} match expected {expected_w}x{expected_h}")
                dim_pass += 1
            else:
                print(f"FAIL: Component 2 - {fname} dimensions {actual_w}x{actual_h} != expected {expected_w}x{expected_h}")
            img.close()

        if dim_pass == 3:
            print(f"PASS: Component 2 - All 3 images have correct 300 DPI dimensions (0.4 pts)")
            total_score += 0.4
        elif dim_pass > 0:
            partial = round(0.4 * dim_pass / 3, 2)
            print(f"PARTIAL: Component 2 - {dim_pass}/3 images correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - No images have correct dimensions")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: DPI metadata is approximately 300 (0.3 points)
    # Verifies the images were rendered at the requested 300 DPI resolution
    try:
        from PIL import Image
        dpi_pass = 0
        for fname in EXPECTED_FILES:
            fpath = os.path.join(SLIDES_DIR, fname)
            if not os.path.isfile(fpath):
                print(f"FAIL: Component 3 - {fname} not found, cannot check DPI")
                continue
            img = Image.open(fpath)
            dpi_info = img.info.get('dpi', None)
            img.close()
            if dpi_info is not None:
                dpi_x, dpi_y = dpi_info
                # Allow tolerance: 290-310 DPI
                if 290 <= dpi_x <= 310 and 290 <= dpi_y <= 310:
                    print(f"PASS: Component 3 - {fname} DPI ({dpi_x:.1f}, {dpi_y:.1f}) is ~300")
                    dpi_pass += 1
                else:
                    print(f"FAIL: Component 3 - {fname} DPI ({dpi_x:.1f}, {dpi_y:.1f}) not ~300")
            else:
                print(f"FAIL: Component 3 - {fname} has no DPI metadata")

        if dpi_pass == 3:
            print(f"PASS: Component 3 - All 3 images have ~300 DPI metadata (0.3 pts)")
            total_score += 0.3
        elif dpi_pass > 0:
            partial = round(0.3 * dpi_pass / 3, 2)
            print(f"PARTIAL: Component 3 - {dpi_pass}/3 images have correct DPI ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 - No images have correct DPI metadata")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

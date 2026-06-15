"""
Reward Script: Convert PDF pages to high-resolution TIFF images
Task ID: pdf_mbc_076
Domain: pdf
Scoring:
  Component 1 (0.2): tiff_output directory exists with exactly 4 files
  Component 2 (0.2): Files named blueprint_001.tiff through blueprint_004.tiff
  Component 3 (0.2): All files are valid TIFF format with RGB mode
  Component 4 (0.2): All files have 600 DPI resolution
  Component 5 (0.2): TIFF pixel dimensions consistent with 600 DPI rendering of source PDF
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_076'
TIFF_DIR = os.path.join(WORKDIR, 'Documents', 'tiff_output')
PDF_PATH = os.path.join(WORKDIR, 'Documents', 'blueprints.pdf')
EXPECTED_FILES = [f'blueprint_{i:03d}.tiff' for i in range(1, 5)]
EXPECTED_DPI = 600
NUM_PAGES = 4


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

    # Component 1: tiff_output directory exists with exactly 4 files (0.2 points)
    try:
        if os.path.isdir(TIFF_DIR):
            files_in_dir = os.listdir(TIFF_DIR)
            if len(files_in_dir) == NUM_PAGES:
                print(f"PASS: Component 1 -- tiff_output dir exists with {len(files_in_dir)} files (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 -- tiff_output has {len(files_in_dir)} files, expected {NUM_PAGES}")
        else:
            print(f"FAIL: Component 1 -- tiff_output directory does not exist at {TIFF_DIR}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Correct file naming (0.2 points)
    try:
        if os.path.isdir(TIFF_DIR):
            actual_files = sorted(os.listdir(TIFF_DIR))
            if actual_files == sorted(EXPECTED_FILES):
                print(f"PASS: Component 2 -- All files correctly named: {actual_files} (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 -- Expected {sorted(EXPECTED_FILES)}, found {actual_files}")
        else:
            print(f"FAIL: Component 2 -- tiff_output directory does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Valid TIFF format with RGB mode (0.2 points)
    try:
        from PIL import Image
        valid_count = 0
        for fname in EXPECTED_FILES:
            fpath = os.path.join(TIFF_DIR, fname)
            if not os.path.exists(fpath):
                print(f"FAIL: Component 3 -- File missing: {fname}")
                break
            img = Image.open(fpath)
            if img.format != 'TIFF':
                print(f"FAIL: Component 3 -- {fname} format is {img.format}, expected TIFF")
                img.close()
                break
            if img.mode not in ('RGB', 'RGBA'):
                print(f"FAIL: Component 3 -- {fname} mode is {img.mode}, expected RGB/RGBA")
                img.close()
                break
            img.close()
            valid_count += 1
        if valid_count == NUM_PAGES:
            print(f"PASS: Component 3 -- All 4 files are valid TIFF with correct color mode (0.2 pts)")
            total_score += 0.2
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: 600 DPI resolution (0.2 points)
    try:
        from PIL import Image
        dpi_ok_count = 0
        for fname in EXPECTED_FILES:
            fpath = os.path.join(TIFF_DIR, fname)
            if not os.path.exists(fpath):
                break
            img = Image.open(fpath)
            dpi = img.info.get('dpi', (0, 0))
            img.close()
            # Allow small tolerance for DPI (within 1%)
            if not (abs(dpi[0] - EXPECTED_DPI) < 6 and abs(dpi[1] - EXPECTED_DPI) < 6):
                print(f"FAIL: Component 4 -- {fname} DPI is {dpi}, expected ~({EXPECTED_DPI}, {EXPECTED_DPI})")
                break
            dpi_ok_count += 1
        if dpi_ok_count == NUM_PAGES:
            print(f"PASS: Component 4 -- All files have {EXPECTED_DPI} DPI (0.2 pts)")
            total_score += 0.2
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Pixel dimensions consistent with 600 DPI from A4 PDF (0.2 points)
    # A4 at 72 pts: 595x842. At 600 DPI: (595/72)*600 x (842/72)*600 = ~4958 x 7017
    try:
        from PIL import Image
        import pymupdf
        doc = pymupdf.open(PDF_PATH)
        dims_ok_count = 0
        for i, fname in enumerate(EXPECTED_FILES):
            fpath = os.path.join(TIFF_DIR, fname)
            if not os.path.exists(fpath):
                break
            img = Image.open(fpath)
            w, h = img.size
            img.close()
            # Expected dimensions from PDF page at 600 DPI
            page = doc[i]
            expected_w = int(page.rect.width / 72 * EXPECTED_DPI)
            expected_h = int(page.rect.height / 72 * EXPECTED_DPI)
            # Allow small tolerance (within 2 pixels)
            if abs(w - expected_w) > 2 or abs(h - expected_h) > 2:
                print(f"FAIL: Component 5 -- {fname} size is {w}x{h}, expected ~{expected_w}x{expected_h}")
                break
            dims_ok_count += 1
        doc.close()
        if dims_ok_count == NUM_PAGES:
            print(f"PASS: Component 5 -- All TIFF dimensions match 600 DPI rendering of PDF pages (0.2 pts)")
            total_score += 0.2
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

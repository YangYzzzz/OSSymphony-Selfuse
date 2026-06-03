"""
Reward Script: Export slides 1, 5, and 10 as individual PNG images at 300 DPI
Task ID: impress_rp_035
Domain: libreoffice_impress
Scoring:
  Component 1 (0.30): All three PNG files exist with correct names
  Component 2 (0.30): Images are high resolution (>=3000px wide, indicating ~300 DPI)
  Component 3 (0.20): DPI metadata is approximately 300
  Component 4 (0.20): Images contain distinct, non-trivial content
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'impress_rp_035'
EXPORTS_DIR = os.path.join(WORKDIR, 'exports')

EXPECTED_FILES = ['slide_01.png', 'slide_05.png', 'slide_10.png']

# Minimum pixel width to consider "high resolution" at ~300 DPI
# Standard widescreen slide at 300 DPI: ~4000x2250 or ~4000x3000
# We use 3000 as a conservative threshold
MIN_WIDTH = 3000
MIN_HEIGHT = 1500

# DPI tolerance: accept 250-350 as approximately 300 DPI
DPI_MIN = 250
DPI_MAX = 350

# Minimum file size in bytes to consider non-trivial content
MIN_FILE_SIZE = 5000


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: exports directory exists
    if not os.path.isdir(EXPORTS_DIR):
        print(f"CRITICAL: Exports directory not found: {EXPORTS_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All three PNG files exist with correct names (0.30 points)
    try:
        files_found = 0
        for fname in EXPECTED_FILES:
            fpath = os.path.join(EXPORTS_DIR, fname)
            if os.path.isfile(fpath):
                files_found += 1
                print(f"  Found: {fname}")
            else:
                print(f"  Missing: {fname}")

        if files_found == len(EXPECTED_FILES):
            print(f"PASS: Component 1 -- All {len(EXPECTED_FILES)} PNG files exist (0.30 pts)")
            total_score += 0.30
        elif files_found > 0:
            partial = round(0.30 * files_found / len(EXPECTED_FILES), 2)
            print(f"PARTIAL: Component 1 -- {files_found}/{len(EXPECTED_FILES)} files found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 -- No expected PNG files found in {EXPORTS_DIR}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Early exit if no files found (remaining checks need the files)
    if total_score == 0.0:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Import PIL for image analysis
    try:
        from PIL import Image
    except ImportError:
        print("ERROR: PIL/Pillow not available -- cannot verify image properties")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Images are high resolution indicating ~300 DPI (0.30 points)
    try:
        highres_count = 0
        for fname in EXPECTED_FILES:
            fpath = os.path.join(EXPORTS_DIR, fname)
            if not os.path.isfile(fpath):
                continue
            img = Image.open(fpath)
            w, h = img.size
            if w >= MIN_WIDTH and h >= MIN_HEIGHT:
                highres_count += 1
                print(f"  {fname}: {w}x{h} -- high resolution")
            else:
                print(f"  {fname}: {w}x{h} -- below threshold ({MIN_WIDTH}x{MIN_HEIGHT})")

        if highres_count == len(EXPECTED_FILES):
            print(f"PASS: Component 2 -- All images are high resolution (0.30 pts)")
            total_score += 0.30
        elif highres_count > 0:
            partial = round(0.30 * highres_count / len(EXPECTED_FILES), 2)
            print(f"PARTIAL: Component 2 -- {highres_count}/{len(EXPECTED_FILES)} high-res ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- No images meet minimum resolution")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: DPI metadata is approximately 300 (0.20 points)
    try:
        dpi_ok_count = 0
        for fname in EXPECTED_FILES:
            fpath = os.path.join(EXPORTS_DIR, fname)
            if not os.path.isfile(fpath):
                continue
            img = Image.open(fpath)
            dpi = img.info.get('dpi', (None, None))
            if dpi and dpi[0] is not None and dpi[1] is not None:
                avg_dpi = (dpi[0] + dpi[1]) / 2.0
                if DPI_MIN <= avg_dpi <= DPI_MAX:
                    dpi_ok_count += 1
                    print(f"  {fname}: DPI={dpi[0]:.1f}x{dpi[1]:.1f} -- within range")
                else:
                    print(f"  {fname}: DPI={dpi[0]:.1f}x{dpi[1]:.1f} -- outside range [{DPI_MIN}-{DPI_MAX}]")
            else:
                print(f"  {fname}: No DPI metadata found")

        if dpi_ok_count == len(EXPECTED_FILES):
            print(f"PASS: Component 3 -- All images have ~300 DPI metadata (0.20 pts)")
            total_score += 0.20
        elif dpi_ok_count > 0:
            partial = round(0.20 * dpi_ok_count / len(EXPECTED_FILES), 2)
            print(f"PARTIAL: Component 3 -- {dpi_ok_count}/{len(EXPECTED_FILES)} with correct DPI ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- No images have ~300 DPI metadata")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Images contain distinct, non-trivial content (0.20 points)
    # Verify files have meaningful size and are distinct from each other
    try:
        valid_count = 0
        file_sizes = {}
        for fname in EXPECTED_FILES:
            fpath = os.path.join(EXPORTS_DIR, fname)
            if not os.path.isfile(fpath):
                continue
            fsize = os.path.getsize(fpath)
            file_sizes[fname] = fsize
            if fsize >= MIN_FILE_SIZE:
                valid_count += 1
                print(f"  {fname}: {fsize} bytes -- non-trivial content")
            else:
                print(f"  {fname}: {fsize} bytes -- too small (min {MIN_FILE_SIZE})")

        # Check that files are distinct (different sizes suggest different slide content)
        sizes = list(file_sizes.values())
        all_distinct = len(set(sizes)) == len(sizes) if len(sizes) == len(EXPECTED_FILES) else False

        if valid_count == len(EXPECTED_FILES) and all_distinct:
            print(f"PASS: Component 4 -- All images have distinct, non-trivial content (0.20 pts)")
            total_score += 0.20
        elif valid_count == len(EXPECTED_FILES):
            # Files are non-trivial but may not all be distinct
            print(f"PARTIAL: Component 4 -- All non-trivial but not all distinct (0.15 pts)")
            total_score += 0.15
        elif valid_count > 0:
            partial = round(0.20 * valid_count / len(EXPECTED_FILES), 2)
            print(f"PARTIAL: Component 4 -- {valid_count}/{len(EXPECTED_FILES)} non-trivial ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- No images have non-trivial content")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()

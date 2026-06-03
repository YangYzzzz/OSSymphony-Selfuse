"""
Reward Script: Convert first 5 pages of presentation.pdf to 300 DPI PNG images
Task ID: pdf_ro_018
Domain: pdf

Scoring:
  Component 1 (0.30): All 5 PNG files exist (slide_1.png - slide_5.png)
  Component 2 (0.40): Images have correct dimensions for 300 DPI render (~3000x2250)
  Component 3 (0.10): No extra slide files beyond the required 5
  Component 4 (0.20): Images are non-trivial (valid PNG with substantial content)
"""

import os
import struct
import zlib

WORKDIR = '/home/user'
SLIDES_DIR = os.path.join(WORKDIR, 'Documents', 'slides')
TASK_ID = 'pdf_ro_018'

# Expected: 300 DPI on 10x7.5 inch pages => 3000x2250 pixels
# Allow +/- 50 pixel tolerance for rounding differences
EXPECTED_WIDTH = 3000
EXPECTED_HEIGHT = 2250
TOLERANCE = 50


def read_png_dimensions(filepath):
    """Read PNG width and height from the IHDR chunk without PIL."""
    with open(filepath, 'rb') as f:
        header = f.read(8)
        # PNG signature: 137 80 78 71 13 10 26 10
        if header[:8] != b'\x89PNG\r\n\x1a\n':
            return None, None
        # IHDR chunk: 4 bytes length, 4 bytes type, then width(4) height(4)
        chunk_len = f.read(4)
        chunk_type = f.read(4)
        if chunk_type != b'IHDR':
            return None, None
        width = struct.unpack('>I', f.read(4))[0]
        height = struct.unpack('>I', f.read(4))[0]
        return width, height


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: slides directory exists
    if not os.path.isdir(SLIDES_DIR):
        print(f"CRITICAL: Slides directory not found: {SLIDES_DIR}")
        print("REWARD: 0.0")
        return 0.0

    expected_files = [f'slide_{i}.png' for i in range(1, 6)]

    # Component 1: All 5 PNG files exist (0.30 points, 0.06 each)
    try:
        existing_count = 0
        for fname in expected_files:
            fpath = os.path.join(SLIDES_DIR, fname)
            if os.path.isfile(fpath):
                existing_count += 1
                print(f"PASS: {fname} exists")
            else:
                print(f"FAIL: {fname} does not exist")

        comp1_score = existing_count * 0.06
        if existing_count == 5:
            print(f"PASS: Component 1 -- All 5 slide files exist ({comp1_score:.2f} pts)")
        else:
            print(f"PARTIAL: Component 1 -- {existing_count}/5 slide files exist ({comp1_score:.2f} pts)")
        if existing_count > 0:
            total_score += comp1_score
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Correct dimensions for 300 DPI (0.40 points, 0.08 each)
    try:
        dim_pass_count = 0
        for fname in expected_files:
            fpath = os.path.join(SLIDES_DIR, fname)
            if not os.path.isfile(fpath):
                print(f"FAIL: {fname} not found, skipping dimension check")
                continue
            w, h = read_png_dimensions(fpath)
            if w is None or h is None:
                print(f"FAIL: {fname} is not a valid PNG file")
                continue
            w_ok = abs(w - EXPECTED_WIDTH) <= TOLERANCE
            h_ok = abs(h - EXPECTED_HEIGHT) <= TOLERANCE
            if w_ok and h_ok:
                dim_pass_count += 1
                print(f"PASS: {fname} dimensions {w}x{h} within tolerance of {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}")
            else:
                print(f"FAIL: {fname} dimensions {w}x{h} expected ~{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}")

        comp2_score = dim_pass_count * 0.08
        if dim_pass_count == 5:
            print(f"PASS: Component 2 -- All 5 images have correct 300 DPI dimensions ({comp2_score:.2f} pts)")
        else:
            print(f"PARTIAL: Component 2 -- {dim_pass_count}/5 images have correct dimensions ({comp2_score:.2f} pts)")
        if dim_pass_count > 0:
            total_score += comp2_score
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: No extra slide files (0.10 points)
    try:
        all_files = os.listdir(SLIDES_DIR)
        # Filter for files that look like slide_N.png with N > 5
        extra_slides = [f for f in all_files if f.startswith('slide_') and f.endswith('.png') and f not in expected_files]
        # Also check for any other unexpected files
        unexpected = [f for f in all_files if f not in expected_files]

        if len(extra_slides) == 0 and existing_count == 5:
            print(f"PASS: Component 3 -- No extra slide files found ({0.10:.2f} pts)")
            total_score += 0.10
        elif len(extra_slides) > 0:
            print(f"FAIL: Component 3 -- Found extra slide files: {extra_slides}")
        else:
            print(f"FAIL: Component 3 -- Not all required slides exist yet")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Images have substantial content / not blank (0.20 points, 0.04 each)
    # A 300 DPI render of a real presentation slide should produce a file of at least 10KB
    try:
        content_pass_count = 0
        MIN_FILE_SIZE = 10000  # 10KB minimum for a real rendered page
        for fname in expected_files:
            fpath = os.path.join(SLIDES_DIR, fname)
            if not os.path.isfile(fpath):
                print(f"FAIL: {fname} not found, skipping content check")
                continue
            fsize = os.path.getsize(fpath)
            if fsize >= MIN_FILE_SIZE:
                content_pass_count += 1
                print(f"PASS: {fname} has substantial content ({fsize} bytes)")
            else:
                print(f"FAIL: {fname} too small ({fsize} bytes), likely blank or corrupt")

        comp4_score = content_pass_count * 0.04
        if content_pass_count == 5:
            print(f"PASS: Component 4 -- All 5 images have substantial content ({comp4_score:.2f} pts)")
        else:
            print(f"PARTIAL: Component 4 -- {content_pass_count}/5 images have content ({comp4_score:.2f} pts)")
        if content_pass_count > 0:
            total_score += comp4_score
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

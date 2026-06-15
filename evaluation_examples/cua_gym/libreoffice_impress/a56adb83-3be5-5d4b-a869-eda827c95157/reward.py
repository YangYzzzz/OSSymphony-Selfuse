"""
Reward Script: Export each slide as individual PNG images
Task ID: impress_fix_069
Domain: libreoffice_impress
Scoring:
  Component 1 (0.25): Directory exists and contains exactly 8 PNG files
  Component 2 (0.35): All 8 files have correct names (slide_01.png .. slide_08.png)
  Component 3 (0.25): All images meet minimum resolution (1024x768)
  Component 4 (0.15): All images are valid, non-trivial PNGs (>1KB each)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'impress_fix_069'
SLIDE_DIR = os.path.join(WORKDIR, 'Desktop', 'slide_images')
EXPECTED_COUNT = 8
EXPECTED_NAMES = [f'slide_{i:02d}.png' for i in range(1, EXPECTED_COUNT + 1)]
MIN_WIDTH = 1024
MIN_HEIGHT = 768


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Directory exists and contains exactly 8 PNG files (0.25 points)
    try:
        if not os.path.isdir(SLIDE_DIR):
            print(f"FAIL: Component 1 — Directory {SLIDE_DIR} does not exist")
            # No directory means nothing else can pass
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        png_files = [f for f in os.listdir(SLIDE_DIR) if f.lower().endswith('.png')]
        if len(png_files) == EXPECTED_COUNT:
            print(f"PASS: Component 1 — Directory exists with exactly {EXPECTED_COUNT} PNG files (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_COUNT} PNG files, found {len(png_files)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 8 files have correct names slide_01.png through slide_08.png (0.35 points)
    try:
        actual_files = set(os.listdir(SLIDE_DIR))
        matching = 0
        for name in EXPECTED_NAMES:
            if name in actual_files:
                matching += 1
            else:
                print(f"  MISS: {name} not found in directory")

        if matching == EXPECTED_COUNT:
            print(f"PASS: Component 2 — All {EXPECTED_COUNT} expected filenames present (0.35 pts)")
            total_score += 0.35
        elif matching > 0:
            partial = round(0.35 * matching / EXPECTED_COUNT, 3)
            print(f"PARTIAL: Component 2 — {matching}/{EXPECTED_COUNT} filenames correct (+{partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No expected filenames found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All images meet minimum resolution 1024x768 (0.25 points)
    try:
        from PIL import Image
        resolution_pass = 0
        for name in EXPECTED_NAMES:
            fpath = os.path.join(SLIDE_DIR, name)
            if os.path.isfile(fpath):
                img = Image.open(fpath)
                w, h = img.size
                if w >= MIN_WIDTH and h >= MIN_HEIGHT:
                    resolution_pass += 1
                else:
                    print(f"  LOW_RES: {name} is {w}x{h}, expected >= {MIN_WIDTH}x{MIN_HEIGHT}")
            else:
                print(f"  SKIP: {name} not found for resolution check")

        if resolution_pass == EXPECTED_COUNT:
            print(f"PASS: Component 3 — All images meet minimum resolution {MIN_WIDTH}x{MIN_HEIGHT} (0.25 pts)")
            total_score += 0.25
        elif resolution_pass > 0:
            partial = round(0.25 * resolution_pass / EXPECTED_COUNT, 3)
            print(f"PARTIAL: Component 3 — {resolution_pass}/{EXPECTED_COUNT} meet resolution (+{partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No images meet minimum resolution")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All images are valid, non-trivial PNGs >1KB (0.15 points)
    try:
        from PIL import Image
        valid_count = 0
        for name in EXPECTED_NAMES:
            fpath = os.path.join(SLIDE_DIR, name)
            if os.path.isfile(fpath):
                fsize = os.path.getsize(fpath)
                if fsize < 1024:
                    print(f"  TINY: {name} is only {fsize} bytes")
                    continue
                # Verify it's actually a valid PNG by loading it
                img = Image.open(fpath)
                img.verify()
                valid_count += 1

        if valid_count == EXPECTED_COUNT:
            print(f"PASS: Component 4 — All {EXPECTED_COUNT} images are valid non-trivial PNGs (0.15 pts)")
            total_score += 0.15
        elif valid_count > 0:
            partial = round(0.15 * valid_count / EXPECTED_COUNT, 3)
            print(f"PARTIAL: Component 4 — {valid_count}/{EXPECTED_COUNT} valid PNGs (+{partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No valid non-trivial PNG files found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

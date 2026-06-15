"""
Reward Script: Export all slides of a 5-slide presentation as individual PNG images.
Task ID: osworld_impress_export_image_003
Domain: libreoffice_impress
Scoring:
  Component 1: All 5 expected PNG files exist (one per slide)  — 0.5 pts
  Component 2: All 5 PNG files are valid (non-empty, readable) — 0.3 pts
  Component 3: PNG dimensions are consistent with presentation  — 0.2 pts
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_impress_export_image_003'
EXPECTED_SLIDE_COUNT = 5


def verify_task():
    """
    Verify that all 5 slides of the presentation were exported as individual PNG files.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Build expected file paths: osworld_impress_export_image_003-1.png ... -5.png
    expected_files = [
        os.path.join(WORKDIR, f'{TASK_ID}-{i}.png')
        for i in range(1, EXPECTED_SLIDE_COUNT + 1)
    ]

    # Component 1: All 5 PNG files exist (0.5 points)
    # This FAILS on initial_env (no PNG files) and PASSES on golden_env (5 PNG files present)
    try:
        found_count = 0
        missing = []
        for path in expected_files:
            if os.path.exists(path) and os.path.getsize(path) > 0:
                found_count += 1
            else:
                missing.append(os.path.basename(path))

        if found_count == EXPECTED_SLIDE_COUNT:
            print(f"PASS: Component 1 — All {EXPECTED_SLIDE_COUNT} PNG files exist (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Only {found_count}/{EXPECTED_SLIDE_COUNT} PNG files found. Missing: {missing}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All PNG files are valid images (non-corrupted) (0.3 points)
    # This FAILS on initial_env (files don't exist) and PASSES on golden_env (valid images)
    try:
        from PIL import Image

        valid_count = 0
        invalid = []
        for path in expected_files:
            if not os.path.exists(path):
                invalid.append(os.path.basename(path) + " (missing)")
                continue
            try:
                with Image.open(path) as img:
                    img.verify()  # Verify integrity without fully loading
                valid_count += 1
            except Exception as img_err:
                invalid.append(f"{os.path.basename(path)} ({img_err})")

        if valid_count == EXPECTED_SLIDE_COUNT:
            print(f"PASS: Component 2 — All {EXPECTED_SLIDE_COUNT} PNG files are valid images (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — {valid_count}/{EXPECTED_SLIDE_COUNT} valid. Invalid: {invalid}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: PNG files have consistent and reasonable dimensions (0.2 points)
    # The presentation is 12188952 EMU wide x 6858000 EMU tall (widescreen 16:9 ratio).
    # Expected exported resolution should be consistent across all 5 slides.
    # This FAILS on initial_env (no files) and PASSES on golden_env (consistent valid dimensions).
    try:
        from PIL import Image

        widths = []
        heights = []
        read_errors = []

        for path in expected_files:
            if not os.path.exists(path):
                read_errors.append(os.path.basename(path) + " (missing)")
                continue
            try:
                with Image.open(path) as img:
                    w, h = img.size
                    widths.append(w)
                    heights.append(h)
            except Exception as img_err:
                read_errors.append(f"{os.path.basename(path)} ({img_err})")

        dims_consistent = (
            len(read_errors) == 0
            and len(widths) == EXPECTED_SLIDE_COUNT
            and len(set(widths)) == 1
            and len(set(heights)) == 1
            and widths[0] > 0
            and heights[0] > 0
        )
        if dims_consistent:
            print(f"PASS: Component 3 — All {EXPECTED_SLIDE_COUNT} PNG files have consistent dimensions "
                  f"{widths[0]}x{heights[0]} (0.2 pts)")
            total_score += 0.2
        elif len(read_errors) > 0 or len(widths) < EXPECTED_SLIDE_COUNT:
            print(f"FAIL: Component 3 — Cannot read all {EXPECTED_SLIDE_COUNT} PNG files. Errors: {read_errors}")
        else:
            print(f"FAIL: Component 3 — PNG dimensions are inconsistent: widths={widths}, heights={heights}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.1f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

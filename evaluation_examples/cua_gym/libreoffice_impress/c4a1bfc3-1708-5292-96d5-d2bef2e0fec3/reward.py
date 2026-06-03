"""
Reward Script: Export slides 1, 3, 5, 7 as PNG images to ~/Desktop/SelectedSlideImages/
Task ID: impress_el_016
Domain: libreoffice_impress
Scoring:
  Component 1 (0.15): Target directory exists
  Component 2 (0.15): Exactly 4 PNG files in directory
  Component 3 (0.30): Correct filenames referencing slides 1, 3, 5, 7
  Component 4 (0.20): All files are valid PNG images
  Component 5 (0.20): No extraneous slide files present
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'impress_el_016'
TARGET_DIR = os.path.join(WORKDIR, 'Desktop', 'SelectedSlideImages')

# The expected slide numbers that should be exported
EXPECTED_SLIDES = {1, 3, 5, 7}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Target directory exists (0.15 points)
    # This directory does NOT exist in initial_env, only created by the task.
    try:
        if os.path.isdir(TARGET_DIR):
            print(f"PASS: Component 1 — Directory {TARGET_DIR} exists (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Directory {TARGET_DIR} does not exist")
            # If directory doesn't exist, nothing else can pass
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # List all files in the target directory
    try:
        all_files = os.listdir(TARGET_DIR)
        all_files_lower = [f.lower() for f in all_files]
    except Exception as e:
        print(f"ERROR: Cannot list directory: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Exactly 4 files in directory (0.15 points)
    try:
        png_files = [f for f in all_files if f.lower().endswith('.png')]
        if len(png_files) == 4:
            print(f"PASS: Component 2 — Exactly 4 PNG files found: {sorted(png_files)} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Expected 4 PNG files, found {len(png_files)}: {sorted(png_files)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct filenames referencing slides 1, 3, 5, 7 (0.30 points)
    # We check that slide numbers 1, 3, 5, 7 are represented in the filenames.
    # Common naming patterns: Slide1.png, slide_1.png, slide1.png, 1.png, etc.
    try:
        import re
        found_slide_numbers = set()
        for f in all_files:
            if not f.lower().endswith('.png'):
                continue
            # Extract numbers from filename
            numbers = re.findall(r'(\d+)', f)
            for n in numbers:
                num = int(n)
                if num in EXPECTED_SLIDES:
                    found_slide_numbers.add(num)

        matched = found_slide_numbers & EXPECTED_SLIDES
        match_ratio = len(matched) / len(EXPECTED_SLIDES)
        points = round(0.30 * match_ratio, 2)
        if match_ratio == 1.0:
            print(f"PASS: Component 3 — All expected slides found in filenames: {sorted(matched)} ({points} pts)")
            total_score += points
        elif match_ratio > 0:
            missing = EXPECTED_SLIDES - matched
            print(f"PARTIAL: Component 3 — Found slides {sorted(matched)}, missing {sorted(missing)} ({points} pts)")
            total_score += points
        else:
            print(f"FAIL: Component 3 — No expected slide numbers found in filenames")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All files are valid PNG images (0.20 points)
    try:
        from PIL import Image
        valid_count = 0
        for f in png_files:
            fpath = os.path.join(TARGET_DIR, f)
            try:
                img = Image.open(fpath)
                img.verify()  # verify it's a valid image
                valid_count += 1
            except Exception as img_e:
                print(f"  WARNING: {f} is not a valid PNG image: {img_e}")

        if len(png_files) > 0:
            validity_ratio = valid_count / len(png_files)
        else:
            validity_ratio = 0.0
        points = round(0.20 * validity_ratio, 2)
        if validity_ratio == 1.0:
            print(f"PASS: Component 4 — All {valid_count} PNG files are valid images ({points} pts)")
            total_score += points
        elif validity_ratio > 0:
            print(f"PARTIAL: Component 4 — {valid_count}/{len(png_files)} valid PNGs ({points} pts)")
            total_score += points
        else:
            print(f"FAIL: Component 4 — No valid PNG files found")
    except ImportError:
        # Fallback: check PNG magic bytes if PIL not available
        valid_count = 0
        PNG_MAGIC = b'\x89PNG\r\n\x1a\n'
        for f in png_files:
            fpath = os.path.join(TARGET_DIR, f)
            try:
                with open(fpath, 'rb') as fh:
                    header = fh.read(8)
                    if header == PNG_MAGIC:
                        valid_count += 1
            except Exception:
                pass
        if len(png_files) > 0:
            validity_ratio = valid_count / len(png_files)
        else:
            validity_ratio = 0.0
        points = round(0.20 * validity_ratio, 2)
        if validity_ratio == 1.0:
            print(f"PASS: Component 4 — All {valid_count} files have valid PNG headers ({points} pts)")
            total_score += points
        elif validity_ratio > 0:
            print(f"PARTIAL: Component 4 — {valid_count}/{len(png_files)} have valid PNG headers ({points} pts)")
            total_score += points
        else:
            print(f"FAIL: Component 4 — No files have valid PNG headers")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: No extraneous slide files (0.20 points)
    # Only slides 1, 3, 5, 7 should be present. No slides 2, 4, 6, 8, 9, 10.
    try:
        import re
        extraneous = set()
        for f in all_files:
            if not f.lower().endswith('.png'):
                continue
            numbers = re.findall(r'(\d+)', f)
            for n in numbers:
                num = int(n)
                if num not in EXPECTED_SLIDES and 1 <= num <= 20:
                    extraneous.add(num)

        non_png_files = [f for f in all_files if not f.lower().endswith('.png')]

        if len(extraneous) == 0 and len(non_png_files) == 0:
            print(f"PASS: Component 5 — No extraneous slide files or non-PNG files (0.20 pts)")
            total_score += 0.20
        else:
            if extraneous:
                print(f"FAIL: Component 5 — Extraneous slide numbers found: {sorted(extraneous)}")
            if non_png_files:
                print(f"FAIL: Component 5 — Non-PNG files found: {non_png_files}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

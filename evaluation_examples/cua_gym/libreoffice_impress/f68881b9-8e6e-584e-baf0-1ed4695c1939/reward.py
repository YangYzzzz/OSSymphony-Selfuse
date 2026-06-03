"""
Reward Script: Export all 6 slides as individual PNG images to ~/slide_exports/
Task ID: osworld_impress_export_image_007
Domain: libreoffice_impress
Scoring:
  Component 1: All 6 PNG files exist with correct naming (slide_01.png ... slide_06.png) — 0.5 pts
  Component 2: All 6 files are valid PNG images (checked via PIL) — 0.3 pts
  Component 3: All 6 PNG images contain non-trivial content (file size > 1000 bytes each) — 0.2 pts
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_impress_export_image_007'
EXPORT_DIR = os.path.join(WORKDIR, 'slide_exports')
EXPECTED_FILES = [f'slide_{i:02d}.png' for i in range(1, 7)]  # slide_01.png ... slide_06.png


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: slide_exports directory must exist
    if not os.path.isdir(EXPORT_DIR):
        print(f"CRITICAL: slide_exports directory not found at {EXPORT_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All 6 PNG files exist with correct names (0.5 points)
    # This checks that the agent created all 6 sequentially named files.
    # Fails on initial_env (empty directory) and passes on golden_env (6 files present).
    try:
        existing_files = set(os.listdir(EXPORT_DIR))
        found_count = 0
        missing = []
        for fname in EXPECTED_FILES:
            if fname in existing_files:
                found_count += 1
            else:
                missing.append(fname)

        if found_count == 6:
            print(f"PASS: Component 1 — All 6 PNG files present (0.5 pts)")
            total_score += 0.5
        elif found_count > 0:
            partial = round(0.5 * (found_count / 6), 4)
            print(f"PARTIAL: Component 1 — {found_count}/6 files present ({partial} pts). Missing: {missing}")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No expected PNG files found in {EXPORT_DIR}. Missing: {missing}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All present PNG files are valid PNG images (0.3 points)
    # Uses PIL to verify the file is a genuine PNG with valid image data.
    # Fails on initial_env (no files) and passes on golden_env (all valid PNGs).
    try:
        from PIL import Image

        valid_png_count = 0
        invalid = []
        for fname in EXPECTED_FILES:
            fpath = os.path.join(EXPORT_DIR, fname)
            if not os.path.isfile(fpath):
                continue
            try:
                img = Image.open(fpath)
                img.verify()  # verifies PNG integrity without loading full pixel data
                valid_png_count += 1
            except Exception as img_e:
                invalid.append(f"{fname}: {img_e}")

        present_count = sum(1 for f in EXPECTED_FILES if os.path.isfile(os.path.join(EXPORT_DIR, f)))

        if present_count == 0:
            print(f"FAIL: Component 2 — No files to validate (0.0 pts)")
        elif valid_png_count == 6:
            print(f"PASS: Component 2 — All 6 files are valid PNG images (0.3 pts)")
            total_score += 0.3
        elif valid_png_count > 0:
            partial = round(0.3 * (valid_png_count / 6), 4)
            print(f"PARTIAL: Component 2 — {valid_png_count}/6 valid PNG images ({partial} pts). Invalid: {invalid}")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No valid PNG images found. Issues: {invalid}")
    except ImportError:
        # PIL not available; fallback: check PNG magic bytes manually
        try:
            PNG_SIG = b'\x89PNG\r\n\x1a\n'
            valid_png_count = 0
            for fname in EXPECTED_FILES:
                fpath = os.path.join(EXPORT_DIR, fname)
                if not os.path.isfile(fpath):
                    continue
                with open(fpath, 'rb') as f:
                    header = f.read(8)
                if header == PNG_SIG:
                    valid_png_count += 1
            if valid_png_count == 6:
                print(f"PASS: Component 2 — All 6 files have valid PNG signature (0.3 pts) [magic-byte fallback]")
                total_score += 0.3
            elif valid_png_count > 0:
                partial = round(0.3 * (valid_png_count / 6), 4)
                print(f"PARTIAL: Component 2 — {valid_png_count}/6 files have PNG signature ({partial} pts) [magic-byte fallback]")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — No files with valid PNG signature (magic-byte fallback)")
        except Exception as e:
            print(f"ERROR: Component 2 (fallback) — {e}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 6 PNG images are non-trivial (file size > 1000 bytes each) (0.2 points)
    # This checks that each image actually contains slide content (not blank/zero-byte files).
    # Fails on initial_env (no files) and passes on golden_env (all sizeable images).
    try:
        MIN_SIZE = 1000  # bytes — a valid exported slide should be much larger
        sizeable_count = 0
        too_small = []
        for fname in EXPECTED_FILES:
            fpath = os.path.join(EXPORT_DIR, fname)
            if not os.path.isfile(fpath):
                continue
            size = os.path.getsize(fpath)
            if size > MIN_SIZE:
                sizeable_count += 1
            else:
                too_small.append(f"{fname}: {size} bytes")

        present_count = sum(1 for f in EXPECTED_FILES if os.path.isfile(os.path.join(EXPORT_DIR, f)))

        if present_count == 0:
            print(f"FAIL: Component 3 — No files to check size (0.0 pts)")
        elif sizeable_count == 6:
            print(f"PASS: Component 3 — All 6 PNG files have content (>1000 bytes each) (0.2 pts)")
            total_score += 0.2
        elif sizeable_count > 0:
            partial = round(0.2 * (sizeable_count / 6), 4)
            print(f"PARTIAL: Component 3 — {sizeable_count}/6 files sizeable ({partial} pts). Too small: {too_small}")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No files large enough to contain real slide content. Issues: {too_small}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

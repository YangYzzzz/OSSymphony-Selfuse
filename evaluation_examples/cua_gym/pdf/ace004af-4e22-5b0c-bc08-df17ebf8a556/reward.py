"""
Reward Script: Extract images from accident_report.pdf and save as individual PNGs
Task ID: pdf_legal_079
Domain: pdf
Scoring:
  Component 1 (0.3): Correct number of files (6) in photos/ directory
  Component 2 (0.3): Files named photo_1.png through photo_6.png
  Component 3 (0.2): All files are valid PNG images with non-trivial size
  Component 4 (0.2): Extracted image count matches PDF embedded image count
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_079'
PDF_PATH = os.path.join(WORKDIR, 'legal', 'personal_injury', 'accident_report.pdf')
PHOTOS_DIR = os.path.join(WORKDIR, 'legal', 'personal_injury', 'photos')
EXPECTED_COUNT = 6


def count_pdf_images(pdf_path):
    """Count the number of embedded images in the PDF."""
    try:
        import fitz
        doc = fitz.open(pdf_path)
        total = 0
        for page in doc:
            total += len(page.get_images(full=True))
        doc.close()
        return total
    except Exception as e:
        print(f"WARN: Could not count PDF images: {e}")
        return EXPECTED_COUNT  # fallback to expected count


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: PDF must exist
    if not os.path.exists(PDF_PATH):
        print(f"CRITICAL: PDF not found at {PDF_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: photos directory must exist
    if not os.path.isdir(PHOTOS_DIR):
        print(f"CRITICAL: Photos directory not found at {PHOTOS_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # List all files in photos directory
    try:
        all_files = sorted(os.listdir(PHOTOS_DIR))
        png_files = [f for f in all_files if f.endswith('.png')]
    except Exception as e:
        print(f"CRITICAL: Cannot list photos directory: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Correct number of PNG files (0.3 points)
    # Initial env has 0 files; golden should have 6
    try:
        file_count = len(png_files)
        if file_count == EXPECTED_COUNT:
            print(f"PASS: Component 1 — Found {file_count} PNG files (expected {EXPECTED_COUNT}) (0.3 pts)")
            total_score += 0.3
        elif file_count > 0:
            # Partial credit: proportional to how many images extracted
            partial = 0.3 * min(file_count, EXPECTED_COUNT) / EXPECTED_COUNT
            print(f"PARTIAL: Component 1 — Found {file_count} PNG files (expected {EXPECTED_COUNT}) ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No PNG files found in {PHOTOS_DIR}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Files named photo_1.png through photo_6.png (0.3 points)
    # Initial env has no files; golden should have exact names
    try:
        expected_names = {f"photo_{i}.png" for i in range(1, EXPECTED_COUNT + 1)}
        actual_names = set(png_files)
        matching = expected_names & actual_names
        if matching == expected_names:
            print(f"PASS: Component 2 — All expected filenames present: {sorted(expected_names)} (0.3 pts)")
            total_score += 0.3
        elif len(matching) > 0:
            partial = 0.3 * len(matching) / len(expected_names)
            print(f"PARTIAL: Component 2 — {len(matching)}/{len(expected_names)} expected names found ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No expected filenames found. Present: {sorted(actual_names)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All files are valid PNG images with non-trivial size (0.2 points)
    # Initial env has no files; golden files should be valid PNGs > 1KB
    try:
        if len(png_files) == 0:
            print("FAIL: Component 3 — No PNG files to validate")
        else:
            valid_count = 0
            for fname in png_files:
                fpath = os.path.join(PHOTOS_DIR, fname)
                fsize = os.path.getsize(fpath)
                if fsize < 1024:
                    print(f"  WARN: {fname} is only {fsize} bytes (possibly corrupt)")
                    continue
                # Check PNG magic bytes
                with open(fpath, 'rb') as f:
                    header = f.read(8)
                if header[:4] == b'\x89PNG':
                    valid_count += 1
                else:
                    print(f"  WARN: {fname} does not have PNG header")

            if valid_count == EXPECTED_COUNT:
                print(f"PASS: Component 3 — All {valid_count} files are valid PNGs > 1KB (0.2 pts)")
                total_score += 0.2
            elif valid_count > 0:
                partial = 0.2 * valid_count / EXPECTED_COUNT
                print(f"PARTIAL: Component 3 — {valid_count}/{EXPECTED_COUNT} valid PNGs ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — No valid PNG files found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Image count matches PDF embedded image count (0.2 points)
    # Initial env has no extracted images; golden should match PDF image count
    try:
        pdf_image_count = count_pdf_images(PDF_PATH)
        extracted_count = len(png_files)
        if extracted_count == pdf_image_count and extracted_count > 0:
            print(f"PASS: Component 4 — Extracted count ({extracted_count}) matches PDF image count ({pdf_image_count}) (0.2 pts)")
            total_score += 0.2
        elif extracted_count > 0 and extracted_count != pdf_image_count:
            # Some images extracted but not matching PDF count
            ratio = min(extracted_count, pdf_image_count) / max(extracted_count, pdf_image_count)
            partial = 0.2 * ratio
            print(f"PARTIAL: Component 4 — Extracted {extracted_count} but PDF has {pdf_image_count} images ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No images extracted (PDF has {pdf_image_count} images)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

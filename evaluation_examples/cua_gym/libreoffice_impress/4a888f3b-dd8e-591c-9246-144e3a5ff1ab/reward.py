"""
Reward Script: Export all slides as individual JPEG images to Desktop/slide_images
Task ID: impstruct_044
Domain: libreoffice_impress
Scoring:
  Component 1 (0.20): slide_images folder exists on Desktop
  Component 2 (0.35): Correct number of JPEG files matching presentation slide count (6)
  Component 3 (0.30): All files are valid, loadable JPEG images
  Component 4 (0.15): All images have reasonable non-degenerate dimensions
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'impstruct_044'
SLIDE_IMAGES_DIR = os.path.join(WORKDIR, 'Desktop', 'slide_images')
PPTX_PATH = os.path.join(WORKDIR, 'photo_album.pptx')
EXPECTED_SLIDE_COUNT = 6


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Precondition: presentation file must exist ---
    if not os.path.exists(PPTX_PATH):
        print(f"CRITICAL: Presentation file not found: {PPTX_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Get actual slide count from the presentation for cross-validation
    try:
        from pptx import Presentation
        prs = Presentation(PPTX_PATH)
        actual_slide_count = len(prs.slides)
        print(f"INFO: Presentation has {actual_slide_count} slides")
    except Exception as e:
        print(f"WARN: Could not read presentation: {e}. Using expected count {EXPECTED_SLIDE_COUNT}")
        actual_slide_count = EXPECTED_SLIDE_COUNT

    # Component 1: slide_images folder exists on Desktop (0.20 points)
    # This is a task-introduced change: the folder does NOT exist in the initial state
    try:
        if os.path.isdir(SLIDE_IMAGES_DIR):
            print(f"PASS: Component 1 -- slide_images folder exists at {SLIDE_IMAGES_DIR} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 -- slide_images folder not found at {SLIDE_IMAGES_DIR}")
            # If folder doesn't exist, no point checking further
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Correct number of JPEG files (0.35 points)
    # The task asks to export ALL slides as JPEG. We check that the number of
    # image files matches the slide count.
    try:
        all_files = os.listdir(SLIDE_IMAGES_DIR)
        # Filter for JPEG files (common extensions)
        jpeg_files = [f for f in all_files if f.lower().endswith(('.jpg', '.jpeg'))]
        print(f"INFO: Found {len(jpeg_files)} JPEG files in slide_images: {sorted(jpeg_files)}")

        if len(jpeg_files) == actual_slide_count:
            print(f"PASS: Component 2 -- {len(jpeg_files)} JPEG files match {actual_slide_count} slides (0.35 pts)")
            total_score += 0.35
        elif len(jpeg_files) > 0:
            # Partial credit: some slides exported but not all
            if actual_slide_count > 0:
                partial = round(0.35 * min(len(jpeg_files), actual_slide_count) / actual_slide_count, 2)
                print(f"PARTIAL: Component 2 -- {len(jpeg_files)} JPEG files vs {actual_slide_count} expected ({partial} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 2 -- No JPEG files found in slide_images folder")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: All JPEG files are valid, loadable images (0.30 points)
    # Verifies each file is actually a proper JPEG image, not a corrupted file
    try:
        from PIL import Image
        valid_count = 0
        for fname in sorted(jpeg_files):
            fpath = os.path.join(SLIDE_IMAGES_DIR, fname)
            try:
                img = Image.open(fpath)
                img.verify()  # Verify it's a valid image
                if img.format == 'JPEG':
                    valid_count += 1
                    print(f"  OK: {fname} is valid JPEG")
                else:
                    print(f"  WARN: {fname} format is {img.format}, not JPEG")
            except Exception as e:
                print(f"  FAIL: {fname} is not a valid image: {e}")

        if valid_count == actual_slide_count and len(jpeg_files) == actual_slide_count:
            print(f"PASS: Component 3 -- All {valid_count} files are valid JPEG images (0.30 pts)")
            total_score += 0.30
        elif valid_count > 0:
            if actual_slide_count > 0:
                partial = round(0.30 * valid_count / actual_slide_count, 2)
                print(f"PARTIAL: Component 3 -- {valid_count}/{actual_slide_count} valid JPEG images ({partial} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 3 -- No valid JPEG images found")
    except ImportError:
        print(f"ERROR: Component 3 -- PIL/Pillow not available, skipping image validation")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: All images have reasonable dimensions (0.15 points)
    # Exported slides should have non-degenerate dimensions (at least 100x100)
    try:
        from PIL import Image
        reasonable_count = 0
        for fname in sorted(jpeg_files):
            fpath = os.path.join(SLIDE_IMAGES_DIR, fname)
            try:
                img = Image.open(fpath)
                w, h = img.size
                if w >= 100 and h >= 100:
                    reasonable_count += 1
                    print(f"  OK: {fname} dimensions {w}x{h}")
                else:
                    print(f"  WARN: {fname} has small dimensions {w}x{h}")
            except Exception as e:
                print(f"  FAIL: {fname} could not read dimensions: {e}")

        if reasonable_count == actual_slide_count and len(jpeg_files) == actual_slide_count:
            print(f"PASS: Component 4 -- All {reasonable_count} images have reasonable dimensions (0.15 pts)")
            total_score += 0.15
        elif reasonable_count > 0:
            if actual_slide_count > 0:
                partial = round(0.15 * reasonable_count / actual_slide_count, 2)
                print(f"PARTIAL: Component 4 -- {reasonable_count}/{actual_slide_count} images have reasonable dimensions ({partial} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 4 -- No images with reasonable dimensions found")
    except ImportError:
        print(f"ERROR: Component 4 -- PIL/Pillow not available")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

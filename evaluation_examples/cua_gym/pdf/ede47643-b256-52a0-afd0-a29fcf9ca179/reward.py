"""
Reward Script: Extract images from pages 5-8 of product_catalog.pdf
Task ID: pdf_mbc_080
Domain: pdf
Scoring:
  Component 1 (0.2): Directory exists with 8 correctly named PNG files
  Component 2 (0.3): Each image has correct dimensions matching PDF source
  Component 3 (0.5): Pixel content of extracted images matches PDF source
"""

import os
import io

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_080'
PDF_PATH = os.path.join(WORKDIR, 'Documents', 'product_catalog.pdf')
IMG_DIR = os.path.join(WORKDIR, 'Documents', 'catalog_images')

# Expected files: mapping of filename -> (page_0indexed, image_index)
EXPECTED_FILES = {
    'page5_img1.png': (4, 0),
    'page5_img2.png': (4, 1),
    'page6_img1.png': (5, 0),
    'page6_img2.png': (5, 1),
    'page6_img3.png': (5, 2),
    'page7_img1.png': (6, 0),
    'page7_img2.png': (6, 1),
    'page8_img1.png': (7, 0),
}


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

    # Component 1: Directory exists with 8 correctly named PNG files (0.2 points)
    try:
        if not os.path.isdir(IMG_DIR):
            print(f"FAIL: Component 1 -- catalog_images directory does not exist")
        else:
            actual_files = set(os.listdir(IMG_DIR))
            expected_names = set(EXPECTED_FILES.keys())
            missing = expected_names - actual_files
            extra = actual_files - expected_names

            if len(missing) == 0 and len(actual_files) == 8:
                print(f"PASS: Component 1 -- All 8 expected files present with correct names (0.2 pts)")
                total_score += 0.2
            else:
                if missing:
                    print(f"FAIL: Component 1 -- Missing files: {sorted(missing)}")
                if extra:
                    print(f"FAIL: Component 1 -- Extra files: {sorted(extra)}")
                if len(actual_files) != 8:
                    print(f"FAIL: Component 1 -- Expected 8 files, found {len(actual_files)}")
                # Partial: give credit proportional to correct files present
                correct_count = len(expected_names & actual_files)
                if correct_count > 0:
                    partial = 0.2 * (correct_count / 8)
                    print(f"PARTIAL: Component 1 -- {correct_count}/8 correct files ({partial:.2f} pts)")
                    total_score += partial
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Image dimensions match PDF source (0.3 points)
    try:
        import pymupdf
        from PIL import Image

        doc = pymupdf.open(PDF_PATH)
        dim_matches = 0
        dim_total = 0

        for fname, (page_idx, img_idx) in EXPECTED_FILES.items():
            fpath = os.path.join(IMG_DIR, fname)
            if not os.path.exists(fpath):
                print(f"FAIL: Component 2 -- {fname} not found, cannot check dimensions")
                dim_total += 1
                continue

            dim_total += 1
            try:
                # Get expected dimensions from PDF
                page_imgs = doc[page_idx].get_images()
                if img_idx >= len(page_imgs):
                    print(f"FAIL: Component 2 -- {fname}: PDF page {page_idx+1} has fewer than {img_idx+1} images")
                    continue

                expected_w = page_imgs[img_idx][2]
                expected_h = page_imgs[img_idx][3]

                # Get actual dimensions from saved file
                saved_img = Image.open(fpath)
                actual_w, actual_h = saved_img.size

                if actual_w == expected_w and actual_h == expected_h:
                    dim_matches += 1
                else:
                    print(f"FAIL: Component 2 -- {fname}: expected {expected_w}x{expected_h}, got {actual_w}x{actual_h}")
            except Exception as e:
                print(f"ERROR: Component 2 -- {fname}: {e}")

        doc.close()

        if dim_total > 0 and dim_matches > 0:
            dim_score = 0.3 * (dim_matches / dim_total)
            if dim_matches == dim_total:
                print(f"PASS: Component 2 -- All {dim_matches}/{dim_total} images have correct dimensions (0.3 pts)")
            else:
                print(f"PARTIAL: Component 2 -- {dim_matches}/{dim_total} images have correct dimensions ({dim_score:.2f} pts)")
            total_score += dim_score
        elif dim_total > 0:
            print(f"FAIL: Component 2 -- No images have correct dimensions")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Pixel content matches PDF source images (0.5 points)
    try:
        import pymupdf
        from PIL import Image
        import numpy as np

        doc = pymupdf.open(PDF_PATH)
        pixel_matches = 0
        pixel_total = 0

        for fname, (page_idx, img_idx) in EXPECTED_FILES.items():
            fpath = os.path.join(IMG_DIR, fname)
            if not os.path.exists(fpath):
                pixel_total += 1
                continue

            pixel_total += 1
            try:
                # Extract image from PDF
                page_imgs = doc[page_idx].get_images()
                if img_idx >= len(page_imgs):
                    continue

                xref = page_imgs[img_idx][0]
                img_data = doc.extract_image(xref)
                pdf_img = Image.open(io.BytesIO(img_data['image'])).convert('RGB')

                # Load saved image
                saved_img = Image.open(fpath).convert('RGB')

                pdf_arr = np.array(pdf_img)
                saved_arr = np.array(saved_img)

                if pdf_arr.shape != saved_arr.shape:
                    print(f"FAIL: Component 3 -- {fname}: shape mismatch PDF={pdf_arr.shape} saved={saved_arr.shape}")
                    continue

                # Compare pixel content (allow small tolerance for compression)
                mean_diff = np.abs(pdf_arr.astype(float) - saved_arr.astype(float)).mean()
                if mean_diff < 5.0:  # tolerance for potential compression differences
                    pixel_matches += 1
                else:
                    print(f"FAIL: Component 3 -- {fname}: pixel content differs (mean_diff={mean_diff:.2f})")
            except Exception as e:
                print(f"ERROR: Component 3 -- {fname}: {e}")

        doc.close()

        if pixel_total > 0 and pixel_matches > 0:
            pixel_score = 0.5 * (pixel_matches / pixel_total)
            if pixel_matches == pixel_total:
                print(f"PASS: Component 3 -- All {pixel_matches}/{pixel_total} images match PDF source content (0.5 pts)")
            else:
                print(f"PARTIAL: Component 3 -- {pixel_matches}/{pixel_total} images match PDF source content ({pixel_score:.2f} pts)")
            total_score += pixel_score
        elif pixel_total > 0:
            print(f"FAIL: Component 3 -- No images match PDF source content")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

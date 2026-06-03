"""
Reward Script: Convert color figures on pages 4-6 to grayscale
Task ID: pdf_res_052
Domain: pdf
Scoring:
  Component 1 (0.2): Output file exists at correct path with 10 pages
  Component 2 (0.5): Pages 4-6 (0-indexed 3-5) are grayscale in the output
  Component 3 (0.3): Non-target pages (0-2, 6-9) are visually unchanged from original
"""

import os
import pymupdf
from PIL import Image
import numpy as np

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_052'

OUTPUT_PATH = os.path.join(WORKDIR, 'papers', 'color_paper_bw.pdf')
ORIGINAL_PATH = os.path.join(WORKDIR, 'papers', 'color_paper.pdf')

# Pages 4-6 in task (1-indexed) = pages 3-5 in 0-indexed
TARGET_PAGES = [3, 4, 5]
NON_TARGET_PAGES = [0, 1, 2, 6, 7, 8, 9]


def render_page(doc, page_idx, scale=1.5):
    """Render a page to a numpy RGB array."""
    page = doc[page_idx]
    mat = pymupdf.Matrix(scale, scale)
    pix = page.get_pixmap(matrix=mat)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return np.array(img)


def is_grayscale(arr, tolerance=1.5):
    """Check if a rendered page image is grayscale.
    A page is grayscale if the mean absolute channel differences are within tolerance.
    tolerance=1.5 allows for minor rounding artifacts from rendering."""
    r = arr[:, :, 0].astype(float)
    g = arr[:, :, 1].astype(float)
    b = arr[:, :, 2].astype(float)
    mean_diff_rg = np.mean(np.abs(r - g))
    mean_diff_rb = np.mean(np.abs(r - b))
    mean_diff_gb = np.mean(np.abs(g - b))
    return mean_diff_rg <= tolerance and mean_diff_rb <= tolerance and mean_diff_gb <= tolerance


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ========================================================
    # Component 1: Output file exists with correct page count (0.2 points)
    # This FAILS on initial_env (file doesn't exist) and PASSES on golden_env
    # ========================================================
    try:
        if not os.path.exists(OUTPUT_PATH):
            print(f"FAIL: Component 1 -- Output file not found: {OUTPUT_PATH}")
            print("REWARD: 0.0")
            return 0.0

        out_doc = pymupdf.open(OUTPUT_PATH)
        page_count = out_doc.page_count
        out_doc.close()

        if page_count == 10:
            print(f"PASS: Component 1 -- Output file exists with {page_count} pages (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- Expected 10 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # ========================================================
    # Component 2: Pages 4-6 are grayscale in output (0.5 points)
    # Each page worth ~0.167 points; all 3 must pass for full credit
    # This FAILS on initial_env (file doesn't exist, early return above)
    # ========================================================
    try:
        out_doc = pymupdf.open(OUTPUT_PATH)
        gray_count = 0
        for pg in TARGET_PAGES:
            arr = render_page(out_doc, pg)
            if is_grayscale(arr):
                gray_count += 1
                print(f"PASS: Component 2 -- Page {pg + 1} is grayscale")
            else:
                r = arr[:, :, 0].astype(float)
                g = arr[:, :, 1].astype(float)
                mean_diff = np.mean(np.abs(r - g))
                print(f"FAIL: Component 2 -- Page {pg + 1} is NOT grayscale (mean channel diff: {mean_diff:.2f})")
        out_doc.close()

        # Proportional scoring: each grayscale target page earns a share
        page_score = 0.5 * (gray_count / len(TARGET_PAGES))
        if gray_count == len(TARGET_PAGES):
            print(f"PASS: Component 2 -- All target pages grayscale ({page_score:.2f} pts)")
            total_score += page_score
        elif gray_count > 0:
            print(f"PARTIAL: Component 2 -- {gray_count}/{len(TARGET_PAGES)} target pages grayscale ({page_score:.2f} pts)")
            total_score += page_score
        else:
            print(f"FAIL: Component 2 -- No target pages are grayscale (0.00 pts)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # ========================================================
    # Component 3: Non-target pages are unchanged (0.3 points)
    # Compare rendered pixels of non-target pages between original and output
    # Mean pixel difference should be very small (< 2.0 to account for rendering)
    # This FAILS on initial_env (file doesn't exist, early return above)
    # ========================================================
    try:
        if not os.path.exists(ORIGINAL_PATH):
            print(f"FAIL: Component 3 -- Original file not found: {ORIGINAL_PATH}")
        else:
            orig_doc = pymupdf.open(ORIGINAL_PATH)
            out_doc = pymupdf.open(OUTPUT_PATH)
            unchanged_count = 0

            for pg in NON_TARGET_PAGES:
                orig_arr = render_page(orig_doc, pg, scale=1.0)
                out_arr = render_page(out_doc, pg, scale=1.0)

                if orig_arr.shape == out_arr.shape:
                    mean_diff = np.mean(np.abs(orig_arr.astype(float) - out_arr.astype(float)))
                    if mean_diff < 2.0:
                        unchanged_count += 1
                        print(f"PASS: Component 3 -- Page {pg + 1} unchanged (pixel diff: {mean_diff:.2f})")
                    else:
                        print(f"FAIL: Component 3 -- Page {pg + 1} changed (pixel diff: {mean_diff:.2f})")
                else:
                    print(f"FAIL: Component 3 -- Page {pg + 1} size mismatch: {orig_arr.shape} vs {out_arr.shape}")

            orig_doc.close()
            out_doc.close()

            # Proportional scoring
            page_score = 0.3 * (unchanged_count / len(NON_TARGET_PAGES))
            if unchanged_count == len(NON_TARGET_PAGES):
                print(f"PASS: Component 3 -- All non-target pages unchanged ({page_score:.2f} pts)")
                total_score += page_score
            elif unchanged_count > 0:
                print(f"PARTIAL: Component 3 -- {unchanged_count}/{len(NON_TARGET_PAGES)} non-target pages unchanged ({page_score:.2f} pts)")
                total_score += page_score
            else:
                print(f"FAIL: Component 3 -- All non-target pages changed (0.00 pts)")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()

"""
Reward Script: Apply image edits from client_feedback.docx to product.png and save as product_revised.png
Task ID: osworld_multi_apps_writer_gimp_060
Domain: multi_apps (LibreOffice Writer + GIMP)

Scoring Rubric:
  Component 1: product_revised.png exists and has significantly white background (>50% pure white pixels) — 0.4 pts
  Component 2: Background is fully replaced with pure white (>80% pure white pixels) — 0.3 pts
  Component 3: Sharpness is increased compared to original product.png — 0.3 pts
  Total: 1.0

Task Requirements (from client_feedback.docx):
  - Remove shadow on the right side of product
  - Change background to pure white (RGB: 255, 255, 255)
  - Increase sharpness (factor ~2.0 recommended)
  - Save as product_revised.png on the Desktop
"""

import os
from PIL import Image, ImageFilter
import numpy as np

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_writer_gimp_060'

ORIGINAL_PATH = f'{WORKDIR}/product.png'
REVISED_PATH = f'{WORKDIR}/product_revised.png'


def count_pure_white_fraction(img_path):
    """Return fraction of pixels that are exactly (255, 255, 255)."""
    img = Image.open(img_path).convert('RGB')
    arr = np.array(img, dtype=np.float32)
    total = arr.shape[0] * arr.shape[1]
    pure_white = int(np.sum(
        (arr[:, :, 0] == 255) & (arr[:, :, 1] == 255) & (arr[:, :, 2] == 255)
    ))
    return pure_white / total if total > 0 else 0.0


def compute_edge_mean(img_path):
    """Compute edge mean as a proxy for sharpness using PIL FIND_EDGES filter."""
    img = Image.open(img_path).convert('RGB')
    edges = img.filter(ImageFilter.FIND_EDGES)
    arr = np.array(edges, dtype=np.float32)
    return float(np.mean(arr))


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: original product.png must exist
    if not os.path.isfile(ORIGINAL_PATH):
        print(f"CRITICAL: Original file not found: {ORIGINAL_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: product_revised.png must exist to score anything
    if not os.path.isfile(REVISED_PATH):
        print(f"FAIL: product_revised.png not found at {REVISED_PATH}")
        print("Score: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: product_revised.png found at {REVISED_PATH}")

    # -----------------------------------------------------------------------
    # Component 1: product_revised.png exists AND has a significantly white
    #              background (>50% pure white pixels) — 0.4 points
    #
    # The original product.png has 0% pure white pixels. Any meaningful
    # background replacement must produce at least 50% pure white pixels.
    # -----------------------------------------------------------------------
    try:
        revised_white_fraction = count_pure_white_fraction(REVISED_PATH)
        original_white_fraction = count_pure_white_fraction(ORIGINAL_PATH)
        print(f"INFO: Original pure-white fraction: {original_white_fraction:.4f}")
        print(f"INFO: Revised pure-white fraction: {revised_white_fraction:.4f}")

        WHITE_THRESHOLD_BASIC = 0.50  # >50% must be pure white
        if revised_white_fraction > WHITE_THRESHOLD_BASIC and revised_white_fraction > original_white_fraction + 0.10:
            print(f"PASS: Component 1 — product_revised.png has white background "
                  f"({revised_white_fraction:.2%} pure white, exceeds 50% threshold) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — product_revised.png pure-white fraction "
                  f"{revised_white_fraction:.2%} does not exceed 50% threshold (or change from original)")
    except Exception as e:
        print(f"ERROR: Component 1 — could not analyze white fraction: {e}")

    # -----------------------------------------------------------------------
    # Component 2: Background is fully replaced with pure white (>80% pure
    #              white pixels) — 0.3 points
    #
    # The task requests pure white (255,255,255) background. A fully compliant
    # result should have ≥80% of all pixels as pure white, indicating that
    # the entire background (not just parts) has been replaced.
    # This builds on Component 1 — scores only if near-complete replacement.
    # -----------------------------------------------------------------------
    try:
        WHITE_THRESHOLD_FULL = 0.80  # >80% must be pure white
        if revised_white_fraction >= WHITE_THRESHOLD_FULL:
            print(f"PASS: Component 2 — background fully replaced with pure white "
                  f"({revised_white_fraction:.2%} >= 80% threshold) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — pure-white fraction {revised_white_fraction:.2%} "
                  f"is below 80% threshold for full background replacement")
    except Exception as e:
        print(f"ERROR: Component 2 — could not check full white background: {e}")

    # -----------------------------------------------------------------------
    # Component 3: Sharpness has been increased compared to original — 0.3 pts
    #
    # The task requests sharpness enhancement (factor ~2.0). We measure sharpness
    # via the mean intensity of edge-detected pixels using PIL FIND_EDGES.
    # A sharpened image has stronger, more visible edges.
    # -----------------------------------------------------------------------
    try:
        edge_orig = compute_edge_mean(ORIGINAL_PATH)
        edge_rev = compute_edge_mean(REVISED_PATH)
        print(f"INFO: Edge mean (sharpness proxy) original: {edge_orig:.4f}")
        print(f"INFO: Edge mean (sharpness proxy) revised: {edge_rev:.4f}")

        SHARPNESS_DELTA_THRESHOLD = 0.001  # even minimal improvement counts
        if edge_rev > edge_orig + SHARPNESS_DELTA_THRESHOLD:
            print(f"PASS: Component 3 — sharpness increased in revised image "
                  f"(edge mean: {edge_rev:.4f} > {edge_orig:.4f}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — sharpness not increased "
                  f"(edge mean revised {edge_rev:.4f} not > original {edge_orig:.4f})")
    except Exception as e:
        print(f"ERROR: Component 3 — could not check sharpness: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()

"""
Reward Script: Read edit_specs.docx and apply transformations to product_photo.png
Task ID: osworld_multi_apps_writer_to_gimp_003
Domain: multi_apps (libreoffice_writer + gimp)

Task: Read instructions from edit_specs.docx and apply them to product_photo.png:
  - Step 1: Rotate the image 90 degrees clockwise
  - Step 2: Add a 10-pixel solid red border (RGB: 255, 0, 0) around the entire image
  - Save result as product_photo_edited.png on the Desktop

Scoring Rubric:
  Component 1: Output file dimensions match expected (320x420) — 0.4 pts
               (original 400x300 -> rotated 300x400 -> +10px border each side = 320x420)
  Component 2: Red border (10px, RGB 255,0,0) on all four edges — 0.3 pts
  Component 3: Inner content matches 90-deg clockwise rotation of original — 0.3 pts
  Total: 1.0
"""

import os
import sys

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_writer_to_gimp_003'

OUTPUT_FILE = f'{WORKDIR}/product_photo_edited.png'
ORIGINAL_FILE = f'{WORKDIR}/product_photo.png'

# Expected dimensions: original is 400x300, after 90-deg CW rotation: 300x400,
# then +10px border on each side: width=320, height=420
EXPECTED_WIDTH = 320
EXPECTED_HEIGHT = 420
BORDER_SIZE = 10


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: output file must exist
    if not os.path.isfile(OUTPUT_FILE):
        print(f"PRECONDITION FAIL: Output file not found: {OUTPUT_FILE}")
        print(f"Score: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: original file must exist for rotation comparison
    if not os.path.isfile(ORIGINAL_FILE):
        print(f"PRECONDITION FAIL: Original file not found: {ORIGINAL_FILE}")
        print(f"Score: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    try:
        from PIL import Image
        import numpy as np
    except ImportError as e:
        print(f"CRITICAL: Cannot import required libraries: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load the edited image
    try:
        img_edited = Image.open(OUTPUT_FILE).convert('RGB')
        actual_width, actual_height = img_edited.size
        print(f"INFO: Edited image loaded — size: {img_edited.size}, mode: {img_edited.mode}")
    except Exception as e:
        print(f"CRITICAL: Cannot load edited image {OUTPUT_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load the original image for comparison
    try:
        img_orig = Image.open(ORIGINAL_FILE).convert('RGB')
        orig_width, orig_height = img_orig.size
        print(f"INFO: Original image loaded — size: {img_orig.size}")
    except Exception as e:
        print(f"CRITICAL: Cannot load original image {ORIGINAL_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    arr_edited = np.array(img_edited)

    # Component 1: Output file dimensions match expected (320x420) (0.4 points)
    # Expected: original 400x300 -> rotate 90-deg CW -> 300x400 -> add 10px border -> 320x420
    try:
        if actual_width == EXPECTED_WIDTH and actual_height == EXPECTED_HEIGHT:
            print(f"PASS: Component 1 — Dimensions match expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT} "
                  f"(rotated + border). (0.4 pts)")
            total_score += 0.4
        else:
            # Check if dimensions suggest rotation but with different border size
            # After rotation only (no border): 300x400
            # After rotation + 20px border: 340x440
            expected_rotated_no_border = (orig_height, orig_width)  # (300, 400)
            if actual_width == expected_rotated_no_border[0] and actual_height == expected_rotated_no_border[1]:
                print(f"FAIL: Component 1 — Rotation detected but border not applied. "
                      f"Size: {actual_width}x{actual_height}, expected: {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}.")
            elif actual_width == orig_width and actual_height == orig_height:
                print(f"FAIL: Component 1 — No rotation detected. "
                      f"Size: {actual_width}x{actual_height} equals original {orig_width}x{orig_height}.")
            else:
                print(f"FAIL: Component 1 — Unexpected dimensions {actual_width}x{actual_height}, "
                      f"expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}.")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check dimensions: {e}")

    # Component 2: Red border of 10 pixels on all four edges (0.3 points)
    # The outer 10 pixels on each side should all be red (255, 0, 0)
    try:
        # Only check if dimensions match (otherwise border coords are undefined)
        if actual_width == EXPECTED_WIDTH and actual_height == EXPECTED_HEIGHT:
            # Extract border strips
            top_border = arr_edited[:BORDER_SIZE, :, :]       # rows 0-9
            bottom_border = arr_edited[-BORDER_SIZE:, :, :]    # rows -10 to end
            left_border = arr_edited[:, :BORDER_SIZE, :]       # cols 0-9
            right_border = arr_edited[:, -BORDER_SIZE:, :]     # cols -10 to end

            def is_red_border(strip):
                """Check that all pixels in the border strip are red (255, 0, 0)."""
                r = strip[:, :, 0]
                g = strip[:, :, 1]
                b = strip[:, :, 2]
                red_fraction = np.mean((r == 255) & (g == 0) & (b == 0))
                return red_fraction, r.mean(), g.mean(), b.mean()

            top_red, tr, tg, tb = is_red_border(top_border)
            bottom_red, br, bg, bb = is_red_border(bottom_border)
            left_red, lr, lg, lb = is_red_border(left_border)
            right_red, rr, rg, rb = is_red_border(right_border)

            # Require >99% of border pixels to be pure red
            threshold = 0.99
            all_red = (top_red >= threshold and bottom_red >= threshold and
                       left_red >= threshold and right_red >= threshold)

            if all_red:
                print(f"PASS: Component 2 — All {BORDER_SIZE}px border edges are red (255,0,0). "
                      f"Red fractions: top={top_red:.3f}, bottom={bottom_red:.3f}, "
                      f"left={left_red:.3f}, right={right_red:.3f}. (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Border is not fully red. "
                      f"Red fractions: top={top_red:.3f} (R={tr:.1f},G={tg:.1f},B={tb:.1f}), "
                      f"bottom={bottom_red:.3f} (R={br:.1f},G={bg:.1f},B={bb:.1f}), "
                      f"left={left_red:.3f} (R={lr:.1f},G={lg:.1f},B={lb:.1f}), "
                      f"right={right_red:.3f} (R={rr:.1f},G={rg:.1f},B={rb:.1f}). "
                      f"Expected all >= {threshold}.")
        else:
            # Try to detect red border even if dimensions differ
            # Check corner pixels
            corners = [arr_edited[0, 0], arr_edited[0, -1], arr_edited[-1, 0], arr_edited[-1, -1]]
            red_corners = sum(1 for c in corners if c[0] == 255 and c[1] == 0 and c[2] == 0)
            print(f"FAIL: Component 2 — Cannot verify border; dimensions {actual_width}x{actual_height} "
                  f"don't match expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}. "
                  f"Red corners: {red_corners}/4.")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check red border: {e}")

    # Component 3: Inner content matches 90-degree clockwise rotation of original (0.3 points)
    # After removing the 10px border, the inner content should match the original rotated 90-deg CW
    try:
        if actual_width == EXPECTED_WIDTH and actual_height == EXPECTED_HEIGHT:
            # Extract inner region (remove 10px border on all sides)
            inner = arr_edited[BORDER_SIZE:-BORDER_SIZE, BORDER_SIZE:-BORDER_SIZE, :]
            # Expected inner shape: (orig_width, orig_height, 3) = (400, 300, 3)
            expected_inner_height = orig_width   # 400
            expected_inner_width = orig_height   # 300

            # Rotate original 90 degrees clockwise (PIL rotate(-90) or transpose ROTATE_270)
            # PIL.Image.rotate(-90, expand=True) rotates clockwise
            img_rotated = img_orig.rotate(-90, expand=True)
            arr_rotated = np.array(img_rotated.convert('RGB'))

            print(f"INFO: Inner shape: {inner.shape}, Rotated original shape: {arr_rotated.shape}")

            if inner.shape == arr_rotated.shape:
                # Pixel-level comparison with tolerance for compression artifacts
                diff = np.abs(inner.astype(float) - arr_rotated.astype(float))
                mean_diff = float(np.mean(diff))
                max_diff = float(np.max(diff))
                # Fraction of pixels that are nearly identical (within tolerance of 10)
                match_fraction = float(np.mean(np.all(diff < 10, axis=2)))

                print(f"INFO: Pixel diff — mean={mean_diff:.2f}, max={max_diff:.2f}, "
                      f"match_fraction (tol=10)={match_fraction:.4f}")

                # Consider it a match if >95% of pixels are within 10 intensity units
                if match_fraction >= 0.95:
                    print(f"PASS: Component 3 — Inner content matches 90-deg CW rotation of original. "
                          f"Match fraction: {match_fraction:.4f}. (0.3 pts)")
                    total_score += 0.3
                else:
                    # Try counterclockwise rotation to distinguish
                    img_rotated_ccw = img_orig.rotate(90, expand=True)
                    arr_rotated_ccw = np.array(img_rotated_ccw.convert('RGB'))
                    if arr_rotated_ccw.shape == inner.shape:
                        diff_ccw = np.abs(inner.astype(float) - arr_rotated_ccw.astype(float))
                        match_ccw = float(np.mean(np.all(diff_ccw < 10, axis=2)))
                        if match_ccw >= 0.95:
                            print(f"FAIL: Component 3 — Inner content matches 90-deg CCW (not CW) rotation. "
                                  f"Task requires clockwise rotation. CW match: {match_fraction:.4f}, "
                                  f"CCW match: {match_ccw:.4f}.")
                        else:
                            print(f"FAIL: Component 3 — Inner content does not match CW or CCW rotation. "
                                  f"CW match: {match_fraction:.4f}, CCW match: {match_ccw:.4f}.")
                    else:
                        print(f"FAIL: Component 3 — Inner content match fraction too low: {match_fraction:.4f} "
                              f"(threshold: 0.95). Mean diff: {mean_diff:.2f}.")
            else:
                print(f"FAIL: Component 3 — Inner region shape {inner.shape} does not match "
                      f"expected rotated shape {arr_rotated.shape}.")
        else:
            # If dimensions differ but rotation was partial, try without border
            # Attempt to verify if inner content at least looks like rotated original
            print(f"FAIL: Component 3 — Cannot verify rotation; dimensions "
                  f"{actual_width}x{actual_height} don't match expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}.")
    except Exception as e:
        print(f"ERROR: Component 3 — Could not check rotation: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.1f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()

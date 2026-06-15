"""
Reward Script: Read banner_instructions.docx and modify banner_template.png, saving as banner_final.png
Task ID: osworld_multi_apps_writer_to_gimp_006
Domain: multi_apps (libreoffice_writer + gimp)

Instructions (from banner_instructions.docx):
  Step 1: Resize to exactly 1200 x 400 pixels
  Step 2: Change background to #1A237E (dark navy blue = RGB 26, 35, 126)
  Step 3: Add "SUMMER SALE" text centered horizontally and vertically, font size 72, white (#FFFFFF)
  Step 4: Save as banner_final.png on Desktop (do NOT overwrite banner_template.png)

Scoring Rubric:
  Component 1: banner_final.png exists with correct dimensions (1200x400) — 0.30 pts
  Component 2: Background color is dark navy blue (#1A237E) at corners   — 0.30 pts
  Component 3: White text region is present and horizontally centered     — 0.30 pts
  Component 4: banner_template.png is unmodified (original 800x300 size) — 0.10 pts
  Total: 1.0
"""

import os
import sys

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_writer_to_gimp_006'

FINAL_PATH    = f'{WORKDIR}/banner_final.png'
TEMPLATE_PATH = f'{WORKDIR}/banner_template.png'

# Expected values from task instructions
EXPECTED_WIDTH   = 1200
EXPECTED_HEIGHT  = 400
EXPECTED_BG_RGB  = (26, 35, 126)   # #1A237E
BG_TOLERANCE     = 15              # per-channel tolerance for background color check

# Original template dimensions
TEMPLATE_ORIG_WIDTH  = 800
TEMPLATE_ORIG_HEIGHT = 300


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    try:
        from PIL import Image
        import numpy as np
    except ImportError as e:
        print(f"CRITICAL: Missing required library: {e}")
        print("REWARD: 0.0")
        return 0.0

    total_score = 0.0

    # Precondition gate: banner_final.png must exist to score anything
    if not os.path.isfile(FINAL_PATH):
        print(f"FAIL: banner_final.png not found at {FINAL_PATH}")
        print("\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Load the final image
    try:
        img = Image.open(FINAL_PATH)
        arr_rgb = None  # lazy compute
    except Exception as e:
        print(f"CRITICAL: Cannot open banner_final.png: {e}")
        print("\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # ---------------------------------------------------------------
    # Component 1: banner_final.png exists with correct dimensions
    #              (1200 x 400 pixels)  — 0.30 points
    # ---------------------------------------------------------------
    try:
        width, height = img.size
        if width == EXPECTED_WIDTH and height == EXPECTED_HEIGHT:
            print(f"PASS: Component 1 — dimensions correct: {width}x{height} (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}, "
                  f"got {width}x{height}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---------------------------------------------------------------
    # Component 2: Background color is dark navy blue (#1A237E) at corners
    #              Expected RGB ≈ (26, 35, 126)  — 0.30 points
    # ---------------------------------------------------------------
    try:
        arr_rgb = np.array(img.convert("RGB"))
        exp_r, exp_g, exp_b = EXPECTED_BG_RGB

        # Sample 5x5 patches at all four corners
        corners = {
            "top-left":     arr_rgb[:5, :5],
            "top-right":    arr_rgb[:5, -5:],
            "bottom-left":  arr_rgb[-5:, :5],
            "bottom-right": arr_rgb[-5:, -5:],
        }

        corners_pass = 0
        for name, patch in corners.items():
            mean = patch.mean(axis=(0, 1))
            r_ok = abs(mean[0] - exp_r) <= BG_TOLERANCE
            g_ok = abs(mean[1] - exp_g) <= BG_TOLERANCE
            b_ok = abs(mean[2] - exp_b) <= BG_TOLERANCE
            if r_ok and g_ok and b_ok:
                corners_pass += 1
            else:
                print(f"  BG corner {name}: got RGB=({mean[0]:.0f},{mean[1]:.0f},{mean[2]:.0f}) "
                      f"expected≈({exp_r},{exp_g},{exp_b})")

        if corners_pass == 4:
            print(f"PASS: Component 2 — background color #1A237E confirmed at all 4 corners (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — only {corners_pass}/4 corners matched #1A237E background")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---------------------------------------------------------------
    # Component 3: White text region present and horizontally centered
    #              ("SUMMER SALE" white text, centered on 1200x400 canvas)
    #              — 0.30 points
    # ---------------------------------------------------------------
    try:
        if arr_rgb is None:
            arr_rgb = np.array(img.convert("RGB"))

        # Identify bright (near-white) pixels — these represent the text overlay
        # White text: all channels > 200
        WHITE_THRESHOLD = 200
        bright_mask = np.all(arr_rgb > WHITE_THRESHOLD, axis=2)
        bright_count = bright_mask.sum()

        text_detected = False
        text_centered = False
        detail_msg = ""

        if bright_count > 500:   # at least 500 bright pixels = some text is present
            bright_coords = np.where(bright_mask)
            x_min = bright_coords[1].min()
            x_max = bright_coords[1].max()
            text_center_x = (x_min + x_max) / 2.0
            img_center_x  = EXPECTED_WIDTH / 2.0   # 600.0

            horiz_offset = abs(text_center_x - img_center_x)
            # Allow up to 5% of image width (60 px) off-center
            CENTER_TOLERANCE_PX = EXPECTED_WIDTH * 0.05

            text_detected = True
            if horiz_offset <= CENTER_TOLERANCE_PX:
                text_centered = True
                detail_msg = (f"bright_pixels={bright_count}, "
                              f"text_center_x={text_center_x:.1f} vs img_center_x={img_center_x:.1f}, "
                              f"offset={horiz_offset:.1f}px")
            else:
                detail_msg = (f"text not centered: center_x={text_center_x:.1f} "
                              f"vs expected {img_center_x:.1f}, offset={horiz_offset:.1f}px")
        else:
            detail_msg = f"too few bright pixels ({bright_count}) — text may be missing or not white"

        if text_detected and text_centered:
            print(f"PASS: Component 3 — white text overlay present and centered ({detail_msg}) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — {detail_msg}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---------------------------------------------------------------
    # Component 4: Original banner_template.png is unmodified (800x300)
    #              — 0.10 points
    # ---------------------------------------------------------------
    try:
        if not os.path.isfile(TEMPLATE_PATH):
            print(f"FAIL: Component 4 — banner_template.png missing from Desktop")
        else:
            tmpl = Image.open(TEMPLATE_PATH)
            tw, th = tmpl.size
            if tw == TEMPLATE_ORIG_WIDTH and th == TEMPLATE_ORIG_HEIGHT:
                print(f"PASS: Component 4 — banner_template.png preserved at original {tw}x{th} (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 — banner_template.png was modified: "
                      f"got {tw}x{th}, expected {TEMPLATE_ORIG_WIDTH}x{TEMPLATE_ORIG_HEIGHT}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ---------------------------------------------------------------
    # Final
    # ---------------------------------------------------------------
    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task()

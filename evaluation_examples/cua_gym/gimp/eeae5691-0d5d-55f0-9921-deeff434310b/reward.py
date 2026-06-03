"""
Reward Script: Employee Badge with Photo Composite
Task ID: pdf_cross_081
Domain: gimp
Scoring:
  - Component 1: employee_badge.png exists (0.1 pts)
  - Component 2: employee_badge.pdf exists (0.1 pts)
  - Component 3: Badge PNG has correct dimensions from 300 DPI rendering (0.2 pts)
  - Component 4: Photo region at (50,80) shows employee photo (not placeholder) (0.35 pts)
  - Component 5: Badge PDF has 1 page (0.1 pts)
  - Component 6: Badge template structure preserved in header area (0.15 pts)
Total: 1.0
"""

import os

WORKDIR = '/home/user/Documents'
OUTPUT_PNG = f'{WORKDIR}/employee_badge.png'
OUTPUT_PDF = f'{WORKDIR}/employee_badge.pdf'
BADGE_TEMPLATE_PDF = f'{WORKDIR}/badge_template.pdf'
EMPLOYEE_PHOTO = f'{WORKDIR}/employee_photo.jpg'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: employee_badge.png exists (0.1 pts)
    # Gate: if the output PNG doesn't exist, most checks fail
    try:
        if os.path.isfile(OUTPUT_PNG) and os.path.getsize(OUTPUT_PNG) > 1000:
            print(f"PASS: Component 1 — employee_badge.png exists and has content (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — employee_badge.png missing or empty")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: employee_badge.pdf exists (0.1 pts)
    try:
        if os.path.isfile(OUTPUT_PDF) and os.path.getsize(OUTPUT_PDF) > 1000:
            print(f"PASS: Component 2 — employee_badge.pdf exists and has content (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 2 — employee_badge.pdf missing or empty")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Load PNG for detailed checks
    try:
        from PIL import Image
        import numpy as np
        badge_img = Image.open(OUTPUT_PNG).convert("RGB")
        badge_arr = np.array(badge_img)
        w, h = badge_img.size
    except Exception as e:
        print(f"ERROR: Cannot load badge PNG: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 3: Badge PNG has correct dimensions (0.2 pts)
    # The badge template PDF is 243x387 pts; at 300 DPI: 243 * 300/72 = 1012.5 ~ 1013
    # and 387 * 300/72 = 1612.5 ~ 1613
    # Allow a tolerance of ±5 pixels
    try:
        expected_w_min, expected_w_max = 1008, 1018
        expected_h_min, expected_h_max = 1608, 1618
        if (expected_w_min <= w <= expected_w_max and
                expected_h_min <= h <= expected_h_max):
            print(f"PASS: Component 3 — Badge PNG has correct dimensions {w}x{h} "
                  f"(expected ~1013x1613 from 300 DPI rendering) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Badge PNG dimensions {w}x{h} not in expected range "
                  f"({expected_w_min}-{expected_w_max} x {expected_h_min}-{expected_h_max})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Photo region at (50,80) to (200,280) contains employee photo (0.35 pts)
    # The employee photo is resized 150x200 and pasted at (50,80).
    # The badge template placeholder (before pasting) has a blue-gray color from the header area.
    # After pasting the employee photo (portrait with tan skin, blue shirt, gradient bg),
    # the region should be distinctly different from the gray placeholder.
    # Key check: the photo region should NOT be dominated by the gray placeholder color (0.88,0.88,0.88)
    # and should contain color variation consistent with a portrait photo.
    try:
        # Photo region: x=50 to 200, y=80 to 280 (150x200 pixels)
        photo_region = badge_arr[80:280, 50:200]
        photo_h, photo_w = photo_region.shape[:2]

        if photo_h != 200 or photo_w != 150:
            print(f"FAIL: Component 4 — Photo region extracted size {photo_w}x{photo_h}, "
                  f"expected 150x200 (badge too small?)")
        else:
            # The template placeholder has mostly grayish/bluish pixels
            # (avg ~112, 143, 204 from rendering)
            # The employee photo region should be more colorful and less blue-dominant
            # Check 1: Mean color differs sufficiently from template placeholder
            region_mean = photo_region.mean(axis=(0, 1))

            # The placeholder region in template has high blue (avg ~204 blue channel)
            # The photo paste results in a region with more varied colors
            # The employee photo has: tan face (~255,220,185), dark hair (~80,40,20),
            # blue shirt (~30,60,130), light bg (~180,200,220)
            # Average after resize will be a mix, resulting in more neutral colors

            # Key distinguisher: template placeholder has R=112, G=143, B=204
            # After paste: R=137, G=133, B=140 (much more neutral, less blue-dominant)
            # Check: green channel significantly less than what template has
            template_placeholder_g = 143.0
            template_placeholder_b = 204.0

            # If blue dominance is gone (B < 180) and pixel variance is high = photo is pasted
            region_std = photo_region.std()
            b_channel_mean = region_mean[2]

            # Template placeholder: B ~204, std ~40 (some variation from "Photo Here" text)
            # Photo pasted: B ~140, std higher due to image content variation

            if b_channel_mean < 180 and region_std > 30:
                print(f"PASS: Component 4 — Photo region at (50,80) contains employee photo "
                      f"(avg color: R={region_mean[0]:.1f} G={region_mean[1]:.1f} B={region_mean[2]:.1f}, "
                      f"std={region_std:.1f}; not placeholder) (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 4 — Photo region at (50,80) appears to still show "
                      f"placeholder (avg B={b_channel_mean:.1f} >= 180 or std={region_std:.1f} <= 30). "
                      f"Employee photo was not pasted correctly.")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Badge PDF has exactly 1 page (0.1 pts)
    try:
        import pymupdf
        pdf_doc = pymupdf.open(OUTPUT_PDF)
        num_pages = len(pdf_doc)
        pdf_doc.close()
        if num_pages == 1:
            print(f"PASS: Component 5 — employee_badge.pdf has 1 page (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 5 — employee_badge.pdf has {num_pages} pages, expected 1")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Badge header area preserved (blue company header still present) (0.15 pts)
    # The top of the badge (y=0 to 50 in 300 DPI = ~209 pixels) should have blue header
    # The blue color is approximately (25, 76, 178) = (0.1, 0.3, 0.7) * 255
    try:
        # Top header region: first ~209 rows, full width
        header_rows = int(50 * 300 / 72)  # 50pt * (300dpi/72pt) ≈ 208 px
        header_region = badge_arr[:header_rows, :]
        header_mean = header_region.mean(axis=(0, 1))

        # Blue header: R ~25, G ~76, B ~178
        # Check blue is significantly higher than red
        if header_mean[2] > header_mean[0] * 3 and header_mean[2] > 100:
            print(f"PASS: Component 6 — Badge header area preserved with blue color "
                  f"(avg R={header_mean[0]:.1f} G={header_mean[1]:.1f} B={header_mean[2]:.1f}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 — Badge header blue color not detected "
                  f"(avg R={header_mean[0]:.1f} G={header_mean[1]:.1f} B={header_mean[2]:.1f})")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

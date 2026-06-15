"""
Reward Script: Process event_photo.jpg using GIMP as instructed in processing_request.docx
Task ID: osworld_multi_apps_writer_to_gimp_010
Domain: multi_apps (libreoffice_writer + gimp)

Task Summary:
  The agent reads 'processing_request.docx' on the Desktop, which specifies:
    1. Resize event_photo.jpg to exactly 1920x1080 (no aspect ratio preservation)
    2. Increase brightness by a factor of 1.3
    3. Add watermark text "Event 2025" in the bottom-right corner (white, semi-transparent)
  Output must be saved as 'event_photo_processed.jpg' on the Desktop.

Scoring Rubric:
  Component 1: Output file exists and has correct dimensions (1920x1080)  — 0.35 pts
  Component 2: Image brightness is significantly increased (~1.3x)          — 0.35 pts
  Component 3: Watermark "Event 2025" visible in bottom-right corner        — 0.30 pts
  Total: 1.0

Note: The initial state has NO event_photo_processed.jpg, so these checks fail on initial_env.
"""

import os
from PIL import Image, ImageStat
import numpy as np

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_writer_to_gimp_010'

# Target output file path
OUTPUT_FILE = os.path.join(WORKDIR, 'event_photo_processed.jpg')

# Original source file path
SOURCE_FILE = os.path.join(WORKDIR, 'event_photo.jpg')

# Expected dimensions after resize
TARGET_WIDTH = 1920
TARGET_HEIGHT = 1080

# Brightness factor specified in the document
BRIGHTNESS_FACTOR = 1.3

# Original source image brightness (measured baseline from initial_env)
# Original image (2560x1440) had brightness ~100.03
# After resize and 1.3x brightness: expected ~130
ORIGINAL_BRIGHTNESS_APPROX = 100.0  # known approximate value from initial_env
EXPECTED_BRIGHTNESS_MIN = 110.0  # after 1.3x, must be clearly above original
EXPECTED_BRIGHTNESS_MAX = 200.0  # upper bound to guard against over-brightened artifacts


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: Check output file exists
    if not os.path.isfile(OUTPUT_FILE):
        print(f"FAIL: Output file not found: {OUTPUT_FILE}")
        print(f"Score: 0.0/1.0")
        print(f"REWARD: 0.0")
        return 0.0

    # Load the output image
    try:
        img = Image.open(OUTPUT_FILE).convert("RGB")
    except Exception as e:
        print(f"CRITICAL: Cannot load output file {OUTPUT_FILE}: {e}")
        print(f"Score: 0.0/1.0")
        print(f"REWARD: 0.0")
        return 0.0

    # Component 1: Output file exists with correct dimensions 1920x1080 (0.35 points)
    # This FAILS on initial_env (no event_photo_processed.jpg exists)
    # This PASSES on golden_env (event_photo_processed.jpg is 1920x1080)
    try:
        width, height = img.size
        if width == TARGET_WIDTH and height == TARGET_HEIGHT:
            print(f"PASS: Component 1 — Correct dimensions {width}x{height} (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — Expected {TARGET_WIDTH}x{TARGET_HEIGHT}, found {width}x{height}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Image brightness is significantly increased by factor ~1.3 (0.35 points)
    # Original image brightness was ~100, after 1.3x should be ~130
    # We check that the processed brightness is in range [110, 200]
    # This FAILS on initial_env (no processed file exists, handled by precondition above)
    # This PASSES on golden_env (brightness ~127.5, within expected range)
    try:
        gray = img.convert('L')
        brightness = ImageStat.Stat(gray).mean[0]
        if EXPECTED_BRIGHTNESS_MIN <= brightness <= EXPECTED_BRIGHTNESS_MAX:
            print(f"PASS: Component 2 — Brightness {brightness:.2f} is in expected range "
                  f"[{EXPECTED_BRIGHTNESS_MIN}, {EXPECTED_BRIGHTNESS_MAX}] (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — Brightness {brightness:.2f} not in expected range "
                  f"[{EXPECTED_BRIGHTNESS_MIN}, {EXPECTED_BRIGHTNESS_MAX}]")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Watermark "Event 2025" visible in bottom-right corner (0.30 points)
    # The watermark is white/semi-transparent text. We detect it by:
    # - Looking for bright pixels (>180 in all channels) in the bottom-right region
    # - The original event_photo.jpg had 0 white pixels in the bottom-right region
    # - The golden image has white-ish pixels from the watermark text
    # This FAILS on initial_env (original has no bright pixels in bottom-right)
    # This PASSES on golden_env (watermark creates bright pixels in bottom-right)
    try:
        img_arr = np.array(img)
        img_width, img_height = img.size

        # Define bottom-right corner region (last 25% width, last 15% height)
        br_x_start = int(img_width * 0.75)
        br_y_start = int(img_height * 0.85)
        br_region = img_arr[br_y_start:, br_x_start:]

        # Count pixels that are bright (white-ish, > 200 on all channels)
        # These indicate the white watermark text
        bright_mask = (br_region[:, :, 0] > 200) & (br_region[:, :, 1] > 200) & (br_region[:, :, 2] > 200)
        bright_pixel_count = np.sum(bright_mask)
        total_br_pixels = br_region.shape[0] * br_region.shape[1]
        bright_ratio = bright_pixel_count / max(total_br_pixels, 1)

        # Original image has 0 bright pixels in BR; watermark adds visible text
        # A threshold of 0.005 (0.5%) ensures genuine white text is detected
        if bright_ratio >= 0.005:
            print(f"PASS: Component 3 — Watermark detected in bottom-right corner "
                  f"(bright pixels ratio: {bright_ratio:.4f}, count: {bright_pixel_count}) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — No watermark detected in bottom-right corner "
                  f"(bright pixels ratio: {bright_ratio:.4f}, count: {bright_pixel_count}); "
                  f"Expected 'Event 2025' text watermark")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

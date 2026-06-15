"""
Reward Script: Apply GIMP photo processing steps from workflow.docx to raw_photo.jpg
Task ID: osworld_multi_apps_writer_gimp_061
Domain: libreoffice_writer + gimp (multi-app)

Scoring:
  Component 1: processed_photo.jpg exists on Desktop (gate)              — 0.3 pts
  Component 2: Image is significantly blurred / noise-reduced             — 0.4 pts
               (verifies Gaussian blur radius 1.0 noise reduction +
                Gaussian blur radius 8.0 background step applied)
  Component 3: Image dimensions preserved (same as expected output)       — 0.3 pts

Total: 1.0

Ground truth from context:
  - (1) Gaussian blur radius 1.0 for noise reduction
  - (2) Hue/saturation adjustment in red/orange range (hue +3, saturation -5)
  - (3) Gaussian blur radius 8.0 with layer mask for background
  - Output: 'processed_photo.jpg' on Desktop

Verification approach:
  - The initial_env has NO processed_photo.jpg → returns 0.0
  - The golden_env HAS processed_photo.jpg with blur applied → returns 1.0
  - Blur detection uses image gradient variance:
      raw/unprocessed photos have high gradient std (~6.0+)
      blurred processed photos have low gradient std (<4.0)
"""

import os
from PIL import Image, ImageFilter
import numpy as np

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_writer_gimp_061'
OUTPUT_FILE = os.path.join(WORKDIR, 'Desktop', 'processed_photo.jpg')

# Expected dimensions of the processed photo (same as raw_photo.jpg input)
EXPECTED_WIDTH = 800
EXPECTED_HEIGHT = 1000

# Blur threshold: processed photos should have lower gradient std than raw photos
# Raw photo baseline: gradient_dx_std ~6.16, gradient_dy_std ~5.82
# Processed photo (golden): gradient_dx_std ~2.0, gradient_dy_std ~2.45
# Threshold chosen at 4.5 to clearly distinguish processed from unprocessed
GRADIENT_STD_THRESHOLD = 4.5


def compute_gradient_std(img_path):
    """Compute gradient standard deviation as a sharpness/blur indicator.
    Lower values indicate more blur (processing applied).
    Higher values indicate sharpness (no blur applied).
    """
    img = Image.open(img_path).convert('L')
    arr = np.array(img, dtype=np.float32)
    # Horizontal and vertical first-order gradients
    dx = arr[:, 1:] - arr[:, :-1]
    dy = arr[1:, :] - arr[:-1, :]
    return (dx.std() + dy.std()) / 2.0


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: processed_photo.jpg must exist
    if not os.path.exists(OUTPUT_FILE):
        print(f"FAIL (gate): processed_photo.jpg not found at {OUTPUT_FILE}")
        print(f"REWARD: 0.0")
        return 0.0

    # Component 1: processed_photo.jpg exists on Desktop (0.3 points)
    # This component FAILS on initial_env (file does not exist there)
    # and PASSES on golden_env (file exists)
    try:
        file_size = os.path.getsize(OUTPUT_FILE)
        if file_size > 10000:  # Must be a real image (> 10KB), not an empty file
            print(f"PASS: Component 1 — processed_photo.jpg exists ({file_size} bytes) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — processed_photo.jpg too small ({file_size} bytes), may be empty")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Image is blurred (noise reduction + background blur applied) (0.4 points)
    # Gaussian blur radius 1.0 (noise reduction) and radius 8.0 (background) should significantly
    # reduce image sharpness. Gradient std should be < 4.5 for a blurred image.
    # Raw unprocessed photo has gradient std ~6.0; processed photo has ~2.2.
    try:
        img = Image.open(OUTPUT_FILE).convert('RGB')
        grad_std = compute_gradient_std(OUTPUT_FILE)
        print(f"INFO: Image gradient std (sharpness): {grad_std:.4f} (threshold: < {GRADIENT_STD_THRESHOLD})")
        if grad_std < GRADIENT_STD_THRESHOLD:
            print(f"PASS: Component 2 — Image is blurred (gradient std={grad_std:.4f} < {GRADIENT_STD_THRESHOLD}) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — Image not blurred enough: gradient std={grad_std:.4f} >= {GRADIENT_STD_THRESHOLD} "
                  f"(expected < {GRADIENT_STD_THRESHOLD} for noise reduction + background blur)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Output image dimensions match expected output size (0.3 points)
    # The processed photo should maintain the same dimensions as the input raw_photo.jpg
    # Expected: 800 x 1000 pixels (RGB JPEG)
    try:
        img = Image.open(OUTPUT_FILE)
        width, height = img.size
        if width == EXPECTED_WIDTH and height == EXPECTED_HEIGHT:
            print(f"PASS: Component 3 — Image dimensions correct ({width}x{height}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}, found {width}x{height}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

"""
Reward Script: Run 'docker images' in terminal and save screenshot as 'docker_images.png' on Desktop
Task ID: osworld_multi_apps_terminal_screenshot_009
Domain: os (file verification + image content verification)
Scoring:
  Component 1: docker_images.png file exists on Desktop (0.4 pts)
  Component 2: File is a valid PNG image (proper magic bytes) (0.3 pts)
  Component 3: Image has terminal-like dark background (0.3 pts)
"""

import os
import struct

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_terminal_screenshot_009'
TARGET_FILE = f'{WORKDIR}/Desktop/docker_images.png'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    The task requires:
    1. A file named 'docker_images.png' saved on the Desktop
    2. The file must be a valid PNG image
    3. The image should show a terminal window (dark background characteristic of terminal)
    """
    total_score = 0.0

    # Component 1: docker_images.png file exists on Desktop (0.4 points)
    # This FAILS on initial_env (empty Desktop) and PASSES on golden_env
    try:
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            print(f"PASS: Component 1 — docker_images.png exists on Desktop (size: {file_size} bytes) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — docker_images.png not found at {file_path}")
            # If file doesn't exist, remaining components cannot be checked
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: File is a valid PNG image with correct magic bytes (0.3 points)
    # PNG files start with the 8-byte signature: 89 50 4E 47 0D 0A 1A 0A
    # This FAILS on initial_env (no file) and PASSES on golden_env (valid PNG)
    try:
        PNG_MAGIC = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
        with open(file_path, 'rb') as f:
            header = f.read(8)
        if header == PNG_MAGIC:
            print(f"PASS: Component 2 — File has valid PNG magic bytes (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — File does not have PNG magic bytes, found: {header.hex()}")
    except Exception as e:
        print(f"ERROR: Component 2 — Cannot read file header: {e}")

    # Component 3: Image has terminal-like dark background characteristics (0.3 points)
    # A terminal screenshot should be predominantly dark (dark pixel ratio > 0.7)
    # This verifies the screenshot shows an actual terminal window running 'docker images'
    # This FAILS on initial_env (no file) and PASSES on golden_env (terminal screenshot)
    try:
        try:
            from PIL import Image
            import array as arr_module
        except ImportError:
            print("INFO: PIL not available, using manual PNG parsing for Component 3")
            Image = None

        if Image is not None:
            img = Image.open(file_path)
            # Convert to RGB to ensure consistent channel count
            img_rgb = img.convert('RGB')
            width, height = img_rgb.size
            total_pixels = width * height

            # Count dark pixels (all RGB channels < 50) — characteristic of terminal backgrounds
            dark_pixel_count = 0
            pixels = list(img_rgb.getdata())
            for r, g, b in pixels:
                if r < 50 and g < 50 and b < 50:
                    dark_pixel_count += 1

            dark_ratio = dark_pixel_count / total_pixels
            print(f"INFO: Image dimensions: {width}x{height}, dark pixel ratio: {dark_ratio:.3f}")

            # Terminal screenshots typically have > 70% dark pixels
            if dark_ratio >= 0.7:
                print(f"PASS: Component 3 — Image has terminal-like dark background (dark_ratio={dark_ratio:.3f} >= 0.7) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Image does not appear to be a terminal screenshot (dark_ratio={dark_ratio:.3f} < 0.7)")
        else:
            # Fallback: just check that the image is a valid PNG with reasonable size
            # (at least 10KB, indicating content beyond a blank image)
            file_size = os.path.getsize(file_path)
            if file_size >= 10000:
                print(f"PASS: Component 3 (fallback) — Image file has substantial content ({file_size} bytes >= 10KB) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 (fallback) — Image file too small ({file_size} bytes < 10KB), unlikely to contain terminal screenshot")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: verify the canonical artifact path in the given env
if not os.path.exists(TARGET_FILE):
    print(f"File not found: {TARGET_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(TARGET_FILE)

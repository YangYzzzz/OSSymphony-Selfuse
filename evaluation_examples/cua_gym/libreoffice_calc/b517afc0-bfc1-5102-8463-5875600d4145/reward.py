"""
Reward Script: Execute 'env | sort' in terminal, save screenshot as env_vars.png on Desktop
Task ID: osworld_multi_apps_terminal_screenshot_012
Domain: os (multi_apps)
Scoring:
  - Component 1 (0.5): env_vars.png is a valid PNG file on the Desktop
  - Component 2 (0.3): Image has dark terminal-style background (mean pixel < 80, indicating terminal)
  - Component 3 (0.2): Image contains text-like pixels (light pixels among dark background = terminal text)
"""

import os
import struct

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_terminal_screenshot_012'
PNG_PATH = f'{WORKDIR}/Desktop/env_vars.png'


def is_valid_png(file_path):
    """Check if file is a valid PNG by reading its header bytes."""
    PNG_MAGIC = b'\x89PNG\r\n\x1a\n'
    try:
        with open(file_path, 'rb') as f:
            header = f.read(8)
        return header == PNG_MAGIC
    except Exception:
        return False


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: env_vars.png is a valid PNG file on the Desktop (0.5 points)
    # This checks that the file exists AND is a valid PNG (not just any file).
    # Fails on initial_env (file not present) and passes on golden_env.
    try:
        if not os.path.isfile(file_path):
            print(f"FAIL: Component 1 — {file_path} does not exist")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        if is_valid_png(file_path):
            file_size = os.path.getsize(file_path)
            print(f"PASS: Component 1 — env_vars.png is a valid PNG file on Desktop (size: {file_size} bytes) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — {file_path} exists but is not a valid PNG file")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Image has dark terminal-style background (0.3 points)
    # A terminal screenshot will have a predominantly dark background (mean pixel value < 80).
    # This distinguishes a terminal screenshot from a bright/white screenshot.
    # Fails on initial_env (file not present) and passes on golden_env.
    try:
        import numpy as np
        from PIL import Image

        img = Image.open(file_path)
        arr = np.array(img.convert('RGB'))
        mean_pixel = arr.mean()

        if mean_pixel < 80:
            print(f"PASS: Component 2 — Image has dark terminal-style background (mean pixel: {mean_pixel:.2f} < 80) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Image does not appear to be a terminal screenshot (mean pixel: {mean_pixel:.2f}, expected < 80)")
    except ImportError:
        # If PIL/numpy not available, skip this component and log
        print("SKIP: Component 2 — PIL/numpy not available; checking file size as proxy")
        # Fallback: A valid terminal screenshot should be > 5000 bytes (non-trivial content)
        try:
            file_size = os.path.getsize(file_path)
            if file_size > 5000:
                print(f"PASS: Component 2 (fallback) — file size {file_size} bytes suggests non-trivial image content (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 (fallback) — file size {file_size} bytes too small for a terminal screenshot")
        except Exception as e2:
            print(f"ERROR: Component 2 fallback — {e2}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Image contains text-like pixels (0.2 points)
    # A terminal screenshot with environment variable output will have light-colored text
    # pixels against the dark background. We check for the presence of light pixels
    # (value > 180) spread across multiple rows of the image, which indicates text content.
    # Fails on initial_env (file not present) and passes on golden_env.
    try:
        import numpy as np
        from PIL import Image

        img = Image.open(file_path)
        arr = np.array(img.convert('RGB'))

        # Count light pixels (text) vs total pixels
        light_pixels = (arr > 180).all(axis=2)
        light_pixel_count = light_pixels.sum()
        total_pixels = arr.shape[0] * arr.shape[1]
        light_percentage = light_pixel_count / total_pixels * 100

        # Check that light pixels appear in multiple rows (text content spread across image)
        rows_with_light = int(np.any(light_pixels, axis=1).sum())

        if light_pixel_count > 100 and rows_with_light > 5:
            print(f"PASS: Component 3 — Image contains text-like pixels ({light_pixel_count} light pixels, {rows_with_light} rows with text) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Image lacks text-like content (light_pixels: {light_pixel_count}, rows_with_light: {rows_with_light})")
    except ImportError:
        # If PIL/numpy not available, skip component 3
        print("SKIP: Component 3 — PIL/numpy not available; cannot verify image text content")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path on VM
if not os.path.isfile(PNG_PATH):
    print(f"File not found: {PNG_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(PNG_PATH)

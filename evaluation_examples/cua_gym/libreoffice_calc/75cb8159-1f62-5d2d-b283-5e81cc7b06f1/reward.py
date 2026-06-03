"""
Reward Script: Save terminal screenshot of crontab output to Desktop
Task ID: osworld_multi_apps_terminal_screenshot_011
Domain: multi_apps (OS + terminal + screenshot)
Scoring:
  Component 1 (0.5): crontab_output.png exists at /home/user/Desktop/crontab_output.png
  Component 2 (0.3): File is a valid PNG image (PNG magic bytes + loadable)
  Component 3 (0.2): Image has terminal screenshot characteristics (dark background > 50% of pixels)
Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_terminal_screenshot_011'
TARGET_FILE = '/home/user/Desktop/crontab_output.png'

# PNG magic bytes signature
PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Task: Run 'crontab -l' in terminal, screenshot the terminal window,
          save as 'crontab_output.png' on the Desktop.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: crontab_output.png exists on the Desktop (0.5 points)
    # This is the primary deliverable of the task — saving the screenshot file.
    try:
        if os.path.isfile(TARGET_FILE):
            file_size = os.path.getsize(TARGET_FILE)
            print(f"PASS: Component 1 — crontab_output.png exists on Desktop (size: {file_size} bytes) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — crontab_output.png not found at {TARGET_FILE}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: File is a valid PNG image (0.3 points)
    # Verifies the file was actually saved as PNG format (not just renamed).
    try:
        if os.path.isfile(TARGET_FILE):
            # Check PNG magic bytes
            with open(TARGET_FILE, 'rb') as f:
                header = f.read(8)
            png_valid = (header == PNG_SIGNATURE)
            if png_valid:
                print(f"PASS: Component 2 — crontab_output.png has valid PNG signature (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — File does not have PNG magic bytes. Header: {header.hex()[:16]}")
        else:
            print(f"FAIL: Component 2 — File not found, cannot verify PNG format")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Image has terminal screenshot characteristics (0.2 points)
    # A terminal screenshot has predominantly dark background (dark background pixel ratio > 50%).
    # This distinguishes an actual terminal screenshot from a blank or unrelated image.
    try:
        if os.path.isfile(TARGET_FILE):
            try:
                from PIL import Image
                import struct

                # Use raw pixel data analysis without numpy
                img = Image.open(TARGET_FILE)
                img = img.convert('RGB')
                width, height = img.size

                # Check image dimensions — minimum reasonable size for a terminal screenshot
                if width < 50 or height < 50:
                    print(f"FAIL: Component 3 — Image too small ({width}x{height}), not a valid screenshot")
                else:
                    # Sample pixels to check dark background ratio
                    # Sample a subset of pixels for efficiency
                    dark_count = 0
                    sample_count = 0
                    step = max(1, (width * height) // 5000)  # Sample ~5000 pixels

                    pixels = list(img.getdata())
                    for idx in range(0, len(pixels), step):
                        r, g, b = pixels[idx]
                        sample_count += 1
                        # Dark pixel: all channels below threshold (typical terminal background)
                        if r < 80 and g < 80 and b < 80:
                            dark_count += 1

                    dark_ratio = dark_count / sample_count if sample_count > 0 else 0
                    print(f"  Image size: {width}x{height}, dark pixel ratio: {dark_ratio:.4f} (sampled {sample_count} pixels)")

                    if dark_ratio > 0.5:
                        print(f"PASS: Component 3 — Image has terminal-like dark background (dark ratio: {dark_ratio:.2%}) (0.2 pts)")
                        total_score += 0.2
                    else:
                        print(f"FAIL: Component 3 — Image dark ratio {dark_ratio:.2%} is too low for a terminal screenshot (need > 50%)")
            except ImportError:
                # PIL not available — try basic file size heuristic
                file_size = os.path.getsize(TARGET_FILE)
                # A terminal screenshot should be at least a few KB
                if file_size > 1000:
                    print(f"PASS: Component 3 — File has reasonable size ({file_size} bytes) suggesting valid screenshot content (PIL not available for full check) (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 3 — File too small ({file_size} bytes), likely not a valid screenshot")
        else:
            print(f"FAIL: Component 3 — File not found, cannot verify image characteristics")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path on VM
if not os.path.isfile(TARGET_FILE):
    print(f"File not found: {TARGET_FILE}")
    print("REWARD: 0.0")
else:
    verify_task()

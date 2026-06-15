"""
Reward Script: Take a terminal screenshot of 'ifconfig' and save as 'network_info.png' on Desktop
Task ID: osworld_multi_apps_terminal_screenshot_003
Domain: os (terminal/screenshot)
Scoring:
  Component 1: network_info.png exists on Desktop (0.4 pts)
  Component 2: File is a valid PNG (0.3 pts)
  Component 3: Image content is consistent with a terminal screenshot (0.3 pts)
Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_terminal_screenshot_003'
TARGET_FILE = os.path.join(WORKDIR, 'Desktop', 'network_info.png')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: network_info.png exists on the Desktop (0.4 points)
    # This FAILS on initial_env (empty Desktop) and PASSES on golden_env
    try:
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            if file_size > 1000:
                print(f"PASS: Component 1 — network_info.png exists on Desktop (size: {file_size} bytes) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — network_info.png exists but is too small ({file_size} bytes), likely invalid")
        else:
            print(f"FAIL: Component 1 — network_info.png not found at {file_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: File is a valid PNG (0.3 points)
    # The file must have the correct PNG magic bytes (89 50 4E 47 0D 0A 1A 0A)
    # This FAILS on initial_env (file does not exist) and PASSES on golden_env
    try:
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                header = f.read(8)
            expected_header = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
            if header == expected_header:
                print(f"PASS: Component 2 — File has valid PNG magic bytes (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — File does not have valid PNG header: {header.hex()}")
        else:
            print(f"FAIL: Component 2 — Cannot check PNG header, file does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Image is consistent with a terminal screenshot (0.3 points)
    # A terminal screenshot should have:
    #   - Dark background dominating (>60% pixels with mean intensity < 80)
    #   - Limited unique colors (< 2000) typical of terminal text rendering
    #   - Non-trivial image dimensions (width > 200, height > 100)
    # This FAILS on initial_env (file does not exist) and PASSES on golden_env
    try:
        if os.path.isfile(file_path):
            from PIL import Image
            import numpy as np

            img = Image.open(file_path)
            width, height = img.size

            # Check dimensions are reasonable for a terminal window
            if width < 200 or height < 100:
                print(f"FAIL: Component 3 — Image dimensions too small for a terminal screenshot: {width}x{height}")
            else:
                arr = np.array(img.convert('RGB'))
                total_pixels = arr.shape[0] * arr.shape[1]

                # Check for dark background (terminal characteristic)
                mean_intensity = arr.mean(axis=2)
                dark_pixels = int((mean_intensity < 80).sum())
                dark_ratio = dark_pixels / total_pixels

                # Count unique colors (limited in terminal = text rendering)
                flat = arr.reshape(-1, 3)
                unique_colors = len(set(map(tuple, flat.tolist())))

                print(f"  Image dimensions: {width}x{height}")
                print(f"  Dark pixels (<80 intensity): {dark_pixels}/{total_pixels} ({dark_ratio*100:.1f}%)")
                print(f"  Unique colors: {unique_colors}")

                # Terminal screenshot criteria: predominantly dark background + limited color palette
                is_dark = dark_ratio > 0.60
                is_limited_colors = unique_colors < 5000

                if is_dark and is_limited_colors:
                    print(f"PASS: Component 3 — Image is consistent with a terminal screenshot "
                          f"(dark_ratio={dark_ratio:.2f}, unique_colors={unique_colors}) (0.3 pts)")
                    total_score += 0.3
                elif is_dark:
                    print(f"FAIL: Component 3 — Image is dark but has too many colors ({unique_colors}), "
                          f"may not be a terminal screenshot")
                else:
                    print(f"FAIL: Component 3 — Image does not appear to be a dark terminal screenshot "
                          f"(dark_ratio={dark_ratio:.2f})")
        else:
            print(f"FAIL: Component 3 — Cannot check image content, file does not exist")
    except ImportError:
        # PIL/numpy not available — skip this component gracefully
        print(f"SKIP: Component 3 — PIL/numpy not available, skipping image content check")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(os.path.dirname(TARGET_FILE)):
    print(f"Desktop directory not found: {os.path.dirname(TARGET_FILE)}")
    print("REWARD: 0.0")
else:
    verify_task(TARGET_FILE)

"""
Reward Script: Take a screenshot of Chrome showing httpbin.org/get and save to Desktop
Task ID: osworld_multi_apps_sys_browser_os_003
Domain: os/browser
Scoring:
  - Component 1 (0.5 pts): File /home/user/Desktop/httpbin_screenshot.png exists
  - Component 2 (0.3 pts): File is a valid PNG image (correct magic bytes)
  - Component 3 (0.2 pts): PNG has reasonable screenshot dimensions (>= 100x100 pixels)
"""

import os
import struct

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_sys_browser_os_003'
SCREENSHOT_PATH = '/home/user/Desktop/httpbin_screenshot.png'

# PNG magic bytes: 137 80 78 71 13 10 26 10
PNG_MAGIC = b'\x89PNG\r\n\x1a\n'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Task: Take a screenshot of Chrome window showing httpbin.org/get,
          save it to /home/user/Desktop/httpbin_screenshot.png.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Screenshot file exists at expected path (0.5 points)
    # This FAILS on initial_env (file not present) and PASSES on golden_env
    try:
        if os.path.isfile(SCREENSHOT_PATH):
            file_size = os.path.getsize(SCREENSHOT_PATH)
            print(f"PASS: Component 1 — screenshot file exists at {SCREENSHOT_PATH} (size: {file_size} bytes) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — screenshot file not found at {SCREENSHOT_PATH}")
            # No point checking further components if file doesn't exist
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — could not check file existence: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: File is a valid PNG (correct magic bytes) (0.3 points)
    # This FAILS on initial_env (file not present) and PASSES on golden_env
    try:
        with open(SCREENSHOT_PATH, 'rb') as f:
            header = f.read(8)
        if header == PNG_MAGIC:
            print(f"PASS: Component 2 — file has valid PNG magic bytes (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — file does not have valid PNG magic bytes, got: {header[:8].hex()}")
    except Exception as e:
        print(f"ERROR: Component 2 — could not read file header: {e}")

    # Component 3: PNG has reasonable screenshot dimensions (>= 100x100) (0.2 points)
    # This FAILS on initial_env (file not present) and PASSES on golden_env
    # A real screenshot should be at least 100x100 pixels
    try:
        with open(SCREENSHOT_PATH, 'rb') as f:
            # Skip PNG signature (8 bytes)
            f.seek(8)
            # Read IHDR chunk: 4-byte length, 4-byte type, then width/height
            chunk_length = struct.unpack('>I', f.read(4))[0]
            chunk_type = f.read(4).decode('ascii', errors='replace')
            if chunk_type == 'IHDR':
                width = struct.unpack('>I', f.read(4))[0]
                height = struct.unpack('>I', f.read(4))[0]
                if width >= 100 and height >= 100:
                    print(f"PASS: Component 3 — PNG has screenshot dimensions {width}x{height} (>= 100x100) (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 3 — PNG dimensions {width}x{height} are too small (< 100x100), not a real screenshot")
            else:
                print(f"FAIL: Component 3 — first PNG chunk is '{chunk_type}', expected 'IHDR'; cannot determine dimensions")
    except Exception as e:
        print(f"ERROR: Component 3 — could not read PNG dimensions: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()

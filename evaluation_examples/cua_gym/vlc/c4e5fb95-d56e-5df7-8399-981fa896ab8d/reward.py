"""
FINAL REWARD SCRIPT - SUCCESS
Task: Capture high-resolution screenshot and save as /home/user/Desktop/movie_poster.bmp.
Generated: 2025-09-13 13:19:20
Status: success
Model: azure-o3
Total Steps: 3
"""

import os
import struct

"""
Reward Script for VLC Screenshot Task
Task: Capture a high-resolution screenshot and save it as
       /home/user/Desktop/movie_poster.bmp

This script verifies task completion in three progressive steps:
1. File existence **and** valid BMP header         – 0.30 pts
2. Resolution ≥ 1920 × 1080 (Full HD)              – 0.40 pts
3. Resolution ≥ 3000 × 2000 (very high resolution) – 0.30 pts
Only when all three checks pass does the script return 1.0.
The script prints detailed diagnostics and always outputs the final
reward as  "REWARD: X.X".
"""

def _get_bmp_dimensions(file_path: str):
    """Return (width, height) from a BMP file header."""
    with open(file_path, "rb") as f:
        header = f.read(26)  # BMP width/height live at offset 18 & 22 (4 bytes each)
    if len(header) < 26 or header[0:2] != b"BM":
        raise ValueError("File is not a valid BMP")
    width  = int.from_bytes(header[18:22], "little", signed=False)
    height = int.from_bytes(header[22:26], "little", signed=False)
    return width, height

def verify_task():
    target = "/home/user/Desktop/movie_poster.bmp"
    score  = 0.0
    max_score = 1.0

    # --- Check 1: File exists & is a valid BMP --------------------------------
    if os.path.exists(target):
        try:
            width, height = _get_bmp_dimensions(target)
            print(f"✓ Found BMP {target} – dimensions: {width}×{height}")
            score += 0.30  # earned for correct file + valid BMP header

            # --- Check 2: At least Full-HD resolution --------------------------
            if width >= 1920 and height >= 1080:
                print("✓ Resolution is at least Full HD (1920×1080)")
                score += 0.40
            else:
                print("✗ Resolution below Full HD threshold")

            # --- Check 3: Very high resolution (≥3K×2K) ------------------------
            if width >= 3000 and height >= 2000:
                print("✓ Resolution is very high (≥3000×2000)")
                score += 0.30
            else:
                print("ℹ Resolution below very-high threshold – no extra points")
        except Exception as e:
            print("✗ Invalid BMP file:", e)
    else:
        print("✗ Screenshot file not found at", target)

    # Cap score at 1.0
    final_score = min(score, max_score)
    print(f"REWARD: {final_score}")
    return final_score

if __name__ == "__main__":
    verify_task()

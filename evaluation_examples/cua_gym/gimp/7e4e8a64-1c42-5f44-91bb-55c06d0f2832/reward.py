"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m aiming for a chunky 8-bit look. How can I pixelate the whole image so each block is exactly 10 × 10 px?
Generated: 2025-09-01 13:37:37
Status: success
Model: o3
Total Steps: 13
"""

import subprocess
import numpy as np
from PIL import Image

# 📁 MAIN XCF PATH – provided in the task context (DO NOT SEARCH!)
XCF_FILE_PATH = "/tmp/pixelate_task.xcf"

# Temporary file for flattened export
_TMP_PNG_PATH = "/tmp/__pixelate_verify_temp.png"


def verify_pixelate_blocks(xcf_path: str, block_size: int = 10) -> float:
    """Verify that the XCF image is pixel-ated with exact block_size × block_size
    squares.  Returns a progressive score between 0.0 and 1.0 based on how
    closely the image matches perfect pixelation.                
    """

    print("================ PIXELATE VERIFICATION ================")
    total_score = 0.0  # Progressive score

    # 1) Flatten the XCF to a PNG using xcftools (xcf2png)
    print("🔄 Converting XCF to PNG with xcf2png …")
    result = subprocess.run([
        "xcf2png", xcf_path, "-o", _TMP_PNG_PATH
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print("❌ xcf2png conversion failed:")
        print(result.stderr)
        print("========================================================")
        return 0.0  # Cannot continue without rendered image
    print("✓ Conversion successful")

    # 2) Load flattened PNG
    try:
        img = Image.open(_TMP_PNG_PATH).convert("RGB")
    except Exception as e:
        print(f"❌ Failed to load PNG: {e}")
        print("========================================================")
        return 0.0

    width, height = img.size
    print(f"Image dimensions: {width}×{height}")

    # 3) Dimension multiple check (prerequisite for exact tiling)
    dims_multiple = (width % block_size == 0) and (height % block_size == 0)
    if dims_multiple:
        print(f"✓ Dimensions are multiples of {block_size} (good sign)")
    else:
        print(f"⚠️  Dimensions are NOT multiples of {block_size} – edge blocks may be partial")

    # 4) Compare to ideal pixelated reconstruction
    small_w, small_h = width // block_size, height // block_size
    if small_w == 0 or small_h == 0:
        print("❌ Image too small for the requested block size")
        print("========================================================")
        return 0.0

    img_small = img.resize((small_w, small_h), Image.NEAREST)
    img_recon = img_small.resize((width, height), Image.NEAREST)

    arr_orig = np.array(img)
    arr_recon = np.array(img_recon)

    diff_pixels = np.count_nonzero(np.any(arr_orig != arr_recon, axis=-1))
    total_pixels = width * height
    diff_ratio = diff_pixels / total_pixels
    print(f"Differing-pixel ratio vs. ideal {block_size}×{block_size} blocks: {diff_ratio:.4f}")

    # 5) Progressive scoring based on similarity to ideal pixelation
    if diff_ratio < 0.10:
        total_score = 1.0      # Perfect / near-perfect pixelation
    elif diff_ratio < 0.20:
        total_score = 0.8
    elif diff_ratio < 0.30:
        total_score = 0.6
    elif diff_ratio < 0.40:
        total_score = 0.4
    elif diff_ratio < 0.50:
        total_score = 0.2
    else:
        total_score = 0.0

    # 6) Dimension penalty if size isn’t exact multiple
    if not dims_multiple and total_score > 0.0:
        print("Applying dimension penalty (-0.2)")
        total_score = max(0.0, total_score - 0.2)

    total_score = min(total_score, 1.0)  # Safety cap
    print(f"Computed score: {total_score}")
    print("========================================================")
    return total_score


if __name__ == "__main__":
    reward_value = verify_pixelate_blocks(XCF_FILE_PATH, block_size=10)
    print(f"REWARD: {reward_value}")

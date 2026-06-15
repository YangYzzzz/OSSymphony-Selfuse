"""
FINAL REWARD SCRIPT - SUCCESS
Task: I just opened a selfie in GIMP and it’s mirrored—the phone is showing up in my left hand instead of my right. What’s the quickest way to flip the entire image horizontally so it reads correctly?
Generated: 2025-09-01 12:49:48
Status: success
Model: o3
Total Steps: 17
"""

import subprocess
import os
from PIL import Image
import numpy as np

# 🚨 CRITICAL: use the EXACT path provided in the task context – NO SEARCHING!
XCF_PATH = "/tmp/flip_selfie_task.xcf"


def _export_xcf_to_png(xcf_path: str, png_path: str) -> bool:
    """Export the given XCF file to a temporary PNG using xcftools (xcf2png)."""
    try:
        # xcf2png writes the PNG directly to png_path
        subprocess.run(["xcf2png", xcf_path, "-o", png_path], check=True, capture_output=True)
        print("✓ XCF exported to PNG via xcf2png (prerequisite passed)")
        return True
    except FileNotFoundError:
        # xcftools not installed – cannot verify
        print("✗ xcftools (xcf2png) not installed. Cannot verify task.")
        return False
    except subprocess.CalledProcessError as e:
        print("✗ xcf2png failed → task verification failed. Stderr:\n", e.stderr.decode() if e.stderr else str(e))
        return False


def _analyse_halves_rgb(arr: np.ndarray):
    """Return mean RGB values for left and right halves of the image array."""
    h, w, _ = arr.shape
    half = w // 2
    left_half = arr[:, :half]
    right_half = arr[:, half:]
    left_mean = left_half.reshape(-1, 3).mean(axis=0)
    right_mean = right_half.reshape(-1, 3).mean(axis=0)
    return left_mean, right_mean


def verify_horizontal_flip(xcf_path: str) -> float:
    """Verify that the selfie has been flipped horizontally.

    Scoring:
        1.0 – Correctly flipped (blue-ish pixels on LEFT, red-ish pixels on RIGHT)
        0.5 – Mixed/partial orientation detected
        0.0 – Still mirrored or verification failed
    """
    print(f"🎯 Verifying horizontal flip for XCF (path from context): {xcf_path}")
    total_score = 0.0
    max_score = 1.0

    # 1) Export to PNG (prerequisite ‒ no points, but mandatory)
    export_png = "/tmp/__verify_export.png"
    if not _export_xcf_to_png(xcf_path, export_png):
        print("REWARD: 0.0")
        return 0.0

    # 2) Analyse pixel colours to determine orientation
    try:
        img = Image.open(export_png).convert("RGB")
        arr = np.array(img)
        left_mean, right_mean = _analyse_halves_rgb(arr)
        print(f"Left half mean RGB: {np.round(left_mean, 1)}")
        print(f"Right half mean RGB: {np.round(right_mean, 1)}")

        # Reference colours after correct flip
        blue_ref = np.array([50, 50, 200])   # expected LEFT half (bluish)
        red_ref  = np.array([200, 50, 50])   # expected RIGHT half (reddish)

        # Compute Euclidean distances to references
        left_to_blue  = np.linalg.norm(left_mean  - blue_ref)
        left_to_red   = np.linalg.norm(left_mean  - red_ref)
        right_to_red  = np.linalg.norm(right_mean - red_ref)
        right_to_blue = np.linalg.norm(right_mean - blue_ref)

        # Determine orientation flags
        left_is_blue  = left_to_blue  < left_to_red
        right_is_red  = right_to_red < right_to_blue

        if left_is_blue and right_is_red:
            print("✓ Image appears correctly flipped (blue on left, red on right)")
            total_score = 1.0
        elif (not left_is_blue) and (not right_is_red):
            print("✗ Image appears still mirrored (blue on right, red on left)")
            total_score = 0.0
        else:
            print("⚠️  Mixed indicators – partial correctness (half orientation)")
            total_score = 0.5
    except Exception as e:
        print("✗ Error analysing image orientation:", e)
        total_score = 0.0
    finally:
        # Clean up temporary PNG
        if os.path.exists(export_png):
            os.remove(export_png)

    final_score = min(max(total_score, 0.0), max_score)
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    # Run verification when script is executed
    verify_horizontal_flip(XCF_PATH)


"""
FINAL REWARD SCRIPT - SUCCESS
Task: I scanned a hand-drawn logo at 600 DPI and it looks too gray. In GIMP, could you turn it into a pure black-and-white graphic by applying Threshold with the lower slider at 135 and the upper slider at 255?
Generated: 2025-09-01 13:50:26
Status: success
Model: o3
Total Steps: 11
"""

import os
import subprocess
import tempfile
import shutil
import traceback
from PIL import Image

# CRITICAL: Use the exact path provided in the task context – DO NOT SEARCH!
XCF_FILE_PATH = "/tmp/threshold_logo.xcf"


def verify_threshold_binarisation(file_path: str) -> float:
    """Verify that the image in the given XCF file has been converted to a
    pure black-and-white (binary) graphic, consistent with applying a
    Threshold (≥135, ≤255) operation.

    Scoring (progressive):
        0.8 – image contains ONLY two grey levels (0 & 255)
        0.2 – both 0 *and* 255 are present (ensures true binarisation, not all-white/black)
    Returns a float between 0.0 and 1.0 and prints detailed diagnostics.
    """

    print(f"\n🎯 Verifying GIMP threshold task for file: {file_path}")
    total_score = 0.0
    max_score = 1.0

    # ---------- Prerequisite: file must exist ----------
    if not os.path.isfile(file_path):
        print("✗ XCF file not found – task failed")
        print("REWARD: 0.0")
        return 0.0  # No points if the task artefact is missing

    # ---------- Step 1: Export XCF → PNG for pixel analysis ----------
    tmp_dir = tempfile.mkdtemp(prefix="verify_threshold_")
    png_path = os.path.join(tmp_dir, "export.png")

    try:
        # Use xcftools (xcf2png) – quickest way to get pixel data
        export = subprocess.run([
            "xcf2png", file_path, "-o", png_path
        ], capture_output=True, text=True)

        if export.returncode != 0 or not os.path.exists(png_path):
            print("✗ Failed to export XCF to PNG with xcf2png")
            print(export.stderr.strip())
            print("REWARD: 0.0")
            return 0.0

        print("✓ XCF successfully exported to PNG for analysis")

        # ---------- Step 2: Pixel analysis ----------
        img = Image.open(png_path).convert("L")  # force greyscale
        pixels = list(img.getdata())
        unique_vals = set(pixels)
        print(f"Unique grey levels found: {sorted(unique_vals)[:10]} … (total {len(unique_vals)})")

        # 2.1  Check binary property (only 0 & 255)
        if unique_vals.issubset({0, 255}):
            print("✓ Image is strictly black and white (binary)")
            total_score += 0.8

            # 2.2  Ensure both tones are present (non-empty foreground/background)
            if {0, 255}.issubset(unique_vals):
                print("✓ Both black and white pixels present – proper thresholding confirmed")
                total_score += 0.2
            else:
                print("⚠️  Only one colour present – partial thresholding")
        else:
            print("✗ Image contains additional grey levels – threshold not applied correctly")

    except FileNotFoundError:
        print("✗ xcftools is not installed in the environment – cannot verify task")
        # No score in this environment error condition
    except Exception as e:
        print("✗ Unexpected error during verification:")
        traceback.print_exc()
    finally:
        # Clean temporary directory
        shutil.rmtree(tmp_dir, ignore_errors=True)

    # ---------- Final score ----------
    final_score = min(total_score, max_score)
    print(f"REWARD: {final_score}")
    return final_score


# -------------------- Run verification --------------------
if __name__ == "__main__":
    verify_threshold_binarisation(XCF_FILE_PATH)


"""
FINAL REWARD SCRIPT - SUCCESS
Task: My photo looks a bit washed-out—could you show me how to give the contrast a quick +15 boost in GIMP so it looks punchier?
Generated: 2025-09-01 12:53:42
Status: success
Model: o3
Total Steps: 16
"""

import os
import subprocess
import traceback
from PIL import Image
import numpy as np

# =============================================================
#  📁 MANDATORY XCF FILE PATH – DO NOT CHANGE / DO NOT SEARCH
# =============================================================
XCF_PATH = "/tmp/contrast_boost_task.xcf"  # ← provided in task context

# -------------------------------------------------------------
#  Helper : export composite image from XCF using xcftools
# -------------------------------------------------------------

def _export_xcf_to_png(xcf_path: str, png_path: str) -> bool:
    """Export the composite visible image of XCF to PNG.
    Returns True on success, False otherwise."""
    try:
        # Ensure previous temp file (if any) is removed so we are not fooled
        if os.path.exists(png_path):
            os.remove(png_path)

        # Use xcftools' xcf2png – fastest way to get a flattened view
        result = subprocess.run([
            "xcf2png", xcf_path, "-o", png_path
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print("✗ xcf2png failed:", result.stderr.strip())
            return False

        if not os.path.isfile(png_path):
            print("✗ PNG export file was not created – unexpected failure")
            return False

        return True
    except FileNotFoundError:
        # xcftools not installed → cannot verify → 0 points
        print("✗ xcftools (xcf2png) is not installed in the VM")
        return False
    except Exception as e:
        print("✗ Exception during PNG export:", e)
        traceback.print_exc()
        return False

# -------------------------------------------------------------
#  Core verification logic
# -------------------------------------------------------------

def verify_contrast_boost(xcf_path: str) -> float:
    """Verify that the image has received a meaningful contrast boost.

    Scoring rubric (progressive):
        • Luminance std-dev  < 35 → 0.0   (image still very flat)
        • 35 ≤ std-dev < 45 → 0.3   (slight improvement)
        • 45 ≤ std-dev < 55 → 0.6   (moderate contrast)
        • std-dev ≥ 55      → 1.0   (strong contrast – expected +15 boost)

    Returns the calculated reward score (0.0 – 1.0).
    """
    TOTAL_SCORE = 0.0

    # 0) Prerequisite – file must exist
    if not os.path.isfile(xcf_path):
        print("✗ Task file is missing → cannot verify → REWARD: 0.0")
        return 0.0

    print(f"🎯 Verifying contrast boost for file: {xcf_path}")

    # 1) Export composite PNG
    tmp_png = "/tmp/__contrast_check_export.png"
    if not _export_xcf_to_png(xcf_path, tmp_png):
        print("REWARD: 0.0")
        return 0.0

    # 2) Load image and compute luminance standard-deviation (contrast proxy)
    try:
        from PIL import ImageStat
        img = Image.open(tmp_png)
        # Convert to grayscale (luminance)
        lum = img.convert("L")
        arr = np.asarray(lum, dtype=np.float32)
        std = float(arr.std())
        print(f"   • Luminance std-dev (contrast metric): {std:.2f}")

        # 3) Progressive scoring based on measured contrast
        if std >= 55:
            TOTAL_SCORE = 1.0
            print("✓ Strong contrast detected (>=55) → full credit")
        elif std >= 45:
            TOTAL_SCORE = 0.6
            print("✓ Moderate contrast detected (45–55) → partial credit (0.6)")
        elif std >= 35:
            TOTAL_SCORE = 0.3
            print("✓ Slight contrast detected (35–45) → minimal credit (0.3)")
        else:
            TOTAL_SCORE = 0.0
            print("✗ Contrast still low (<35) → no credit")
    except Exception as e:
        print("✗ Exception during contrast analysis:", e)
        traceback.print_exc()
        TOTAL_SCORE = 0.0
    finally:
        # Clean-up temporary PNG
        if os.path.exists(tmp_png):
            os.remove(tmp_png)

    # 4) Clamp score to [0,1]
    TOTAL_SCORE = max(0.0, min(1.0, TOTAL_SCORE))

    print(f"REWARD: {TOTAL_SCORE}")
    return TOTAL_SCORE

# -------------------------------------------------------------
#  Execute verification when script is run
# -------------------------------------------------------------
if __name__ == "__main__":
    verify_contrast_boost(XCF_PATH)


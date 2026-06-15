"""
FINAL REWARD SCRIPT - SUCCESS
Task: I have a PDF 'flowchart.pdf' created from a drawing program. Convert it to PNG 'flowchart.png' with transparent background for use in presentations.
Generated: 2025-11-29 09:33:41
Status: success
Model: o3
Total Steps: 4
"""

from pathlib import Path
from typing import Tuple
from PyPDF2 import PdfReader
from PIL import Image
import random

# -----------------------------------------------------------------------------
# Reward verification script
# -----------------------------------------------------------------------------
# Task:  Convert a drawing programme PDF (flowchart.pdf) to a PNG (flowchart.png)
#        that keeps a transparent background so it can be dropped into slides.
# This script awards up to 1.0 points according to four REAL, FALSIFIABLE checks:
#   1) PNG exists and opens successfully                                       0.2
#   2) PNG truly contains transparency (alpha channel + at least 1 fully
#      transparent pixel)                                                     0.4
#   3) PNG aspect-ratio matches the PDF’s first page within 5 %               0.3
#   4) PNG resolution is practical (>300 px in either dimension)              0.1
# The sum of the weights is 1.0, so a fully correct conversion yields 1.0.
# -----------------------------------------------------------------------------

def analyse_transparency(img: Image.Image, sample: int = 5000) -> Tuple[bool, float]:
    """Return (transparent_pixel_found, ratio_transparent_pixels)."""
    if img.mode not in ("RGBA", "LA") and "transparency" not in img.info:
        return False, 0.0

    rgba = img.convert("RGBA")
    w, h = rgba.size
    total = w * h

    # Sample a subset of the image to avoid large memory/time cost
    sample_cnt = min(sample, total)
    indices = range(total) if sample_cnt == total else random.sample(range(total), sample_cnt)
    data = rgba.getdata()

    transparent = 0
    for i in indices:
        # each item is (r, g, b, a)
        if data[i][3] == 0:
            transparent += 1
    return transparent > 0, transparent / sample_cnt if sample_cnt else 0.0


def verify_conversion(pdf_path: str, png_path: str) -> float:
    max_score = 1.0
    score = 0.0
    weights = {
        "png_exists": 0.2,
        "transparency": 0.4,
        "aspect_ratio": 0.3,
        "resolution": 0.1,
    }

    print(f"Verifying conversion of '{pdf_path}' -> '{png_path}'\n")

    pdf_file = Path(pdf_path)
    png_file = Path(png_path)

    # ------------------------------------------------- 0) sanity: source PDF
    if not pdf_file.exists():
        print(f"✗ Source PDF not found: {pdf_file}")
    else:
        print(f"✓ Found source PDF ({pdf_file})")

    # ------------------------------------------------- 1) PNG exists & opens
    img = None
    if png_file.exists():
        try:
            img = Image.open(png_file)
            img.verify()            # quick structural verification
            img = Image.open(png_file)  # reopen for further analysis
            print(f"✓ PNG opens: format={img.format}, mode={img.mode}, size={img.size}")
            score += weights["png_exists"]
        except Exception as e:
            print(f"✗ Cannot open PNG: {e}")
            img = None
    else:
        print(f"✗ PNG file not found: {png_file}")

    # ------------------------------------------------- 2) Transparency check
    if img is not None:
        transparent, ratio = analyse_transparency(img)
        print(f"Transparency: alpha={img.mode in ('RGBA','LA')}, transparent pixels ratio={ratio:.2%}")
        if transparent:
            print("✓ PNG contains transparent background pixels")
            score += weights["transparency"]
        else:
            print("✗ PNG lacks transparent background")

        # ------------------------------------------------ 3) Aspect-ratio check
        try:
            reader = PdfReader(str(pdf_file))
            mediabox = reader.pages[0].mediabox
            pdf_w, pdf_h = float(mediabox.width), float(mediabox.height)
            pdf_ratio = pdf_w / pdf_h if pdf_h else 0
            img_ratio = img.width / img.height if img.height else 0
            diff = abs(pdf_ratio - img_ratio) / pdf_ratio if pdf_ratio else 1
            print(f"PDF size: {pdf_w}×{pdf_h} pt (ratio {pdf_ratio:.4f})")
            print(f"PNG size: {img.width}×{img.height} px (ratio {img_ratio:.4f}) – diff {diff:.2%}")
            if diff <= 0.05:  # ≤5 % difference
                print("✓ Aspect-ratio matches within 5 % tolerance")
                score += weights["aspect_ratio"]
            else:
                print("✗ Aspect-ratio mismatch exceeds 5 % tolerance")
        except Exception as e:
            print(f"✗ Could not compare aspect ratios: {e}")

        # ------------------------------------------------ 4) Resolution check
        if img.width >= 300 or img.height >= 300:
            print("✓ PNG resolution adequate (≥300 px in at least one dimension)")
            score += weights["resolution"]
        else:
            print("✗ PNG resolution too low (<300 px in both dimensions)")

    # ------------------------------------------------- Summary
    final_score = min(score, max_score)
    print(f"\nTotal score: {final_score:.2f}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score

# -----------------------------------------------------------------------------
# Execute verification when the script runs as main
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    verify_conversion("/home/user/flowchart.pdf", "/home/user/flowchart.png")

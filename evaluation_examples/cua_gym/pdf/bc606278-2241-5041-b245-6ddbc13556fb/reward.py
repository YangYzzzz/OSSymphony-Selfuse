"""
FINAL REWARD SCRIPT - SUCCESS
Task: Please convert the PDF 'certificate.pdf' on Desktop to a high-resolution PNG image 'certificate.png' at 300 DPI for printing.
Generated: 2025-11-29 09:33:03
Status: success
Model: o3
Total Steps: 4
"""

import traceback
from pathlib import Path
from typing import Tuple

from PIL import Image
from PyPDF2 import PdfReader

"""
Reward Script: PDF ➜ 300 DPI PNG Conversion Verifier
----------------------------------------------------
This script verifies that the user has converted the Desktop PDF
  "certificate.pdf" → "certificate.png" at high-resolution (≈300 DPI)
for printing.
Scoring rubric (total 1.0):
  • 0.2 – PNG file exists on Desktop.
  • 0.5 – Pixel dimensions correspond to PDF page-size rendered at 300 DPI
          (±5 px tolerance, orientation agnostic).
  • 0.3 – PNG metadata *or* effective resolution shows ≥300 DPI.
The script prints detailed diagnostics for auditability and finishes with
  "REWARD: X.X" (float 0.0-1.0).
"""

def _load_desktop_paths() -> Tuple[Path, Path]:
    desk = Path.home() / "Desktop"
    return desk / "certificate.pdf", desk / "certificate.png"

def _expected_pixel_dims(pdf_path: Path) -> Tuple[float, float]:
    reader = PdfReader(str(pdf_path))
    page = reader.pages[0]
    width_pt = float(page.mediabox.width)
    height_pt = float(page.mediabox.height)
    width_in, height_in = width_pt / 72.0, height_pt / 72.0  # 1 pt = 1/72 in
    return width_in * 300.0, height_in * 300.0  # 300 DPI target

def verify_conversion() -> float:
    total, MAX = 0.0, 1.0
    pdf_path, png_path = _load_desktop_paths()

    # 1) PNG existence -------------------------------------------------------
    if png_path.exists():
        print("✓ certificate.png exists (0.2 points)")
        total += 0.2
    else:
        print("✗ Missing certificate.png – task not completed")
        print(f"REWARD: {total}")
        return total  # Early exit, cannot check further aspects

    # 2) Open PNG ------------------------------------------------------------
    try:
        img = Image.open(png_path)
        width_px, height_px = img.size
        print(f"PNG pixel dimensions: {width_px} × {height_px}")
    except Exception as exc:
        print(f"✗ Error opening PNG: {exc}")
        print(f"REWARD: {total}")
        return total

    # 3) Determine expected dimensions from PDF -----------------------------
    try:
        if not pdf_path.exists():
            # Fallback – golden file (initial PDF may be renamed during grading)
            pdf_path = Path("/home/user/please_convert_the_pdf_certificatepdf_on_desktop_to_a_high_resolution_png_image_certificatepng_at_30_golden.pdf")
        exp_w, exp_h = _expected_pixel_dims(pdf_path)
        print(f"Expected ~300 DPI pixel size: {exp_w:.0f} × {exp_h:.0f}")
        tol = 5  # pixel tolerance
        dims_match = (
            abs(width_px - exp_w) <= tol and abs(height_px - exp_h) <= tol
        ) or (
            abs(width_px - exp_h) <= tol and abs(height_px - exp_w) <= tol  # swapped orientation ok
        )
        if dims_match:
            print("✓ PNG dimensions match 300 DPI target (0.5 points)")
            total += 0.5
        else:
            print("✗ PNG dimensions are not consistent with 300 DPI rendering")
    except Exception as exc:
        print("✗ Error reading PDF for expected size:", exc)
        traceback.print_exc()

    # 4) DPI verification ----------------------------------------------------
    dpi_meta = img.info.get("dpi") or img.info.get("resolution")  # (x,y)
    meta_ok = False
    if dpi_meta and isinstance(dpi_meta, (tuple, list)):
        print(f"PNG metadata DPI: {dpi_meta}")
        meta_ok = dpi_meta[0] >= 290 and dpi_meta[1] >= 290
    # If metadata missing/low, compute effective DPI from PDF physical size
    eff_ok = False
    try:
        page_w_in = exp_w / 300.0  # reverse from earlier calculation
        page_h_in = exp_h / 300.0
        eff_dpi_x, eff_dpi_y = width_px / page_w_in, height_px / page_h_in
        eff_ok = eff_dpi_x >= 290 and eff_dpi_y >= 290
    except Exception:
        pass

    if meta_ok:
        print("✓ PNG metadata indicates ≥300 DPI (0.3 points)")
        total += 0.3
    elif eff_ok:
        print(f"✓ Effective DPI ≥300 (≈{eff_dpi_x:.1f}, {eff_dpi_y:.1f}) based on dimensions (0.3 points)")
        total += 0.3
    else:
        print("✗ Neither metadata nor effective DPI meet the 300 DPI requirement")

    final_score = min(total, MAX)
    print(f"REWARD: {final_score}")
    return final_score

# ------------------------------
if __name__ == "__main__":
    verify_conversion()

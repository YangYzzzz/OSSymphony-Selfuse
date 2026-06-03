"""
FINAL REWARD SCRIPT - SUCCESS
Task: Quick question: in LibreOffice Impress, what's the fastest way to export *only* slide 120 as a 300 DPI PNG and drop it on my Desktop with the exact filename “slide120.png”?
Generated: 2025-09-10 17:46:50
Status: success
Model: azure-o3
Total Steps: 18
"""

import os
from pptx import Presentation
from PIL import Image

def verify_export_slide_120_png():
    """Reward script for verifying that only slide 120 of the given presentation
    was exported as a 300-DPI PNG named exactly 'slide120.png' on the user's
    Desktop.
    
    Progressive scoring (total 1.0):
        • 0.20 – PNG named correctly on Desktop
        • 0.20 – File is a valid, readable PNG image
        • 0.50 – Pixel dimensions match a 300-DPI export of the slide size
        • 0.10 – Desktop contains exactly one PNG file (indicates only slide 120 exported)
    """

    # -------- Paths & constants --------
    desktop_dir      = os.path.expanduser('~/Desktop')
    png_filename     = 'slide120.png'
    png_path         = os.path.join(desktop_dir, png_filename)
    presentation_path = os.path.expanduser(
        '~/quick_question_in_libreoffice_impress_whats_the_fastest_way_to_export_only_slide_120_as_a_300_dpi_pn_golden.pptx'
    )
    SLIDE_NUMBER     = 120
    TARGET_DPI       = 300
    PIXEL_TOLERANCE  = 4   # allow a few pixels tolerance for rounding/scaling

    max_score = 1.0
    score     = 0.0

    print("--- Verifying 300-DPI export of slide 120 ---")
    print(f"Expected PNG path : {png_path}")
    print(f"Presentation path : {presentation_path}\n")

    # -------- 1. File existence & correct name/location (0.20) --------
    if os.path.exists(png_path):
        print("✓ PNG file found on Desktop with correct filename")
        score += 0.20
    else:
        print("✗ PNG file not found – cannot proceed with further checks")
        print(f"REWARD: {score}")
        return score   # no further checks possible

    # -------- 2. Validate PNG integrity (0.20) --------
    try:
        with Image.open(png_path) as img:
            img_format = img.format
            width_px, height_px = img.size
            img_info  = img.info
        if img_format == 'PNG':
            print("✓ File is a valid PNG image")
            score += 0.20
        else:
            print(f"✗ File format is {img_format}, expected PNG")
    except Exception as e:
        print(f"✗ Failed to open PNG image: {e}")
        print(f"REWARD: {score}")
        return score

    # -------- 3. Verify pixel dimensions vs 300-DPI slide export (0.50) --------
    try:
        prs = Presentation(presentation_path)
        total_slides = len(prs.slides)
        if SLIDE_NUMBER > total_slides:
            print(f"✗ Presentation only has {total_slides} slides; slide {SLIDE_NUMBER} missing")
        else:
            # Slide dimensions in inches (914400 EMUs per inch)
            width_in  = prs.slide_width  / 914400.0
            height_in = prs.slide_height / 914400.0
            expected_w = int(round(width_in  * TARGET_DPI))
            expected_h = int(round(height_in * TARGET_DPI))

            print(f"Expected dimensions @{TARGET_DPI} DPI : {expected_w} × {expected_h} px")
            print(f"Actual PNG dimensions          : {width_px} × {height_px} px")

            if abs(width_px - expected_w) <= PIXEL_TOLERANCE and \
               abs(height_px - expected_h) <= PIXEL_TOLERANCE:
                print("✓ PNG dimensions match 300-DPI export of slide")
                score += 0.50
            else:
                print("✗ PNG dimensions do not match expected 300-DPI export")
    except Exception as e:
        print(f"✗ Error verifying slide dimensions: {e}")

    # -------- 4. Ensure only one PNG on Desktop (0.10) --------
    try:
        png_files_on_desktop = [f for f in os.listdir(desktop_dir) if f.lower().endswith('.png')]
        if len(png_files_on_desktop) == 1:
            print("✓ Desktop contains exactly one PNG file – likely only requested slide exported")
            score += 0.10
        else:
            print(f"⚠ Desktop contains {len(png_files_on_desktop)} PNG files (expected 1)")
    except Exception as e:
        print(f"⚠ Could not list Desktop contents: {e}")

    # -------- Final score --------
    final_score = min(score, max_score)
    print("\n--- Verification Complete ---")
    print(f"REWARD: {final_score}")
    return final_score

# Run verification when executed directly
if __name__ == "__main__":
    verify_export_slide_120_png()

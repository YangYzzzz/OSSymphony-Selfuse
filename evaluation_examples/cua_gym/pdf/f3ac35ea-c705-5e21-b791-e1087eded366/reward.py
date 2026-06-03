"""
FINAL REWARD SCRIPT - SUCCESS
Task: Please convert the PDF 'catalog.pdf' in /home/user/Documents/Sales to individual PNG images for each page, saved in folder 'catalog_images'.
Generated: 2025-11-29 09:28:36
Status: success
Model: o3
Total Steps: 4
"""

from pathlib import Path
from PyPDF2 import PdfReader

# Reward script for: "Convert the PDF 'catalog.pdf' in /home/user/Documents/Sales to individual
# PNG images for each page, saved in folder 'catalog_images'"
# ------------------------------------------------------------
# Scoring rubric (adds up to 1.0):
#   0.20  Folder "catalog_images" exists in the same directory as the PDF
#   0.20  At least one PNG image exists in that folder
#   0.30  Number of PNG files exactly equals the number of pages in the source PDF
#   0.30  Every PNG file is a valid, non-empty image that can be opened with Pillow (PIL)
# ------------------------------------------------------------


def verify_pdf_to_png(pdf_path: str, images_folder: str) -> float:
    """Verify that each page in the given PDF has been converted to a PNG image.

    Returns a progressive score between 0.0 and 1.0. Prints detailed
    diagnostics for each verification step and always prints the final
    reward as:  REWARD: <score>
    """

    max_score = 1.0
    score = 0.0

    print(f"Verifying conversion of '{pdf_path}' to PNG images in folder '{images_folder}'")

    # --------------------------------------------------------
    # Step 1: Load the PDF and determine page count
    # --------------------------------------------------------
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        print("✗ PDF file not found – cannot verify task")
        print("REWARD:", score)
        return score

    try:
        reader = PdfReader(str(pdf_file))
        num_pages = len(reader.pages)
        print(f"✓ PDF loaded successfully – page count: {num_pages}")
    except Exception as e:
        print("✗ Failed to read PDF:", e)
        print("REWARD:", score)
        return score

    # --------------------------------------------------------
    # Step 2: Verify that the images folder exists
    # --------------------------------------------------------
    img_folder = Path(images_folder)
    if img_folder.is_dir():
        print("✓ Images folder exists")
        score += 0.20
    else:
        print("✗ Images folder is missing or not a directory")
        print("REWARD:", score)
        return score  # Cannot continue without folder

    # --------------------------------------------------------
    # Step 3: Enumerate PNG files in folder
    # --------------------------------------------------------
    png_files = sorted(img_folder.glob("*.png"))
    if png_files:
        print(f"✓ Found {len(png_files)} PNG image(s)")
        score += 0.20
    else:
        print("✗ No PNG images found in folder")
        print("REWARD:", score)
        return score  # No point in further checks

    # --------------------------------------------------------
    # Step 4: Check that PNG count equals PDF page count
    # --------------------------------------------------------
    if len(png_files) == num_pages:
        print("✓ Image count matches PDF page count")
        score += 0.30
    else:
        print(f"✗ Image count ({len(png_files)}) does not match PDF pages ({num_pages})")

    # --------------------------------------------------------
    # Step 5: Validate every PNG can be opened & has dimensions > 0
    # --------------------------------------------------------
    all_images_ok = True
    try:
        from PIL import Image
        for img_path in png_files:
            try:
                with Image.open(img_path) as img:
                    img.verify()  # Verify integrity without decoding full image
                with Image.open(img_path) as img2:  # reopen to read dimensions
                    width, height = img2.size
                if width <= 0 or height <= 0:
                    print(f"✗ Image '{img_path.name}' has invalid size {width}x{height}")
                    all_images_ok = False
                    break
            except Exception as img_err:
                print(f"✗ Failed to open/verify '{img_path.name}': {img_err}")
                all_images_ok = False
                break
    except ImportError:
        print("✗ Pillow (PIL) library not installed – cannot validate images")
        all_images_ok = False

    if all_images_ok:
        print("✓ All PNG images verified successfully (opened & non-empty)")
        score += 0.30
    else:
        print("✗ One or more PNG images are corrupt or invalid")

    # --------------------------------------------------------
    # Final score (capped to 1.0)
    # --------------------------------------------------------
    final_score = min(score, max_score)
    print("REWARD:", final_score)
    return final_score


if __name__ == "__main__":
    # Hard-coded paths per task instructions
    pdf_src = "/home/user/Documents/Sales/catalog.pdf"
    images_dir = "/home/user/Documents/Sales/catalog_images"
    verify_pdf_to_png(pdf_src, images_dir)


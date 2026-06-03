"""
FINAL REWARD SCRIPT - SUCCESS
Task: I need to convert the PDF presentation 'meeting_slides.pdf' to individual slide images (PNG) in folder 'slides_export' on Desktop.
Generated: 2025-11-29 09:32:25
Status: success
Model: o3
Total Steps: 2
"""

from pathlib import Path
from PyPDF2 import PdfReader

"""
Reward script for task:
"I need to convert the PDF presentation 'meeting_slides.pdf' to individual slide images (PNG) in folder 'slides_export' on Desktop."

The script verifies completion by checking:
1. The source PDF exists and its page count can be determined.
2. The folder ~/Desktop/slides_export exists and contains PNG files.
3. The number of PNG files exactly matches the page-count of the PDF.
4. Every PNG file has a valid PNG signature (first 8-byte header), proving they are real images.

Scoring (progressive):
- 0.3  Export folder contains one or more PNG files.
- 0.4  PNG count equals PDF page-count.
- 0.3  All PNGs have valid headers.

Total = 1.0 when all conditions are satisfied.
"""

# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def locate_pdf() -> Path | None:
    """Return the path to the source PDF if it exists, else None."""
    candidate_paths = [
        Path("/home/user/i_need_to_convert_the_pdf_presentation_meeting_slidespdf_to_individual_slide_images_png_in_folder_sl_golden.pdf"),
        Path.home() / "Desktop" / "meeting_slides.pdf",
        Path("/home/user/meeting_slides.pdf"),
    ]
    for p in candidate_paths:
        if p.exists():
            return p
    return None


def count_pdf_pages(pdf_path: Path) -> int | None:
    """Return the number of pages in the PDF or None on failure."""
    try:
        reader = PdfReader(str(pdf_path))
        return len(reader.pages)
    except Exception as exc:
        print(f"✗ Error reading PDF '{pdf_path}': {exc}")
        return None


def list_png_files(directory: Path):
    """Return a sorted list of *.png Paths inside *directory*."""
    return sorted(p for p in directory.iterdir() if p.is_file() and p.suffix.lower() == ".png")


def is_valid_png(file_path: Path) -> bool:
    """Check the 8-byte PNG signature of *file_path*."""
    try:
        with file_path.open("rb") as fh:
            return fh.read(8) == b"\x89PNG\r\n\x1a\n"
    except Exception as exc:
        print(f"✗ Error reading PNG '{file_path}': {exc}")
        return False

# --------------------------------------------------
# Verification routine
# --------------------------------------------------

def verify_task() -> float:
    total_score = 0.0

    # 1. Locate PDF & determine page count
    pdf_path = locate_pdf()
    pdf_pages = None
    if pdf_path is not None:
        pdf_pages = count_pdf_pages(pdf_path)
        if pdf_pages is not None:
            print(f"✓ Located PDF: {pdf_path} with {pdf_pages} pages")
        else:
            print("✗ Failed to read PDF page-count – cannot continue page matching check")
    else:
        print("✗ Source PDF not found – cannot verify page matching criterion")

    # 2. Locate export directory & PNGs
    export_dir = Path.home() / "Desktop" / "slides_export"
    png_files = []
    if export_dir.exists() and export_dir.is_dir():
        png_files = list_png_files(export_dir)
        if png_files:
            print(f"✓ Found export directory with {len(png_files)} PNG files")
            total_score += 0.3  # points for generating at least one PNG
        else:
            print("✗ Export directory exists but contains no PNG files")
    else:
        print(f"✗ Export directory not found at {export_dir}")

    # 3. PNG count matches PDF pages
    if pdf_pages is not None and png_files:
        if len(png_files) == pdf_pages:
            print("✓ PNG count matches PDF page-count")
            total_score += 0.4
        else:
            print(f"✗ PNG count ({len(png_files)}) does not match PDF pages ({pdf_pages})")
    # Skip message handled implicitly when either list is empty / pdf missing

    # 4. Validate every PNG header
    if png_files:
        bad_pngs = [f for f in png_files if not is_valid_png(f)]
        if not bad_pngs:
            print("✓ All PNG files have valid headers")
            total_score += 0.3
        else:
            print(f"✗ {len(bad_pngs)} PNG file(s) have invalid headers: {bad_pngs[:3]} …")

    # Clamp and print final reward
    reward = min(total_score, 1.0)
    print(f"REWARD: {reward}")
    return reward

# --------------------------------------------------
# Script entry-point
# --------------------------------------------------
if __name__ == "__main__":
    verify_task()

"""
FINAL REWARD SCRIPT - SUCCESS
Task: I have a scanned PDF 'book_scanned.pdf' that's just images. Convert it to a searchable PDF 'book_searchable.pdf' using OCR in /home/user/Books.
Generated: 2025-11-29 09:28:31
Status: success
Model: o3
Total Steps: 4
"""

from pathlib import Path
from typing import Tuple
from PyPDF2 import PdfReader

def _text_stats(pdf_path: Path) -> Tuple[float, list[int]]:
    """Return percentage of pages that contain >20 characters of text and per-page char counts."""
    reader = PdfReader(str(pdf_path))
    pages = reader.pages
    text_pages = 0
    char_counts: list[int] = []
    for page in pages:
        txt = page.extract_text() or ""
        txt_len = len(txt.strip())
        char_counts.append(txt_len)
        if txt_len > 20:
            text_pages += 1
    ratio = text_pages / len(pages) if pages else 0.0
    return ratio, char_counts

def verify_ocr_conversion() -> float:
    """Verify that a scanned PDF was converted into a searchable (OCR) PDF.

    Scoring rubric (progressive):
      • 0.2 – searchable PDF exists at expected path
      • 0.2 – page count of searchable matches original scanned PDF
      • 0.6 – at least 80 % of pages in searchable PDF contain >20 characters *and*
               improvement over scanned version is ≥60 % of pages.
    Returns
    -------
    float
        Reward between 0.0 and 1.0 inclusive.
    """
    base_dir = Path("/home/user/Books")
    scanned_path = base_dir / "book_scanned.pdf"
    searchable_path = base_dir / "book_searchable.pdf"

    total_score = 0.0
    max_score = 1.0

    # 1) Existence check (no points for directory presence, only for correct file)
    if searchable_path.exists():
        print("✓ Found 'book_searchable.pdf'")
        total_score += 0.2
    else:
        print("✗ Missing 'book_searchable.pdf' – task incomplete")
        print("REWARD: 0.0")
        return 0.0  # Cannot proceed without output file

    # Load PDFs (scanned may not exist, handle gracefully)
    try:
        searchable_reader = PdfReader(str(searchable_path))
        searchable_pages = len(searchable_reader.pages)
    except Exception as e:
        print(f"✗ Error opening searchable PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    scanned_pages = None
    if scanned_path.exists():
        try:
            scanned_reader = PdfReader(str(scanned_path))
            scanned_pages = len(scanned_reader.pages)
        except Exception as e:
            print(f"⚠️  Could not open scanned PDF: {e}")

    # 2) Page-count consistency
    if scanned_pages is not None and scanned_pages == searchable_pages:
        print(f"✓ Page count matches original ({searchable_pages} pages)")
        total_score += 0.2
    elif scanned_pages is not None:
        print(f"✗ Page count mismatch – scanned: {scanned_pages}, searchable: {searchable_pages}")
    else:
        print("⚠️  Original scanned PDF not found – skipping page-count check")

    # 3) OCR quality assessment
    searchable_ratio, searchable_char_counts = _text_stats(searchable_path)
    print(f"Searchable PDF: {searchable_ratio:.2%} of pages contain >20 chars")

    scanned_ratio = 0.0
    if scanned_path.exists():
        scanned_ratio, _ = _text_stats(scanned_path)
        print(f"Scanned PDF: {scanned_ratio:.2%} of pages contain >20 chars")

    improvement = searchable_ratio - scanned_ratio
    if searchable_ratio >= 0.80 and improvement >= 0.60:
        print("✓ OCR detected on a large majority of pages – quality acceptable")
        total_score += 0.6
    else:
        print("✗ OCR quality insufficient (did not meet ratio/improvement thresholds)")

    final_score = min(total_score, max_score)
    print(f"REWARD: {final_score}")
    return final_score

# Execute verification when script runs
award = verify_ocr_conversion()


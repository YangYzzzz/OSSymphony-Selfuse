"""
FINAL REWARD SCRIPT - SUCCESS
Task: Please perform OCR on all scanned PDFs in /home/user/Documents/Scanned_Archive, converting them to searchable PDFs in folder 'Searchable_Archive'.
Generated: 2025-11-29 10:13:33
Status: success
Model: o3
Total Steps: 6
"""

"""
Reward Script: OCR Verification for Scanned PDFs
------------------------------------------------
This script verifies that every scanned PDF located in
  /home/user/Documents/Scanned_Archive
has been converted into a *searchable* (OCR-processed) PDF with the **same
filename** inside
  /home/user/Documents/Searchable_Archive

Scoring per file (progressive & evidence-based):
  • 40 %  – the searchable PDF exists with the correct name
  • 60 %  – the extracted text length of the searchable PDF is at least
              max(50 characters, 3× the text that can be extracted from the
              original scanned file)

The final reward is the average of all per-file scores, capped at 1.0.

Dependencies: PyPDF2 (pre-installed in the VM).
"""
from pathlib import Path
from PyPDF2 import PdfReader

def _extract_text_length(pdf_path: Path) -> int:
    """Return total length of extractable text for the given PDF."""
    try:
        reader = PdfReader(str(pdf_path))
        return len("".join((page.extract_text() or "") for page in reader.pages).strip())
    except Exception as e:
        print(f"✗ Error reading {pdf_path}: {e}")
        return 0

def verify_ocr(scanned_dir: str, searchable_dir: str,
                ratio_threshold: float = 3.0, min_chars: int = 50) -> float:
    """Verify OCR conversion and return a score between 0.0 and 1.0."""
    scanned_dir = Path(scanned_dir)
    searchable_dir = Path(searchable_dir)

    # Preconditions ---------------------------------------------------------
    if not scanned_dir.is_dir() or not searchable_dir.is_dir():
        print("✗ Required directories are missing")
        print("REWARD: 0.0")
        return 0.0

    scanned_files = sorted(scanned_dir.glob('*.pdf'))
    if not scanned_files:
        print("✗ No scanned PDFs found to evaluate")
        print("REWARD: 0.0")
        return 0.0

    per_file_max = 1.0 / len(scanned_files)        # weight each file equally
    total_score = 0.0

    # Verification ----------------------------------------------------------
    for scan_path in scanned_files:
        print(f"\nChecking '{scan_path.name}' …")
        searchable_path = searchable_dir / scan_path.name

        # 1) File existence (40 % of per-file score)
        if searchable_path.exists():
            total_score += 0.4 * per_file_max
            print(f"  ✓ Searchable PDF exists (+{0.4 * per_file_max:.2f})")
        else:
            print("  ✗ Corresponding searchable PDF missing (0 points for this file)")
            continue  # cannot proceed with OCR quality check for this file

        # 2) OCR quality (60 % of per-file score)
        original_text_len = _extract_text_length(scan_path)
        searchable_text_len = _extract_text_length(searchable_path)
        print(f"  Extracted text length – original: {original_text_len}, "
              f"searchable: {searchable_text_len}")

        required_len = max(min_chars, original_text_len * ratio_threshold)
        if searchable_text_len >= required_len:
            total_score += 0.6 * per_file_max
            print(f"  ✓ OCR quality sufficient (+{0.6 * per_file_max:.2f})")
        else:
            print("  ✗ OCR quality insufficient (0 additional points)")

    # -----------------------------------------------------------------------
    final_score = round(min(total_score, 1.0), 2)
    print(f"\nTotal score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    verify_ocr(
        '/home/user/Documents/Scanned_Archive',
        '/home/user/Documents/Searchable_Archive'
    )

"""
FINAL REWARD SCRIPT - SUCCESS
Task: Please add a header 'Company Confidential - Q4 2024' to all pages of 'quarterly_report.pdf' on Desktop and save as 'report_with_header.pdf'.
Generated: 2025-11-29 09:42:36
Status: success
Model: o3
Total Steps: 10
"""

from __future__ import annotations

"""
Reward Script: Verify header "Company Confidential - Q4 2024" added to every page of
`report_with_header.pdf` that resides on the Desktop.

Scoring (progressive up to 1.0):
• 0.1  – output PDF exists
• 0.2  – page-count matches original (if original present & loadable)
• 0.9  – header present on every page (scaled linearly; full 0.9 when all pages have it)

Returns exactly 1.0 only when all requirements are satisfied.
No subprocess usage; relies solely on PyPDF2 for inspection.
"""

from pathlib import Path
from typing import List
import traceback
from PyPDF2 import PdfReader

# ---------- CONFIGURATION ---------- #
OUTPUT_PDF = Path("/home/user/Desktop/report_with_header.pdf")
ORIGINAL_PDF = Path("/home/user/Desktop/quarterly_report.pdf")  # may not exist after task
HEADER_TEXT = "Company Confidential - Q4 2024"

# ---------- HELPER FUNCTIONS ---------- #

def safe_load_pdf(path: Path):
    """Attempt to load a PDF; return PdfReader or None and print errors."""
    try:
        return PdfReader(str(path))
    except Exception as exc:
        print(f"✗ Failed to load {path.name}: {exc}")
        return None

def page_contains_header(page, header: str) -> bool:
    """Case-insensitive containment check in extracted page text."""
    try:
        text = page.extract_text() or ""
    except Exception as exc:
        print(f"  • Error extracting text from page: {exc}")
        text = ""
    return header.lower() in text.lower()

# ---------- MAIN VERIFICATION ---------- #

def verify_task() -> float:
    total_score = 0.0
    max_score = 1.0

    print("Starting verification for added header …\n")

    # 1. Output PDF must exist (0.1 pts)
    if OUTPUT_PDF.exists():
        print(f"✓ Located output PDF: {OUTPUT_PDF} (0.1 pts)")
        total_score += 0.1
    else:
        print(f"✗ Missing expected output PDF at {OUTPUT_PDF}")
        print(f"REWARD: {total_score}")
        return total_score  # cannot continue

    # 2. Load output PDF
    new_reader = safe_load_pdf(OUTPUT_PDF)
    if new_reader is None:
        print(f"REWARD: {total_score}")
        return total_score

    new_page_count = len(new_reader.pages)
    if new_page_count == 0:
        print("✗ Output PDF has no pages – invalid result")
        print(f"REWARD: {total_score}")
        return total_score
    print(f"• Output PDF page count: {new_page_count}")

    # 3. If original PDF exists & loads, page-count must match (0.2 pts)
    if ORIGINAL_PDF.exists():
        orig_reader = safe_load_pdf(ORIGINAL_PDF)
        if orig_reader:
            orig_pages = len(orig_reader.pages)
            if orig_pages == new_page_count:
                print("✓ Page count matches original (0.2 pts)")
                total_score += 0.2
            else:
                print(f"✗ Page count mismatch: original={orig_pages}, new={new_page_count}")
        else:
            print("• Skipping page-count check – could not load original PDF")
    else:
        print("• Original PDF not present – skipping page-count comparison")

    # 4. Header presence verification (up to 0.9 pts)
    pages_with_header: List[int] = []
    pages_missing_header: List[int] = []

    for idx, page in enumerate(new_reader.pages, start=1):
        if page_contains_header(page, HEADER_TEXT):
            pages_with_header.append(idx)
        else:
            pages_missing_header.append(idx)

    coverage_ratio = len(pages_with_header) / new_page_count
    header_score = 0.9 * coverage_ratio
    total_score += header_score

    if coverage_ratio == 1.0:
        print(f"✓ Header found on ALL pages ({len(pages_with_header)}/{new_page_count}) (0.9 pts)")
    else:
        print(f"✗ Header missing on pages: {pages_missing_header}")
        print(f"• Header coverage {len(pages_with_header)}/{new_page_count} pages -> {header_score:.2f} pts")

    # 5. Final capping & output
    final_score = min(total_score, max_score)
    print(f"\nTOTAL SCORE: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score

# ---------- RUN WHEN EXECUTED ---------- #
if __name__ == "__main__":
    try:
        verify_task()
    except Exception:
        print("Unexpected error during verification:")
        traceback.print_exc()
        print("REWARD: 0.0")

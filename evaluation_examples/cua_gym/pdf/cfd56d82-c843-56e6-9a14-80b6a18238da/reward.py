"""
FINAL REWARD SCRIPT - SUCCESS
Task: I need to OCR only pages 5-15 of 'mixed_document.pdf' on Desktop (which has both text and scanned pages) and save to 'ocr_pages_5_15.txt'.
Generated: 2025-11-29 10:07:23
Status: success
Model: o3
Total Steps: 12
"""

import os
import re
from pathlib import Path
from typing import List, Dict

"""
Reward Script: Verify OCR extraction for pages 5–15 only
Task requirement:
1. An OCR text file named 'ocr_pages_5_15.txt' must exist on the Desktop.
2. The file must contain OCR results **only** for pages 5 through 15 of 'mixed_document.pdf'.
   - Exactly those 11 pages, no more, no less.
   - Page sections must appear in ascending order (5 … 15).
3. Each page section must contain at least one non-blank line (either real OCR text or a placeholder such as [NO_TEXT_FOUND]).
The script awards:
  • 0.50  – correct page set (exactly 5-15)
  • 0.30  – page markers in correct ascending order
  • 0.20  – each page block has at least one content line
Total = 1.0 on full success; progressive scoring otherwise.
"""

PDF_NAME = "mixed_document.pdf"   # not opened, but kept for clarity
TXT_NAME = "ocr_pages_5_15.txt"
EXPECTED_PAGES = list(range(5, 16))  # 5-15 inclusive


def parse_ocr_file(lines: List[str]):
    """Return (order_list, page->list_of_lines) from OCR TXT lines."""
    page_re = re.compile(r"^---\s*Page\s+(\d+)\s*---$", re.IGNORECASE)
    order: List[int] = []
    sections: Dict[int, List[str]] = {}
    current_page = None

    for ln in lines:
        m = page_re.match(ln.strip())
        if m:
            # Store buffer for previous page (if any)
            current_page = int(m.group(1))
            order.append(current_page)
            sections[current_page] = []
        else:
            if current_page is not None:
                sections[current_page].append(ln)
    return order, sections


def verify_task() -> float:
    total_score = 0.0
    max_score = 1.0

    desktop_dir = Path.home() / "Desktop"
    txt_path = desktop_dir / TXT_NAME

    # Step 1: Ensure OCR text file exists
    if not txt_path.exists():
        print(f"✗ Missing OCR output file: {txt_path}")
        print("REWARD: 0.0")
        return 0.0
    print(f"✓ Found OCR output file: {txt_path}")

    # Step 2: Read & parse file
    lines = txt_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    order, sections = parse_ocr_file(lines)

    # Requirement A: Exact page set 5-15
    pages_set = set(sections.keys())
    expected_set = set(EXPECTED_PAGES)
    if pages_set == expected_set:
        print("✓ OCR file contains exactly pages 5-15")
        total_score += 0.5
    else:
        missing = expected_set - pages_set
        extra = pages_set - expected_set
        if missing:
            print(f"✗ Missing page markers: {sorted(missing)}")
        if extra:
            print(f"✗ Unexpected page markers present: {sorted(extra)}")

    # Requirement B: Correct ascending order
    if order == EXPECTED_PAGES:
        print("✓ Page markers are in correct ascending order 5-15")
        total_score += 0.3
    else:
        print(f"✗ Page marker order incorrect: {order}")

    # Requirement C: Non-empty content per page
    all_have_content = True
    for p in EXPECTED_PAGES:
        content_lines = [ln.strip() for ln in sections.get(p, []) if ln.strip()]
        if not content_lines:
            print(f"✗ Page {p} has no content lines")
            all_have_content = False
            break
    if all_have_content:
        print("✓ Each page section contains at least one content line")
        total_score += 0.2

    final_score = round(min(total_score, max_score), 2)
    print(f"Total score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task()

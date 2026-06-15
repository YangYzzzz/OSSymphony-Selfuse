"""
FINAL REWARD SCRIPT - SUCCESS
Task: Add both a header 'Marketing Plan 2025' and footer with page numbers to 'marketing_plan.pdf' in /home/user/Documents/Marketing. Save as 'plan_formatted.pdf'.
Generated: 2025-11-29 09:49:57
Status: success
Model: o3
Total Steps: 9
"""

"""Reward script for verifying PDF header and footer additions.

This script checks the file /home/user/Documents/Marketing/plan_formatted.pdf
and awards a progressive score based on:
  • Presence of the header text "Marketing Plan 2025" on every page (0.5 pts)
  • Presence of the correct footer page number ("Page X") on every page (0.5 pts)
A perfect score of 1.0 is returned only when **all** pages contain both the
required header and the correct footer number.

The script relies solely on PyPDF2 for text extraction and performs real,
falsifiable checks—no hard-coded truths or default-state points are given.
"""
from __future__ import annotations
import re
from pathlib import Path
from typing import Tuple

try:
    from PyPDF2 import PdfReader  # type: ignore
except ImportError as exc:  # PyPDF2 should exist, but guard just in case.
    print(f"✗ PyPDF2 missing: {exc}")
    print("REWARD: 0.0")
    raise SystemExit(0)

HEADER_KEYWORD = "marketing plan 2025"  # lower-case for case-insensitive match
EXPECTED_PDF = "/home/user/Documents/Marketing/plan_formatted.pdf"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def inspect_page(page, page_num: int) -> Tuple[bool, bool]:
    """Return (has_header, has_footer_number) for a single page."""
    text = page.extract_text() or ""
    text_lower = text.lower()

    # Header check – keyword anywhere in text (positional data unreliable)
    has_header = HEADER_KEYWORD in text_lower

    # Footer check – look for exact "page <num>" (word boundaries, allow spaces)
    footer_regex = rf"\bpage\s*{page_num}\b"
    has_footer = re.search(footer_regex, text_lower) is not None

    return has_header, has_footer


# ---------------------------------------------------------------------------
# Main verification routine
# ---------------------------------------------------------------------------

def verify_pdf_header_footer(pdf_path: str) -> float:
    print(f"Verifying formatted PDF at: {pdf_path}")
    path = Path(pdf_path)
    if not path.exists():
        print("✗ File not found.")
        print("REWARD: 0.0")
        return 0.0

    # Load PDF -----------------------------------------------------------------
    try:
        reader = PdfReader(str(path))
    except Exception as e:
        print(f"✗ Failed to read PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    total_pages = len(reader.pages)
    if total_pages == 0:
        print("✗ PDF contains zero pages – invalid.")
        print("REWARD: 0.0")
        return 0.0

    print(f"Total pages detected: {total_pages}")

    # Iterate pages ------------------------------------------------------------
    header_hits = 0
    footer_hits = 0
    for idx, page in enumerate(reader.pages):
        page_num = idx + 1  # human-friendly 1-based index
        has_header, has_footer = inspect_page(page, page_num)
        header_hits += int(has_header)
        footer_hits += int(has_footer)
        print(
            f"Page {page_num}: Header={'✓' if has_header else '✗'} | "
            f"FooterNumber={'✓' if has_footer else '✗'}"
        )

    # Scoring ------------------------------------------------------------------
    header_score = 0.5 * (header_hits / total_pages)
    footer_score = 0.5 * (footer_hits / total_pages)
    total_score = round(min(header_score + footer_score, 1.0), 4)

    print(f"Header present on {header_hits}/{total_pages} pages → {header_score:.2f} pts")
    print(f"Footer page numbers correct on {footer_hits}/{total_pages} pages → {footer_score:.2f} pts")
    print(f"REWARD: {total_score}")

    return total_score


# ---------------------------------------------------------------------------
# Script entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    verify_pdf_header_footer(EXPECTED_PDF)


"""
FINAL REWARD SCRIPT - SUCCESS
Task: I need to insert 'corrected_page.pdf' (1 page) to replace page 8 in 'report.pdf' (20 pages) on Desktop. Save as 'report_corrected.pdf'.
Generated: 2025-11-29 09:39:35
Status: success
Model: o3
Total Steps: 4
"""

from __future__ import annotations

"""
Reward Script: Verify that page 8 in report.pdf was correctly replaced by
corrected_page.pdf and saved as report_corrected.pdf on the Desktop.

Scoring (progressive):
    0.0  – any critical file missing / unreadable
    +0.2 – output PDF exists *and* still contains exactly 20 pages
    +0.5 – page 8 of the output matches corrected_page.pdf (content hash)
    +0.3 – all other pages (1-7 & 9-20) are **identical** to original report.pdf
    --------------------------------------------------------------
    1.0 – all checks pass

Notes:
• Uses PyPDF2 only (already installed).
• Relies on deterministic text-based MD5 hashes of each page; if a page has
  no extractable text, the raw content stream bytes are hashed instead, still
  giving a reliable fingerprint without needing external tools.
• No subprocess usage (security requirement).
"""

from pathlib import Path
import hashlib
import traceback
from PyPDF2 import PdfReader


def _page_hash(page) -> str:
    """Return a deterministic hash for a PDF page.
    Prefer extracted text; fall back to raw content streams if text is empty."""
    try:
        text = page.extract_text() or ""
    except Exception:
        text = ""

    if text.strip():
        data = text.strip().encode("utf-8")
    else:
        try:
            contents = page.get_contents()
            if contents is None:
                data = b""
            elif isinstance(contents, list):
                data = b"".join(c.get_data() for c in contents)
            else:
                data = contents.get_data()
        except Exception:
            # Fallback to string representation (should rarely happen)
            data = str(page).encode("utf-8")
    return hashlib.md5(data).hexdigest()


def verify_pdf_replacement() -> float:
    desktop = Path.home() / "Desktop"
    orig_path = desktop / "report.pdf"
    corr_path = desktop / "corrected_page.pdf"
    out_path = desktop / "report_corrected.pdf"

    # ---- preliminary: ensure all files exist (no points, but hard-fail) ----
    for p in (orig_path, corr_path, out_path):
        if not p.exists():
            print(f"✗ Missing required file: {p}")
            print("REWARD: 0.0")
            return 0.0
        print(f"✓ Found {p}")

    # ---- open PDFs ----
    try:
        orig_reader = PdfReader(str(orig_path))
        corr_reader = PdfReader(str(corr_path))
        out_reader = PdfReader(str(out_path))
    except Exception as e:
        print(f"✗ Error opening PDFs: {e}")
        traceback.print_exc()
        print("REWARD: 0.0")
        return 0.0

    total_score = 0.0
    max_score = 1.0

    # ---- requirement 1: page-count correct ----
    if len(orig_reader.pages) == 20 and len(out_reader.pages) == 20:
        print("✓ Output PDF has 20 pages (matches original)")
        total_score += 0.2
    else:
        print("✗ Page-count mismatch between original and output")

    # ---- requirement 2: page 8 replaced by corrected_page.pdf ----
    replacement_ok = False
    if len(corr_reader.pages) == 1:
        corr_hash = _page_hash(corr_reader.pages[0])
        out_page8_hash = _page_hash(out_reader.pages[7])  # zero-based index 7 ⇒ page 8
        if corr_hash == out_page8_hash:
            replacement_ok = True
            print("✓ Page 8 in output matches corrected_page.pdf")
            total_score += 0.5
        else:
            print("✗ Page 8 in output does NOT match corrected_page.pdf")
    else:
        print("✗ corrected_page.pdf should contain exactly 1 page but has "
              f"{len(corr_reader.pages)}")

    # ---- requirement 3: all other pages unchanged ----
    unchanged = True
    for idx in list(range(0, 7)) + list(range(8, 20)):
        if _page_hash(orig_reader.pages[idx]) != _page_hash(out_reader.pages[idx]):
            print(f"✗ Page {idx + 1} differs between original and output")
            unchanged = False
            break
    if unchanged:
        print("✓ All pages except page 8 remain unchanged")
        total_score += 0.3

    # ---- final score ----
    final_score = min(total_score, max_score)
    print(f"Total score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_pdf_replacement()


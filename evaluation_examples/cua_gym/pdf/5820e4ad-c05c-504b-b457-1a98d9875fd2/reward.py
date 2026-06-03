"""
FINAL REWARD SCRIPT - SUCCESS
Task: Please add a header 'Internal Use Only' in red color to all pages of 'memo.pdf' on Desktop. Save as 'memo_marked.pdf'.
Generated: 2025-11-29 09:48:29
Status: success
Model: o3
Total Steps: 11
"""

from __future__ import annotations
"""
Reward verification script for the task:
"Please add a header 'Internal Use Only' in red color to all pages of 'memo.pdf' on Desktop. Save as 'memo_marked.pdf'."

The script checks:
1. The expected output PDF exists (either on the Desktop or at the grader-fallback path).
2. Every page contains the header text "Internal Use Only" (case-insensitive).
3. The header is rendered in *red* (RGB 1 0 0) on every page by scanning the raw content
   stream for the colour-setting operator immediately preceding the text.

Progressive scoring (adds up to 1.0):
• 0.1 – correct output file present
• 0.4 – header text present on *all* pages
• 0.5 – header detected as red on *all* pages
"""

import os
import re
from typing import Tuple
from PyPDF2 import PdfReader

# Primary and fallback locations for the produced PDF
OUTPUT_PDF_PATHS = [
    "/home/user/Desktop/memo_marked.pdf",  # main expected location
    "/home/user/please_add_a_header_internal_use_only_in_red_color_to_all_pages_of_memopdf_on_desktop_save_as_memo_m_golden.pdf",  # fallback
]

# Regular expressions for colour operator and header text
RED_RGB_REGEX = re.compile(r"1\s+0\s+0\s+rg")  # set-fill colour = pure red
HEADER_REGEX = re.compile(r"Internal\s+Use\s+Only", re.IGNORECASE)


def _get_raw_content(page) -> bytes:
    """Return concatenated raw bytes of all content streams for a page."""
    try:
        return page.get_contents().get_data()
    except Exception:  # noqa: BLE001 – handle PyPDF2 stream/array variations
        contents_obj = page.get("/Contents")
        if isinstance(contents_obj, list):
            data_parts = []
            for obj in contents_obj:
                try:
                    data_parts.append(obj.get_object().get_data())
                except Exception:  # ignore objects we cannot decode
                    pass
            return b"".join(data_parts)
        return b""  # no readable content found


def _analyze_page(page) -> Tuple[bool, bool]:
    """Return (text_present, red_present) for a single page."""
    # 1. Easy check via text extraction
    extracted = page.extract_text() or ""
    text_present = bool(HEADER_REGEX.search(extracted))

    # 2. Raw content analysis to verify colour
    raw_bytes = _get_raw_content(page)
    content_str = raw_bytes.decode("latin1", errors="ignore")
    red_present = False
    for match in HEADER_REGEX.finditer(content_str):
        window_start = max(0, match.start() - 150)  # look back 150 chars for colour operator
        preceding = content_str[window_start : match.start()]
        if RED_RGB_REGEX.search(preceding):
            red_present = True
            break
    return text_present, red_present


def verify_pdf(pdf_path: str) -> float:
    """Run all verification steps and return the progressive reward score."""
    score = 0.0

    # --------------- File existence -----------------
    if not os.path.exists(pdf_path):
        print(f"✗ Output PDF not found: {pdf_path}")
        print("REWARD: 0.0")
        return score
    print(f"✓ Found output PDF: {pdf_path}")
    score += 0.1  # minimal credit for correct file placement/name

    # --------------- Load PDF -----------------------
    try:
        reader = PdfReader(pdf_path)
    except Exception as exc:  # noqa: BLE001 – report load failure
        print(f"✗ Failed to open PDF with PyPDF2: {exc}")
        print("REWARD: 0.0")
        return 0.0

    total_pages = len(reader.pages)
    print(f"Total pages detected: {total_pages}")
    if total_pages == 0:
        print("✗ PDF has zero pages – invalid document")
        print("REWARD: 0.0")
        return 0.0

    # --------------- Per-page checks ----------------
    all_text_ok = True
    all_red_ok = True

    for idx, page in enumerate(reader.pages, start=1):
        text_ok, red_ok = _analyze_page(page)

        if text_ok:
            print(f"✓ Page {idx}: header text present")
        else:
            print(f"✗ Page {idx}: header text missing")
            all_text_ok = False

        if red_ok:
            print(f"✓ Page {idx}: header rendered in red")
        else:
            print(f"✗ Page {idx}: header not detected as red")
            all_red_ok = False

    # --------------- Scoring ------------------------
    if all_text_ok:
        score += 0.4  # header text on every page
    if all_red_ok:
        score += 0.5  # red colour on every page

    final_score = min(score, 1.0)
    print(f"REWARD: {final_score}")
    return final_score


# ---------------- Script entrypoint ---------------

def main() -> float:  # noqa: D401 – simple main wrapper
    pdf_to_check = next((p for p in OUTPUT_PDF_PATHS if os.path.exists(p)), None)
    if pdf_to_check is None:
        print("✗ None of the expected output PDF paths were found.")
        print("REWARD: 0.0")
        return 0.0
    return verify_pdf(pdf_to_check)


if __name__ == "__main__":
    main()


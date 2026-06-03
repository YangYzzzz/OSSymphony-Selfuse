"""
FINAL REWARD SCRIPT - SUCCESS
Task: Extract the references section from 'literature_review.pdf' in /home/user/Research (last 5 pages) and save to 'bibliography.txt'.
Generated: 2025-11-29 09:15:00
Status: success
Model: o3
Total Steps: 6
"""

"""
Reward script for task:
Extract the references section from 'literature_review.pdf' in /home/user/Research (last 5 pages)
and save the extracted text to 'bibliography.txt'.

Scoring rubric (progressive, 0.0–1.0):
    • 0.1  – bibliography.txt exists and is non-empty.
    • 0.75 – 0.15 for EACH of the 5 last PDF pages whose text (first 120 chars, normalised)
              is found inside bibliography.txt (order is irrelevant).
    • 0.15 – bibliography.txt does NOT contain text from the first page of the PDF, ensuring that
              only the reference section (last pages) was exported.
Exactly 1.0 is awarded only when all checks pass.

No points are given for natural conditions (file existence of the PDF, page count, etc.).
The script prints detailed diagnostics and always outputs the reward as:
    REWARD: <float>

Author: Auto-generated
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import List

from PyPDF2 import PdfReader

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _normalize(text: str) -> str:
    """Return lowercase text with all consecutive whitespace collapsed to a single space."""
    return re.sub(r"\s+", " ", text).strip().lower()

# ---------------------------------------------------------------------------
# Core verification logic
# ---------------------------------------------------------------------------

def verify_task(pdf_path: str | Path, txt_path: str | Path) -> float:
    pdf_path = Path(pdf_path)
    txt_path = Path(txt_path)

    print(f"Verifying task for PDF: {pdf_path}\nExpecting TXT : {txt_path}\n")

    total_score = 0.0  # progressive score accumulator
    max_score = 1.0

    # -------------------------------------------------------------------
    # 1. Basic existence & non-empty TXT (0.1)
    # -------------------------------------------------------------------
    if txt_path.exists() and txt_path.stat().st_size > 0:
        print("✓ bibliography.txt exists and is not empty (+0.1)")
        total_score += 0.1
    else:
        print("✗ bibliography.txt missing or empty (0 points)")
        # If the file doesn't exist, further checks will fail; return early
        print(f"REWARD: {total_score}")
        return total_score

    # Load required artefacts
    try:
        reader = PdfReader(str(pdf_path))
    except Exception as e:
        print(f"✗ Failed to open PDF '{pdf_path}': {e}")
        print(f"REWARD: {total_score}")
        return total_score

    pdf_pages: List = reader.pages
    num_pages = len(pdf_pages)
    if num_pages < 5:
        print(f"✗ PDF only has {num_pages} pages (<5). Cannot verify last 5 pages.")
        print(f"REWARD: {total_score}")
        return total_score

    # Prepare normalised text content for comparison
    bibliography_text_norm = _normalize(txt_path.read_text(encoding="utf-8", errors="ignore"))

    # -------------------------------------------------------------------
    # 2. Verify each of the last 5 pages appears in bibliography.txt (0.15 each)
    # -------------------------------------------------------------------
    start_idx = num_pages - 5
    snippet_value = 0.15  # per-page value (5 × 0.15 = 0.75)

    for page_index in range(start_idx, num_pages):
        page = pdf_pages[page_index]
        page_text = page.extract_text() or ""
        page_norm = _normalize(page_text)
        snippet = page_norm[:120]  # first 120 normalised characters as quick signature

        if snippet and snippet in bibliography_text_norm:
            print(f"✓ Found snippet from PDF page {page_index + 1} in bibliography (+{snippet_value})")
            total_score += snippet_value
        else:
            print(f"✗ Snippet from PDF page {page_index + 1} NOT found in bibliography (0 points)")

    # -------------------------------------------------------------------
    # 3. Ensure non-reference content is NOT included (0.15)
    #    We take the first page (definitely not in references) as sentinel.
    # -------------------------------------------------------------------
    first_page_text = pdf_pages[0].extract_text() or ""
    first_page_snippet_norm = _normalize(first_page_text[:120])

    if first_page_snippet_norm and first_page_snippet_norm not in bibliography_text_norm:
        print("✓ Non-reference content absent from bibliography (+0.15)")
        total_score += 0.15
    else:
        print("✗ Detected non-reference text in bibliography (0 points)")

    # -------------------------------------------------------------------
    # Final score clamped to [0, 1]
    # -------------------------------------------------------------------
    final_score = min(total_score, max_score)
    print(f"\nTotal score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score

# ---------------------------------------------------------------------------
# Script entrypoint
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    verify_task(
        pdf_path="/home/user/Research/literature_review.pdf",
        txt_path="/home/user/Research/bibliography.txt",
    )


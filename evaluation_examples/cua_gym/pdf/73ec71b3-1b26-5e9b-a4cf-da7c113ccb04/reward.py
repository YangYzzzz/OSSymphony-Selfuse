"""
FINAL REWARD SCRIPT - SUCCESS
Task: Extract all text from the presentation handout 'workshop_slides.pdf' on Desktop and save it to 'workshop_notes.txt', including slide numbers.
Generated: 2025-11-29 09:12:11
Status: success
Model: o3
Total Steps: 8
"""

from __future__ import annotations

"""Reward Verification Script
Task: Extract all text from the presentation handout 'workshop_slides.pdf' on Desktop and save it to 'workshop_notes.txt', including slide numbers.

Scoring (max 1.0):
 • 0.2  – workshop_notes.txt exists and contains >50 characters of text.
 • 0.4  – Every slide number ("Slide N") for all pages appears in the notes. Partial credit proportional.
 • 0.4  – Text from each slide is present in the notes. We take an 80-char snippet from each page and look for it (case-insensitive) in the notes. Partial credit proportional.

No points are given for merely having the PDF; that is a prerequisite, not task progress.
The script prints detailed diagnostics and always outputs "REWARD: X.X".
"""

import os
import re
from pathlib import Path
from typing import List

from PyPDF2 import PdfReader


################################################################################
# Utility helpers
################################################################################

def _clean(text: str | None) -> str:
    """Collapse all whitespace to single spaces for easier comparison."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


################################################################################
# Core verification logic
################################################################################

def verify_extraction() -> float:
    """Verify that the text (with slide numbers) has been extracted correctly."""
    pdf_path = Path("/home/user/Desktop/workshop_slides.pdf")
    notes_path = Path("/home/user/Desktop/workshop_notes.txt")

    total_score = 0.0
    max_score = 1.0

    print(f"Verifying extraction for PDF: {pdf_path}")
    print(f"Expecting notes file at: {notes_path}")

    # ---------------------------------------------------------------------
    # Prerequisite: source PDF must be present (NO points awarded here)
    # ---------------------------------------------------------------------
    if not pdf_path.exists():
        print("✗ Source PDF not found – task failed.")
        print("REWARD: 0.0")
        return 0.0

    reader = PdfReader(str(pdf_path))
    num_pages: int = len(reader.pages)
    print(f"PDF page count: {num_pages}")

    # ---------------------------------------------------------------------
    # Requirement 1 – Notes file exists & has substantial text (0.2)
    # ---------------------------------------------------------------------
    if notes_path.exists() and notes_path.is_file():
        raw_content = notes_path.read_text(encoding="utf-8", errors="ignore")
        cleaned_content = _clean(raw_content)
        if len(cleaned_content) >= 50:
            total_score += 0.2
            print("✓ Notes file exists with substantial content (0.2)")
        else:
            print("✗ Notes file too small (<50 chars) – no points")
            cleaned_content = ""
    else:
        print("✗ Notes file missing – cannot verify further")
        cleaned_content = ""

    # If content is missing we cannot continue with other checks
    if not cleaned_content:
        final = round(total_score, 2)
        print(f"REWARD: {final}")
        return final

    # ---------------------------------------------------------------------
    # Requirement 2 – Slide numbers included (up to 0.4)
    # ---------------------------------------------------------------------
    numbers_found = 0
    for idx in range(num_pages):
        pattern = re.compile(rf"\bslide\s+{idx + 1}\b", re.IGNORECASE)
        if pattern.search(cleaned_content):
            numbers_found += 1
    ratio_numbers = numbers_found / num_pages if num_pages else 0
    score_numbers = 0.4 * ratio_numbers
    total_score += score_numbers
    print(f"Slide numbers found: {numbers_found}/{num_pages} (+{score_numbers:.2f})")

    # ---------------------------------------------------------------------
    # Requirement 3 – Actual slide text present (up to 0.4)
    # ---------------------------------------------------------------------
    snippets_found = 0
    for page_index, page in enumerate(reader.pages):
        page_text = _clean(page.extract_text())
        if not page_text:
            print(f"Page {page_index + 1} has no extractable text – skipping snippet check")
            continue
        snippet = page_text[:80]  # first 80 chars is enough to be distinctive
        if snippet and snippet.lower() in cleaned_content.lower():
            snippets_found += 1
        else:
            print(f"✗ Snippet from page {page_index + 1} not found in notes")
    ratio_snippets = snippets_found / num_pages if num_pages else 0
    score_snippets = 0.4 * ratio_snippets
    total_score += score_snippets
    print(f"Slide text snippets matched: {snippets_found}/{num_pages} (+{score_snippets:.2f})")

    # ---------------------------------------------------------------------
    # Final score (capped at 1.0)
    # ---------------------------------------------------------------------
    final_score = round(min(total_score, max_score), 2)
    print(f"REWARD: {final_score}")
    return final_score


################################################################################
# Script entry point
################################################################################
if __name__ == "__main__":
    verify_extraction()


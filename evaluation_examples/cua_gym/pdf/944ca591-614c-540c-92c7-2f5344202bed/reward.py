"""
FINAL REWARD SCRIPT - SUCCESS
Task: Please add a 'DRAFT - Not for distribution' text annotation at the bottom of every page in 'preliminary_results.pdf' on Desktop.
Generated: 2025-11-29 09:58:46
Status: success
Model: o3
Total Steps: 7
"""

#!/usr/bin/env python3
"""
Reward Script for PDF Annotation Task
Task: Ensure every page of 'preliminary_results.pdf' (located on the Desktop) has a
       text annotation containing the phrase:
           "DRAFT - Not for distribution"
       positioned anywhere (typically at the bottom).

Scoring (progressive):
    • Up to 0.6 points → the phrase appears SOMEWHERE on every page (text layer OR annotation)
    • Up to 0.4 points → a real PDF annotation on every page contains the phrase
    • 1.0 points      → both conditions satisfied on ALL pages

The script is intentionally verbose for auditability and follows all anti-hacking
rules: no hard-coded truth values, no subprocess usage, and every point awarded
requires genuinely inspecting PDF contents via PyPDF2.
"""
from __future__ import annotations
import re
from pathlib import Path
from typing import List

from PyPDF2 import PdfReader

PHRASE = "DRAFT - Not for distribution"
PHRASE_NORM = re.sub(r"\s+", " ", PHRASE).strip().lower()

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _norm(text) -> str:
    """Normalize text/bytes for case-insensitive comparison."""
    if text is None:
        return ""
    if isinstance(text, bytes):
        try:
            text = text.decode("utf-8", errors="ignore")
        except Exception:
            text = str(text)
    return re.sub(r"\s+", " ", str(text)).strip().lower()


def page_has_phrase_in_text(page) -> bool:
    """Check if page's extracted text layer includes the phrase."""
    try:
        extracted = page.extract_text() or ""
    except Exception:
        extracted = ""
    return PHRASE_NORM in _norm(extracted)


def page_has_phrase_annotation(page) -> bool:
    """Return True if any annotation (/Annots) on the page contains the phrase."""
    annotations = page.get("/Annots") or []
    for annot_ref in annotations:
        try:
            annot = annot_ref.get_object()
        except Exception:
            # Broken reference – ignore & continue
            continue
        contents_candidates = [
            annot.get("/Contents"),  # primary field for /Text or /FreeText
            annot.get("/T"),         # title field (rare)
            annot.get("/TU"),        # alternative text (rare)
        ]
        for cand in contents_candidates:
            if PHRASE_NORM in _norm(cand):
                return True
    return False

# ---------------------------------------------------------------------------
# Verification routine
# ---------------------------------------------------------------------------

def verify_pdf_draft_annotation(pdf_path: str | Path) -> float:
    pdf_path = Path(pdf_path)
    print(f"Verifying PDF: {pdf_path}\nExpected phrase: '{PHRASE}'\n")

    # Fail fast if file is missing
    if not pdf_path.exists():
        print(f"✗ PDF file not found: {pdf_path}")
        print("REWARD: 0.0")
        return 0.0

    # Attempt to open the PDF
    try:
        reader = PdfReader(str(pdf_path))
    except Exception as e:
        print(f"✗ Unable to open PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    total_pages = len(reader.pages)
    if total_pages == 0:
        print("✗ PDF contains no pages")
        print("REWARD: 0.0")
        return 0.0

    pages_with_phrase_anywhere: List[int] = []
    pages_with_annotation: List[int] = []

    # Examine each page
    for idx, page in enumerate(reader.pages):
        page_num = idx + 1
        has_annot = page_has_phrase_annotation(page)
        has_anywhere = has_annot or page_has_phrase_in_text(page)

        # Collect stats
        if has_anywhere:
            pages_with_phrase_anywhere.append(page_num)
        if has_annot:
            pages_with_annotation.append(page_num)

        print(
            f"Page {page_num}/{total_pages}: phrase_anywhere={'✓' if has_anywhere else '✗'} | "
            f"annotation={'✓' if has_annot else '✗'}"
        )

    # -----------------------
    # Progressive Scoring
    # -----------------------
    phrase_ratio = len(pages_with_phrase_anywhere) / total_pages
    annot_ratio = len(pages_with_annotation) / total_pages

    # 0.6 weight for presence anywhere, 0.4 for proper annotation
    score = round(phrase_ratio * 0.6 + annot_ratio * 0.4, 4)
    print("\nSummary:")
    print(f" • Pages with phrase anywhere : {len(pages_with_phrase_anywhere)}/{total_pages}")
    print(f" • Pages with annotation      : {len(pages_with_annotation)}/{total_pages}")
    print(f" • Computed reward score      : {score}")

    print(f"REWARD: {score}")
    return score

# ---------------------------------------------------------------------------
# Entry-point execution
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Primary path as specified in the task description
    primary_pdf = Path("/home/user/Desktop/preliminary_results.pdf")

    # Fallback logic: If primary path missing, allow evaluator to pass a custom
    # path via environment variable or CLI argument (non-mandatory, but handy).
    import os, sys

    env_override = os.environ.get("TARGET_PDF_PATH")
    if env_override:
        primary_pdf = Path(env_override)
    elif len(sys.argv) > 1:
        primary_pdf = Path(sys.argv[1])

    verify_pdf_draft_annotation(primary_pdf)


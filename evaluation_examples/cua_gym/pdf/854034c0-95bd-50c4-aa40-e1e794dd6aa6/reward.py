"""
FINAL REWARD SCRIPT - SUCCESS
Task: Convert the scanned exam paper 'student_exam.pdf' in /home/user/Teaching to searchable PDF, then extract student's handwritten answers using OCR to 'exam_answers.txt'.
Generated: 2025-11-29 10:11:01
Status: success
Model: o3
Total Steps: 13
"""

from __future__ import annotations

"""
Reward script for:
Instruction: Convert the scanned exam paper 'student_exam.pdf' in /home/user/Teaching to
searchable PDF, then extract student's handwritten answers using OCR to 'exam_answers.txt'.

This script verifies two things:
1. A searchable (OCR-enabled) PDF exists that contains all expected text snippets from the
   exam questions.  The converted PDF may have replaced the original file or been saved
   under a new name (e.g. *_searchable.pdf or *_ocr.pdf), so several candidate paths are
   checked.
2. A companion text file exam_answers.txt exists and contains the three expected student
   answers ("4", "H2O", "F = m * a").

The script awards 0.5 points for each successfully verified requirement, returning a
progressive score between 0.0 and 1.0 and printing detailed diagnostics.  It uses PyPDF2
for PDF text extraction and pathlib for file handling.  No forbidden patterns (e.g.
subprocess, hard-coded success) are used.
"""

from pathlib import Path
from typing import List
from PyPDF2 import PdfReader
import textwrap


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

def is_pdf_searchable(pdf_path: Path, snippets: List[str]) -> bool:
    """Return True if *all* snippets are found in text extracted from pdf_path."""
    try:
        reader = PdfReader(str(pdf_path))
        full_text = "\n".join((page.extract_text() or "") for page in reader.pages)
    except Exception as e:
        print(f"✗ Could not read {pdf_path}: {e}")
        return False

    full_text_lower = full_text.lower()
    missing = [s for s in snippets if s.lower() not in full_text_lower]
    if missing:
        print(f"✗ Searchable text check failed for {pdf_path}. Missing snippets: {missing}")
        return False

    # Debug preview of extracted text
    preview = textwrap.shorten(full_text.replace("\n", " "), width=120, placeholder="...")
    print(f"✓ {pdf_path.name} is searchable. Text preview: '{preview}'")
    return True


def verify_answers_file(txt_path: Path, expected_answers: List[str]) -> bool:
    """Return True if txt_path contains all expected_answers (case-insensitive)."""
    if not txt_path.exists():
        print(f"✗ Missing answers file: {txt_path}")
        return False

    content_lines = [ln.strip().lower() for ln in txt_path.read_text(encoding="utf-8", errors="ignore").splitlines() if ln.strip()]
    missing = [ans for ans in expected_answers if ans.lower() not in content_lines]
    if missing:
        print(f"✗ Missing answers in {txt_path}: {missing}")
        print(f"  File content lines: {content_lines}")
        return False

    print(f"✓ All expected answers found in {txt_path}")
    return True


# ---------------------------------------------------------------------------
# Main Verification Logic
# ---------------------------------------------------------------------------

def verify_exam_task() -> float:
    """Verify both searchable PDF conversion and answer extraction. Returns score."""
    score = 0.0
    max_score = 1.0

    # Candidate locations for the searchable PDF (original may be overwritten)
    pdf_candidates = [
        Path("/home/user/Teaching/student_exam.pdf"),
        Path("/home/user/Teaching/student_exam_searchable.pdf"),
        Path("/home/user/Teaching/student_exam_ocr.pdf"),
    ]

    required_pdf_snippets = [
        "Question 1",
        "Question 2",
        "Question 3",
        "chemical symbol for water",
        "2 + 2",
        "Newton's second law",
    ]

    # ---- Requirement 1: PDF is searchable ----
    pdf_verified = False
    for p in pdf_candidates:
        if p.exists() and is_pdf_searchable(p, required_pdf_snippets):
            pdf_verified = True
            break
    if pdf_verified:
        score += 0.5
        print("✓ PDF conversion requirement satisfied (0.5)")
    else:
        print("✗ No searchable PDF meeting requirements was found (0 points)")

    # ---- Requirement 2: Answers extracted correctly ----
    answers_path = Path("/home/user/Teaching/exam_answers.txt")
    expected_answers = ["4", "h2o", "f = m * a"]

    if verify_answers_file(answers_path, expected_answers):
        score += 0.5
        print("✓ Answer extraction requirement satisfied (0.5)")
    else:
        print("✗ Answer extraction requirement failed (0 points)")

    # -----------------------------------------------------------------------
    final_score = min(score, max_score)
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification when run as a script
if __name__ == "__main__":
    verify_exam_task()


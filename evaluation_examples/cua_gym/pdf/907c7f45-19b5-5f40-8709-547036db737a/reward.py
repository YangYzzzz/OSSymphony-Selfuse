"""
FINAL REWARD SCRIPT - SUCCESS
Task: Please merge 'cover_letter.pdf' and 'resume.pdf' from /home/user/Documents/JobApplications into 'application_complete.pdf', with cover letter first.
Generated: 2025-11-29 09:34:51
Status: success
Model: o3
Total Steps: 1
"""

from pathlib import Path
from PyPDF2 import PdfReader
import re

def normalize_text(text: str) -> str:
    """Utility to normalise extracted PDF text for reliable comparison."""
    if text is None:
        return ""
    # Collapse whitespace and lowercase for robust equality checks
    return re.sub(r"\s+", " ", text).strip().lower()

def extract_page_texts(pdf_path: Path) -> list[str]:
    """Return a list with normalised text of every page in the PDF."""
    reader = PdfReader(str(pdf_path))
    texts = []
    for idx, page in enumerate(reader.pages):
        txt = page.extract_text() or ""
        texts.append(normalize_text(txt))
    return texts

def verify_merge(base_dir: Path = Path('/home/user/Documents/JobApplications')) -> float:
    """Verify that cover_letter.pdf and resume.pdf were merged into application_complete.pdf
    with the cover letter pages appearing first.
    Returns a progressive score between 0.0 and 1.0 and prints detailed feedback.
    """
    total_score = 0.0
    max_score   = 1.0

    # Define expected file locations
    cover_path  = base_dir / 'cover_letter.pdf'
    resume_path = base_dir / 'resume.pdf'
    output_path = base_dir / 'application_complete.pdf'

    # 1. Ensure source PDFs exist (no points – prerequisite, but abort if missing)
    if not cover_path.exists() or not resume_path.exists():
        print(f"✗ Source PDFs missing inside {base_dir}")
        return 0.0

    # 2. Extract text from source PDFs (needed for content comparison)
    try:
        cover_texts  = extract_page_texts(cover_path)
        resume_texts = extract_page_texts(resume_path)
        print(f"Cover letter pages: {len(cover_texts)}; Resume pages: {len(resume_texts)}")
    except Exception as e:
        print(f"✗ Error reading source PDFs: {e}")
        return 0.0

    # 3. Verify merged PDF exists
    if not output_path.exists():
        print(f"✗ Output PDF not found: {output_path}")
        return 0.0

    # 4. Read merged PDF content
    try:
        merged_texts = extract_page_texts(output_path)
        print(f"Merged PDF pages: {len(merged_texts)} (expected {len(cover_texts) + len(resume_texts)})")
    except Exception as e:
        print(f"✗ Error reading merged PDF: {e}")
        return 0.0

    expected_pages = len(cover_texts) + len(resume_texts)

    # 4a. Page-count verification (0.3 pts)
    if len(merged_texts) == expected_pages:
        print("✓ Page count matches expected")
        total_score += 0.3
    else:
        print("✗ Page count mismatch")

    # 4b. Cover letter must appear first in exact order (0.35 pts)
    cover_match_pages = sum(
        1 for idx, src_text in enumerate(cover_texts)
        if idx < len(merged_texts) and merged_texts[idx] == src_text
    )
    if cover_match_pages == len(cover_texts):
        print("✓ All cover letter pages match at beginning of merged PDF")
        total_score += 0.35
    else:
        print(f"✗ Cover letter pages match count: {cover_match_pages}/{len(cover_texts)}")

    # 4c. Resume must appear after cover letter, in exact order (0.35 pts)
    resume_start_index = len(merged_texts) - len(resume_texts)
    resume_match_pages = sum(
        1 for j, src_text in enumerate(resume_texts)
        if 0 <= resume_start_index + j < len(merged_texts)
        and merged_texts[resume_start_index + j] == src_text
    )
    if resume_match_pages == len(resume_texts):
        print("✓ All resume pages match at end of merged PDF")
        total_score += 0.35
    else:
        print(f"✗ Resume pages match count: {resume_match_pages}/{len(resume_texts)}")

    # Cap score to 1.0 and round for neatness
    final_score = round(min(total_score, max_score), 3)
    print(f"REWARD: {final_score}")
    return final_score

# Execute verification when script is run directly
if __name__ == '__main__':
    verify_merge()


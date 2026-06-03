"""
FINAL REWARD SCRIPT - SUCCESS
Task: Extract the comparison matrix from 'product_comparison.pdf' in /home/user/Downloads and save to 'comparison_matrix.csv'.
Generated: 2025-11-29 09:18:33
Status: success
Model: o3
Total Steps: 5
"""

import re
from pathlib import Path
from typing import List
from PyPDF2 import PdfReader

"""
Reward script for the task:
"Extract the comparison matrix from 'product_comparison.pdf' in /home/user/Downloads
 and save to 'comparison_matrix.csv'."

The script verifies two things:
1.  The expected comparison matrix can be located inside the source PDF by looking for the
    deterministic markers  BEGIN_COMPARISON_MATRIX  and  END_COMPARISON_MATRIX .
2.  A CSV file named  comparison_matrix.csv  exists in one of the common export locations
    and its contents match the matrix extracted from the PDF.  Matching is performed by
    token comparison so that minor whitespace / newline differences do not cause failure.

Progressive scoring (max 1.0):
  • 0.3 points  – CSV file is present in an expected location.
  • 0.7×R       – Content similarity where R is the fraction of tokens from the expected
                   matrix that appear in the CSV (R = 1 → +0.7 points).

Thus the score is:
  score = 0.3  (if CSV present)  +  0.7 * token_match_ratio
Final score is capped at 1.0 and rounded to four decimals.
"""

def extract_matrix_from_pdf(pdf_path: Path) -> str:
    """Return the raw text of the comparison matrix located between the
    BEGIN_COMPARISON_MATRIX and END_COMPARISON_MATRIX markers."""
    reader = PdfReader(str(pdf_path))
    full_text = "".join(page.extract_text() or "" for page in reader.pages)
    match = re.search(r"BEGIN_COMPARISON_MATRIX(.*?)END_COMPARISON_MATRIX", full_text, re.S)
    if not match:
        raise ValueError("Comparison matrix markers not found in PDF")
    return match.group(1).strip()

def normalize_for_tokenising(text: str) -> List[str]:
    """Convert arbitrary whitespace/newline separated text to a list of tokens
    splitting on commas OR whitespace so that CSV with or without newlines
    is handled uniformly."""
    collapsed = re.sub(r"\s+", " ", text.strip())
    return [tok for tok in re.split(r"[ ,]+", collapsed) if tok]

def verify_task() -> float:
    # Paths
    pdf_path = Path("/home/user/Downloads/product_comparison.pdf")
    csv_candidates = [
        Path("/home/user/Downloads/comparison_matrix.csv"),
        Path("/home/user/comparison_matrix.csv"),
        Path("/home/user/Documents/comparison_matrix.csv"),
    ]

    # 1) Extract expected matrix text from the PDF
    try:
        expected_matrix = extract_matrix_from_pdf(pdf_path)
        print("✓ Extracted comparison matrix from PDF")
    except Exception as e:
        print(f"✗ Failed to extract matrix from PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # 2) Locate CSV file
    csv_path = next((p for p in csv_candidates if p.exists()), None)
    score = 0.0
    if not csv_path:
        print("✗ comparison_matrix.csv not found in expected locations")
        print("REWARD: 0.0")
        return 0.0

    print(f"✓ Found CSV at {csv_path}")
    score += 0.3  # Presence credit

    # 3) Read and compare content
    csv_content = csv_path.read_text(encoding="utf-8", errors="ignore").strip()

    expected_tokens = normalize_for_tokenising(expected_matrix)
    actual_tokens   = normalize_for_tokenising(csv_content)

    match_count = sum(1 for tok in expected_tokens if tok in actual_tokens)
    ratio = match_count / max(len(expected_tokens), 1)

    print(f"Token match: {match_count}/{len(expected_tokens)} (ratio={ratio:.2f})")

    score += 0.7 * ratio  # Content similarity credit

    final = round(min(score, 1.0), 4)
    print(f"REWARD: {final}")
    return final

if __name__ == "__main__":
    verify_task()

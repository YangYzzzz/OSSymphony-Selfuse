"""
FINAL REWARD SCRIPT - SUCCESS
Task: Extract the correlation matrix from 'statistical_analysis.pdf' (page 18) in /home/user/Research and save to 'correlation_matrix.csv'.
Generated: 2025-11-29 09:22:37
Status: success
Model: o3
Total Steps: 4
"""

from __future__ import annotations

"""
Reward Script for Task:
Extract the correlation matrix from 'statistical_analysis.pdf' (page 18)
in /home/user/Research and save it to 'correlation_matrix.csv'.

Scoring Criteria (total 1.0):
 - 0.2  Correct CSV file is present in one of the expected locations
 - 0.8  CSV content EXACTLY matches the correlation matrix lines found on
        page 18 of the PDF (order & text match line-by-line)

The script uses PyPDF2 to extract text from the designated page and then
compares that to the contents of the CSV.  Progressive scoring is applied
according to the proportion of lines that match.
"""

from pathlib import Path
from typing import List
from PyPDF2 import PdfReader

PDF_PATH = "/home/user/Research/statistical_analysis.pdf"
CSV_CANDIDATES = [
    Path("/home/user/Research/correlation_matrix.csv"),
    Path("/home/user/correlation_matrix.csv"),
]
PAGE_INDEX = 17  # page 18 (0-based index)


def extract_matrix_lines_from_pdf(pdf_path: str, *, page_index: int) -> List[str]:
    """Return list of CSV-style lines (containing commas) from the given PDF page."""
    try:
        reader = PdfReader(pdf_path)
        if page_index >= len(reader.pages):
            print(f"✗ PDF has only {len(reader.pages)} pages; page {page_index + 1} missing")
            return []
        text = reader.pages[page_index].extract_text() or ""
    except Exception as e:
        print(f"✗ Error reading PDF: {e}")
        return []

    # Keep only non-empty lines that look like comma-separated values
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    matrix_lines = [ln for ln in lines if "," in ln]

    print(f"Extracted {len(matrix_lines)} matrix lines from PDF page {page_index + 1}")
    for ln in matrix_lines:
        print("  PDF:", ln)
    return matrix_lines


def read_csv_lines(csv_path: Path) -> List[str]:
    """Read CSV file and return list of non-empty trimmed lines."""
    try:
        content = csv_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"✗ Error reading CSV {csv_path}: {e}")
        return []

    lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
    print(f"Read {len(lines)} non-empty lines from CSV {csv_path}")
    for ln in lines:
        print("  CSV:", ln)
    return lines


def verify_task() -> float:
    score = 0.0

    # Step 1: locate CSV file
    csv_path: Path | None = None
    for candidate in CSV_CANDIDATES:
        if candidate.exists():
            csv_path = candidate
            print(f"✓ Found CSV at {csv_path}")
            score += 0.2  # File present at expected location (20%)
            break
    if csv_path is None:
        print("✗ correlation_matrix.csv not found in expected locations")
        print("REWARD: 0.0")
        return 0.0

    # Step 2: extract expected matrix lines from PDF
    expected_lines = extract_matrix_lines_from_pdf(PDF_PATH, page_index=PAGE_INDEX)
    if not expected_lines:
        print("✗ Unable to extract matrix lines from PDF; verification halted")
        print(f"REWARD: {score}")
        return score  # Cannot continue without reference data

    # Step 3: read CSV file
    csv_lines = read_csv_lines(csv_path)
    if not csv_lines:
        print("✗ CSV is empty; verification halted")
        print(f"REWARD: {score}")
        return score

    # Step 4: compare contents line-by-line (order matters)
    total_required = len(expected_lines)
    matching = 0
    for exp, got in zip(expected_lines, csv_lines):
        if exp == got:
            matching += 1
        else:
            print("✗ Line mismatch:\n   expected:", exp, "\n   CSV:     ", got)

    # Any extra trailing lines in CSV count as mismatches (do not award)
    line_match_ratio = matching / total_required if total_required else 0.0
    content_score = 0.8 * line_match_ratio  # up to 0.8 pts
    score += content_score

    if content_score == 0.8:
        print("✓ All matrix lines match between PDF and CSV (0.8 points)")
    else:
        print(f"Partial match: {matching}/{total_required} lines correct ({content_score:.2f} points)")

    # Final capping & print
    final = round(min(score, 1.0), 3)
    print(f"REWARD: {final}")
    return final


if __name__ == "__main__":
    verify_task()


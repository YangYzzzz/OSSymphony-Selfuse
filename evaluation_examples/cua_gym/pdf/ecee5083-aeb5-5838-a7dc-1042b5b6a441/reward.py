"""
FINAL REWARD SCRIPT - SUCCESS
Task: I have a table with merged cells in 'survey_results.pdf' on page 4. Extract it to 'survey_data.csv' and unmerge the cells appropriately.
Generated: 2025-11-29 09:19:47
Status: success
Model: o3
Total Steps: 10
"""

from __future__ import annotations
"""Reward script for:
Task –  ‘I have a table with merged cells in “survey_results.pdf” on page 4.  
Extract it to “survey_data.csv” and unmerge the cells appropriately.’

Verification strategy
---------------------
1. Read page 4 (index 3) of survey_results.pdf using PyPDF2 and parse the table text
   into structured rows:  (question, [strongly-agree, agree, neutral]).
2. Open survey_data.csv and check:
      • File exists
      • Header row is exactly  ["Question","Strongly Agree","Agree","Neutral"]
      • No residual merged-cell label “Responses” appears anywhere
      • Every subsequent data row exactly matches the text & numbers extracted from
        the PDF.
3. Progressive scoring → 1.0 only when every requirement passes.

The script prints detailed diagnostics for every check and always finishes with:
    REWARD: <score>
where <score> ∈ [0.0,1.0].
"""
import csv
import re
from pathlib import Path
from typing import List, Tuple
from PyPDF2 import PdfReader

# ---------- Constants ----------
PDF_PATH = "/home/user/survey_results.pdf"
CSV_PATH = "/home/user/survey_data.csv"
PAGE_INDEX = 3  # page-4 (0-based index)

# ---------- Helper functions ----------

def extract_table_from_pdf(pdf_path: str, page_index: int = 3) -> List[Tuple[str, List[str]]]:
    """Return list of (question, [num1,num2,num3]) parsed from the PDF page."""
    reader = PdfReader(pdf_path)
    if page_index >= len(reader.pages):
        raise ValueError("PDF does not contain requested page index")

    text = reader.pages[page_index].extract_text() or ""
    tokens = [t.strip() for t in text.split("\n") if t.strip()]

    # Skip header tokens until after the merged-cell label “Responses”
    try:
        start = next(i for i, t in enumerate(tokens) if t.lower() == "responses") + 1
    except StopIteration:
        # Fallback: start after token "Question" if “Responses” not found
        try:
            start = next(i for i, t in enumerate(tokens) if t.lower() == "question") + 1
        except StopIteration:
            start = 0

    data_tokens = tokens[start:]
    rows: List[Tuple[str, List[str]]] = []
    i = 0
    while i < len(data_tokens):
        question = data_tokens[i]
        nums: List[str] = []
        j = i + 1
        while j < len(data_tokens) and len(nums) < 3:
            if re.fullmatch(r"[-+]?\d+(?:\.\d+)?", data_tokens[j]):
                nums.append(data_tokens[j])
                j += 1
            else:
                break
        if len(nums) == 3:
            rows.append((question, nums))
        i = j  # advance pointer
    return rows


def verify_csv(csv_path: str, pdf_rows: List[Tuple[str, List[str]]]) -> Tuple[float, List[str]]:
    """Return progressive score (0-1) and debug messages list."""
    msgs: List[str] = []
    score = 0.0

    path = Path(csv_path)
    if not path.exists():
        msgs.append(f"✗ CSV not found at {csv_path}")
        return score, msgs
    msgs.append("✓ CSV file exists (0.0)")

    with path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.reader(fh))

    if not rows:
        msgs.append("✗ CSV is empty")
        return score, msgs

    # 1) Header verification – 0.25 pts
    expected_header = ["Question", "Strongly Agree", "Agree", "Neutral"]
    header = [c.strip() for c in rows[0]]
    if header == expected_header:
        score += 0.25
        msgs.append("✓ Header correct (0.25)")
    else:
        msgs.append(f"✗ Header incorrect – expected {expected_header} got {header}")

    # 2) Data rows vs PDF – 0.55 pts if perfect
    data_rows = rows[1:]
    if len(data_rows) != len(pdf_rows):
        msgs.append(
            f"✗ Row count mismatch – CSV {len(data_rows)} vs PDF {len(pdf_rows)}"
        )
    else:
        match = True
        for idx, (csv_r, (pdf_q, pdf_nums)) in enumerate(zip(data_rows, pdf_rows), 1):
            csv_q = csv_r[0].strip()
            csv_nums = [c.strip() for c in csv_r[1:4]]
            if csv_q != pdf_q or csv_nums != pdf_nums:
                match = False
                msgs.append(
                    f"✗ Row {idx} mismatch – CSV ({csv_q}, {csv_nums}) vs PDF ({pdf_q}, {pdf_nums})"
                )
        if match:
            score += 0.55
            msgs.append("✓ All data rows match PDF (0.55)")

    # 3) Ensure merged-cell label “Responses” removed – 0.2 pts
    full_lower = "\n".join([",".join(r) for r in rows]).lower()
    if "responses" not in full_lower:
        score += 0.2
        msgs.append("✓ ‘Responses’ label absent (0.2)")
    else:
        msgs.append("✗ ‘Responses’ label still present in CSV")

    return min(score, 1.0), msgs


# ---------- Main verification ----------

def verify_task() -> float:
    print("Verifying task: extract table & unmerge cells\n")

    # Parse PDF
    try:
        pdf_rows = extract_table_from_pdf(PDF_PATH, PAGE_INDEX)
        print(f"Extracted {len(pdf_rows)} data rows from PDF page 4:")
        for r in pdf_rows:
            print("  ", r)
    except Exception as e:
        print(f"Error while parsing PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Verify CSV
    score, messages = verify_csv(CSV_PATH, pdf_rows)
    for m in messages:
        print(m)

    final = round(score, 4)
    print(f"\nREWARD: {final}")
    return final


if __name__ == "__main__":
    verify_task()


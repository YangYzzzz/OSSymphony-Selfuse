"""
FINAL REWARD SCRIPT - SUCCESS
Task: Extract the schedule table from 'conference_program.pdf' on Desktop (page 8) and save to 'session_schedule.csv'.
Generated: 2025-11-29 09:20:37
Status: success
Model: o3
Total Steps: 15
"""

import csv
import os
import re
from pathlib import Path
from PyPDF2 import PdfReader

# -------------------------------------------------------------
# Reward Verification Script
# Task: Extract the schedule table from page-8 of
#       '~/Desktop/conference_program.pdf' and save it as
#       '~/Desktop/session_schedule.csv'
#
# Scoring rubric (progressive, max = 1.0):
#   • 0.20  – CSV exists & header contains required columns
#   • 0.80  – Each of the 5 expected rows is present (0.16 ea.)
#            – Order of columns/rows does NOT matter, case/spacing
#              is ignored when matching.
# -------------------------------------------------------------

def _norm(txt: str) -> str:
    """Normalize text for case-insensitive, whitespace-agnostic comparison."""
    return re.sub(r"\s+", " ", str(txt).strip()).lower()

def verify_task() -> float:
    csv_path = Path.home() / "Desktop" / "session_schedule.csv"
    pdf_path = Path.home() / "Desktop" / "conference_program.pdf"

    required_header = ["time", "session", "room"]
    expected_rows = [
        ["09:00", "Opening Remarks", "Hall A"],
        ["10:00", "Machine Learning 101", "Hall B"],
        ["11:00", "Coffee Break", "Lobby"],
        ["11:30", "Deep Learning", "Hall A"],
        ["12:30", "Lunch", "Dining Hall"],
    ]

    total_score = 0.0
    max_score = 1.0
    header_weight = 0.20
    row_weight   = 0.80 / len(expected_rows)

    # ---------------------------------------------------------
    # 1) Verify CSV existence & load
    # ---------------------------------------------------------
    if not csv_path.exists():
        print(f"✗ CSV file not found at: {csv_path}")
        print("REWARD: 0.0")
        return 0.0
    print(f"✓ CSV file located: {csv_path}")

    try:
        with csv_path.open("r", encoding="utf-8", newline="") as fh:
            csv_rows = list(csv.reader(fh))
    except Exception as exc:
        print(f"✗ Failed to read CSV – {exc}")
        print("REWARD: 0.0")
        return 0.0

    if not csv_rows:
        print("✗ CSV is empty")
        print("REWARD: 0.0")
        return 0.0

    # ---------------------------------------------------------
    # 2) Header validation (case-insensitive, any order allowed)
    # ---------------------------------------------------------
    header_norm = [_norm(h) for h in csv_rows[0]]
    print("Header detected:", csv_rows[0])

    if all(col in header_norm for col in required_header):
        total_score += header_weight
        print("✓ Header contains all required columns (0.20)")
        # map required column -> index for later row checks
        col_index = {col: header_norm.index(col) for col in required_header}
    else:
        missing = [col for col in required_header if col not in header_norm]
        print(f"✗ Missing header columns: {missing}")
        col_index = {col: i for i, col in enumerate(required_header)}  # fallback

    # ---------------------------------------------------------
    # 3) Data-row verification (order not important)
    # ---------------------------------------------------------
    data_rows = [r for r in csv_rows[1:] if any(cell.strip() for cell in r)]
    print(f"Detected {len(data_rows)} non-empty data rows")

    # Normalised copy of csv data for quick membership tests
    norm_data_rows = [[_norm(cell) for cell in row] for row in data_rows]

    for exp in expected_rows:
        exp_norm = [_norm(cell) for cell in exp]
        found = False
        for row in norm_data_rows:
            # Make sure row is long enough for indexed access
            if len(row) <= max(col_index.values()):
                continue
            if all(_norm(exp[i]) == row[col_index[required_header[i]]] for i in range(3)):
                found = True
                break
        if found:
            total_score += row_weight
            print(f"✓ Row present: {exp} (+{row_weight:.2f})")
        else:
            print(f"✗ Row missing: {exp}")

    # ---------------------------------------------------------
    # 4) Optional diagnostic cross-check against PDF page-8 text
    # ---------------------------------------------------------
    try:
        if pdf_path.exists():
            pdf_reader = PdfReader(str(pdf_path))
            page8_text = pdf_reader.pages[7].extract_text() or ""
            page8_norm = _norm(page8_text)
            if all(all(_norm(cell) in page8_norm for cell in row) for row in expected_rows):
                print("✓ PDF cross-validation successful (diagnostic – no extra points)")
            else:
                print("! Warning: PDF cross-validation found missing cells (diagnostic only)")
    except Exception as exc:
        print(f"! PDF cross-validation skipped due to error: {exc}")

    # ---------------------------------------------------------
    # Final scoring
    # ---------------------------------------------------------
    final_score = min(total_score, max_score)
    print(f"Total Score: {final_score:.2f} / {max_score}")
    print(f"REWARD: {final_score}")
    return final_score

# Run verification when executed directly
if __name__ == "__main__":
    verify_task()


"""
FINAL REWARD SCRIPT - SUCCESS
Task: I have a table with footnote markers in 'clinical_trial.pdf'. Extract the table to 'trial_results.csv', removing footnote references but keeping the data.
Generated: 2025-11-29 09:23:39
Status: success
Model: o3
Total Steps: 8
"""

from pathlib import Path
import csv
import re
from PyPDF2 import PdfReader


def verify_clinical_trial_extraction():
    """Verify that the table from clinical_trial.pdf has been correctly extracted to
    trial_results.csv with footnote markers removed while preserving the data."""

    # ------------------------------------------------------------------
    # CONFIGURATION
    # ------------------------------------------------------------------
    pdf_path = Path("/home/user/clinical_trial.pdf")
    csv_path = Path("/home/user/trial_results.csv")

    # Common PDF footnote symbols that should NOT appear in the CSV
    footnote_chars = set([
        "*", "†", "‡", "§", "¶", "‖", "ª", "¹", "²", "³",
    ])

    # Expected clean table content (header + rows) after extraction
    expected_header = [
        "Group",
        "Patients",
        "Response Rate",
        "Adverse Events",
    ]
    expected_rows = [
        ["Placebo", "50", "12%", "Mild"],
        ["Drug A", "48", "35%", "Moderate"],
    ]

    # ------------------------------------------------------------------
    # VERIFICATION LOGIC
    # ------------------------------------------------------------------
    score = 0.0
    max_score = 1.0

    # 1) Ensure the original PDF actually contains footnote markers -------
    try:
        reader = PdfReader(str(pdf_path))
        pdf_text = "\n".join(page.extract_text() or "" for page in reader.pages)
        if any(char in pdf_text for char in footnote_chars):
            print("✓ PDF contains footnote markers (pre-condition satisfied) — 0.2")
            score += 0.2
        else:
            print("✗ No footnote markers detected in PDF (unexpected)")
    except Exception as exc:
        print(f"✗ Failed to read PDF: {exc}")
        # Without the PDF we cannot continue meaningfully
        return 0.0

    # 2) Check that the CSV file exists -----------------------------------
    if csv_path.exists():
        print("✓ CSV file exists — 0.1")
        score += 0.1
    else:
        print("✗ CSV file missing: trial_results.csv not found")
        return 0.0  # Cannot award further points without the file

    # 3) Load and analyse CSV content -------------------------------------
    try:
        with csv_path.open(newline="", encoding="utf-8") as fh:
            raw_rows = list(csv.reader(fh))
    except Exception as exc:
        print(f"✗ Failed to read CSV: {exc}")
        return score

    # Strip whitespace and drop completely empty rows
    rows = [
        [cell.strip() for cell in row]
        for row in raw_rows
        if any(cell.strip() for cell in row)
    ]

    if not rows:
        print("✗ CSV is empty")
        return score

    # 3a) Verify header ----------------------------------------------------
    header_ok = rows[0] == expected_header
    if header_ok:
        print("✓ Header matches expected — 0.2")
        score += 0.2
    else:
        print(f"✗ Header mismatch. Found: {rows[0]}")

    # 3b) Verify data rows -------------------------------------------------
    data_rows = rows[1:]
    matched = 0
    for expected in expected_rows:
        if expected in data_rows:
            matched += 1
    if matched == len(expected_rows):
        print("✓ All expected data rows present — 0.3")
        score += 0.3
    else:
        print(f"✗ Missing or incorrect data rows: matched {matched} / {len(expected_rows)}")

    # 3c) Ensure footnote characters were removed -------------------------
    csv_has_footnote = any(
        any(char in cell for char in footnote_chars)
        for row in data_rows
        for cell in row
    )
    if not csv_has_footnote:
        print("✓ No footnote markers remain in CSV — 0.2")
        score += 0.2
    else:
        print("✗ Footnote markers still present in CSV")

    # ------------------------------------------------------------------
    # FINAL SCORING
    # ------------------------------------------------------------------
    final_score = min(score, max_score)
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification when the script is run ------------------------------
if __name__ == "__main__":
    verify_clinical_trial_extraction()


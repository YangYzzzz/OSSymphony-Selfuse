"""
FINAL REWARD SCRIPT - SUCCESS
Task: Extract the data table from page 8 of 'financial_report.pdf' on Desktop and save it as 'quarterly_results.csv'.
Generated: 2025-11-29 09:17:08
Status: success
Model: o3
Total Steps: 8
"""

from pathlib import Path
import csv
import re
from PyPDF2 import PdfReader

# ---------------- Helper Functions -----------------

def normalize_money(value: str) -> str:
    """Remove every non-digit character so that $100,000 -> 100000."""
    return re.sub(r"[^0-9]", "", value or "")


def extract_pdf_table(pdf_path: Path, page_index: int = 7):
    """Extract (Quarter, Revenue, Profit) tuples from the target PDF page.
    Assumes the table is laid-out vertically as:
        Quarter\nRevenue\nProfit
    for every quarter row.
    """
    reader = PdfReader(str(pdf_path))
    if page_index >= len(reader.pages):
        raise ValueError(
            f"PDF has only {len(reader.pages)} pages, cannot access page {page_index+1}"
        )

    text = reader.pages[page_index].extract_text() or ""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    quarter_re = re.compile(r"^Q[1-4]\s+20\d{2}$", re.I)
    rows = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if quarter_re.match(line):
            if i + 2 < len(lines):
                rev = normalize_money(lines[i + 1])
                prof = normalize_money(lines[i + 2])
                rows.append((line, rev, prof))
                i += 3
                continue
        i += 1
    return rows

# ---------------- Verification Logic ----------------

def verify_task():
    desktop = Path("/home/user/Desktop")
    csv_path = desktop / "quarterly_results.csv"
    pdf_path = desktop / "financial_report.pdf"

    total_score = 0.0  # progressive scoring
    max_score = 1.0

    # 1) CSV must exist and contain data ----------------------------------
    if not csv_path.exists():
        print(f"✗ Missing CSV file at {csv_path}")
        print("REWARD: 0.0")
        return 0.0
    try:
        with csv_path.open(newline="", encoding="utf-8") as f:
            csv_rows = list(csv.reader(f))
    except Exception as e:
        print(f"✗ Failed to read CSV: {e}")
        print("REWARD: 0.0")
        return 0.0
    if len(csv_rows) < 2:
        print("✗ CSV appears empty (needs header + data)")
        print("REWARD: 0.1")
        return 0.1
    print("✓ CSV file found and has data (0.2)")
    total_score += 0.2

    # 2) Header verification ----------------------------------------------
    expected_header = ["quarter", "revenue", "profit"]
    actual_header = [h.strip().lower() for h in csv_rows[0]]
    if actual_header == expected_header:
        print("✓ Header row matches expected (0.2)")
        total_score += 0.2
    else:
        print(f"✗ Header mismatch. Found {actual_header}, expected {expected_header}")

    # 3) Check that all four quarters are present --------------------------
    csv_data = {}
    for row in csv_rows[1:]:
        if len(row) < 3:
            continue
        quarter = row[0].strip()
        revenue = normalize_money(row[1])
        profit = normalize_money(row[2])
        csv_data[quarter] = (revenue, profit)

    expected_quarters = [f"Q{i} 2024" for i in range(1, 5)]
    missing_quarters = [q for q in expected_quarters if q not in csv_data]
    if not missing_quarters:
        print("✓ All four quarters present in CSV (0.2)")
        total_score += 0.2
    else:
        print(f"✗ Missing quarters in CSV: {missing_quarters}")

    # 4) Cross-validate CSV numbers against the PDF source -----------------
    if pdf_path.exists():
        try:
            pdf_rows = extract_pdf_table(pdf_path)
            if pdf_rows:
                pdf_data = {q: (rev, prof) for q, rev, prof in pdf_rows}
                mismatches = []
                for q in expected_quarters:
                    if q not in pdf_data or q not in csv_data:
                        mismatches.append((q, "missing"))
                    else:
                        csv_rev, csv_prof = csv_data[q]
                        pdf_rev, pdf_prof = pdf_data[q]
                        if csv_rev != pdf_rev or csv_prof != pdf_prof:
                            mismatches.append((q, csv_rev, pdf_rev, csv_prof, pdf_prof))
                if not mismatches:
                    print("✓ CSV numeric values match PDF source (0.4)")
                    total_score += 0.4
                else:
                    print(f"✗ Data mismatches between CSV and PDF: {mismatches}")
            else:
                print("✗ Failed to extract table rows from PDF for comparison")
        except Exception as e:
            print(f"✗ Error processing PDF: {e}")
    else:
        print(f"✗ PDF file not found at {pdf_path}; cannot cross-validate values")

    # ---------------- Final Score ----------------------------------------
    final_score = min(total_score, max_score)
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification when script is run directly
if __name__ == "__main__":
    verify_task()

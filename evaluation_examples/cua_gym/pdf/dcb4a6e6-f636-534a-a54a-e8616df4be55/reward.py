"""
FINAL REWARD SCRIPT - SUCCESS
Task: I need to extract the financial statement tables from 'annual_report.pdf' (pages 25-30) and save as separate files: 'income_statement.csv', 'balance_sheet.csv', and 'cash_flow.csv'.
Generated: 2025-11-29 09:20:21
Status: success
Model: o3
Total Steps: 9
"""

"""Reward script for verifying extraction of financial statement tables to CSV files.
Verifies that three CSV files (income_statement.csv, balance_sheet.csv, cash_flow.csv)
exist and contain expected rows extracted from pages 25-30 of annual_report.pdf.
Returns a progressive score (0.0–1.0) based on how many CSVs are correct.
"""
from pathlib import Path
from typing import List

# ---------------------------------------------------------------------------
# Expected CSV content for each financial statement
# ---------------------------------------------------------------------------
EXPECTED_INCOME = [
    "Year,Revenue,Expenses,Profit",
    "2022,1000,700,300",
    "2021,900,650,250",
    "2020,850,600,250",
]
EXPECTED_BALANCE = [
    "Item,2022,2021,2020",
    "Assets,2000,1800,1600",
    "Liabilities,800,700,600",
    "Equity,1200,1100,1000",
]
EXPECTED_CASH = [
    "Year,Net Cash from Ops,Net Cash from Invest,Net Cash from Finance",
    "2022,400,-200,50",
    "2021,350,-150,40",
    "2020,300,-100,30",
]

CSV_SPECS = [
    ("income_statement.csv", EXPECTED_INCOME),
    ("balance_sheet.csv", EXPECTED_BALANCE),
    ("cash_flow.csv", EXPECTED_CASH),
]

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def candidate_paths(filename: str):
    """Generate plausible locations for the output files."""
    bases = [
        Path("/tmp"),                # Default location used by golden script
        Path.cwd(),                  # Current working directory
        Path.home(),                 # /home/user
        Path.home() / "Documents",  # User documents
        Path.home() / "Desktop",    # User desktop
    ]
    yielded = set()
    for base in bases:
        p = base / filename
        if p not in yielded:
            yielded.add(p)
            yield p


def locate_file(filename: str) -> Path | None:
    """Return the first existing candidate path for the given filename."""
    for p in candidate_paths(filename):
        if p.exists():
            return p
    return None


def verify_csv(csv_path: Path | None, expected_rows: List[str]) -> bool:
    """Check that csv_path exists and contains every expected row (order-independent)."""
    if not csv_path or not csv_path.exists():
        print(f"✗ Missing file: {csv_path if csv_path else 'None'}")
        return False

    try:
        lines = [ln.strip() for ln in csv_path.read_text(encoding="utf-8", errors="ignore").splitlines() if ln.strip()]
    except Exception as exc:
        print(f"✗ Could not read {csv_path}: {exc}")
        return False

    all_present = True
    for row in expected_rows:
        if row in lines:
            print(f"✓ {csv_path.name} contains expected row: {row}")
        else:
            all_present = False
            print(f"✗ {csv_path.name} is missing expected row: {row}")
    return all_present

# ---------------------------------------------------------------------------
# Main verification logic
# ---------------------------------------------------------------------------

def verify_task() -> float:
    print("Verifying extracted financial statement CSV files...")
    passed = 0

    for filename, expected in CSV_SPECS:
        print(f"\nChecking {filename} ...")
        path = locate_file(filename)
        if verify_csv(path, expected):
            passed += 1
        else:
            print(f"Verification failed for {filename}")

    total = len(CSV_SPECS)
    score = passed / total  # Progressive scoring 0.0 – 1.0

    print(f"\nCSV files verified successfully: {passed}/{total}")
    print(f"REWARD: {score}")
    return score

# ---------------------------------------------------------------------------
# Execute verification when script is run directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    verify_task()


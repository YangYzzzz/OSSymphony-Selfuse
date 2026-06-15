"""
FINAL REWARD SCRIPT - SUCCESS
Task: Extract the pricing table from page 3 of 'service_catalog.pdf' in /home/user/Documents/Sales and save to 'pricing_data.xlsx' in Excel format.
Generated: 2025-11-29 09:18:49
Status: success
Model: o3
Total Steps: 9
"""

from pathlib import Path
import re
import openpyxl
from PyPDF2 import PdfReader

def norm_money(value: str) -> str:
    """Normalize monetary strings by stripping everything except digits, sign and decimal point."""
    if value is None:
        return ""
    return re.sub(r"[^0-9.\-]", "", str(value))

def verify_task() -> float:
    """
    Verification script for task:
    "Extract the pricing table from page 3 of 'service_catalog.pdf' in /home/user/Documents/Sales
    and save to 'pricing_data.xlsx' in Excel format."
    
    Returns a progressive score between 0.0 and 1.0 based on how many requirements
    are satisfied. Prints detailed diagnostics for transparency.
    """
    print("Starting verification for pricing table extraction task…")

    # Expected file locations
    pdf_path = Path("/home/user/Documents/Sales/service_catalog.pdf")
    excel_path = Path("/home/user/Documents/Sales/pricing_data.xlsx")

    # Scoring accumulator
    score = 0.0

    # ------------------------------------------------------------------
    # 1. Verify PDF still contains pricing table on page 3  (0.2 points)
    # ------------------------------------------------------------------
    try:
        reader = PdfReader(str(pdf_path))
        if len(reader.pages) >= 3:
            page3_text = (reader.pages[2].extract_text() or "").lower()
            keywords = ["pricing table", "basic", "standard", "premium"]
            if all(k in page3_text for k in keywords):
                print("✓ Page 3 of PDF contains expected pricing keywords (0.2 points)")
                score += 0.2
            else:
                print("✗ One or more pricing keywords missing from PDF page 3 (0 points)")
        else:
            print("✗ PDF does not have at least 3 pages (0 points)")
    except Exception as e:
        print(f"✗ Error loading or reading PDF: {e} (0 points)")

    # ------------------------------------------------------------------
    # 2. Verify extracted Excel file structure & data  (0.8 points total)
    #    2a. Worksheet exists & header correct            (0.3 points)
    #    2b. All pricing rows present & values correct   (0.5 points)
    # ------------------------------------------------------------------
    if not excel_path.exists():
        print("✗ pricing_data.xlsx not found at expected location (0 points)")
        final = max(0.0, min(score, 1.0))
        print(f"REWARD: {final}")
        return final

    try:
        wb = openpyxl.load_workbook(excel_path)
        sheet = wb.active

        # Gather rows while discarding trailing empty rows
        rows = list(sheet.iter_rows(values_only=True))
        rows = [r for r in rows if any(cell is not None and str(cell).strip() != "" for cell in r)]
        if not rows:
            print("✗ Worksheet is empty (0 points)")
            final = max(0.0, min(score, 1.0))
            print(f"REWARD: {final}")
            return final

        # 2a. Header verification
        header = [str(c).strip().lower() if c is not None else "" for c in rows[0][:3]]
        expected_header = ["plan", "monthly", "annual"]
        if header == expected_header:
            print("✓ Header row matches expected ['Plan','Monthly','Annual'] (0.3 points)")
            score += 0.3
        else:
            print(f"✗ Header row mismatch. Found {header}, expected {expected_header} (0 points)")

        # 2b. Data rows verification
        expected_data = {
            "basic": ("$10", "$100"),
            "standard": ("$20", "$200"),
            "premium": ("$30", "$300"),
        }
        found_correct = 0
        for row in rows[1:]:
            if len(row) < 3 or row[0] is None:
                continue
            plan_name = str(row[0]).strip().lower()
            if plan_name in expected_data:
                exp_monthly, exp_annual = expected_data[plan_name]
                mon_ok = norm_money(row[1]) == norm_money(exp_monthly)
                ann_ok = norm_money(row[2]) == norm_money(exp_annual)
                if mon_ok and ann_ok:
                    found_correct += 1
        if found_correct == len(expected_data):
            print("✓ All expected pricing rows present with correct values (0.5 points)")
            score += 0.5
        else:
            print(f"✗ Only {found_correct}/{len(expected_data)} pricing rows correct (0 points)")

    except Exception as e:
        print(f"✗ Error opening or verifying Excel file: {e} (0 points)")

    # ------------------------------------------------------------------
    # Final score capping and output
    # ------------------------------------------------------------------
    final_score = max(0.0, min(score, 1.0))
    print(f"Final score breakdown: {score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score

# Execute verification when run as script
if __name__ == "__main__":
    verify_task()

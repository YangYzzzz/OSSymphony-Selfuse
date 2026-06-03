"""
FINAL REWARD SCRIPT - SUCCESS
Task: Batch convert all Excel spreadsheets (.xlsx) in /home/user/Documents/Data to PDF, saving in folder 'Data_PDF' with all sheets included.
Generated: 2025-11-29 10:15:56
Status: success
Model: o3
Total Steps: 12
"""

"""
Reward Script for Task:
Batch convert all Excel spreadsheets (.xlsx) in /home/user/Documents/Data to PDF,
saving them in /home/user/Documents/Data_PDF with ALL sheets included.

The script awards points for EACH workbook based on:
  • Matching PDF file present (0.3)
  • PDF page-count ≥ sheet-count, full match gets more points (up to 0.3)
  • Every sheet-name text found somewhere in the PDF pages (up to 0.4)

The final reward is the average across all workbooks, capped at 1.0.
"""
from pathlib import Path
from typing import List
from PyPDF2 import PdfReader
import openpyxl
import sys


def verify_batch_conversion(data_dir: str, pdf_dir: str) -> float:
    """Verify that every .xlsx in data_dir has a corresponding PDF in pdf_dir
    containing all sheets (as separate pages with their names visible).
    Returns a float score between 0.0 and 1.0 and prints detailed feedback."""

    data_dir_path = Path(data_dir)
    pdf_dir_path = Path(pdf_dir)

    print(f"Data directory : {data_dir_path}")
    print(f"PDF  directory : {pdf_dir_path}\n")

    xlsx_paths: List[Path] = sorted(data_dir_path.glob("*.xlsx"))
    if not xlsx_paths:
        print("✗ No .xlsx files found – cannot evaluate task")
        print("REWARD: 0.0")
        return 0.0

    total_possible = float(len(xlsx_paths))  # each workbook worth up to 1.0 before averaging
    accumulated = 0.0

    # --- iterate over every workbook -------------------------------------------------------
    for wb_path in xlsx_paths:
        print(f"--- Verifying {wb_path.name} ---")
        base_name = wb_path.stem
        expected_pdf = pdf_dir_path / f"{base_name}.pdf"
        wb_score = 0.0  # per-file running score

        # 1) Load workbook to get sheet names
        try:
            wb = openpyxl.load_workbook(wb_path, read_only=True, data_only=True)
            sheet_names = wb.sheetnames
            wb.close()
            sheet_count = len(sheet_names)
            print(f"  • Sheet count = {sheet_count} → {sheet_names}")
        except Exception as e:
            print(f"  ✗ Failed to read workbook ({e}) – skipping further checks for this file")
            continue

        # 2) Check for PDF existence (exact or best-effort name match)
        if expected_pdf.exists():
            print(f"  ✓ PDF present          : {expected_pdf.name}")
            wb_score += 0.3
            pdf_path = expected_pdf
        else:
            # fall-back: any PDF starting with the same base name
            alt_matches = list(pdf_dir_path.glob(f"{base_name}*.pdf"))
            if alt_matches:
                pdf_path = alt_matches[0]
                print(f"  ✓ PDF present (alt)    : {pdf_path.name}")
                wb_score += 0.25  # small penalty for unexpected naming
            else:
                print("  ✗ Corresponding PDF not found – no further checks possible for this workbook")
                accumulated += wb_score
                continue

        # 3) Inspect PDF content
        try:
            reader = PdfReader(str(pdf_path))
            page_count = len(reader.pages)
            print(f"  • PDF page count       : {page_count}")

            # Page-count scoring
            if page_count == sheet_count:
                print("  ✓ Page count matches sheet count (perfect)")
                wb_score += 0.3
            elif page_count > sheet_count:
                print("  ⚠ Page count exceeds sheet count (acceptable)")
                wb_score += 0.2
            else:
                print("  ✗ Page count less than sheet count (no points)")

            # Extract text from all pages once for sheet-name search
            combined_text = "\n".join((page.extract_text() or "") for page in reader.pages).lower()
            found_names = sum(1 for s in sheet_names if s.lower() in combined_text)
            ratio = found_names / sheet_count if sheet_count else 0
            if ratio == 1:
                print("  ✓ All sheet names located in PDF text")
            else:
                print(f"  ⚠ {found_names}/{sheet_count} sheet names located in PDF text")
            wb_score += 0.4 * ratio  # proportional awarding
        except Exception as e:
            print(f"  ✗ Error reading PDF ({e}) – skipping remaining checks for this workbook")

        print(f"  → Workbook score       : {wb_score:.2f}/1.00\n")
        accumulated += wb_score

    # --- final aggregation -----------------------------------------------------------------
    final_score = 0.0 if total_possible == 0 else round(min(accumulated / total_possible, 1.0), 2)
    print(f"Overall score            : {accumulated:.2f}/{total_possible:.2f}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    # Paths per task instructions
    DATA_DIR = "/home/user/Documents/Data"
    PDF_DIR  = "/home/user/Documents/Data_PDF"
    verify_batch_conversion(DATA_DIR, PDF_DIR)


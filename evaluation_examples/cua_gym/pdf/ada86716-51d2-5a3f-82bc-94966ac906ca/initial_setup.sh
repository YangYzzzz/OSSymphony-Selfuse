#!/usr/bin/env bash
set -euo pipefail
# ---------------------------------------------------------------------------
#  INITIAL SET-UP SCRIPT
#  Creates two dummy Excel workbooks in /home/user/Documents/Data
#  and writes placeholder PDFs (ONE page each) to /home/user/Documents/Data_PDF
# ---------------------------------------------------------------------------

# 1) Required absolute paths extracted verbatim from task instruction
DATA_DIR="/home/user/Documents/Data"
PDF_DIR="/home/user/Documents/Data_PDF"

# 2) Create folders
mkdir -p "${DATA_DIR}"
mkdir -p "${PDF_DIR}"

# 3) Install Python dependencies if missing
python3 - <<'PY'
import sys, subprocess, importlib.util

def ensure(pkg):
    if importlib.util.find_spec(pkg) is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])

for package in ("reportlab", "PyPDF2", "openpyxl"):
    ensure(package)
PY

# 4) Python block – build sample .xlsx files and placeholder PDFs
python3 <<'PY'
from pathlib import Path
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from PyPDF2 import PdfReader
from openpyxl import Workbook

DATA_DIR = Path("/home/user/Documents/Data")
PDF_DIR  = Path("/home/user/Documents/Data_PDF")

# ------------------------------------------------------------------------
# Helper: create a workbook with deterministic contents
# ------------------------------------------------------------------------
def make_wb(filename, sheets):
    wb = Workbook()
    # Remove default sheet
    wb.remove(wb.active)
    for sheet_name, first_cell in sheets:
        ws = wb.create_sheet(title=sheet_name)
        ws["A1"] = first_cell
        # Fill a small deterministic grid
        for r in range(2, 7):
            for c in range(1, 6):
                ws.cell(row=r, column=c, value=f"{sheet_name[:3]}-{r}-{c}")
    wb.save(filename)

# 1) sales_Q1.xlsx  (2 sheets)
make_wb(DATA_DIR / "sales_Q1.xlsx",
        [("Summary",  "Sales Summary"),
         ("Details",  "Detailed Lines")])

# 2) inventory.xlsx (2 sheets)
make_wb(DATA_DIR / "inventory.xlsx",
        [("Stock",  "Current Stock"),
         ("Orders", "Purchase Orders")])

# ------------------------------------------------------------------------
# Build a ONE-PAGE placeholder PDF for every workbook
# ------------------------------------------------------------------------
styles = getSampleStyleSheet()
for xlsx in DATA_DIR.glob("*.xlsx"):
    pdf_path = PDF_DIR / f"{xlsx.stem}.pdf"
    doc = SimpleDocTemplate(str(pdf_path), pagesize=LETTER)
    story = [
        Paragraph(f"Placeholder PDF for {xlsx.name}", styles["Title"]),
        Spacer(1, 24),
        Paragraph("Conversion pending...", styles["Normal"])
    ]
    doc.build(story)

    # Quick sanity check via PyPDF2
    pages = len(PdfReader(str(pdf_path)).pages)
    print(f"Wrote {pdf_path} ({pages} page)")

print("Initial set-up complete.")
PY

# 5) Final summary
echo "------------------------------------------------"
echo "Excel files in ${DATA_DIR}:   $(ls -1 "${DATA_DIR}"/*.xlsx | wc -l)"
echo "Placeholder PDFs in ${PDF_DIR}: $(ls -1 "${PDF_DIR}"/*.pdf | wc -l)"
echo "Initial script finished successfully."
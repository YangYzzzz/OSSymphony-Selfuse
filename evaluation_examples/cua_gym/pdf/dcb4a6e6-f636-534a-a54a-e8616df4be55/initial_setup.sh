#!/usr/bin/env bash
set -euo pipefail
#
# Initial PDF creator for:
#   /tmp/annual_report.pdf          (40-page dummy report)
#
# NOTE:  The original task instruction does not specify any directory.
#        To keep an absolute path that is writable on any stock Ubuntu
#        install, this script stores everything in /tmp.
#

# ----------------------------------------------------------------------
# 1) Make sure the target directory exists
# ----------------------------------------------------------------------
mkdir -p /tmp

# ----------------------------------------------------------------------
# 2) Ensure dependencies are present
# ----------------------------------------------------------------------
# Install dependencies if missing
python3 - <<'PY'
import importlib, subprocess, sys, pathlib, textwrap

for pkg in ("reportlab", "PyPDF2"):
    try:
        importlib.import_module(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])

# ------------------------------------------------------------------
# 3) Build the placeholder /tmp/annual_report.pdf
# ------------------------------------------------------------------
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER

pdf_path = "/tmp/annual_report.pdf"
c = canvas.Canvas(pdf_path, pagesize=LETTER)

# Helper blocks –  text for each financial statement
income_lines = [
    "Income Statement",
    "Year,Revenue,Expenses,Profit",
    "2022,1000,700,300",
    "2021,900,650,250",
    "2020,850,600,250",
]
balance_lines = [
    "Balance Sheet",
    "Item,2022,2021,2020",
    "Assets,2000,1800,1600",
    "Liabilities,800,700,600",
    "Equity,1200,1100,1000",
]
cash_lines = [
    "Cash Flow Statement",
    "Year,Net Cash from Ops,Net Cash from Invest,Net Cash from Finance",
    "2022,400,-200,50",
    "2021,350,-150,40",
    "2020,300,-100,30",
]

for p in range(1, 41):                # pages 1 .. 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, 750, f"Annual Report - Page {p}")

    # Pages 25-30 receive tables
    if p in (25, 26):
        c.setFont("Helvetica", 10)
        y = 700
        for ln in income_lines:
            c.drawString(72, y, ln)
            y -= 14
    elif p in (27, 28):
        c.setFont("Helvetica", 10)
        y = 700
        for ln in balance_lines:
            c.drawString(72, y, ln)
            y -= 14
    elif p in (29, 30):
        c.setFont("Helvetica", 10)
        y = 700
        for ln in cash_lines:
            c.drawString(72, y, ln)
            y -= 14

    c.showPage()

c.save()
print(f"Created {pdf_path}")
PY

echo "Initial PDF written to /tmp/annual_report.pdf (40 pages)"
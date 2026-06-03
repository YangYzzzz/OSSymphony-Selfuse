#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Initial PDF setup script
# Creates 8 individual contract signature pages and a placeholder
# '/home/user/Documents/Contracts/signed_contract.pdf'
###############################################################################

# 1. Ensure target directory exists
mkdir -p /home/user/Documents/Contracts

# 2. Install ReportLab & PyPDF2 if missing
python3 - <<'PY'
import subprocess, sys, importlib.util, pathlib, os

def ensure(pkg):
    if importlib.util.find_spec(pkg) is None:  # not installed
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])

for package in ("reportlab", "PyPDF2"):
    ensure(package)
PY

# 3. Generate the 8 individual signature page PDFs + placeholder merged file
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
import os

DIR = "/home/user/Documents/Contracts"
os.makedirs(DIR, exist_ok=True)

# Create 8 signed pages
for i in range(1, 9):
    fname = f"{DIR}/signature_page_{i}.pdf"
    c = canvas.Canvas(fname, pagesize=LETTER)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, 720, f"Contract Page {i}")
    c.setFont("Helvetica", 12)
    c.drawString(72, 680, "Signed by Party A and Party B")
    c.drawString(72, 640, f"(Page {i} of 8)")
    # Fake signature line
    c.line(72, 120, 300, 120)
    c.drawString(72, 100, "Signature")
    c.save()

# Placeholder merged contract
placeholder = f"{DIR}/signed_contract.pdf"
c = canvas.Canvas(placeholder, pagesize=LETTER)
c.setFont("Helvetica-Bold", 14)
c.drawString(72, 720, "Signed Contract (Placeholder)")
c.drawString(72, 700, "This file will be replaced by the merged document.")
c.save()
PY

echo "Initial PDFs generated in /home/user/Documents/Contracts:"
ls -1 /home/user/Documents/Contracts
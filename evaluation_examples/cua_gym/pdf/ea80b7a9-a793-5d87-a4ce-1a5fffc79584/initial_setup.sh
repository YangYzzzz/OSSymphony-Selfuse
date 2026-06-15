#!/usr/bin/env bash
set -euo pipefail
#
# Creates the password-protected, water-marked starting file:
#   /home/user/Documents/protected_draft.pdf
#

# 1. Ensure target directory exists
mkdir -p /home/user/Documents

# 2. Install dependencies if missing
python3 - <<'PY'
import subprocess, sys, importlib.util, json, textwrap, os

def ensure(pkg):
    if importlib.util.find_spec(pkg) is None:          # not installed
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])

for p in ("reportlab", "PyPDF2"):
    ensure(p)
PY

# 3. Build the PDF, add watermark, and encrypt it
python3 <<'PY'
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import os, tempfile

# ------------------------------------------------------------------
OUTPUT_FILE = "/home/user/Documents/protected_draft.pdf"
TMP_FILE    = "/home/user/Documents/_tmp_unencrypted.pdf"
PW          = "temp123"
# ------------------------------------------------------------------

# ----- 3A. Create base PDF with a big "DRAFT" watermark ------------
c = canvas.Canvas(TMP_FILE, pagesize=A4)
width, height = A4

# Main report text
c.setFont("Helvetica-Bold", 16)
c.drawString(72, height - 72, "Quarterly Financial Summary")

c.setFont("Helvetica", 12)
text = c.beginText(72, height - 110)
for line in (
        "Revenue increased by 12% compared to last year.",
        "Net profit margin remains stable at 8.4%.",
        "Further cost optimizations are planned for Q3."):
    text.textLine(line)
c.drawText(text)

# Watermark
c.saveState()
c.setFont("Helvetica-Bold", 100)
c.setFillGray(0.85)                 # light grey
c.translate(width * 0.5, height * 0.4)
c.rotate(45)
c.drawCentredString(0, 0, "DRAFT")
c.restoreState()
c.save()

# ----- 3B. Encrypt the PDF with password 'temp123' -----------------
reader = PdfReader(TMP_FILE)
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

writer.encrypt(user_password=PW, owner_password=PW)
with open(OUTPUT_FILE, "wb") as fp:
    writer.write(fp)

os.remove(TMP_FILE)
print(f"Created encrypted watermark PDF: {OUTPUT_FILE}")
PY

echo "Initial PDF ready at /home/user/Documents/protected_draft.pdf (password: temp123)"
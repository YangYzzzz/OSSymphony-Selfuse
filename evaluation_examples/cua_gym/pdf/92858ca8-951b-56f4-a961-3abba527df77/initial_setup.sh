#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Initial script
# Purpose : Build the starting PDF  “meeting_slides.pdf” on the Desktop
# Path    : /home/user/Desktop/meeting_slides.pdf
###############################################################################

#-----------------------------------------------------------------------------
# 1. Install required Python libraries if they are missing
#-----------------------------------------------------------------------------
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"   2>/dev/null || pip3 install --user PyPDF2

#-----------------------------------------------------------------------------
# 2. Ensure target directory exists
#-----------------------------------------------------------------------------
mkdir -p /home/user/Desktop

#-----------------------------------------------------------------------------
# 3. Create a simple 3-page presentation PDF
#-----------------------------------------------------------------------------
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER

pdf_path = "/home/user/Desktop/meeting_slides.pdf"
c        = canvas.Canvas(pdf_path, pagesize=LETTER)
width, height = LETTER

for page_no in range(1, 4):
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(width/2, height/2, f"Slide {page_no}")
    c.showPage()

c.save()
print(f"[INITIAL] Created 3-page PDF at {pdf_path}")
PY

echo "[INITIAL] Script completed successfully."
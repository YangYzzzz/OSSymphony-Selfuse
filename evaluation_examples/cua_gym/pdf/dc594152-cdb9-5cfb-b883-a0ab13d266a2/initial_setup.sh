#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Initial script – builds the “raw” PDF exactly as named in the task wording.
# Target files:
#   • /home/user/flowchart.pdf  (no PNG is produced in this stage)
###############################################################################

#-----------------------------------------------------------------------
# 1. Make sure the required Python libraries are available
#-----------------------------------------------------------------------
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"     2>/dev/null || pip3 install --user PyPDF2

#-----------------------------------------------------------------------
# 2. Prepare target directory and absolute path (NO env-vars allowed)
#-----------------------------------------------------------------------
mkdir -p /home/user
PDF_PATH="/home/user/flowchart.pdf"

#-----------------------------------------------------------------------
# 3. Generate a very small flow-chart style PDF with ReportLab
#-----------------------------------------------------------------------
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors

pdf_path = "/home/user/flowchart.pdf"
c        = canvas.Canvas(pdf_path, pagesize=LETTER)
page_w, page_h = LETTER           # 612 × 792 points for US-Letter

# BLOCK 1 – “Start”
c.setStrokeColor(colors.black)
c.setFillColor(colors.lightblue)
c.rect(200, page_h-150, 200, 50, fill=1)
c.setFillColor(colors.black)
c.setFont("Helvetica", 12)
c.drawCentredString(300, page_h-135, "Start")

# Arrow ↓
c.line(300, page_h-150, 300, page_h-200)
c.line(295, page_h-190, 300, page_h-200)
c.line(305, page_h-190, 300, page_h-200)

# BLOCK 2 – “Process”
c.setFillColor(colors.lightgreen)
c.rect(200, page_h-250, 200, 50, fill=1)
c.setFillColor(colors.black)
c.drawCentredString(300, page_h-235, "Process")

# Arrow ↓
c.line(300, page_h-250, 300, page_h-300)
c.line(295, page_h-290, 300, page_h-300)
c.line(305, page_h-290, 300, page_h-300)

# BLOCK 3 – “End”
c.setFillColor(colors.pink)
c.rect(200, page_h-350, 200, 50, fill=1)
c.setFillColor(colors.black)
c.drawCentredString(300, page_h-335, "End")

c.save()
print(f"[initial] Created {pdf_path}")
PY

echo "✓ Initial PDF ready: /home/user/flowchart.pdf"
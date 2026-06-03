#!/usr/bin/env bash
set -euo pipefail
#
# Initial script – builds the baseline PDF exactly at
# /home/user/Projects/engineering_design.pdf
#

# 1. Ensure target directory exists
mkdir -p /home/user/Projects

# 2. Install Python dependencies if missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"    2>/dev/null || pip3 install --user PyPDF2   # PyPDF2 not used here, but keep parity

# 3. Generate the 10-page engineering_design.pdf
python3 <<'PY'
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

pdf_path = "/home/user/Projects/engineering_design.pdf"
c = canvas.Canvas(pdf_path, pagesize=A4)
width, height = A4

for page_num in range(1, 11):
    if page_num == 6:
        # Page 6 – contains the diagram
        c.setFont("Helvetica-Bold", 14)
        c.drawString(180, height - 72, "Page 6: Engineering Diagram")
        # Mock diagram rectangle
        diagram_x, diagram_y = 100, 400
        diagram_w, diagram_h = 400, 300
        c.setStrokeColorRGB(0.2, 0.2, 0.2)
        c.rect(diagram_x, diagram_y, diagram_w, diagram_h, stroke=1, fill=0)
        c.setFont("Helvetica", 12)
        c.drawString(diagram_x + 10, diagram_y + diagram_h - 20, "Diagram: Engine Layout")
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(diagram_x + 10, diagram_y - 20, "(Problem area will be circled in the golden version)")
    else:
        # Generic pages
        c.setFont("Helvetica", 12)
        c.drawString(72, height - 72, f"Engineering Design Document - Page {page_num}")

    c.showPage()

c.save()
PY

echo "Initial PDF created at /home/user/Projects/engineering_design.pdf (10 pages, no annotations)"
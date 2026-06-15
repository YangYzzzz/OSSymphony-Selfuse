#!/usr/bin/env bash
set -euo pipefail
#
# Initial script – creates the source PDF “map.pdf” in /home/user/Downloads
# which will later be “converted” to SVG by the golden script.
#

# 1. Absolute directory & file path extracted verbatim from the task instruction
TARGET_DIR="/home/user/Downloads"
PDF_FILE="/home/user/Downloads/map.pdf"

# 2. Make sure the directory exists
mkdir -p "${TARGET_DIR}"

# 3. Install Python dependencies if they are missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2" 2>/dev/null || pip3 install --user PyPDF2

# 4. Build a deterministic placeholder “map” PDF with ReportLab
python3 <<'PY'
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

pdf_path = "/home/user/Downloads/map.pdf"
c = canvas.Canvas(pdf_path, pagesize=A4)

# Draw a very simple grid-style “map” placeholder
width, height = A4
grid_size = 50
for x in range(0, int(width), grid_size):
    c.line(x, 0, x, height)
for y in range(0, int(height), grid_size):
    c.line(0, y, width, y)

c.setFont("Helvetica-Bold", 24)
c.drawCentredString(width / 2, height - 40, "Sample Map")
c.setFont("Helvetica", 12)
c.drawCentredString(width / 2, 40, "Initial PDF to be converted to SVG")

c.showPage()
c.save()
PY

echo "Initial artifact created:"
echo "  • PDF : ${PDF_FILE}"
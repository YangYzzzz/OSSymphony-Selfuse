#!/usr/bin/env bash
set -euo pipefail
#
# Initial script: create the source multi-page PDF
# File to generate: /home/user/Desktop/presentation.pdf
#

# 1) Make sure the Desktop directory exists
mkdir -p /home/user/Desktop

# 2) Install Python dependencies if they are missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"   2>/dev/null || pip3 install --user PyPDF2

# 3) Build the deterministic 3-page presentation PDF
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

output_path = "/home/user/Desktop/presentation.pdf"
c = canvas.Canvas(output_path, pagesize=LETTER)

slide_titles = ["Slide 1", "Slide 2", "Slide 3"]
w, h = LETTER
for title in slide_titles:
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(w / 2.0, h / 2.0, title)
    c.showPage()
c.save()

print(f"Created {output_path} containing {len(slide_titles)} slides.")
PY

echo "Initial PDF ready: /home/user/Desktop/presentation.pdf"
#!/usr/bin/env bash
set -euo pipefail
# Initial script – creates the mixed PDF that contains both textual and scanned-style pages
# Target file: /home/user/Desktop/mixed_document.pdf

# 1. Ensure the Desktop directory exists
mkdir -p /home/user/Desktop

# 2. Install python dependencies if they are missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"     2>/dev/null || pip3 install --user PyPDF2

# 3. Build the initial PDF
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors

pdf_path = "/home/user/Desktop/mixed_document.pdf"
c = canvas.Canvas(pdf_path, pagesize=LETTER)
w, h = LETTER

for page in range(1, 21):              # 20 pages total
    if page in range(1, 5) or page in range(16, 21):
        # Textual pages
        c.setFont("Helvetica", 12)
        c.drawString(72, h - 72, f"Textual Content – Page {page}")
        text_obj = c.beginText(72, h - 100)
        text_obj.setFont("Helvetica", 10)
        for i in range(1, 21):
            text_obj.textLine(f"Line {i} of page {page}: deterministic sample text.")
        c.drawText(text_obj)
    else:
        # Simulated scanned pages (filled rectangle, no selectable text)
        c.setFillColor(colors.lightgrey)
        c.rect(50, 100, w - 100, h - 200, fill=1, stroke=0)
    c.showPage()

c.save()
print(f"Created {pdf_path}")
PY

echo "Initial PDF generated at /home/user/Desktop/mixed_document.pdf"
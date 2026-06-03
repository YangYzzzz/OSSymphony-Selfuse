#!/usr/bin/env bash
set -euo pipefail

# Target directory and filenames extracted verbatim from the task instruction
TARGET_DIR="/home/user/Documents"
PDF_PATH="/home/user/Documents/application_filled_scan.pdf"

# Create the directory structure exactly as requested
mkdir -p "$TARGET_DIR"

#--------------------------------------------------------------------
# Install dependencies if they are missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"     2>/dev/null || pip3 install --user PyPDF2
#--------------------------------------------------------------------

# Build a one-page “scanned” form PDF (text only, pretending it was rasterised)
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import datetime

pdf_path = "/home/user/Documents/application_filled_scan.pdf"

c = canvas.Canvas(pdf_path, pagesize=A4)
w, h = A4

# Header
c.setFont("Helvetica-Bold", 16)
c.drawCentredString(w/2, h - 72, "Application Form - Scanned Copy")

# Static field/value pairs
fields = [
    ("Name:", "John Doe"),
    ("Date of Birth:", "1990-01-01"),
    ("Email:", "john.doe@example.com"),
]
c.setFont("Helvetica", 12)
y = h - 144
gap = 28
for label, value in fields:
    c.drawString(72, y, label)
    c.drawString(200, y, value)
    c.line(70, y - 5, w - 70, y - 5)   # underline like a filled-in form
    y -= gap

# Footer
c.setFont("Helvetica-Oblique", 8)
c.drawRightString(w - 72, 36,
                  f"Simulated scan generated {datetime.date.today().isoformat()}")
c.save()
PY

echo "Initial PDF created at: $PDF_PATH"
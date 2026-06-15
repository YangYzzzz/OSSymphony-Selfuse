#!/usr/bin/env bash
set -euo pipefail

# Initial setup script: builds the placeholder redacted PDF exactly where the
# task states it lives – /home/user/Desktop/redacted_report.pdf

# 1. Create the Desktop directory explicitly
mkdir -p /home/user/Desktop

# 2. Install Python dependencies if missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2" 2>/dev/null || pip3 install --user PyPDF2

# 3. Build the initial redacted PDF
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER

pdf_path = "/home/user/Desktop/redacted_report.pdf"

c = canvas.Canvas(pdf_path, pagesize=LETTER)
width, height = LETTER

# Fixed content – deterministic
lines = [
    "Quarterly Financial Overview",
    "",
    "Project: SecretProject",
    "Lead: Alice Johnson",
    "Status: On Schedule",
    "Budget: $5,000,000",
    "",
    "Notes:",
    "All milestones have been met to date. Next review in Q2."
]

# Draw the lines
c.setFont("Helvetica", 12)
leading = 18
for idx, txt in enumerate(lines):
    y = height - 72 - leading * idx
    c.drawString(72, y, txt)

# Overlay black rectangles to simulate redaction (lines 2 and 5 -> idx 2,5)
c.setFillColorRGB(0, 0, 0)
for redacted_idx in (2, 5):
    y = height - 72 - leading * redacted_idx
    # Slightly larger rectangle to cover the full text line
    c.rect(70, y - 3, 410, 15, fill=1, stroke=0)

c.save()
PY

echo "Initial PDF created at /home/user/Desktop/redacted_report.pdf"
#!/usr/bin/env bash
set -euo pipefail

# Task: Create the initial fillable PDF '/home/user/Documents/interactive_form.pdf'

# 1. Ensure target directory exists
mkdir -p /home/user/Documents

# 2. Install dependencies if missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2" 2>/dev/null || pip3 install --user PyPDF2

# 3. Build the fillable PDF with ReportLab
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER

output_path = "/home/user/Documents/interactive_form.pdf"
c = canvas.Canvas(output_path, pagesize=LETTER)

# Title
c.setFont("Helvetica-Bold", 14)
c.drawString(72, 750, "User Information Form")

# Name label and text field
c.setFont("Helvetica", 12)
c.drawString(72, 700, "Name:")
c.acroForm.textfield(
    name="name",
    tooltip="Full Name",
    x=120,
    y=690,
    width=300,
    height=20,
    borderStyle="inset",
    borderWidth=1,
    forceBorder=True,
)

# Newsletter checkbox
c.drawString(72, 650, "Subscribe to newsletter:")
c.acroForm.checkbox(
    name="subscribe",
    tooltip="Subscribe",
    x=220,
    y=640,
    size=15,             # Correct parameter for checkbox size
    borderWidth=1,
    borderStyle="solid",
    checked=False,
)

c.showPage()
c.save()
print(f"Created interactive form at {output_path}")
PY

echo "Initial script finished. File generated: /home/user/Documents/interactive_form.pdf"
#!/usr/bin/env bash
set -euo pipefail

# Absolute directory extracted from task instruction: "on Desktop"
TARGET_DIR="/home/user/Desktop"
INITIAL_PDF="/home/user/Desktop/job_application.pdf"

# Ensure the Desktop directory exists
mkdir -p "${TARGET_DIR}"

# Install dependencies if missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2" 2>/dev/null || pip3 install --user PyPDF2

# Build the blank job application form
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch

output_path = "/home/user/Desktop/job_application.pdf"

c = canvas.Canvas(output_path, pagesize=LETTER)
width, height = LETTER

# Title
c.setFont("Helvetica-Bold", 18)
c.drawCentredString(width / 2.0, height - 1 * inch, "Job Application Form")

# Field labels and AcroForm text fields
c.setFont("Helvetica", 12)
label_x = 1 * inch          # 72 pts
field_x = 2.75 * inch       # where text fields start
start_y = height - 2 * inch
line_gap = 0.6 * inch

fields = [
    ("Name:", "name", ""),
    ("Email:", "email", ""),
    ("Phone:", "phone", ""),
]

for idx, (label, field_name, default) in enumerate(fields):
    y = start_y - idx * line_gap
    c.drawString(label_x, y, label)
    c.acroForm.textfield(
        name=field_name,
        x=field_x,
        y=y - 4,            # Slight down-shift because y is the text baseline
        width=3.5 * inch,
        height=0.3 * inch,
        value=default,
        borderStyle="underlined",
        forceBorder=True,
    )

# Finalize PDF
c.showPage()
c.save()
PY

echo "Created initial blank form: ${INITIAL_PDF}"
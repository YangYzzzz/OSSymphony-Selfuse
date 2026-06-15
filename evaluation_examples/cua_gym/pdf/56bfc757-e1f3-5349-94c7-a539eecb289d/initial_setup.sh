#!/usr/bin/env bash
set -euo pipefail
#
# Creates the *initial* PDF stated in the task instruction:
#   /home/user/Desktop/exam_answer_sheet.pdf
#

# 1. Absolute target directory extracted verbatim from task instruction
TARGET_DIR="/home/user/Desktop"
TARGET_FILE="/home/user/Desktop/exam_answer_sheet.pdf"

# 2. Ensure directory exists
mkdir -p "$TARGET_DIR"

# 3. Install dependencies if missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2" 2>/dev/null || pip3 install --user PyPDF2

# 4. Build the initial PDF (blank answers)
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER

output_path = "/home/user/Desktop/exam_answer_sheet.pdf"

c = canvas.Canvas(output_path, pagesize=LETTER)
width, height = LETTER

# Title
c.setFont("Helvetica-Bold", 16)
c.drawString(72, height - 72, "Exam Answer Sheet")

c.setFont("Helvetica", 12)

# Helper data
options = ["Option 1", "Option 2", "Option 3"]
x_start = 100
x_offset = 150

# Question 1
y1 = height - 120
c.drawString(72, y1, "1. Choose the correct answer:")
for idx, label in enumerate(options):
    x = x_start + idx * x_offset
    c.drawString(x, y1 - 20, label)
    c.acroForm.radio(
        name="q1",
        value=label,
        x=x - 12,
        y=y1 - 28,
        buttonStyle="circle",
        selected=False,
        size=12,
        tooltip=label,
        borderStyle='solid',
        borderWidth=1
    )

# Question 5
y5 = y1 - 120
c.drawString(72, y5, "5. Select the best option:")
for idx, label in enumerate(options):
    x = x_start + idx * x_offset
    c.drawString(x, y5 - 20, label)
    c.acroForm.radio(
        name="q5",
        value=label,
        x=x - 12,
        y=y5 - 28,
        buttonStyle="circle",
        selected=False,
        size=12,
        tooltip=label,
        borderStyle='solid',
        borderWidth=1
    )

c.save()
PY

echo "Initial PDF created at: $TARGET_FILE"
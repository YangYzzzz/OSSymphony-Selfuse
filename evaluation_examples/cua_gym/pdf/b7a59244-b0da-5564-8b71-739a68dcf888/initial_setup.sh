#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------------------
# Initial script: creates a blank shipping label form as
# /home/user/Desktop/shipping_label.pdf
# ------------------------------------------------------------------------------

# 1. Absolute target directory parsed from the task instruction: "on Desktop"
TARGET_DIR="/home/user/Desktop"
mkdir -p "${TARGET_DIR}"

# 2. Install Python dependencies if missing
python3 - <<'PY'
import importlib, subprocess, sys, pathlib

def ensure(pkg):
    try:
        importlib.import_module(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])

for mod in ("reportlab", "PyPDF2"):
    ensure(mod)
PY

# 3. Build the initial blank form PDF
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch

output_path = "/home/user/Desktop/shipping_label.pdf"
c = canvas.Canvas(output_path, pagesize=LETTER)
width, height = LETTER

# Title
c.setFont("Helvetica-Bold", 16)
c.drawString(1 * inch, height - 1 * inch, "Shipping Label Form")

# Field labels
c.setFont("Helvetica", 12)
c.drawString(1 * inch, height - 1.5 * inch, "Sender:")
c.drawString(1 * inch, height - 2.0 * inch, "Recipient:")
c.drawString(1 * inch, height - 2.5 * inch, "Weight:")

# Draw input rectangles
field_w = 4.0 * inch
field_h = 0.35 * inch
base_y = height - 1.6 * inch
for i in range(3):
    c.rect(2.0 * inch, base_y - i * 0.5 * inch, field_w, field_h, stroke=1, fill=0)

# AcroForm text fields so the PDF looks like a form
c.acroForm.textfield(name="sender",
                     tooltip="Sender Address",
                     x=2.0 * inch, y=base_y,
                     width=field_w, height=field_h,
                     borderStyle='inset', forceBorder=True)

c.acroForm.textfield(name="recipient",
                     tooltip="Recipient Address",
                     x=2.0 * inch, y=base_y - 0.5 * inch,
                     width=field_w, height=field_h,
                     borderStyle='inset', forceBorder=True)

c.acroForm.textfield(name="weight",
                     tooltip="Package Weight",
                     x=2.0 * inch, y=base_y - 1.0 * inch,
                     width=field_w, height=field_h,
                     borderStyle='inset', forceBorder=True)

c.showPage()
c.save()
PY

echo "Created /home/user/Desktop/shipping_label.pdf (blank form)"
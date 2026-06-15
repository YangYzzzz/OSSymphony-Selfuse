#!/usr/bin/env bash
set -euo pipefail
#
# Initial script – builds the starting landscape PDF exactly where the task says
# Task text: "Rotate all pages in 'landscape_slides.pdf' on Desktop …"
# → create /home/user/Desktop/landscape_slides.pdf (landscape orientation)

# 1. Make sure the Desktop directory exists
mkdir -p /home/user/Desktop

# 2. Install Python libraries if they are missing
python3 - <<'PY'
import subprocess, sys, importlib.util

def ensure(pkg):
    if importlib.util.find_spec(pkg) is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])

ensure("reportlab")
ensure("PyPDF2")
PY

# 3. Build the landscape PDF with three simple pages
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER, landscape
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

# Absolute path extracted verbatim from task context
output_path = "/home/user/Desktop/landscape_slides.pdf"

# Create a landscape-oriented canvas (we'll use LETTER rotated)
c = canvas.Canvas(output_path, pagesize=landscape(LETTER))

for page_num in range(1, 4):
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(5.5*inch, 4*inch, f"Landscape Slide {page_num}")
    c.setFont("Helvetica", 14)
    c.drawCentredString(5.5*inch, 3*inch,
                        "This is a demo landscape page created for rotation testing.")
    c.showPage()

c.save()
print(f"Created source file at {output_path}")
PY

echo "✅ Initial PDF ready at /home/user/Desktop/landscape_slides.pdf"
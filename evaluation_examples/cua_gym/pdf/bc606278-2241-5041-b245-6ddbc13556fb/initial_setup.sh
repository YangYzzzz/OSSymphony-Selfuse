#!/usr/bin/env bash
set -euo pipefail
#
# Initial script – creates the source PDF exactly as referenced in the task
# Task location wording: "certificate.pdf on Desktop"  ->  /home/user/Desktop/certificate.pdf
#

# Absolute target directory taken literally from the instruction
TARGET_DIR="/home/user/Desktop"
PDF_PATH="/home/user/Desktop/certificate.pdf"

# Ensure the Desktop directory exists (no env-vars allowed)
mkdir -p "$TARGET_DIR"

# Install Python dependencies deterministically if they are absent
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"     2>/dev/null || pip3 install --user PyPDF2

# ---------------------------------------------------------------------
# Build the initial PDF                                                     #
# ---------------------------------------------------------------------
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

pdf_path = "/home/user/Desktop/certificate.pdf"

# Create a simple one-page landscape certificate
c = canvas.Canvas(pdf_path, pagesize=landscape(LETTER))
width, height = landscape(LETTER)

c.setFont("Helvetica-Bold", 36)
c.drawCentredString(width/2, height - 2*inch, "Certificate of Completion")

c.setFont("Helvetica", 16)
c.drawCentredString(width/2, height - 3*inch, "This certifies that")

c.setFont("Helvetica-Bold", 24)
c.drawCentredString(width/2, height - 4*inch, "John Doe")

c.setFont("Helvetica", 16)
c.drawCentredString(width/2, height - 5*inch, "has successfully completed the course.")

# Signature line
c.line(width/2 - 2*inch, height - 6*inch, width/2 + 2*inch, height - 6*inch)
c.setFont("Helvetica", 12)
c.drawCentredString(width/2, height - 6.3*inch, "Director of Training")

c.save()
PY

echo "Initial PDF created at: /home/user/Desktop/certificate.pdf"
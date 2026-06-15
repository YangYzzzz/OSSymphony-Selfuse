#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Initial PDF creation script
# Generates an EMPTY consent form at:
#   /home/user/Documents/Legal/consent_form.pdf
###############################################################################

# Absolute directory extracted from task instruction
TARGET_DIR="/home/user/Documents/Legal"
TARGET_PDF="/home/user/Documents/Legal/consent_form.pdf"

# Create directory structure exactly as requested
mkdir -p "${TARGET_DIR}"

# Install Python dependencies if they are missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"    2>/dev/null || pip3 install --user PyPDF2

# Build the EMPTY consent form
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors

output_path = "/home/user/Documents/Legal/consent_form.pdf"

c = canvas.Canvas(output_path, pagesize=LETTER)
w, h = LETTER

# ---------------------------------------------------------------------------
# Document title
c.setFont("Helvetica-Bold", 16)
c.drawCentredString(w / 2.0, h - 72, "Consent Form")

c.setFont("Helvetica", 12)

# ---------------------------------------------------------------------------
# Date field (blank)
c.drawString(72, h - 120, "Date (YYYY-MM-DD):")
c.acroForm.textfield(
    name="date",
    x=200, y=h - 135,
    width=150, height=20,
    borderStyle="underlined",
    borderWidth=1,
    forceBorder=True,
)

# ---------------------------------------------------------------------------
# Signature field (blank)
c.drawString(72, h - 180, "Signature:")
c.acroForm.textfield(
    name="signature",
    x=200, y=h - 195,
    width=200, height=20,
    borderStyle="underlined",
    borderWidth=1,
    forceBorder=True,
)

# ---------------------------------------------------------------------------
# "I agree" checkbox (unchecked)
c.drawString(72, h - 240, "I agree to the terms and conditions")
c.acroForm.checkbox(
    name="agree",
    x=50, y=h - 248,
    size=14,
    checked=False,
    borderWidth=1,
    buttonStyle="check",
    forceBorder=True,
)

c.showPage()
c.save()
PY

# ---------------------------------------------------------------------------
# Small summary
echo "Created: ${TARGET_PDF}"
python3 - <<'PY'
from PyPDF2 import PdfReader
path = "/home/user/Documents/Legal/consent_form.pdf"
pages = len(PdfReader(path).pages)
print(f"Pages : {pages}")
PY
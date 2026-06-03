#!/usr/bin/env bash
set -euo pipefail
#
# Initial script
# Creates a low–resolution-looking PDF “old_manuscript.pdf” in
# /home/user/Archives.  No OCR is performed here – this is the
# “before” state the golden script will work on.
#

# 1. Absolute task directory
TARGET_DIR="/home/user/Archives"

# 2. Ensure directory exists
mkdir -p "$TARGET_DIR"

# 3. Dependency guard – install ReportLab / PyPDF2 if missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"     2>/dev/null || pip3 install --user PyPDF2

# 4. Create the low-resolution style PDF with ReportLab
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
import random, textwrap, pathlib, datetime

pdf_path = pathlib.Path("/home/user/Archives/old_manuscript.pdf")
c = canvas.Canvas(str(pdf_path), pagesize=LETTER)

# Simulate a faded, low-dpi scan: light gray text, monospaced font, small size
c.setFillGray(0.35)            # light text
c.setFont("Courier", 9)        # small, typewriter feel

margin = 0.75 * inch
width, height = LETTER
usable_width  = width  - 2 * margin
usable_height = height - 2 * margin

# Sample deterministic “antique” paragraph
paragraph = (
    "This is a facsimile of an aged manuscript, "
    "intended solely for OCR demonstration purposes. "
    "All spellings and punctuation are preserved exactly "
    "as in the source text."
)

wrapped_lines = textwrap.wrap(paragraph, width=70)
y = height - margin
for line in wrapped_lines:
    y -= 12
    c.drawString(margin, y, line)

# Add stub footer with a fixed date for determinism
c.setFont("Courier-Oblique", 7)
c.drawString(margin, 0.5 * inch,
             f"Scanned copy – {datetime.date.today().isoformat()} — 100 DPI placeholder")
c.save()
PY

echo "Initial PDF created:"
echo " - /home/user/Archives/old_manuscript.pdf"
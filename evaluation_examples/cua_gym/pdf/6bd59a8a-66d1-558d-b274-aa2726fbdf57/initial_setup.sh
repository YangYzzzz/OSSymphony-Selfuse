#!/usr/bin/env bash
set -euo pipefail

# -----------------------------------------------------------------------------
# Initial Script: build the starting PDFs exactly as described in the task
# Creates:
#   • /home/user/Desktop/report.pdf          (20-page source document)
#   • /home/user/Desktop/corrected_page.pdf  (1-page replacement for page 8)
# -----------------------------------------------------------------------------

# 1. Absolute target directory extracted literally from the task instruction
TARGET_DIR="/home/user/Desktop"
mkdir -p "$TARGET_DIR"

# 2. Ensure dependencies are present
python3 - <<'PY'
import sys, subprocess, importlib.util
for pkg in ("reportlab", "PyPDF2"):
    if importlib.util.find_spec(pkg) is None:  # install only if missing
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])
PY

# 3. Generate the 20-page report.pdf
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER

output_path = "/home/user/Desktop/report.pdf"
c = canvas.Canvas(output_path, pagesize=LETTER)

for page_num in range(1, 21):  # 1 .. 20
    text = f"Report – Page {page_num} of 20"
    c.setFont("Helvetica-Bold", 18)
    width, height = LETTER
    text_width = c.stringWidth(text, "Helvetica-Bold", 18)
    c.drawString((width - text_width) / 2, height / 2, text)
    c.showPage()

c.save()
PY

# 4. Generate the single-page corrected_page.pdf
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER

output_path = "/home/user/Desktop/corrected_page.pdf"
c = canvas.Canvas(output_path, pagesize=LETTER)

msg = "Corrected Content for Page 8"
c.setFont("Helvetica-Bold", 18)
width, height = LETTER
text_width = c.stringWidth(msg, "Helvetica-Bold", 18)
c.drawString((width - text_width) / 2, height / 2, msg)
c.save()
PY

echo "Initial PDFs created in /home/user/Desktop:"
echo "  - report.pdf (20 pages)"
echo "  - corrected_page.pdf (1 page)"
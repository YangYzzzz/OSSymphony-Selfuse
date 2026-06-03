#!/usr/bin/env bash
set -euo pipefail
#
# Initial script – creates a placeholder PDF that represents the yet-to-be-converted
# LibreOffice presentation.  The PDF is written exactly to:
#   /home/user/Desktop/slides_print.pdf
#

# 1. Absolute target path extracted verbatim from task instruction
TARGET_DIR="/home/user/Desktop"
TARGET_PDF="/home/user/Desktop/slides_print.pdf"

# 2. Ensure the directory exists
mkdir -p "${TARGET_DIR}"

# 3. Install Python dependencies deterministically if they are missing
python3 - <<'PY' 2>/dev/null
import sys, subprocess, importlib.util
for pkg in ("reportlab", "PyPDF2"):
    if importlib.util.find_spec(pkg) is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])
PY

# 4. Create a minimal placeholder PDF with ReportLab
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER

pdf_path = "/home/user/Desktop/slides_print.pdf"
c = canvas.Canvas(pdf_path, pagesize=LETTER)
c.setAuthor("Automation Stub")
c.setTitle("slides_print.pdf – pending conversion")
c.setFont("Helvetica-Bold", 16)
c.drawString(72, 720, "slides_print.pdf")
c.setFont("Helvetica", 12)
c.drawString(72, 700, "Placeholder file.")
c.drawString(72, 685, "The LibreOffice presentation 'slides.odp' still needs to be converted.")
c.save()
PY

echo "Initial placeholder PDF created at ${TARGET_PDF}"
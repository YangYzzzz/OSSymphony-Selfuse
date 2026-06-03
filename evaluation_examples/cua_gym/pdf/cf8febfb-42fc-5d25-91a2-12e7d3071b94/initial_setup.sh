#!/usr/bin/env bash
set -euo pipefail
# Initial setup script that creates placeholder “scanned” PDFs
# Target paths come DIRECTLY from the task instruction – no env vars!

# Absolute directories extracted from the task
SCAN_DIR="/home/user/Documents/Scanned_Archive"

# 1. Ensure the directory exists
mkdir -p "${SCAN_DIR}"

# 2. Install Python libraries if they are missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"     2>/dev/null || pip3 install --user PyPDF2

# 3. Create two deterministic, image-only placeholder PDFs
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os, random

random.seed(42)                              # deterministic “noise”
scan_dir = "/home/user/Documents/Scanned_Archive"
files = ["scan_01.pdf", "scan_02.pdf"]

for fname in files:
    path = os.path.join(scan_dir, fname)
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    # Simulate a noisy scan background so extracted-text == None
    for _ in range(600):                    # light grey dots
        x = random.randint(0, int(width))
        y = random.randint(0, int(height))
        c.setFillGray(0.9)
        c.circle(x, y, 0.7, stroke=0, fill=1)

    # Render a rasterised “SCANNED” banner (still text for demo)
    c.setFillGray(0.3)
    c.setFont("Helvetica-Bold", 48)
    c.drawCentredString(width/2, height/2, "SCANNED DOCUMENT")

    c.showPage()
    c.save()
PY

echo "Initial (non-searchable) PDFs created in: ${SCAN_DIR}"
ls -1 "${SCAN_DIR}"
#!/usr/bin/env bash
set -euo pipefail

# -----------------------------------------------------------------------------
# Initial script for "peer_review.pdf"
# Location extracted from task instruction: /home/user/Desktop/peer_review.pdf
# -----------------------------------------------------------------------------

TARGET_DIR="/home/user/Desktop"
TARGET_FILE="/home/user/Desktop/peer_review.pdf"

# 1. Create directory structure
mkdir -p "${TARGET_DIR}"

# 2. Install dependencies if missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"    2>/dev/null || pip3 install --user PyPDF2

# 3. Build an initial 20-page PDF using ReportLab
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

pdf_path = "/home/user/Desktop/peer_review.pdf"

c = canvas.Canvas(pdf_path, pagesize=LETTER)
width, height = LETTER

for page_num in range(1, 21):          # 20 pages
    c.setFont("Helvetica-Bold", 14)
    c.drawString(72, height - 72, f"Peer Review Report – Page {page_num}")
    c.setFont("Helvetica", 11)
    c.drawString(72, height - 100,
                 "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                 "Curabitur vitae semper sapien. Suspendisse potenti.")
    c.showPage()

c.save()
PY

echo "Initial PDF created at: ${TARGET_FILE}"
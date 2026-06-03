#!/usr/bin/env bash
set -euo pipefail

# Absolute target directory extracted from task instruction
TARGET_DIR="/home/user/Documents"
DRAFT_PDF="${TARGET_DIR}/draft_report.pdf"

# 1. Create the target directory
mkdir -p "${TARGET_DIR}"

# 2. Install dependencies if missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"    2>/dev/null || pip3 install --user PyPDF2

# 3. Build the initial PDF (draft_report.pdf) with 15 pages
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

file_path = "/home/user/Documents/draft_report.pdf"
c = canvas.Canvas(file_path, pagesize=A4)

for page_num in range(1, 16):            # 15 deterministic pages
    c.drawString(72, 800, f"Draft Report - Page {page_num}")
    c.showPage()

c.save()
print(f"✓ Created {file_path} with 15 pages.")
PY

echo "Initial PDF ready at ${DRAFT_PDF}"
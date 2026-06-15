#!/usr/bin/env bash
set -euo pipefail

# Target directory and filenames extracted verbatim from the task instruction
TARGET_DIR="/home/user/Documents"
ORIGINAL_PDF="/home/user/Documents/scanned_document.pdf"

# 1. Ensure directory exists
mkdir -p "${TARGET_DIR}"

# 2. Install Python dependencies if missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"     2>/dev/null || pip3 install --user PyPDF2  # (needed by the golden script)

# 3. Build the initial PDF
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER

output_path = "/home/user/Documents/scanned_document.pdf"
c = canvas.Canvas(output_path, pagesize=LETTER)

for page_num in range(1, 9):           # 8-page sample file
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(LETTER[0] / 2.0,
                        LETTER[1] / 2.0,
                        f"Scanned Document Page {page_num}")
    c.showPage()

c.save()
print(f"Created {output_path} with {page_num} pages.")
PY

echo "Initial script complete: generated ${ORIGINAL_PDF}"
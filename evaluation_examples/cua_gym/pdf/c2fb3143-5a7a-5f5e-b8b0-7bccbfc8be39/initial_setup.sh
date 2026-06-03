#!/usr/bin/env bash
set -euo pipefail

# Target directory and filenames extracted verbatim from task instruction
TARGET_DIR="/home/user/Books"
SCANNED_PDF="/home/user/Books/book_scanned.pdf"
BLANK_PNG="/home/user/Books/blank.png"

# Create directory structure
mkdir -p "${TARGET_DIR}"

# Install dependencies if missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2" 2>/dev/null || pip3 install --user PyPDF2

# Build a 1-pixel PNG that will be stretched to fill each PDF page
python3 <<'PY'
import base64, pathlib, textwrap
png_b64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAA"
    "AAC0lEQVR42mP8/x8AAwMCAO++n3cAAAAASUVORK5CYII="
)
path = pathlib.Path("/home/user/Books/blank.png")
path.write_bytes(base64.b64decode(png_b64))
PY

# Create the scanned (image-only) PDF
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

pdf_path = "/home/user/Books/book_scanned.pdf"
img_path = "/home/user/Books/blank.png"
c = canvas.Canvas(pdf_path, pagesize=A4)

# Two pages of “scanned” content consisting only of images
for page_no in range(1, 3):
    c.drawImage(img_path, 0, 0, width=A4[0], height=A4[1])
    c.showPage()
c.save()
PY

echo "Initial PDF created:"
echo "  • ${SCANNED_PDF}"
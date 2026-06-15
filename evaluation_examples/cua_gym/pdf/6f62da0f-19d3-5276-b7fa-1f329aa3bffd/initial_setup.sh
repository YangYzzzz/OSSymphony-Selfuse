#!/usr/bin/env bash
set -euo pipefail
#
# Initial script – creates a multi-page TIFF and a placeholder PDF
#   TIFF  : /home/user/Downloads/scanned_document.tiff   (3 demo pages)
#   PDF   : /home/user/Downloads/scanned_document.pdf    (1-page “pending” stub)
#

# 1) Absolute paths extracted verbatim from the task instruction
TARGET_DIR="/home/user/Downloads"
TIFF_FILE="/home/user/Downloads/scanned_document.tiff"
PDF_FILE="/home/user/Downloads/scanned_document.pdf"

# 2) Ensure the target directory exists
mkdir -p "$TARGET_DIR"

# 3) Install run-time dependencies when missing
python3 - <<'PY'
import subprocess, sys, importlib

def ensure(pkg):
    try:
        importlib.import_module(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])

for lib in ("reportlab", "PyPDF2", "Pillow"):
    ensure(lib)
PY

# 4) Create a deterministic 3-page demo TIFF so later conversion has something to work with
python3 <<'PY'
from PIL import Image, ImageDraw

tiff_path = "/home/user/Downloads/scanned_document.tiff"

pages = []
for idx in range(1, 4):
    img = Image.new("RGB", (600, 800), "white")
    draw = ImageDraw.Draw(img)
    # Pillow ≥10.0: avoid deprecated .textsize – we just pick fixed coords
    draw.text((50, 50), f"Scanned Page {idx}", fill="black")
    pages.append(img)

pages[0].save(tiff_path, save_all=True, append_images=pages[1:])
print(f"Created multi-page TIFF with {len(pages)} pages -> {tiff_path}")
PY

# 5) Generate a 1-page placeholder PDF that signals “conversion pending”
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

pdf_path = "/home/user/Downloads/scanned_document.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=LETTER)
styles = getSampleStyleSheet()
story = [
    Spacer(1, 200),
    Paragraph("Conversion Pending", styles["Title"]),
    Spacer(1, 24),
    Paragraph(
        "This PDF is a placeholder. The golden script will replace it with the fully "
        "converted multi-page document.", styles["Normal"]
    ),
]
doc.build(story)
print(f"Created stub PDF -> {pdf_path}")
PY

echo "Initial setup complete:"
echo "  • /home/user/Downloads/scanned_document.tiff"
echo "  • /home/user/Downloads/scanned_document.pdf (placeholder)"
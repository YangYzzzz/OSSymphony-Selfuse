#!/usr/bin/env bash
set -euo pipefail
#
# Task   : Produce the “scanned” input PDF
# Target : /home/user/Desktop/slides_scan.pdf
# NOTE   : Creates three placeholder slide-images, embeds them as full-page
#          bitmaps so the PDF has *no* text layer (simulating a scanner dump)
#

###############################################################################
# 1. Install dependencies (ReportLab, PyPDF2, Pillow) if they are missing
###############################################################################
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2" 2>/dev/null || pip3 install --user PyPDF2
python3 -c "import PIL" 2>/dev/null || pip3 install --user pillow

###############################################################################
# 2. Ensure the Desktop directory exists exactly as referenced in the task
###############################################################################
mkdir -p /home/user/Desktop

###############################################################################
# 3. Build the scanned-style PDF
###############################################################################
python3 <<'PY'
import os
from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER

desktop_dir = "/home/user/Desktop"
scan_pdf     = os.path.join(desktop_dir, "slides_scan.pdf")

# ---------------------------------------------------------------------------
# Create three simple “scanned” slide images (PNG, 300 DPI 8.5x11 -> 2550×3300)
# ---------------------------------------------------------------------------
image_paths = []
for idx in range(1, 4):
    img = Image.new("RGB", (2550, 3300), "white")
    draw = ImageDraw.Draw(img)
    # A fixed position keeps code simple; we *do not* call draw.textsize()
    draw.text((300, 400), f"Slide {idx}", fill="black")
    pth = os.path.join(desktop_dir, f"slide_{idx}.png")
    img.save(pth, format="PNG")
    image_paths.append(pth)

# ---------------------------------------------------------------------------
# Embed each bitmap as an entire page so the PDF has *no* selectable text
# ---------------------------------------------------------------------------
c = canvas.Canvas(scan_pdf, pagesize=LETTER)
page_w, page_h = LETTER
for img_pth in image_paths:
    c.drawImage(img_pth, 0, 0, width=page_w, height=page_h)
    c.showPage()
c.save()
PY

echo "✅ Created /home/user/Desktop/slides_scan.pdf (3 pages, image-only)"
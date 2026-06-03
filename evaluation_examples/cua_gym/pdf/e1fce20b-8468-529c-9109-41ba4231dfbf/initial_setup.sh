#!/usr/bin/env bash
set -euo pipefail
#
# Initial setup script
# Creates sample catalog PDFs (each embedding two PNG pictures) in
# /home/user/Documents/Catalogs – the directory explicitly mentioned
# in the task instruction.
#
# No extraction happens here; that belongs to the golden script.

# -----------------------------------------------------------------------------
# 1. Install runtime Python dependencies if they are missing
# -----------------------------------------------------------------------------
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"   2>/dev/null || pip3 install --user PyPDF2
python3 -c "import PIL"      2>/dev/null || pip3 install --user Pillow

# -----------------------------------------------------------------------------
# 2. Make sure the exact directory from the instructions exists
# -----------------------------------------------------------------------------
mkdir -p /home/user/Documents/Catalogs

# -----------------------------------------------------------------------------
# 3. Generate deterministic sample assets & PDFs
# -----------------------------------------------------------------------------
python3 <<'PY'
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from PIL import Image, ImageDraw, ImageFont

catalog_dir = "/home/user/Documents/Catalogs"

# Two small catalog files, each containing two product images
for catalog_idx in (1, 2):
    # -------------------------------------------------------------------------
    # Create PNG images on-disk so ReportLab can embed them
    # -------------------------------------------------------------------------
    image_paths = []
    for img_idx in (1, 2):
        img_path = os.path.join(
            catalog_dir, f"product{catalog_idx}_{img_idx}.png"
        )
        image_paths.append(img_path)

        img = Image.new("RGB", (200, 200),
                        color=(40 * catalog_idx, 60 * img_idx, 180))
        draw = ImageDraw.Draw(img)
        # Pillow ≥10: avoid deprecated textsize(); draw simple label instead
        draw.text((10, 90),
                  f"Item {catalog_idx}-{img_idx}",
                  fill=(255, 255, 255),
                  font=ImageFont.load_default())
        img.save(img_path)

    # -------------------------------------------------------------------------
    # Build the PDF itself
    # -------------------------------------------------------------------------
    pdf_path = os.path.join(catalog_dir, f"catalog{catalog_idx}.pdf")
    c = canvas.Canvas(pdf_path, pagesize=LETTER)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(72, 750, f"Catalog {catalog_idx}")

    y_cursor = 500
    for img_path in image_paths:
        c.drawImage(img_path, 72, y_cursor, width=200, height=200)
        y_cursor -= 250  # spacing between pictures

    c.showPage()
    c.save()

print("Sample catalog PDFs created in:", catalog_dir)
PY

echo "INITIAL SCRIPT COMPLETE – PDFs are ready."
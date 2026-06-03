#!/usr/bin/env bash
# Initial script: create a *scanned* multilingual PDF made of images only
# File: /home/user/Desktop/multilingual_notice.pdf
# The PDF is image-only and therefore NOT searchable

set -euo pipefail

# Absolute directory extracted literally from the task instruction
TARGET_DIR="/home/user/Desktop"
TARGET_PDF="/home/user/Desktop/multilingual_notice.pdf"

# Create the Desktop directory if it does not already exist
mkdir -p "$TARGET_DIR"

# Install Python dependencies if missing
python3 - <<'PY'
import subprocess, sys, importlib

def ensure(pkg):
    try:
        importlib.import_module(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])

for p in ("reportlab", "PyPDF2", "Pillow"):
    ensure(p)
PY

# --------------------------------------------------------------------
# Create the image-only (scanned) PDF
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

from PIL import Image, ImageDraw, ImageFont
import io, os, textwrap

output_path = "/home/user/Desktop/multilingual_notice.pdf"
page_w, page_h = A4

# Use a commonly present Truetype font that supports basic Latin + CJK characters
ttf_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font = ImageFont.truetype(ttf_path, 24)

entries = [
    ("English", "Important Notice:\nThe office will be closed tomorrow."),
    ("Español",  "Aviso Importante:\nLa oficina permanecerá cerrada mañana."),
    ("中文",       "通知：\n本办公室明天关闭。"),
]

c = canvas.Canvas(output_path, pagesize=A4)

for lang, text in entries:
    # Produce a white image with the text rendered on it (simulating a scan)
    img = Image.new("RGB", (int(page_w), int(page_h)), "white")
    draw = ImageDraw.Draw(img)

    # Header
    draw.text((60, 60), f"{lang}", font=font, fill="black")

    # Body with simple wrapping
    y = 120
    for para in text.split("\n"):
        for line in textwrap.wrap(para, width=40):
            draw.text((60, y), line, font=font, fill="black")
            y += 40
        y += 20

    # Convert the PIL image to a ReportLab-compatible object
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    bio.seek(0)

    c.drawImage(ImageReader(bio), 0, 0, width=page_w, height=page_h)
    c.showPage()

c.save()
print(f"[initial] Created scanned PDF at {output_path}")
PY

echo "[initial] Done – generated /home/user/Desktop/multilingual_notice.pdf (image-only, non-searchable)"
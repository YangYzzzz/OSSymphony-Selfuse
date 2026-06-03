#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------------------
# Initial script: creates the starting PDF (whitepaper.pdf) and the watermark
# image (logo.png) exactly in /home/user/Desktop
# ------------------------------------------------------------------------------

# 1. Hard-coded absolute output directory extracted from task text
TARGET_DIR="/home/user/Desktop"
mkdir -p "${TARGET_DIR}"

# 2. Ensure required Python libraries are present
python3 - <<'PY'
import subprocess, sys, importlib.util, json, textwrap, pathlib, os

def ensure(pkg):
    try:
        importlib.import_module(pkg)
    except ModuleNotFoundError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])

for p in ("reportlab", "PyPDF2", "Pillow"):
    ensure(p)
PY

# 3. Build supporting asset: logo.png
python3 <<'PY'
from PIL import Image, ImageDraw, ImageFont
import pathlib, os

out_dir = pathlib.Path("/home/user/Desktop")
logo_path = out_dir / "logo.png"

# deterministic 100×40 blue rectangle with white "LOGO" text
img = Image.new("RGBA", (100, 40), (0, 102, 204, 255))
draw = ImageDraw.Draw(img)
# Draw the word "LOGO" near the left side; Pillow ≥10 still supports ImageDraw.text
draw.text((10, 10), "LOGO", fill=(255, 255, 255, 255))
img.save(logo_path)
print(f"Created {logo_path}")
PY

# 4. Create the initial whitepaper.pdf
python3 <<'PY'
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
import pathlib

target_file = pathlib.Path("/home/user/Desktop/whitepaper.pdf")
doc = SimpleDocTemplate(str(target_file), pagesize=A4,
                        leftMargin=72, rightMargin=72,
                        topMargin=72, bottomMargin=72)

styles = getSampleStyleSheet()
story = []

# Minimal deterministic content across 2 pages
for page_num in range(1, 3):
    story.append(Paragraph(f"Whitepaper – Page {page_num}", styles["Title"]))
    story.append(Spacer(1, 24))
    body_text = (
        "This is a sample white-paper used for a watermarking automation demo. "
        "All pages will receive a company branding image in the golden version."
    )
    story.append(Paragraph(body_text, styles["BodyText"]))
    if page_num == 1:
        story.append(PageBreak())

doc.build(story)
print(f"Created {target_file}")
PY

echo "Initial files ready:"
echo "  - /home/user/Desktop/logo.png"
echo "  - /home/user/Desktop/whitepaper.pdf"
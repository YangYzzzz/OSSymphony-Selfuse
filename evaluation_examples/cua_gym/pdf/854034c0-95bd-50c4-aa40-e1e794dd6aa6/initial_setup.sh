#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Initial script                                                              #
# Creates a “scanned / non-searchable” exam PDF at                            #
#              /home/user/Teaching/student_exam.pdf                           #
# along with the raster images that simulate the scan.                        #
###############################################################################

#--------------------------------------------------------------------
# 1. Make sure Python dependencies are present
#--------------------------------------------------------------------
python3 -c "import reportlab" 2>/dev/null  || pip3 install --user reportlab
python3 -c "import PyPDF2"   2>/dev/null  || pip3 install --user PyPDF2
python3 -c "import PIL"      2>/dev/null  || pip3 install --user Pillow   # Pillow supplies PIL

#--------------------------------------------------------------------
# 2. Create target directory from absolute path in task instruction
#--------------------------------------------------------------------
mkdir -p /home/user/Teaching

#--------------------------------------------------------------------
# 3. Build the raster pages and assemble the PDF
#--------------------------------------------------------------------
python3 <<'PY'
import os
from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

out_dir      = "/home/user/Teaching"
pdf_path     = "/home/user/Teaching/student_exam.pdf"

questions = [
    ("Question 1: What is 2 + 2?",                       "Answer: 4"),
    ("Question 2: Write the chemical symbol for water.", "Answer: H2O"),
    ("Question 3: State Newton's second law.",           "Answer: F = m * a"),
]

page_paths = []
w_px, h_px = 595, 842                     # ≈ A4 @ 72 dpi

for idx, (q, a) in enumerate(questions, start=1):
    img_path = f"{out_dir}/page{idx}.png"
    page_paths.append(img_path)

    img  = Image.new("RGB", (w_px, h_px), "white")
    draw = ImageDraw.Draw(img)
    draw.multiline_text((40, 40), f"{q}\n{a}", fill="black")
    img.save(img_path)

# Assemble non-searchable PDF (image–only pages)
c = canvas.Canvas(pdf_path, pagesize=A4)
W, H = A4
for img_path in page_paths:
    c.drawImage(img_path, 0, 0, width=W, height=H)   # full-page raster
    c.showPage()
c.save()

print(f"Created non-searchable scanned PDF: {pdf_path}")
PY

echo "Initial artefacts:"
echo "  • /home/user/Teaching/student_exam.pdf"
echo "  • /home/user/Teaching/page1.png – page3.png"
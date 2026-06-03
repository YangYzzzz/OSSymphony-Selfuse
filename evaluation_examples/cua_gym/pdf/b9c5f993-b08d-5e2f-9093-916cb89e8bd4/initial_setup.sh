#!/usr/bin/env bash
set -euo pipefail
#
# Initial PDF setup script
# Creates /home/user/Books/book_scan.pdf with 10 pages.
# Pages 5‒8 contain a dummy table-of-contents section that we will
# “OCR” (i.e. text-extract) in the golden script.
#

#--------------------------------------------------------------------
# 1. Make sure required libraries are present
#--------------------------------------------------------------------
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"    2>/dev/null || pip3 install --user PyPDF2

#--------------------------------------------------------------------
# 2. Ensure target directory exists
#--------------------------------------------------------------------
mkdir -p /home/user/Books

#--------------------------------------------------------------------
# 3. Build the initial PDF
#--------------------------------------------------------------------
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch

pdf_path = "/home/user/Books/book_scan.pdf"

c = canvas.Canvas(pdf_path, pagesize=LETTER)
toc_lines = [
    "Chapter 1: Introduction.............................................1",
    "Chapter 2: Literature Review......................................15",
    "Chapter 3: Methodology............................................35",
    "Chapter 4: Results................................................58",
    "Chapter 5: Discussion..............................................80",
    "Chapter 6: Conclusion..............................................95",
]

for page_no in range(1, 11):            # 10 pages total
    c.setFont("Times-Roman", 12)
    c.drawString(inch, 10*inch, f"Page {page_no}")

    # Insert TOC on pages 5-8
    if 5 <= page_no <= 8:
        y = 9*inch
        for line in toc_lines:
            c.drawString(inch, y, line)
            y -= 0.3*inch

    c.showPage()

c.save()
print(f"Initial PDF created at {pdf_path}")
PY

#--------------------------------------------------------------------
# 4. Summary
#--------------------------------------------------------------------
echo "Assets generated:"
ls -l /home/user/Books/book_scan.pdf
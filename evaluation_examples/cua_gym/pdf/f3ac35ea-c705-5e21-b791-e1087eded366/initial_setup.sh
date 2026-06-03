#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Initial script: create a starter PDF named “catalog.pdf” exactly at
# /home/user/Documents/Sales/catalog.pdf
#
# The document will contain three simple pages that act as a realistic
# “catalog” placeholder.  No image conversion is done here – that work is
# reserved for the golden script.
###############################################################################

# 1. Ensure the target directory from the task instruction exists
mkdir -p /home/user/Documents/Sales

# 2. Install Python dependencies if they are missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"    2>/dev/null || pip3 install --user PyPDF2

# 3. Build the starter PDF with ReportLab
python3 <<'PY'
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

pdf_path = "/home/user/Documents/Sales/catalog.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=A4)
styles = getSampleStyleSheet()

story = []
for i in range(1, 4):        # produce 3 deterministic pages
    story.append(Paragraph(f"Catalog – Page {i}", styles["Heading1"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        styles["Normal"],
    ))
    if i < 3:                # avoid trailing PageBreak
        story.append(PageBreak())

doc.build(story)
print(f"Created starter PDF at {pdf_path}")
PY

# 4. Summarise
echo "Initial setup complete:"
ls -lh /home/user/Documents/Sales/catalog.pdf
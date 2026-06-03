#!/usr/bin/env bash
set -euo pipefail

# -----------------------------------------------------------------------------
# Initial setup script
# Creates the technical specification PDF
# Path extracted verbatim from task instruction:
#   /home/user/Projects/Documentation/specs_v2.3.pdf
# -----------------------------------------------------------------------------

# 1. Ensure target directory exists
mkdir -p /home/user/Projects/Documentation

# 2. Install Python PDF dependencies if missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"    2>/dev/null || pip3 install --user PyPDF2

# 3. Build the initial PDF with headers, footers, and page numbers
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER

pdf_path = "/home/user/Projects/Documentation/specs_v2.3.pdf"

c = canvas.Canvas(pdf_path, pagesize=LETTER)
width, height = LETTER

header_text = "Technical Specification v2.3"
footer_template = lambda page_num: f"Confidential – Company Internal – Page {page_num}"

# Two-page deterministic sample content
contents = [
    [
        "1. Introduction",
        "This document outlines the technical specifications of the Delta Series microcontroller family.",
        "2. Electrical Characteristics",
        "Operating voltage range: 1.8V to 5.5V.",
        "Current consumption in active mode: 5 mA."
    ],
    [
        "3. Memory",
        "Flash memory: 256 KB.",
        "SRAM: 32 KB.",
        "4. Peripherals",
        "UART, SPI, I2C, ADC, DAC.",
        "End of Specification."
    ]
]

for page_num, lines in enumerate(contents, start=1):
    # Header
    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, height - 50, header_text)
    # Body
    c.setFont("Helvetica", 10)
    y = height - 80
    for line in lines:
        c.drawString(72, y, line)
        y -= 14
    # Footer with page number
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(72, 40, footer_template(page_num))
    c.showPage()

c.save()
PY

echo "Initial PDF created at /home/user/Projects/Documentation/specs_v2.3.pdf"
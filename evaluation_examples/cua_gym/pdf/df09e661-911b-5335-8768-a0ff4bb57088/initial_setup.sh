#!/usr/bin/env bash
set -euo pipefail
#
# Initial script – builds the “plain” PDF that the user later wants
# to convert / make editable.  The file must be created exactly at
# /home/user/Desktop/invoice_template.pdf
#

# 1. Create target directory exactly as extracted from the task
mkdir -p /home/user/Desktop

# 2. Make sure Python libs are available
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"    2>/dev/null || pip3 install --user PyPDF2

# 3. Generate the PDF
python3 <<'PY'
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas

output_path = "/home/user/Desktop/invoice_template.pdf"
c = canvas.Canvas(output_path, pagesize=A4)
width, height = A4

# --- Static invoice layout (non-editable) ---------------------------
c.setFont("Helvetica-Bold", 18)
c.drawString(40, height - 60, "INVOICE")

c.setFont("Helvetica", 10)
c.drawString(40, height - 90, "Seller:")
c.drawString(40, height - 105, "ACME Corporation")
c.drawString(40, height - 120, "123 Business Rd.")
c.drawString(40, height - 135, "Metropolis, CA 90210")

c.drawString(350, height - 90, "Invoice #:")
c.drawString(350, height - 105, "0001")
c.drawString(350, height - 120, "Date:")
c.drawString(350, height - 135, "2024-01-01")

# Table headings
y_start = height - 180
c.setFont("Helvetica-Bold", 10)
c.drawString(40, y_start, "Description")
c.drawString(300, y_start, "Qty")
c.drawString(350, y_start, "Unit Price")
c.drawString(450, y_start, "Line Total")

c.line(40, y_start-5, 550, y_start-5)

# One example line item
c.setFont("Helvetica", 10)
c.drawString(40, y_start-25, "Widget")
c.drawRightString(330, y_start-25, "4")
c.drawRightString(420, y_start-25, "$25.00")
c.drawRightString(550, y_start-25, "$100.00")

# Total
c.setFont("Helvetica-Bold", 10)
c.drawString(350, y_start-80, "TOTAL:")
c.drawRightString(550, y_start-80, "$100.00")

c.save()
PY

echo "Created /home/user/Desktop/invoice_template.pdf"
#!/usr/bin/env bash
set -euo pipefail
#
# Initial set-up script.
# Creates /home/user/Documents/Sales/service_catalog.pdf with a pricing
# table on page-3.  No Excel extraction is done here – that happens in
# the golden script.
#

# --------------------------------------------------------------------
# 1. Ensure target directory exists
# --------------------------------------------------------------------
mkdir -p /home/user/Documents/Sales

# --------------------------------------------------------------------
# 2. Make sure ReportLab & PyPDF2 are available
# --------------------------------------------------------------------
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"     2>/dev/null || pip3 install --user PyPDF2

# --------------------------------------------------------------------
# 3. Build the initial PDF
# --------------------------------------------------------------------
python3 <<'PY'
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
)

pdf_path = "/home/user/Documents/Sales/service_catalog.pdf"

doc    = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    leftMargin=72, rightMargin=72,
    topMargin=72,  bottomMargin=72,
)
styles = getSampleStyleSheet()
story  = []

# ---------- Page-1 ---------------------------------------------------
story.append(Paragraph("Service Catalog", styles["Title"]))
story.append(Spacer(1, 2 * inch))
story.append(Paragraph("Acme Corp", styles["Heading2"]))
story.append(PageBreak())

# ---------- Page-2 ---------------------------------------------------
story.append(Paragraph("Our Services", styles["Heading1"]))
lorem = (
    "We provide a comprehensive suite of cloud-based solutions covering "
    "infrastructure, platform, and software services. This catalog outlines "
    "all pricing tiers and service descriptions."
)
story.append(Spacer(1, 12))
story.append(Paragraph(lorem, styles["Normal"]))
story.append(PageBreak())

# ---------- Page-3  (Pricing Table) ---------------------------------
story.append(Paragraph("Pricing Table", styles["Heading1"]))
story.append(Spacer(1, 12))

pricing_table = [
    ["Plan",     "Monthly", "$",  "Annual", "$"],  # header line
    ["Basic",    "$10",     "",   "$100",   ""],
    ["Standard", "$20",     "",   "$200",   ""],
    ["Premium",  "$30",     "",   "$300",   ""],
]

# Use only three visual columns inside the PDF
visual_table_data = [
    ["Plan", "Monthly", "Annual"],
    ["Basic", "$10", "$100"],
    ["Standard", "$20", "$200"],
    ["Premium", "$30", "$300"],
]

tbl = Table(visual_table_data, colWidths=[2 * inch, 1.5 * inch, 1.5 * inch])
tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9D9D9")),
    ("ALIGN",      (1, 1), (-1, -1), "CENTER"),
    ("GRID",       (0, 0), (-1, -1), 0.5, colors.grey),
    ("FONTSIZE",   (0, 0), (-1, -1), 10),
]))
story.append(tbl)
story.append(PageBreak())

# ---------- Page-4 ---------------------------------------------------
story.append(Paragraph("Contact", styles["Heading1"]))
story.append(Spacer(1, 12))
story.append(Paragraph(
    "For custom plans please e-mail sales@acme.example.com.", styles["Normal"]
))

doc.build(story)
print(f"Created initial PDF at {pdf_path}")
PY

echo "Initial script finished: /home/user/Documents/Sales/service_catalog.pdf created."
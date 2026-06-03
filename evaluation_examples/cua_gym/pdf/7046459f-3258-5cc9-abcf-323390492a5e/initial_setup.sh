#!/usr/bin/env bash
set -euo pipefail
#
# Initial script
# Creates the starting PDF “financial_report.pdf” on the Desktop.
# No CSV extraction is performed here.
#

# 1. Install dependencies if they are missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"    2>/dev/null || pip3 install --user PyPDF2

# 2. Deterministic absolute path extracted from the task instruction
TARGET_DIR="/home/user/Desktop"
PDF_PATH="/home/user/Desktop/financial_report.pdf"

# 3. Make sure the directory exists
mkdir -p "${TARGET_DIR}"

# 4. Build the initial PDF
python3 <<'PY'
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

pdf_path = "/home/user/Desktop/financial_report.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                        rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=72)

styles = getSampleStyleSheet()
story  = []

# Pages 1–7: simple placeholder pages
for i in range(1, 8):
    story.append(Paragraph(f"Financial Report – Page {i}", styles["Heading2"]))
    story.append(Spacer(1, 500))
    story.append(PageBreak())

# Page 8: the table we will later extract
story.append(Paragraph("Quarterly Results", styles["Heading1"]))
story.append(Spacer(1, 12))

data = [
    ["Quarter", "Revenue", "Profit"],
    ["Q1 2024", "$100,000", "$15,000"],
    ["Q2 2024", "$110,000", "$17,000"],
    ["Q3 2024", "$105,000", "$16,000"],
    ["Q4 2024", "$115,000", "$18,000"],
]
tbl = Table(data, colWidths=[100, 120, 120])
tbl.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#F0F0F0")),
    ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
    ("ALIGN",      (1,1), (-1,-1), "RIGHT"),
]))
story.append(tbl)

doc.build(story)
PY

# 5. Summary
echo "✅ Created initial PDF: ${PDF_PATH}"
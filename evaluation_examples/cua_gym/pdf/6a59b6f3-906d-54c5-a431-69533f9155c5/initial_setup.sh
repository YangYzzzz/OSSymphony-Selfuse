#!/usr/bin/env bash
set -euo pipefail
# Initial script: create /home/user/Research/statistical_analysis.pdf
# (18-page dummy report; page 18 contains a correlation matrix table)

# Absolute directory path extracted from task instruction
TARGET_DIR="/home/user/Research"
PDF_PATH="/home/user/Research/statistical_analysis.pdf"

# Ensure directory exists
mkdir -p "$TARGET_DIR"

# Install dependencies if missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2" 2>/dev/null || pip3 install --user PyPDF2

# Build the initial PDF -------------------------------------------------------
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted
from reportlab.lib.styles import getSampleStyleSheet

pdf_path = "/home/user/Research/statistical_analysis.pdf"
styles = getSampleStyleSheet()
doc = SimpleDocTemplate(pdf_path, pagesize=LETTER,
                        rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=72)

story = []
# Pages 1-17: simple placeholders
for i in range(1, 18):
    story.append(Paragraph(f"Statistical Analysis Report – Page {i}", styles["Heading2"]))
    story.append(Spacer(1, 600))
    story.append(PageBreak())

# Page 18: correlation matrix in CSV-ready text
story.append(Paragraph("Correlation Matrix", styles["Heading2"]))
matrix_text = """,Var1,Var2,Var3
Var1,1.0,0.5,-0.2
Var2,0.5,1.0,0.3
Var3,-0.2,0.3,1.0
"""
story.append(Spacer(1, 12))
story.append(Preformatted(matrix_text, styles["Code"]))

doc.build(story)
PY
# ---------------------------------------------------------------------------

echo "Created PDF: $PDF_PATH (18 pages, matrix on page 18)"
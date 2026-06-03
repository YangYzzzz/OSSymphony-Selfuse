#!/usr/bin/env bash
set -euo pipefail
#
# Initial script
# Builds the baseline PDF mentioned in the task instruction.
# Target file: /home/user/Desktop/legal_document.pdf
#

# 1. Ensure the target directory exists (DO NOT use env vars)
mkdir -p /home/user/Desktop

# 2. Install dependencies if they are missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"    2>/dev/null || pip3 install --user PyPDF2

# 3. Build the initial PDF via embedded Python
python3 <<'PY'
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

pdf_path = Path("/home/user/Desktop/legal_document.pdf")

# --- Compose a small but realistic legal-style document ---
doc  = SimpleDocTemplate(str(pdf_path), pagesize=A4,
                         leftMargin=72, rightMargin=72,
                         topMargin=72, bottomMargin=72)

styles = getSampleStyleSheet()
story  = []

paragraphs = [
    "IN THE SUPERIOR COURT OF EXAMPLE COUNTY\nSTATE OF EXAMPLAND",
    "This Agreement (the “Agreement”) is made and entered into on this 1st day of January, 2024, by and between Alpha Corp. (\"Party A\") and Beta LLC (\"Party B\").",
    "WHEREAS, Party A is engaged in the business of providing exemplary goods and services; and",
    "WHEREAS, Party B desires to purchase such goods and services under the terms and conditions set forth herein;",
    "NOW, THEREFORE, in consideration of the mutual covenants and promises contained herein, the parties agree as follows:",
    "1. Term. — The term of this Agreement shall commence on the Effective Date and continue for a period of one (1) year.",
    "2. Governing Law. — This Agreement shall be governed by and construed in accordance with the laws of the State of Exampland.",
    "IN WITNESS WHEREOF, the parties hereto have executed this Agreement as of the date first above written."
]

for text in paragraphs:
    story.append(Paragraph(text.replace("\n", "<br/>"), styles["Normal"]))
    story.append(Spacer(1, 12))

doc.build(story)
PY

echo "Initial PDF created at /home/user/Desktop/legal_document.pdf"
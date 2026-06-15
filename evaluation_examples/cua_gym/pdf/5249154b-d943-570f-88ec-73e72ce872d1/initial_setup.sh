#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# Initial PDF creation script
# Builds /home/user/Desktop/quarterly_report.pdf WITHOUT any header
# ============================================================================

# 1) Absolute directory extracted verbatim from task instruction
TARGET_DIR="/home/user/Desktop"
INITIAL_PDF_PATH="/home/user/Desktop/quarterly_report.pdf"

# 2) Ensure target directory exists
mkdir -p "${TARGET_DIR}"

# 3) Install Python dependencies if they are missing
python3 - <<'PY'
import sys, subprocess, importlib.util, json, textwrap, os
def ensure(pkg):
    if importlib.util.find_spec(pkg) is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])
for p in ("reportlab", "PyPDF2"):
    ensure(p)
PY

# 4) Generate the initial PDF using ReportLab
python3 <<'PY'
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
import os

pdf_path = "/home/user/Desktop/quarterly_report.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                        rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=72)
styles = getSampleStyleSheet()
story = []

# Title
story.append(Paragraph("Quarterly Report", styles["Title"]))
story.append(Spacer(1, 24))

# Three deterministic pages of sample content
lorem = ("This is sample body content for the quarterly report. "
         "It is repeated multiple times to fill pages and make the "
         "document span three pages for demonstration purposes. ")

for i in range(3):
    story.append(Paragraph(f"Section {i+1}", styles["Heading2"]))
    for _ in range(5):
        story.append(Paragraph(lorem, styles["Normal"]))
        story.append(Spacer(1, 12))
    if i < 2:  # add PageBreak after first two pages
        story.append(PageBreak())

doc.build(story)
print(f"Created initial PDF at {pdf_path}")
PY

echo "✔ Initial PDF generated: ${INITIAL_PDF_PATH}"
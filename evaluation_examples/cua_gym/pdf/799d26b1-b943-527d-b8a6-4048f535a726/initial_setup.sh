#!/usr/bin/env bash
set -euo pipefail
#
# Initial script: creates the baseline PDF
# File: /home/user/Research/literature_review.pdf
#

#--------------------------------------------------------------------
# 1. Make sure the target directory from the task instruction exists
#--------------------------------------------------------------------
mkdir -p /home/user/Research

#--------------------------------------------------------------------
# 2. Install dependencies (ReportLab + PyPDF2) if they are missing
#--------------------------------------------------------------------
python3 - <<'PY'
import importlib, subprocess, sys, pathlib

def ensure(pkg):
    try:
        importlib.import_module(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])

for package in ("reportlab", "PyPDF2"):
    ensure(package)
PY

#--------------------------------------------------------------------
# 3. Build the initial PDF with 10 pages (last 5 are “References”)
#--------------------------------------------------------------------
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch

output_path = "/home/user/Research/literature_review.pdf"

doc  = SimpleDocTemplate(output_path, pagesize=LETTER,
                         leftMargin=72, rightMargin=72,
                         topMargin=72, bottomMargin=72)
styles = getSampleStyleSheet()
story  = []

# Five content pages -------------------------------------------------
for i in range(1, 6):
    story.append(Paragraph(f"Literature Review – Section {i}", styles["Heading1"]))
    for _ in range(3):
        story.append(
            Paragraph(
                ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 5).strip(),
                styles["Normal"],
            )
        )
        story.append(Spacer(1, 0.25 * inch))
    story.append(PageBreak())

# Five references pages ---------------------------------------------
for i in range(1, 6):
    story.append(Paragraph(f"References Page {i}", styles["Heading1"]))
    for j in range(1, 6):
        story.append(
            Paragraph(
                f"[{j}] A. Author. “Sample Paper Title {j}”. Journal of Examples, 20{10+j}.",
                styles["Normal"],
            )
        )
        story.append(Spacer(1, 0.15 * inch))
    if i < 5:
        story.append(PageBreak())

doc.build(story)
print(f"Created initial PDF at {output_path}")
PY

echo "✅ Initial PDF written to /home/user/Research/literature_review.pdf"
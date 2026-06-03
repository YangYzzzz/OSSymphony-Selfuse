#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Initial script – builds the “raw” PDF that still contains footnote markers  #
# Target files (MUST match task wording exactly):                             #
#   • /home/user/clinical_trial.pdf                                           #
###############################################################################

# 1. Install Python dependencies when missing
python3 - <<'PY'
import importlib, subprocess, sys

def ensure(pkg: str) -> None:
    try:
        importlib.import_module(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])

for _pkg in ("reportlab", "PyPDF2"):
    ensure(_pkg)
PY

# 2. Make sure the directory from the task instruction exists
mkdir -p /home/user

# 3. Build the PDF with the table that contains footnote markers
python3 <<'PY'
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

pdf_path = "/home/user/clinical_trial.pdf"

doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                        leftMargin=50, rightMargin=50,
                        topMargin=50, bottomMargin=50)

styles = getSampleStyleSheet()
story = [Paragraph("Clinical Trial Results (with footnote markers)",
                   styles["Heading2"]),
         Spacer(1, 12)]

# Table data WITH footnote markers (*, †, ‡, §, ¶)
table_data = [
    ["Group", "Patients", "Response Rate", "Adverse Events"],
    ["Placebo*", "50†", "12%‡", "Mild"],
    ["Drug A§", "48¶", "35%", "Moderate"],
]

tbl = Table(table_data, colWidths=[90, 90, 120, 120])
tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9E1F2")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
    ("ALIGN", (1, 1), (-1, -1), "CENTER"),
]))
story.append(tbl)
story.append(Spacer(1, 12))
story.append(Paragraph(
    "* Placebo; † Number of enrolled patients; ‡ Overall response rate; "
    "§ Investigational product; ¶ Indicates patients who completed the study",
    styles["Normal"]))

doc.build(story)
PY

echo "✓ Created /home/user/clinical_trial.pdf with footnote markers"
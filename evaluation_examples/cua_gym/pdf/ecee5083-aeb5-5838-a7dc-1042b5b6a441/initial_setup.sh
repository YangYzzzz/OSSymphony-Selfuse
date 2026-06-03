#!/usr/bin/env bash
set -euo pipefail
#
# Creates an example PDF called “survey_results.pdf” that contains
# a merged-cell table on page 4.  This represents the “initial state”
# the user starts with.
#

# 1) Install dependencies when missing
python3 - <<'PY'
import importlib.util, subprocess, sys, json, textwrap, os
pkgs = {"reportlab": "reportlab", "PyPDF2": "PyPDF2"}
for _mod, _pip in pkgs.items():
    if importlib.util.find_spec(_mod) is None:               # not installed yet
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", _pip])
PY

# 2) Build the PDF exactly as requested
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors

# Output path comes straight from the task instruction (no extra env vars)
pdf_path = "survey_results.pdf"

doc    = SimpleDocTemplate(pdf_path, pagesize=LETTER,
                           leftMargin=40, rightMargin=40,
                           topMargin=40, bottomMargin=40)
styles = getSampleStyleSheet()
story  = []

# Pages 1-3: simple filler text so that the real table sits on page 4
for page_no in range(1, 4):
    story.append(Paragraph(f"Survey Results – Page {page_no}", styles["Title"]))
    story.append(Spacer(1, 650))        # push everything to next page
    story.append(PageBreak())

# Page 4 – merged-cell table
story.append(Paragraph("Survey Response Breakdown", styles["Title"]))
story.append(Spacer(1, 16))

data = [
    # header row: merge “Responses” across three columns
    ["Question", "Responses", "", ""],
    ["The product is easy to use",     "10", "15", "5"],
    ["Would recommend to others",      "12", "14", "4"],
]

tbl = Table(data, colWidths=[180, 80, 80, 80])
tbl.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),
    ("SPAN", (1, 0), (3, 0)),                 # merged header cell
    ("ALIGN", (1, 1), (-1, -1), "CENTER"),
]))
story.append(tbl)

doc.build(story)
PY

echo "Initial PDF created at: $(pwd)/survey_results.pdf"
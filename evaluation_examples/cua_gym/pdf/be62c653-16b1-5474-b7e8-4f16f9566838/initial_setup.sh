#!/usr/bin/env bash
set -euo pipefail
#
# INITIAL SET-UP  ──────────────────────────────────────────────────────────────
# Builds the research paper  /home/user/Research/experimental_data.pdf
# containing two deterministic tables.  No CSV extraction is done here.
#

# -----------------------------------------------------------------------------#
# 1. Create target directory extracted verbatim from task instruction
# -----------------------------------------------------------------------------#
mkdir -p /home/user/Research

# -----------------------------------------------------------------------------#
# 2. Ensure Python dependencies exist
# -----------------------------------------------------------------------------#
python3 - <<'PY'
import sys, subprocess, importlib.util, pathlib, textwrap, os
def ensure(pkg):
    if importlib.util.find_spec(pkg) is None:          # not installed
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])
for p in ("reportlab", "PyPDF2"):
    ensure(p)
PY

# -----------------------------------------------------------------------------#
# 3. Build the initial PDF with two small tables
# -----------------------------------------------------------------------------#
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

pdf_path = "/home/user/Research/experimental_data.pdf"

doc     = SimpleDocTemplate(pdf_path, pagesize=LETTER,
                            leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
styles  = getSampleStyleSheet()
story   = []

# Title -----------------------------------------------------------------------
story.append(Paragraph("Experimental Data", styles["Title"]))
story.append(Spacer(1, 18))

# ---------- Table 1 ----------------------------------------------------------
data1 = [["Sample", "Temp (°C)", "Pressure (kPa)"],
         ["A",      "25",        "101"],
         ["B",      "30",        "099"]]

story.append(Paragraph("Table 1: Environmental Conditions", styles["Heading2"]))
t1 = Table(data1, colWidths=[120, 120, 120])
t1.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E0E0E0")),
    ("GRID",       (0, 0), (-1, -1), 0.50, colors.black),
]))
story.extend([t1, Spacer(1, 18)])

# ---------- Table 2 ----------------------------------------------------------
data2 = [["Run", "Voltage (V)", "Current (mA)"],
         ["1",   "5",           "10"],
         ["2",   "5",           "12"],
         ["3",   "5",           "11"]]

story.append(Paragraph("Table 2: Electrical Measurements", styles["Heading2"]))
t2 = Table(data2, colWidths=[120, 120, 120])
t2.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E0E0E0")),
    ("GRID",       (0, 0), (-1, -1), 0.50, colors.black),
]))
story.append(t2)

doc.build(story)
PY

echo "✓ Created /home/user/Research/experimental_data.pdf (2 tables)"
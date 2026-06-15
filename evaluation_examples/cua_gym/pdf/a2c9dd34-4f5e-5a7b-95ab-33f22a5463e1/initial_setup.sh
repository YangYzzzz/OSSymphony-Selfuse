#!/usr/bin/env bash
set -euo pipefail
#
# INITIAL SCRIPT
# Creates the source PDF “patient_chart.pdf” on the Desktop.
# No extraction is done here – we just set up the file that the golden
# script will later read.
#

# Absolute target directory & filenames (taken literally from instructions)
TARGET_DIR="/home/user/Desktop"
PDF_PATH="/home/user/Desktop/patient_chart.pdf"

# 1. Ensure the directory exists
mkdir -p "${TARGET_DIR}"

# 2. Make sure Python dependencies are available
python3 - <<'PY'
import subprocess, sys
def ensure(pkg):
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])
for p in ("reportlab", "PyPDF2"):
    ensure(p)
PY

# 3. Build the PDF with a clear “Medication Schedule” table
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

FILE_PATH = "/home/user/Desktop/patient_chart.pdf"

doc = SimpleDocTemplate(
    FILE_PATH,
    pagesize=LETTER,
    rightMargin=72, leftMargin=72,
    topMargin=72, bottomMargin=72,
)
styles = getSampleStyleSheet()
story = []

# Header
story.append(Paragraph("Patient Chart", styles["Title"]))
story.append(Spacer(1, 12))

# Medication Schedule section
story.append(Paragraph("Medication Schedule", styles["Heading2"]))
story.append(Spacer(1, 12))

data = [
    ["Medication", "Dosage", "Frequency", "Start Date", "End Date"],
    ["Aspirin", "100 mg", "Daily", "2023-01-01", "2023-01-31"],
    ["Metformin", "500 mg", "Twice Daily", "2023-02-01", "2023-06-01"],
    ["Lisinopril", "10 mg", "Daily", "2023-03-15", "2023-09-15"],
]
table = Table(data, colWidths=[80, 60, 80, 80, 80])
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D3D3D3")),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("ALIGN", (1, 1), (-1, -1), "CENTER"),
]))
story.append(table)
story.append(Spacer(1, 12))

# Explicit end-marker so the golden script can isolate the table reliably
story.append(Paragraph("End Medication Schedule", styles["Normal"]))

doc.build(story)
PY

echo "Initial PDF created at: ${PDF_PATH}"
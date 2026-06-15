#!/usr/bin/env bash
set -euo pipefail
#
# Creates the starting PDF for the task:
#   /home/user/Desktop/report.pdf
#

# -----------------------------------------------------------------------------
# 1. Ensure destination directory exists (exact absolute path from instruction)
# -----------------------------------------------------------------------------
mkdir -p /home/user/Desktop

# -----------------------------------------------------------------------------
# 2. Install Python dependencies if they are missing
# -----------------------------------------------------------------------------
python3 - <<'PY'
import subprocess, sys, importlib.util, pkg_resources, json, textwrap, os, pathlib, sysconfig
def ensure(pkg):
    if importlib.util.find_spec(pkg) is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])
for p in ("reportlab","PyPDF2"):
    ensure(p)
PY

# -----------------------------------------------------------------------------
# 3. Build the initial PDF using ReportLab
# -----------------------------------------------------------------------------
python3 <<'PY'
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch

output_path = "/home/user/Desktop/report.pdf"

doc = SimpleDocTemplate(output_path, pagesize=A4,
                        leftMargin=72, rightMargin=72, topMargin=72, bottomMargin=72)

styles = getSampleStyleSheet()
story  = []

# Page 1
story.append(Paragraph("Quarterly Report", styles["Title"]))
story.append(Spacer(1, 0.25 * inch))
story.append(Paragraph("Prepared by: Analytics Department", styles["Normal"]))
story.append(Spacer(1, 0.15 * inch))
story.append(Paragraph(
    "This document summarizes the key performance indicators and financial "
    "results for the previous quarter. All data is presented in USD unless "
    "otherwise noted.", styles["BodyText"]))
story.append(PageBreak())

# Page 2
story.append(Paragraph("Key Metrics", styles["Heading1"]))
metrics = [
    ("Revenue Growth", "7.5%"),
    ("Operating Margin", "22.1%"),
    ("Customer Churn", "3.2%"),
    ("Net Promoter Score", "64"),
]
for k, v in metrics:
    story.append(Paragraph(f"<b>{k}:</b> {v}", styles["Normal"]))
    story.append(Spacer(1, 0.1 * inch))

doc.build(story)
print(f"Created {output_path}")
PY

# -----------------------------------------------------------------------------
# 4. Summary
# -----------------------------------------------------------------------------
echo "Initial PDF created at /home/user/Desktop/report.pdf"
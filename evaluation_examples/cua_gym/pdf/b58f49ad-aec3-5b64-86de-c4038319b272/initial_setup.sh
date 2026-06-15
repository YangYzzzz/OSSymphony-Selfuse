#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Initial script
# Creates the baseline PDF: /home/user/Projects/project_plan.pdf
# Page-6 contains a deterministic “Project Timeline” table so that
# the golden script can later extract it.
###############################################################################

# 1. Ensure the target directory from the task instruction exists
mkdir -p /home/user/Projects

# 2. Install PDF dependencies if they are missing
python3 - <<'PY'
import sys, subprocess, importlib.util, pkg_resources, json, os

def ensure(pkg):
    if importlib.util.find_spec(pkg) is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])

# Mandatory libs
ensure("reportlab")
ensure("PyPDF2")

PY

# 3. Build the initial PDF with six pages
python3 <<'PY'
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                PageBreak, Table, TableStyle)
from reportlab.lib import colors

pdf_path = "/home/user/Projects/project_plan.pdf"

doc = SimpleDocTemplate(pdf_path, pagesize=A4)
styles = getSampleStyleSheet()
story = []

# Pages 1-5 : filler content
for i in range(1, 6):
    story.append(Paragraph(f"Project Plan – Section {i}", styles["Heading2"]))
    for j in range(3):
        story.append(
            Paragraph(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                "Integer nec odio. Praesent libero. Sed cursus ante dapibus diam.",
                styles["Normal"],
            )
        )
        story.append(Spacer(1, 12))
    story.append(PageBreak())

# Page-6 : project timeline table
story.append(Paragraph("Project Timeline", styles["Heading2"]))
table_data = [
    ["Phase", "Start", "End", "Owner"],
    ["Planning", "2024-01-01", "2024-01-15", "Alice"],
    ["Design", "2024-01-16", "2024-02-15", "Bob"],
    ["Implementation", "2024-02-16", "2024-04-30", "Charlie"],
    ["Testing", "2024-05-01", "2024-05-31", "Dana"],
]

tbl = Table(table_data, colWidths=[100, 100, 100, 100])
tbl.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ]
    )
)
story.append(tbl)

doc.build(story)
print(f"Created initial PDF at {pdf_path}")
PY

echo "Initial PDF generated: /home/user/Projects/project_plan.pdf (6 pages)"
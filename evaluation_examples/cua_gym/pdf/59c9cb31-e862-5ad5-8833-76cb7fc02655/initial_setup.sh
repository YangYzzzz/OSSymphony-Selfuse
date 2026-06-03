#!/usr/bin/env bash
set -euo pipefail
#
# Initial state builder for the research paper PDF mentioned in the task
# This script creates /home/user/Desktop/manuscript.pdf with placeholder content.

# 1. Ensure the exact directory extracted from the task exists
mkdir -p /home/user/Desktop

# 2. Install dependencies if missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"    2>/dev/null || pip3 install --user PyPDF2

# 3. Build the initial PDF
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

output_path = "/home/user/Desktop/manuscript.pdf"

doc     = SimpleDocTemplate(output_path, pagesize=LETTER,
                            leftMargin=72, rightMargin=72,
                            topMargin=72, bottomMargin=72)
styles  = getSampleStyleSheet()
story   = []

# Title & Abstract
story.append(Paragraph("Research Paper Manuscript", styles["Title"]))
story.append(Spacer(1, 24))
story.append(Paragraph(
    "Abstract: This placeholder abstract outlines the content of the research paper. "
    "It will be elaborated in future drafts.",
    styles["Normal"]
))
story.append(PageBreak())

# Five deterministic placeholder sections
lorem = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
         "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
         "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris "
         "nisi ut aliquip ex ea commodo consequat.")
for i in range(1, 6):
    story.append(Paragraph(f"Section {i}", styles["Heading2"]))
    story.append(Paragraph(lorem, styles["Normal"]))
    story.append(Spacer(1, 12))

doc.build(story)
PY

# 4. Summarise
bytes_count=$(stat -c%s /home/user/Desktop/manuscript.pdf)
echo "Initial PDF created at /home/user/Desktop/manuscript.pdf (${bytes_count} bytes)"
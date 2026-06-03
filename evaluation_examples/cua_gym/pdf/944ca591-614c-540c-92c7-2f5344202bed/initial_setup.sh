#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------------------
# Initial PDF builder for: /home/user/Desktop/preliminary_results.pdf
# This script creates a multi-page “preliminary_results.pdf” WITHOUT any draft
# footer/annotation.  It purposefully represents the *pre-task* state.
# ------------------------------------------------------------------------------

# 1) Ensure the target directory exists
mkdir -p /home/user/Desktop

# 2) Install Python dependencies if they are missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"    2>/dev/null || pip3 install --user PyPDF2

# 3) Build the initial PDF (no footer) via embedded Python
python3 <<'PY'
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

output_path = "/home/user/Desktop/preliminary_results.pdf"

doc  = SimpleDocTemplate(output_path, pagesize=A4,
                         leftMargin=72, rightMargin=72,
                         topMargin=72,  bottomMargin=72)

styles = getSampleStyleSheet()
story  = []

# Deterministic sample content: 2 pages, each with identical body text
body_text = (
    "This is the preliminary analysis of our experimental results. "
    "The figures and tables included herein are subject to change upon "
    "further peer review and validation. "
    "Therefore, distribution outside the core project team is discouraged."
)

for page_num in range(2):
    story.append(Paragraph(f"Section {page_num + 1}", styles["Heading2"]))
    story.append(Spacer(1, 12))
    # Repeat the body text a few times to fill each page
    for _ in range(5):
        story.append(Paragraph(body_text, styles["Normal"]))
        story.append(Spacer(1, 12))
    if page_num == 0:  # Add a page break after the first page
        story.append(PageBreak())

doc.build(story)
print(f"Initial PDF created at: {output_path}")
PY

echo "DONE — generated /home/user/Desktop/preliminary_results.pdf (no footer)"
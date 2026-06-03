#!/usr/bin/env bash
set -euo pipefail

# Absolute directory extracted from task: /home/user/Desktop
TARGET_DIR="/home/user/Desktop"
INITIAL_PDF="/home/user/Desktop/duplex_scan.pdf"

# Create the Desktop directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Install dependencies if missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2" 2>/dev/null || pip3 install --user PyPDF2

# ----------------------------------------------------------------------
# Build the initial duplex_scan.pdf (10-page dummy scan)
# ----------------------------------------------------------------------
python3 <<'PY'
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

output_path = "/home/user/Desktop/duplex_scan.pdf"
styles = getSampleStyleSheet()
doc = SimpleDocTemplate(output_path, pagesize=A4)

story = []
for page_num in range(1, 11):          # 10 pages
    story.append(Paragraph(f"Duplex Scan – Page {page_num}", styles["Title"]))
    story.append(Spacer(1, 500))
    if page_num < 10:
        story.append(PageBreak())

doc.build(story)
print(f"Created initial PDF with {len(story)//3 + 1} pages at {output_path}")
PY

echo "Initial PDF generated at: $INITIAL_PDF"
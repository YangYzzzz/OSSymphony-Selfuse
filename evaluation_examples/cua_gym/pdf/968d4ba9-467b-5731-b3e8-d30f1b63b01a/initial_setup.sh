#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Initial PDF creator
# Creates /home/user/Documents/Marketing/marketing_plan.pdf without any
# header/footer so the golden script can later enhance it.
###############################################################################

TARGET_DIR="/home/user/Documents/Marketing"
INITIAL_PDF="/home/user/Documents/Marketing/marketing_plan.pdf"

echo "Creating initial PDF at: $INITIAL_PDF"

# Install dependencies if missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2" 2>/dev/null || pip3 install --user PyPDF2

# Ensure target directory exists
mkdir -p "$TARGET_DIR"

###############################################################################
# Generate initial PDF (3-page dummy marketing plan)
###############################################################################
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

output_path = "/home/user/Documents/Marketing/marketing_plan.pdf"
doc = SimpleDocTemplate(output_path, pagesize=LETTER,
                        rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=72)

styles = getSampleStyleSheet()
story = []
# Deterministic plain content – no header/footer
sections = [
    ("Executive Summary", "This section summarizes the marketing objectives for 2025 "
                          "and sets the context for all subsequent initiatives."),
    ("Target Audience", "A detailed breakdown of demographic and psychographic factors "
                        "informing the campaign focus."),
    ("Channels & Tactics", "Overview of digital, print, and experiential channels "
                           "that will be leveraged throughout 2025."),
]
for title, body in sections:
    story.append(Paragraph(title, styles["Heading1"]))
    story.append(Spacer(1, 12))
    # repeat body text to fill at least one page
    for _ in range(15):
        story.append(Paragraph(body, styles["Normal"]))
        story.append(Spacer(1, 6))
    story.append(PageBreak())

# Remove last PageBreak for cleanliness
if isinstance(story[-1], PageBreak):
    story.pop()

doc.build(story)
print(f"Initial PDF written to {output_path}")
PY

echo "Initial PDF generation complete."
echo "File created: $INITIAL_PDF"
#!/usr/bin/env bash
# Initial script: creates the starting PDF "/home/user/Desktop/workshop_slides.pdf"
#                (no text-extraction yet)
set -euo pipefail

# Absolute paths derived literally from task instruction
TARGET_DIR="/home/user/Desktop"
PDF_PATH="/home/user/Desktop/workshop_slides.pdf"

# Ensure dependencies are present
python3 - <<'PY' 2>/dev/null || pip3 install --user reportlab
import reportlab
PY
python3 - <<'PY' 2>/dev/null || pip3 install --user PyPDF2
import PyPDF2
PY

# Create the Desktop directory if it does not exist
mkdir -p "$TARGET_DIR"

# ---------------------------------------------------------------------------
# Build a deterministic 5-slide handout PDF
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

output = "/home/user/Desktop/workshop_slides.pdf"
doc = SimpleDocTemplate(output, pagesize=LETTER, rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=72)

styles = getSampleStyleSheet()
story = []

slide_titles = [
    "Welcome & Introduction",
    "Project Goals",
    "Methodology Overview",
    "Results & Discussion",
    "Next Steps & Q&A",
]

for idx, title in enumerate(slide_titles, start=1):
    story.append(Paragraph(f"Slide {idx}: {title}", styles["Heading1"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        "Suspendisse potenti. Integer non eros et justo suscipit "
        "porttitor sit amet nec arcu.", styles["Normal"]
    ))
    if idx != len(slide_titles):
        story.append(PageBreak())

doc.build(story)
print(f"Created {output}")
PY
# ---------------------------------------------------------------------------

echo "Initial setup complete – generated: $PDF_PATH"
#!/usr/bin/env bash
set -euo pipefail

# Absolute PDF path extracted verbatim from task instruction
TARGET_DIR="/home/user/Documents/Projects"
TARGET_PDF="/home/user/Documents/Projects/development_notes.pdf"

# 1. Create output directory
mkdir -p "${TARGET_DIR}"

# 2. Install Python dependencies if missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"    2>/dev/null || pip3 install --user PyPDF2

# 3. Build the initial (plain, un-highlighted) PDF
python3 <<'PY'
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# Absolute output path must match shell variable value exactly
output_path = "/home/user/Documents/Projects/development_notes.pdf"

doc = SimpleDocTemplate(output_path, pagesize=A4,
                        rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=72)

styles = getSampleStyleSheet()
story = []

paragraphs = [
    "Project Roadmap",
    "1. TODO: Refactor the authentication module for better security.",
    "2. The API integration phase has been completed. Status: DONE.",
    "3. Remember to write unit tests for the payment flow. TODO for next sprint.",
    "4. Documentation updates are DONE and reviewed by the QA team.",
]

for line in paragraphs:
    story.append(Paragraph(line, styles["Normal"]))
    story.append(Spacer(1, 12))

doc.build(story)
PY

# 4. Summary
actual_size=$(stat --printf="%s" "${TARGET_PDF}")
echo "Initial PDF created at ${TARGET_PDF} (${actual_size} bytes)"
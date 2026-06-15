#!/usr/bin/env bash
set -euo pipefail
#
# Initial script: create the starting PDF that lives
# on the Desktop exactly as referenced in the task instruction
# (“german_document.pdf on Desktop”).
#

# Absolute paths extracted verbatim from the task wording
TARGET_DIR="/home/user/Desktop"
PDF_PATH="/home/user/Desktop/german_document.pdf"

# Create the directory structure exactly as required
mkdir -p "${TARGET_DIR}"

# Install dependencies if they are missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"     2>/dev/null || pip3 install --user PyPDF2

# Build the initial German-language PDF
python3 <<'PY'
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import os

pdf_path = "/home/user/Desktop/german_document.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                        leftMargin=72, rightMargin=72,
                        topMargin=72, bottomMargin=72)

styles = getSampleStyleSheet()
story = []

# German sample content
german_paragraphs = [
    "Dies ist ein Beispieltext in deutscher Sprache.",
    "Wir erstellen dieses PDF, um eine spätere OCR-Extraktion zu demonstrieren.",
    "Die Genauigkeit wird verbessert, wenn ein spezielles deutschsprachiges Modell verwendet wird."
]

for p in german_paragraphs:
    story.append(Paragraph(p, styles["Normal"]))
    story.append(Spacer(1, 12))

doc.build(story)

print(f"Initial PDF created at: {pdf_path}")
PY

echo "Summary:"
echo "  • Created PDF: ${PDF_PATH}"
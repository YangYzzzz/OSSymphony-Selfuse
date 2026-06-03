#!/usr/bin/env bash
set -euo pipefail

# ABSOLUTE TARGET DIRECTORY (extracted verbatim from task instruction)
TARGET_DIR="/home/user/Documents/JobApplications"

# Ensure the directory exists exactly as written in the task instruction
mkdir -p "$TARGET_DIR"

# Install dependencies if missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2" 2>/dev/null || pip3 install --user PyPDF2

################################################################################
# Build the initial PDFs – stand-in files before the requested merge happens
################################################################################
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import os

TARGET_DIR = "/home/user/Documents/JobApplications"
os.makedirs(TARGET_DIR, exist_ok=True)

styles = getSampleStyleSheet()

def make_doc(path, heading):
    doc = SimpleDocTemplate(path, pagesize=LETTER,
                            leftMargin=72, rightMargin=72,
                            topMargin=72, bottomMargin=72)
    story = [
        Paragraph(heading, styles["Heading1"]),
        Spacer(1, 24),
        Paragraph("This is a deterministic placeholder document generated "
                  "by the initial setup script. It will be replaced by a "
                  "merged version in the golden script.", styles["Normal"])
    ]
    doc.build(story)

# Stand-in cover letter
make_doc(os.path.join(TARGET_DIR, "cover_letter.pdf"), "Cover Letter")

# Stand-in résumé
make_doc(os.path.join(TARGET_DIR, "resume.pdf"), "Résumé")

# Placeholder for the final merged application
make_doc(os.path.join(TARGET_DIR, "application_complete.pdf"),
         "Application (NOT YET MERGED)")
PY

echo "Initial files created in ${TARGET_DIR}:"
echo "  • cover_letter.pdf"
echo "  • resume.pdf"
echo "  • application_complete.pdf (placeholder – not merged)"
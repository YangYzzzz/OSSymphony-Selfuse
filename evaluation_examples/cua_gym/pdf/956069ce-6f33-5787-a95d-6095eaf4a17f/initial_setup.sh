#!/usr/bin/env bash
set -euo pipefail

# Absolute paths extracted verbatim from the task instruction
TARGET_DIR="/home/user/Desktop"
WORD_PATH="/home/user/Desktop/report_draft.docx"
PDF_PATH="/home/user/Desktop/report_final.pdf"

# 1. Ensure the Desktop directory exists
mkdir -p "$TARGET_DIR"

# 2. Install dependencies if they are missing
python3 - <<'PY'
import importlib, subprocess, sys
def ensure(pkg):
    try:
        importlib.import_module(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])
for p in ("reportlab", "PyPDF2", "python-docx"):
    ensure(p)
PY

# 3. Create a simple Word document (report_draft.docx) that will later be "converted"
python3 <<'PY'
from docx import Document

WORD_PATH = "/home/user/Desktop/report_draft.docx"

doc = Document()
doc.add_heading("Report Draft", level=1)
doc.add_paragraph(
    "This draft report is awaiting conversion to PDF. "
    "It contains introductory material and placeholders "
    "for further sections."
)
doc.save(WORD_PATH)
PY

# 4. Build an INITIAL placeholder PDF indicating that conversion is pending
python3 <<'PY'
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

PDF_PATH = "/home/user/Desktop/report_final.pdf"

doc = SimpleDocTemplate(PDF_PATH, pagesize=A4)
styles = getSampleStyleSheet()
story = [
    Paragraph("Conversion Pending", styles["Heading1"]),
    Spacer(1, 12),
    Paragraph(
        "The Word document 'report_draft.docx' has not yet been converted. "
        "Run the golden script to perform the conversion.",
        styles["Normal"],
    ),
]
doc.build(story)
PY

echo "Initial setup complete:"
echo "  • Word file: $WORD_PATH"
echo "  • Placeholder PDF: $PDF_PATH"
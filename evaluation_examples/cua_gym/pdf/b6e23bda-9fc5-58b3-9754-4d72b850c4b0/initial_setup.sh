#!/usr/bin/env bash
set -euo pipefail

# -----------------------------------------------------------------------------
# Initial PDF generator for: /home/user/Desktop/student_essay.pdf
# -----------------------------------------------------------------------------

# 1. Guarantee the Desktop directory exists
mkdir -p /home/user/Desktop

# 2. Install Python dependencies if they are missing
python3 - <<'PY'
import importlib, subprocess, sys, pkg_resources, json, os

def ensure(pkg_name):
    """Install *pkg_name* with pip if import fails."""
    try:
        importlib.import_module(pkg_name)
    except ModuleNotFoundError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg_name])

for lib in ("reportlab", "PyPDF2"):
    ensure(lib)
PY

# 3. Create the *student_essay.pdf* skeleton (no annotations yet)
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

output_path = "/home/user/Desktop/student_essay.pdf"

styles = getSampleStyleSheet()
story = []

# Generate eight simple pages so that pages 2, 4 and 7 exist
for page_num in range(1, 9):
    story.append(Paragraph(f"Student Essay – Page {page_num}", styles["Heading2"]))
    story.append(Spacer(1, 12))
    # Add a few deterministic lines of body text
    for i in range(3):
        story.append(Paragraph(
            "This is sample body text intended solely for PDF-automation demonstrations.", 
            styles["BodyText"]))
        story.append(Spacer(1, 8))
    if page_num < 8:  # Avoid an unnecessary PageBreak on the last page
        story.append(PageBreak())

doc = SimpleDocTemplate(output_path, pagesize=LETTER)
doc.build(story)
PY

echo "Initial PDF created at /home/user/Desktop/student_essay.pdf (8 pages, no annotations)"
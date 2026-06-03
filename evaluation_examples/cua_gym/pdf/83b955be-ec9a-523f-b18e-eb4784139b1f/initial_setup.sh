#!/usr/bin/env bash
set -euo pipefail
# ------------------------------------------------------------------
# Initial setup script for the task:
# "Convert all Word documents (.docx files) in /home/user/Documents/Reports
#  to PDF, saving them in folder 'Reports_PDF' with same filenames."
#
# This script populates /home/user/Documents/Reports with a few sample
# Word documents so that the golden conversion script has something to
# process.
# ------------------------------------------------------------------

# 1. Absolute paths extracted verbatim from the task instruction
DOCX_DIR="/home/user/Documents/Reports"

# 2. Create the directory structure exactly as requested
mkdir -p "${DOCX_DIR}"

# 3. Install dependencies if missing ------------------------------------------------
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab     >/dev/null
python3 -c "import PyPDF2"   2>/dev/null || pip3 install --user PyPDF2         >/dev/null
python3 -c "import docx"     2>/dev/null || pip3 install --user python-docx    >/dev/null
# -----------------------------------------------------------------------------------

# 4. Generate sample Word documents deterministically
python3 <<'PY'
from docx import Document
import os, datetime, random, string

docx_dir = "/home/user/Documents/Reports"
sample_files = ["Report1.docx", "Report2.docx", "Monthly_Summary.docx"]

# Deterministic seed so content is always identical
random.seed(42)

for filename in sample_files:
    path = os.path.join(docx_dir, filename)
    doc = Document()
    doc.add_heading(filename.replace(".docx", ""), level=1)
    doc.add_paragraph(
        "Generated on: " + datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    )
    doc.add_paragraph(
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        "Suspendisse vitae lacus at elit efficitur porta."
    )
    # Add a short deterministic bullet list
    bullets = ["Item " + ch for ch in string.ascii_uppercase[:3]]
    for b in bullets:
        p = doc.add_paragraph(b, style="List Bullet")
    doc.save(path)
PY

# 5. Summary
echo "::SUMMARY::"
echo "Created the following Word documents in ${DOCX_DIR}:"
ls -1 "${DOCX_DIR}"
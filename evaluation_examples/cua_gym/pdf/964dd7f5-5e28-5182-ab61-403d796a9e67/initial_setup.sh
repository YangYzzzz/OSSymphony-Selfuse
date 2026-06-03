#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Initial script: create sample PDF manuals in /home/user/Documents/Manuals
# NO environment variables are used for paths – everything is literal.
###############################################################################

TARGET_DIR="/home/user/Documents/Manuals"

# 1. Ensure target directory exists
mkdir -p "$TARGET_DIR"

# 2. Ensure Python deps
python3 - <<'PY'
import subprocess, sys, importlib.util

def ensure(pkg):
    spec = importlib.util.find_spec(pkg)
    if spec is None:                       # not installed
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])

ensure("reportlab")
ensure("PyPDF2")
PY

# 3. Build three simple multi-page manuals (no page numbers yet)
python3 <<'PY'
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER
from pathlib import Path

target = Path("/home/user/Documents/Manuals")
styles = getSampleStyleSheet()
body = styles["BodyText"]

manual_specs = [
    ("manual1.pdf", 3, "User Manual 1"),
    ("manual2.pdf", 4, "Setup Guide 2"),
    ("manual3.pdf", 2, "Reference Manual 3"),
]

for filename, pages, title in manual_specs:
    doc = SimpleDocTemplate(str(target / filename), pagesize=LETTER)
    story = [Paragraph(title, styles["Title"]), Spacer(1, 24)]
    for p in range(1, pages + 1):
        story.append(Paragraph(f"Content for page {p} of {title}.", body))
        story.append(Spacer(1, 500))
        if p != pages:
            story.append(PageBreak())
    doc.build(story)

print("Created initial manuals:")
for f, *_ in manual_specs:
    print("  •", target / f)
PY

echo "Initial PDF manuals generated in $TARGET_DIR"
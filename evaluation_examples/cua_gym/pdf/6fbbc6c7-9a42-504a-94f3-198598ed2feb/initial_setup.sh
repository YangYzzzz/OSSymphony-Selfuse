#!/usr/bin/env bash
set -euo pipefail

# -----------------------------------------------------------------------------
# Initial PDF builder
# Creates an unchecked checklist form  “preferences.pdf” exactly at
# /home/user/Desktop/preferences.pdf
# -----------------------------------------------------------------------------

TARGET_DIR="/home/user/Desktop"
INITIAL_PDF="/home/user/Desktop/preferences.pdf"

# 1. Ensure the target directory exists (absolute path – no env vars)
mkdir -p "$TARGET_DIR"

# 2. Install Python dependencies if they are missing
python3 - <<'PY'
import sys, subprocess, importlib.util

def ensure(pkg):
    try:
        import importlib
        importlib.import_module(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])
for p in ("reportlab", "PyPDF2"):
    ensure(p)
PY

# 3. Generate the unchecked checklist PDF with ReportLab
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER

file_path = "/home/user/Desktop/preferences.pdf"
c = canvas.Canvas(file_path, pagesize=LETTER)

# Document title
c.setFont("Helvetica-Bold", 16)
c.drawString(72, 750, "Preferences Checklist")

# Checklist options (A-E), all unchecked
c.setFont("Helvetica", 12)
start_y = 700
gap = 40
options = ["Option A", "Option B", "Option C", "Option D", "Option E"]

for idx, label in enumerate(options):
    y = start_y - idx * gap
    # Draw text
    c.drawString(110, y, label)
    # Draw checkbox (unchecked)
    c.acroForm.checkbox(
        name=f"option{label[-1]}",
        tooltip=label,
        x=80,
        y=y - 4,   # align box with text baseline
        size=15,
        checked=False
    )

c.save()
PY

echo "Initial PDF created at: ${INITIAL_PDF}"
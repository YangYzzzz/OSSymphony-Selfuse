#!/usr/bin/env bash
set -euo pipefail
#
# Initial script --------------------------------------------------------------
# Creates two sample fill-able PDFs inside
#   /home/user/Documents/CompletedForms
# They contain simple text-fields that will later be flattened.
#

# 1. Ensure the target directory from the task instruction exists
mkdir -p /home/user/Documents/CompletedForms

# 2. Install Python dependencies if they are missing
python3 - <<'PY'
import subprocess, sys, importlib.util, pathlib, textwrap, json, os

def ensure(pkg):
    """Install *pkg* with pip if import fails."""
    if importlib.util.find_spec(pkg) is None:       # pkg not importable?
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])

for mod in ("reportlab", "PyPDF2"):
    ensure(mod)
PY

# 3. Create two sample AcroForm PDFs
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
import os, itertools

output_dir = "/home/user/Documents/CompletedForms"
os.makedirs(output_dir, exist_ok=True)

# Deterministic form-field payloads
forms = [
    ("CompletedForm1.pdf", {"name": "John Doe", "date": "2024-01-15"}),
    ("CompletedForm2.pdf", {"name": "Jane Smith", "date": "2024-02-20"}),
]

for filename, data in forms:
    path = os.path.join(output_dir, filename)
    c = canvas.Canvas(path, pagesize=LETTER)
    c.setTitle("Sample Fillable Form")
    c.drawString(72, 740, "Sample Application Form")
    c.drawString(72, 720, "(demonstration of AcroForm fields)")
    form = c.acroForm

    # Draw static labels
    c.drawString(72, 680, "Name:")
    c.drawString(72, 640, "Date:")

    # Text fields (interactive)
    form.textfield(
        name="name",
        tooltip="Name",
        x=130, y=668,
        width=250, height=20,
        borderStyle="underlined",
        value=data["name"],
    )
    form.textfield(
        name="date",
        tooltip="Date",
        x=130, y=628,
        width=250, height=20,
        borderStyle="underlined",
        value=data["date"],
    )
    c.showPage()
    c.save()
PY

echo "Initial PDFs with fillable forms created in /home/user/Documents/CompletedForms:"
ls -1 /home/user/Documents/CompletedForms | grep -iE '\.pdf$' || true
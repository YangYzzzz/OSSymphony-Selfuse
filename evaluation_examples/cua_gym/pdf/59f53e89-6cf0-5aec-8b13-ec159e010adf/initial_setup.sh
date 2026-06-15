#!/usr/bin/env bash
set -euo pipefail
###############################################################################
# Initial script for: "Please clear all filled data from 'reusable_form.pdf'
# in /home/user/Documents and save as 'form_blank.pdf' to create a clean template."
#
# This script ONLY builds the starting file
#   /home/user/Documents/reusable_form.pdf
# containing pre-filled demo data.
###############################################################################

# Ensure the target directory exists exactly as requested
mkdir -p /home/user/Documents

# ---------------------------------------------------------------------------
# Install Python dependencies deterministically if they are missing
# ---------------------------------------------------------------------------
python3 - <<'PY'
import importlib.util, subprocess, sys, json, os
for pkg in ("reportlab", "PyPDF2"):
    if importlib.util.find_spec(pkg) is None:                       # Not installed
        print(f"Installing {pkg} …")
        subprocess.check_call([sys.executable, "-m", "pip", "install",
                               "--user", pkg], stdout=subprocess.DEVNULL)
PY

# ---------------------------------------------------------------------------
# Build /home/user/Documents/reusable_form.pdf with filled data
# ---------------------------------------------------------------------------
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER

outfile = "/home/user/Documents/reusable_form.pdf"

def build_filled_form(path:str) -> None:
    c = canvas.Canvas(path, pagesize=LETTER)
    width, height = LETTER

    # Title
    c.setFont("Helvetica-Bold", 14)
    c.drawString(72, height - 72, "Reusable Contact Form")

    # Field labels
    c.setFont("Helvetica", 10)
    c.drawString(72, height - 120, "Name:")
    c.drawString(72, height - 170, "Email:")
    c.drawString(72, height - 220, "Comments:")

    # Interactive form fields (pre-filled)
    form = c.acroForm
    form.textfield(
        name="name", tooltip="Name",
        x=130, y=height - 135, width=300, height=20,
        borderStyle="underlined", value="John Doe"
    )
    form.textfield(
        name="email", tooltip="Email",
        x=130, y=height - 185, width=300, height=20,
        borderStyle="underlined", value="john.doe@example.com"
    )
    form.textfield(
        name="comments", tooltip="Comments",
        x=130, y=height - 280, width=300, height=60,
        borderStyle="underlined", value="I love PDF automation!"
    )
    c.save()

build_filled_form(outfile)
print(f"✅ Created initial PDF with filled fields: {outfile}")
PY
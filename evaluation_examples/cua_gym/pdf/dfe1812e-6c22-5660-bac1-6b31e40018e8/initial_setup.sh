#!/usr/bin/env bash
set -euo pipefail
#
# Creates a deterministic folder hierarchy under
# /home/user/Documents/Projects with two sub-folders.
# Each sub-folder contains two simple PDFs created with ReportLab.
# No merging happens here – this is the “before” state requested
# by the task.

# -----------------------------------------------------------------------------
# 1) Guarantee dependencies
# -----------------------------------------------------------------------------
python3 - <<'PY'
import importlib, sys, subprocess, json, pkg_resources, os, textwrap
needed = ["reportlab", "PyPDF2"]
for pkg in needed:
    try:
        importlib.import_module(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])
PY

# -----------------------------------------------------------------------------
# 2) Create the directory tree and sample PDFs
# -----------------------------------------------------------------------------
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
import os

root_dir = "/home/user/Documents/Projects"
subfolders = ["Alpha", "Beta"]

for sub in subfolders:
    folder_path = os.path.join(root_dir, sub)
    os.makedirs(folder_path, exist_ok=True)
    # create two very small PDFs per subfolder
    for idx in (1, 2):
        pdf_path = os.path.join(folder_path, f"part{idx}.pdf")
        c = canvas.Canvas(pdf_path, pagesize=LETTER)
        c.drawString(72, 720, f"{sub} ‒ Sample document {idx}")
        c.save()
PY

# -----------------------------------------------------------------------------
# 3) Final message
# -----------------------------------------------------------------------------
echo "Initial setup complete."
echo "Created the following PDF files:"
find /home/user/Documents/Projects -type f -name "*.pdf"
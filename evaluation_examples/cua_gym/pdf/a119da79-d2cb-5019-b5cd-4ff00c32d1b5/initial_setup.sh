#!/usr/bin/env bash
set -euo pipefail
#
# Initial placeholder PDF for:  "Convert the CAD drawing 'blueprint.dwg' on Desktop to PDF 'blueprint.pdf' ..."
# Absolute target path extracted from instruction: /home/user/Desktop/blueprint.pdf
#

# 1) Make sure the Desktop directory exists
mkdir -p /home/user/Desktop

# 2) Ensure ReportLab and PyPDF2 are available
python3 - <<'PY'
import sys, subprocess, importlib.util

def ensure(pkg_name: str):
    if importlib.util.find_spec(pkg_name) is None:          # not installed
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg_name])
for mod in ("reportlab", "PyPDF2"):
    ensure(mod)
PY

# 3) Build a minimal placeholder PDF
python3 <<'PY'
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

out_path = "/home/user/Desktop/blueprint.pdf"
c = canvas.Canvas(out_path, pagesize=A4)
w, h = A4

c.setFont("Helvetica-Bold", 18)
c.drawString(72, h - 72, "Blueprint Placeholder")

c.setFont("Helvetica", 12)
c.drawString(72, h - 100, "Source DWG: blueprint.dwg")
c.drawString(72, h - 120, "Status     : NOT YET CONVERTED")
c.drawString(72, h - 160, "This PDF is a temporary placeholder pending full")
c.drawString(72, h - 178, "conversion of the CAD drawing for contractor use.")

c.save()
PY

echo "Initial placeholder created at /home/user/Desktop/blueprint.pdf"
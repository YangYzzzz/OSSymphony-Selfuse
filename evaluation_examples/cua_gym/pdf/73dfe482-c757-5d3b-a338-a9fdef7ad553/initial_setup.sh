#!/usr/bin/env bash
set -euo pipefail
#
# Initial script
# Creates a dummy catalog PDF at /home/user/Documents/Sales/catalog_2024.pdf
#

# ---------------------------------------------------------------------------
# 1. Ensure target directory exists
# ---------------------------------------------------------------------------
mkdir -p /home/user/Documents/Sales

# ---------------------------------------------------------------------------
# 2. Install dependencies (ReportLab & PyPDF2) if missing
# ---------------------------------------------------------------------------
python3 - <<'PY'
import subprocess, sys
for pkg in ("reportlab", "PyPDF2"):
    try:
        __import__(pkg)
    except ModuleNotFoundError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])
PY

# ---------------------------------------------------------------------------
# 3. Build a deterministic sample catalog PDF
# ---------------------------------------------------------------------------
python3 <<'PY'
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

out_path = "/home/user/Documents/Sales/catalog_2024.pdf"

doc = SimpleDocTemplate(out_path, pagesize=A4,
                        leftMargin=40, rightMargin=40,
                        topMargin=60, bottomMargin=40)

styles = getSampleStyleSheet()
story = [
    Paragraph("Product Catalog 2024", styles["Title"]),
    Spacer(1, 12)
]

data = [
    ["Product", "Description"],
    ["Widget A", "High-quality widget for everyday use."],
    ["Gadget B", "Multi-purpose gadget with premium build."],
    ["Device C", "State-of-the-art device with smart features."]
]

table = Table(data, colWidths=[120, 360])
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EFEFEF")),
    ("GRID",       (0, 0), (-1,-1), 0.25, colors.grey),
    ("VALIGN",     (0, 0), (-1,-1), "TOP"),
]))
story.append(table)

doc.build(story)
PY

echo "✅ Created /home/user/Documents/Sales/catalog_2024.pdf"
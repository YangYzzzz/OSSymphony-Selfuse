#!/usr/bin/env bash
set -euo pipefail
#
# Initial script – creates /home/user/Downloads/product_comparison.pdf
# (contains a hidden, white–coloured CSV matrix that will be extracted
#  by the golden script)
#

# 1) Guarantee target directory exists
mkdir -p /home/user/Downloads

# 2) Ensure dependencies are available
python3 - <<'PY'
import subprocess, sys, importlib
def ensure(pkg):
    try:
        importlib.import_module(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])

ensure("reportlab")
PY

# PyPDF2 is not required for the initial script, but keep build parity
python3 -c "import PyPDF2" 2>/dev/null || pip3 install --user PyPDF2 >/dev/null 2>&1

# 3) Build the deterministic PDF
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

pdf_path = "/home/user/Downloads/product_comparison.pdf"

# --- deterministic data ---------------------------
matrix = [
    ["Feature", "Product A", "Product B", "Product C"],
    ["Price", "$100", "$120", "$90"],
    ["Battery Life", "10h", "12h", "8h"],
    ["Weight", "1.2kg", "1.1kg", "1.3kg"],
]
# ---------------------------------------------------

# build visible document -------------------------------------------------------
doc = SimpleDocTemplate(pdf_path, pagesize=LETTER, title="Product Comparison")
styles = getSampleStyleSheet()

story = []
story.append(Paragraph("Product Comparison Matrix", styles["Title"]))
story.append(Spacer(1, 12))

tbl = Table(matrix, repeatRows=1)
tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D3D3D3")),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ("ALIGN", (1, 1), (-1, -1), "CENTER"),
]))
story.append(tbl)
story.append(Spacer(1, 24))

# ------------------------------------------------------------------------------

# Inject a hidden white-text block that carries the CSV – this guarantees
# reliable extraction regardless of how the layout text flows.
hidden_csv_lines = [
    "BEGIN_COMPARISON_MATRIX",
    "Feature,Product A,Product B,Product C",
    "Price,$100,$120,$90",
    "Battery Life,10h,12h,8h",
    "Weight,1.2kg,1.1kg,1.3kg",
    "END_COMPARISON_MATRIX",
]

if "Hidden" not in styles:
    styles.add(ParagraphStyle(name="Hidden",
                              parent=styles["Normal"],
                              fontSize=1,            # tiny font
                              leading=1.2,
                              textColor=colors.white))   # white on white

story.append(Paragraph("\n".join(hidden_csv_lines), styles["Hidden"]))

doc.build(story)
PY

echo "✅ Created /home/user/Downloads/product_comparison.pdf"
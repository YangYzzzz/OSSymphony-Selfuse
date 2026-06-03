#!/usr/bin/env bash
set -euo pipefail
#
# Creates the “scanned” invoice PDF mentioned in the task instruction
# Path strictly follows the wording: /home/user/Documents/Finance/scanned_invoice.pdf
#

# 1. Ensure the target directory exists (NO environment variables allowed)
mkdir -p /home/user/Documents/Finance

# 2. Guard-install Python dependencies
python3 - <<'PY'
import subprocess, sys

def ensure(pkg):
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])

for lib in ("reportlab", "PyPDF2"):
    ensure(lib)
PY

# 3. Generate the initial PDF with deterministic invoice text
python3 <<'PY'
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

pdf_path = "/home/user/Documents/Finance/scanned_invoice.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                        rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)

styles = getSampleStyleSheet()
story = []

# Title
story.append(Paragraph("INVOICE", styles["Title"]))
story.append(Spacer(1, 24))

# Deterministic invoice data that the golden script will later OCR-extract
invoice_data = [
    ("Invoice #", "INV-1001"),
    ("Date", "2024-06-01"),
    ("Vendor", "Acme Corp"),
    ("Amount", "$2,500.00"),
]

table = Table(invoice_data, colWidths=[100, 200])
table.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F5F5F5")),
]))
story.append(table)

story.append(Spacer(1, 24))
story.append(Paragraph("Thank you for your business.", styles["Normal"]))

doc.build(story)
PY

echo "Initial file created: /home/user/Documents/Finance/scanned_invoice.pdf"
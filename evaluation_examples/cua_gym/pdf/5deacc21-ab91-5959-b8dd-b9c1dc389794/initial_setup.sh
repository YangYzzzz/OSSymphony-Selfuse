#!/usr/bin/env bash
set -euo pipefail

# Absolute directory extracted from task instruction
TARGET_DIR="/home/user/Documents"
TARGET_FILE="/home/user/Documents/financial_data.pdf"

# Ensure target directory exists
mkdir -p "${TARGET_DIR}"

# Install dependencies if missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2" 2>/dev/null || pip3 install --user PyPDF2

# Build the initial (unencrypted) PDF
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
import os

output_path = "/home/user/Documents/financial_data.pdf"

doc = SimpleDocTemplate(
    output_path,
    pagesize=LETTER,
    rightMargin=72,
    leftMargin=72,
    topMargin=72,
    bottomMargin=72,
)
styles = getSampleStyleSheet()

story = [
    Paragraph("Financial Data Report", styles["Title"]),
    Spacer(1, 12),
    Paragraph("Prepared by Finance Department", styles["Normal"]),
    Spacer(1, 24),
]

data = [
    ["Quarter", "Revenue ($)", "Expenses ($)", "Profit ($)"],
    ["Q1 2024", "1,200,000", "800,000", "400,000"],
    ["Q2 2024", "1,350,000", "820,000", "530,000"],
    ["Q3 2024", "1,500,000", "900,000", "600,000"],
    ["Q4 2024", "1,650,000", "950,000", "700,000"],
]

table = Table(data, colWidths=[80, 120, 120, 120])
table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ]
    )
)

story.append(table)
doc.build(story)

print(f"Generated {output_path} ({os.path.getsize(output_path)} bytes)")
PY

echo "Initial PDF creation complete."
#!/usr/bin/env bash
set -euo pipefail
#
# Initial script
# Purpose: create the starting PDF mentioned in the task instruction
# Target file: /home/user/Desktop/conference_program.pdf                     (ABSOLUTE PATH)

###############################################################################
# 1. Ensure target directory exists
###############################################################################
mkdir -p /home/user/Desktop

###############################################################################
# 2. Install Python dependencies if they do not exist
###############################################################################
# Install dependencies if missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"     2>/dev/null || pip3 install --user PyPDF2

###############################################################################
# 3. Build the initial PDF with ReportLab
###############################################################################
python3 <<'PY'
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
)
from reportlab.lib import colors

pdf_path = "/home/user/Desktop/conference_program.pdf"

# ────────────────────────────────────────────────────────────────────────────
# Configure the PDF document
# ────────────────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=LETTER,
    leftMargin=72,
    rightMargin=72,
    topMargin=72,
    bottomMargin=72,
)
styles = getSampleStyleSheet()
story = []

# Build 10 deterministic pages; page-8 contains the schedule table
for page_num in range(1, 11):
    story.append(Paragraph(f"Conference Program – Page {page_num}", styles["Heading2"]))
    story.append(Spacer(1, 12))

    if page_num == 8:
        # ------------------------------------------------------------------
        # The schedule table that will later be extracted
        # ------------------------------------------------------------------
        data = [
            ["Time", "Session", "Room"],
            ["09:00", "Opening Remarks", "Hall A"],
            ["10:00", "Machine Learning 101", "Hall B"],
            ["11:00", "Coffee Break", "Lobby"],
            ["11:30", "Deep Learning", "Hall A"],
            ["12:30", "Lunch", "Dining Hall"],
        ]
        tbl = Table(data, colWidths=[80, 250, 100])
        tbl.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D3D3D3")),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        story.append(tbl)
    else:
        # Filler text for non-schedule pages
        lorem = (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
            "Vestibulum imperdiet dignissim ipsum, eu tempor odio commodo a."
        )
        for _ in range(3):
            story.append(Paragraph(lorem, styles["Normal"]))
            story.append(Spacer(1, 12))

    # Insert explicit page break except on the last page
    if page_num < 10:
        story.append(PageBreak())

# Build and save the PDF
doc.build(story)
print(f"Created initial PDF at: {pdf_path}")
PY

###############################################################################
# 4. Wrap-up message
###############################################################################
echo "Initial setup complete: /home/user/Desktop/conference_program.pdf built."
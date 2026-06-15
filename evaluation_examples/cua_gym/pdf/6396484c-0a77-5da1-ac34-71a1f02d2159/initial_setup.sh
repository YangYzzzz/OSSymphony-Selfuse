#!/usr/bin/env bash
set -euo pipefail
#
# Initial set-up script
# Generates the baseline PDF mentioned in the task instruction.
# File created: /home/user/Documents/Academic/university_catalog.pdf
#

# 1) Ensure the target directory exists (ABSOLUTE path – no variables!)
mkdir -p /home/user/Documents/Academic

# 2) Install runtime dependencies if they are not already present
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"    2>/dev/null || pip3 install --user PyPDF2

# 3) Build the baseline PDF with a 45-page layout; page-45 hosts a
#    deterministic course-schedule table.
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
)
from reportlab.lib import colors

pdf_path = "/home/user/Documents/Academic/university_catalog.pdf"

# Deterministic course schedule table data
table_data = [
    ["Course Code", "Course Name",               "Days",     "Time",          "Room"],
    ["CS101",      "Intro to Computer Science",  "Mon/Wed",  "09:00-10:30",   "Room 101"],
    ["MATH201",    "Calculus II",                "Tue/Thu",  "10:45-12:15",   "Room 202"],
    ["PHYS150",    "Physics I",                  "Mon/Wed",  "13:00-14:30",   "Room 303"],
    ["HIST210",    "World History",              "Tue/Thu",  "14:45-16:15",   "Room 404"],
    ["ENG102",     "English Literature",         "Fri",      "09:00-11:45",   "Room 505"],
]

styles = getSampleStyleSheet()
doc = SimpleDocTemplate(pdf_path, pagesize=LETTER)
story = []

# Pages 1-44: simple placeholders
for idx in range(44):
    story.append(Paragraph(f"University Catalog – Placeholder Page {idx+1}", styles["Normal"]))
    story.append(PageBreak())

# Page 45: real table
story.append(Paragraph("Course Schedule", styles["Heading2"]))
story.append(Spacer(1, 12))

table = Table(table_data, colWidths=[80, 200, 80, 100, 80])
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E0E0E0")),
    ("GRID",       (0, 0), (-1,-1), 0.5,             colors.grey),
    ("ALIGN",      (0, 0), (-1,-1), "CENTER"),
    ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
]))
story.append(table)

doc.build(story)
PY

echo "Initial PDF created at /home/user/Documents/Academic/university_catalog.pdf"
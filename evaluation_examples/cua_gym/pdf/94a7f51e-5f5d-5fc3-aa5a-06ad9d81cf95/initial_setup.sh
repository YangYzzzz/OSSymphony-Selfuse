#!/usr/bin/env bash
set -euo pipefail

# ----------------- dependency guard -----------------
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2" 2>/dev/null || pip3 install --user PyPDF2
# ----------------------------------------------------

# Target directory & file extracted verbatim from task instruction
mkdir -p /home/user/Documents/Finance

python3 <<'PY'
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

pdf_path = "/home/user/Documents/Finance/audit_report.pdf"

styles = getSampleStyleSheet()
doc    = SimpleDocTemplate(pdf_path, pagesize=LETTER,
                           leftMargin=72, rightMargin=72,
                           topMargin=72, bottomMargin=72)

story = []
for page_num in range(1, 16):                       # 15-page dummy report
    story.append(Paragraph(f"Audit Report – Page {page_num}", styles["Heading2"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "This is placeholder text for the financial audit report. "
        "Subsequent versions will include review stamps once approved.",
        styles["Normal"]))
    if page_num < 15:
        story.append(PageBreak())

doc.build(story)
print(f"Initial PDF written to {pdf_path}")
PY

echo "✅  Created /home/user/Documents/Finance/audit_report.pdf (initial state)"
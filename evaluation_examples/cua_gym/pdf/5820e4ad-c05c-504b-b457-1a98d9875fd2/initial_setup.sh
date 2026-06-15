#!/usr/bin/env bash
set -euo pipefail

# Absolute directory extracted literally from the task wording
TARGET_DIR="/home/user/Desktop"
INITIAL_PDF="/home/user/Desktop/memo.pdf"

# Ensure the Desktop directory exists
mkdir -p "$TARGET_DIR"

# Install dependencies if missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"    2>/dev/null || pip3 install --user PyPDF2

###############################################################################
# Build the INITIAL PDF – a simple two-page memo with no special header
###############################################################################
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

output_path = "/home/user/Desktop/memo.pdf"

styles = getSampleStyleSheet()
doc    = SimpleDocTemplate(output_path, pagesize=LETTER,
                           leftMargin=72, rightMargin=72,
                           topMargin=72, bottomMargin=72)

story = [
    Paragraph("Quarterly Memo", styles["Title"]),
    Spacer(1, 24),
    Paragraph(
        "This memorandum summarizes key performance indicators for the last "
        "quarter. All numbers are verified and have been approved by the "
        "finance department.", styles["Normal"]),
    Spacer(1, 12),
    Paragraph(
        "Highlights:", styles["Heading2"]),
    Paragraph("- Revenue grew by 8.5 %", styles["Normal"]),
    Paragraph("- Customer churn decreased to 3.2 %", styles["Normal"]),
    PageBreak(),
    Paragraph("Appendix A – Raw Figures", styles["Heading2"]),
    Spacer(1, 12),
    Paragraph(
        "The following raw figures back the highlights presented on the first "
        "page. For detailed breakdowns please consult the attached Excel "
        "workbook.", styles["Normal"]),
]

doc.build(story)
PY

echo "Created initial PDF: ${INITIAL_PDF}"
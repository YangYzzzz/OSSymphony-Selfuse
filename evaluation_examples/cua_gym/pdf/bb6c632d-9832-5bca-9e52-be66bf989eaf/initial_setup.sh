#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------------------
# Initial Script – creates the starting “scan” PDF
# Target file: /home/user/Study/math_textbook_scan.pdf
# ------------------------------------------------------------------------------

# 1. Ensure the exact directory from the task exists
mkdir -p /home/user/Study

# 2. Install ReportLab & PyPDF2 if they are missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"     2>/dev/null || pip3 install --user PyPDF2

# 3. Build a deterministic PDF that looks like a scanned math page
python3 <<'PY'
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

pdf_path = "/home/user/Study/math_textbook_scan.pdf"

doc     = SimpleDocTemplate(pdf_path, pagesize=A4, leftMargin=72, rightMargin=72,
                            topMargin=72, bottomMargin=72)

styles  = getSampleStyleSheet()
# Add a monospace-looking style for equations if not already present
if "Equation" not in styles:
    styles.add(ParagraphStyle(
        name="Equation",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=12,
        leading=14,
    ))

story = [
    Paragraph("Mathematical Equations (Scanned Sample)", styles["Title"]),
    Spacer(1, 18),
]

equations = [
    "E = mc^2",
    "a^2 + b^2 = c^2",
    r"\int_{a}^{b} f(x)\,dx = F(b) - F(a)",
    r"\frac{d}{dx} \sin(x) = \cos(x)",
    r"\nabla \cdot \mathbf{E} = \rho / \varepsilon_0",
]

for eq in equations:
    story.append(Paragraph(eq, styles["Equation"]))
    story.append(Spacer(1, 10))

doc.build(story)
print(f"Created initial PDF at: {pdf_path}")
PY

echo "Initial setup complete – file list:"
ls -l /home/user/Study
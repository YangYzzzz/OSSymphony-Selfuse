#!/usr/bin/env bash
set -euo pipefail
#
# Initial script
# Creates three standalone certificate PDFs inside
#   /home/user/Documents/Certificates
# but does NOT merge them.
#

# 1. Ensure target directory exists
mkdir -p /home/user/Documents/Certificates

# 2. Install dependencies (ReportLab + PyPDF2) if they are missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2" 2>/dev/null || pip3 install --user PyPDF2

# 3. Generate the three individual certificate PDFs
python3 <<'PY'
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

cert_dir = "/home/user/Documents/Certificates"
os.makedirs(cert_dir, exist_ok=True)

styles = getSampleStyleSheet()

cert_specs = [
    ("completion_cert.pdf", "Certificate of Completion"),
    ("participation_cert.pdf", "Certificate of Participation"),
    ("excellence_cert.pdf", "Certificate of Excellence"),
]

for filename, title in cert_specs:
    path = os.path.join(cert_dir, filename)
    doc = SimpleDocTemplate(path, pagesize=LETTER,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)
    story = [
        Paragraph(title, styles["Title"]),
        Spacer(1, 36),
        Paragraph("This certifies that:", styles["Normal"]),
        Spacer(1, 18),
        Paragraph("_______________________________", styles["Normal"]),
        Spacer(1, 36),
        Paragraph("has successfully met the stated requirements.", styles["Normal"]),
    ]
    doc.build(story)
PY

echo "Initial setup complete."
echo "Generated files:"
echo "  /home/user/Documents/Certificates/completion_cert.pdf"
echo "  /home/user/Documents/Certificates/participation_cert.pdf"
echo "  /home/user/Documents/Certificates/excellence_cert.pdf"
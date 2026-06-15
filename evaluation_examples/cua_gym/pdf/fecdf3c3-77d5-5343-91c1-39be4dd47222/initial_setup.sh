#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Initial setup script (placeholder PDF)
# Task reference: Convert the webpage at 'file:///home/user/Documents/report.html'
#                 to PDF 'report_web.pdf' on Desktop.
# This initial script prepares the deterministic starting point:
#   • Creates /home/user/Documents/report.html with static HTML content
#   • Creates a placeholder PDF at /home/user/Desktop/report_web.pdf
###############################################################################

# 1. Create required directories exactly as spelled out in the task
mkdir -p /home/user/Documents
mkdir -p /home/user/Desktop

# 2. Install Python dependencies if they are missing
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"    2>/dev/null || pip3 install --user PyPDF2

# 3. Create a deterministic sample HTML file (only if not already there)
cat > /home/user/Documents/report.html <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Quarterly Report</title>
</head>
<body>
  <h1>Quarterly Report</h1>
  <p>This is a sample HTML report that will later be converted to PDF.</p>
  <p>The goal is to demonstrate ReportLab-based conversion.</p>
</body>
</html>
HTML

# 4. Produce a placeholder PDF using ReportLab
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

output_pdf = "/home/user/Desktop/report_web.pdf"
doc = SimpleDocTemplate(output_pdf, pagesize=LETTER)
styles = getSampleStyleSheet()

story = [
    Paragraph("Placeholder PDF", styles["Title"]),
    Spacer(1, 24),
    Paragraph("The HTML file will be fully converted in the golden script.", styles["Normal"]),
]
doc.build(story)
PY

echo "Initial setup complete:"
echo " • /home/user/Documents/report.html      (HTML source)"
echo " • /home/user/Desktop/report_web.pdf     (placeholder PDF)"
#!/usr/bin/env bash
set -euo pipefail

# Initial script: create the starting double-sided scan simulation
# Target files: /home/user/double_sided.pdf
#               (golden script will also create /home/user/single_sided_ordered.pdf)

# 1. Make sure the target directory exists
mkdir -p /home/user

# 2. Ensure Python dependencies are present
python3 - <<'PY' 2>/dev/null || true
import reportlab, PyPDF2
PY
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2" 2>/dev/null || pip3 install --user PyPDF2

# 3. Build the simulated scanned PDF
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER

output_path = "/home/user/double_sided.pdf"
labels = ["front1", "back1", "front2", "back2", "front3", "back3"]

c = canvas.Canvas(output_path, pagesize=LETTER)
width, height = LETTER

for text in labels:
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(width / 2, height / 2, text)
    c.showPage()

c.save()
print(f"Created initial double-sided PDF at {output_path} with {len(labels)} pages.")
PY
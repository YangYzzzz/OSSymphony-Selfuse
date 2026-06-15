#!/usr/bin/env bash
set -euo pipefail
#
# Initial script
# Creates the placeholder “corrupted” PDF mentioned in the task instruction.
# Absolute path extracted from task:  /home/user/Desktop/damaged_file.pdf
#

# 1. Create target directory exactly as requested
mkdir -p /home/user/Desktop

# 2. Install dependencies if missing
python3 - <<'PY'
import sys, subprocess, importlib.util

def ensure(pkg):
    if importlib.util.find_spec(pkg) is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])

for mod in ("reportlab", "PyPDF2"):
    ensure(mod)
PY

# 3. Build the PDF with ReportLab
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

output_path = "/home/user/Desktop/damaged_file.pdf"

doc = SimpleDocTemplate(output_path, pagesize=LETTER,
                        title="Damaged File Placeholder",
                        author="PDF Automation System")

styles = getSampleStyleSheet()
story = [
    Paragraph("Damaged File – Placeholder Content", styles["Title"]),
    Spacer(1, 12),
    Paragraph("This PDF is intentionally labelled as ‘damaged’ for "
              "subsequent recovery testing. "
              "The quick brown fox jumps over the lazy dog.", styles["Normal"]),
    Spacer(1, 12),
    Paragraph("End of sample page.", styles["Normal"]),
]
doc.build(story)
PY

# 4. Summarise result
echo "Initial placeholder PDF created at /home/user/Desktop/damaged_file.pdf"
ls -lh /home/user/Desktop/damaged_file.pdf
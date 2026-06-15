#!/usr/bin/env bash
set -euo pipefail
# -------------------------------------------------------------
# Initial script : create the source PDF that lives on Desktop
# Target file  : /home/user/Desktop/court_filing.pdf
# -------------------------------------------------------------

echo "[initial] Creating /home/user/Desktop/court_filing.pdf"

# 1. Ensure the Desktop directory exists
mkdir -p /home/user/Desktop

# 2. Install Python dependencies if they are not present
python3 -c "import reportlab" 2>/dev/null || pip3 install --user reportlab
python3 -c "import PyPDF2"     2>/dev/null || pip3 install --user PyPDF2

# 3. Generate the placeholder legal PDF
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

pdf_path = "/home/user/Desktop/court_filing.pdf"

styles = getSampleStyleSheet()
story  = []

legal_paragraphs = [
    "IN THE SUPREME COURT OF THE STATE OF EXAMPLE",
    "Case No. 2023-CV-0001",
    "Comes now the Plaintiff, by and through counsel of record, and files this Complaint against the Defendant, and in support thereof states as follows:",
    "1. The Plaintiff is a resident of Example County and was at all relevant times domiciled therein.",
    "2. The Defendant is a corporation organized under the laws of the State of Example and may be served through its registered agent.",
    "WHEREFORE, premises considered, Plaintiff prays that Defendant be cited to appear and answer herein, and that upon final hearing, Plaintiff have and recover judgment against Defendant for damages within the jurisdictional limits of this Court, costs of court, pre- and post-judgment interest, and for such other and further relief, at law or in equity, to which Plaintiff may show himself justly entitled.",
    "Respectfully submitted,\n\n/s/ Jane Attorney\nJane Attorney (Bar #12345)\nCounsel for Plaintiff"
]

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=LETTER,
    rightMargin=72, leftMargin=72,
    topMargin=72,  bottomMargin=72,
)

for p in legal_paragraphs:
    story.append(Paragraph(p, styles["Normal"]))
    story.append(Spacer(1, 12))

doc.build(story)
PY

echo "[initial] Done. File details:"
ls -l /home/user/Desktop/court_filing.pdf
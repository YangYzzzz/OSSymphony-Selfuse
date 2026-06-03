#!/usr/bin/env bash
set -euo pipefail

################################################################################
# Initial setup script                                                          #
# Creates a dummy conference proceedings PDF at                                #
#      /home/user/Research/proceedings_2023.pdf                                #
# The file mimics three short “papers”.                                         #
################################################################################

# 1. Ensure target directory exists (ABSOLUTE path per task instruction)
mkdir -p /home/user/Research

# 2. Install dependencies if they are missing
python3 - <<'PY'
import importlib, subprocess, sys, pkg_resources, json, pathlib, textwrap, os

def ensure(pkg):
    try:
        importlib.import_module(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])

for p in ("reportlab", "PyPDF2"):
    ensure(p)
PY

# 3. Build the “proceedings_2023.pdf”
python3 <<'PY'
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

pdf_path = "/home/user/Research/proceedings_2023.pdf"

styles = getSampleStyleSheet()
story = []

papers = [
    ("Paper 1: Advances in AI Research",
     "This paper discusses recent advances in artificial intelligence. "
     "It covers neural networks, reinforcement learning, and ethical considerations."),
    ("Paper 2: Quantum Computing Overview",
     "Quantum computing promises exponential speed-ups for certain problems. "
     "We review qubits, entanglement and quantum algorithms."),
    ("Paper 3: Sustainable Energy Solutions",
     "Renewable energy sources such as solar and wind are critical for the future. "
     "This paper analyses storage technologies and smart grids.")
]

for idx, (title, body) in enumerate(papers, start=1):
    story.append(Paragraph(title, styles["Heading1"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(body, styles["Normal"]))
    if idx != len(papers):                  # Page break between papers
        story.append(PageBreak())

doc = SimpleDocTemplate(pdf_path, pagesize=LETTER,
                        title="Conference Proceedings 2023")
doc.build(story)
print(f"Created {pdf_path}")
PY

echo "Initial PDF created at /home/user/Research/proceedings_2023.pdf"
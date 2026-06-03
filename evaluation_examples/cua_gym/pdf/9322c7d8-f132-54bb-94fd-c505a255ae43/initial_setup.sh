#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Initial Script – creates the “starting” PDF only (with bookmarks)
# Target file: /home/user/Desktop/proceedings.pdf      (300 pages, 5 bookmarks)
###############################################################################

# 0. Make sure the Desktop folder exists
mkdir -p /home/user/Desktop

# 1. Install dependencies if they’re missing
python3 - <<'PY'
import importlib, subprocess, sys
for pkg in ("reportlab", "PyPDF2"):
    try:
        importlib.import_module(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])
PY

# 2. Build the 300-page proceedings.pdf with 5 top–level bookmarks
python3 <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER

OUTPUT_PATH = "/home/user/Desktop/proceedings.pdf"
NUM_PAPERS   = 5            # top-level bookmarks
PAGES_EACH   = 60           # 5×60 = 300 pages total
TOTAL_PAGES  = NUM_PAPERS * PAGES_EACH

c = canvas.Canvas(OUTPUT_PATH, pagesize=LETTER)
width, height = LETTER

current_global_page = 1     # 1-based just for the page label

for paper in range(1, NUM_PAPERS + 1):
    bookmark_key = f"paper_{paper}"
    bookmark_title = f"Paper {paper}"
    
    # Place bookmark on *current* page (the first page of this paper)
    c.bookmarkPage(bookmark_key)
    c.addOutlineEntry(bookmark_title, bookmark_key, level=0, closed=False)

    for i in range(PAGES_EACH):
        c.setFont("Helvetica", 12)
        c.drawString(72, height - 72,
                     f"{bookmark_title} – Proceeding Page {current_global_page} / {TOTAL_PAGES}")
        # Draw footer page number
        c.drawString(300, 40, f"{current_global_page}")
        
        current_global_page += 1
        # Only advance to a *new* page if we are NOT on the very last page overall
        if current_global_page <= TOTAL_PAGES:
            c.showPage()

c.save()
print(f"Created initial file: {OUTPUT_PATH} (300 pages)")
PY

echo "Initial script complete – /home/user/Desktop/proceedings.pdf created."
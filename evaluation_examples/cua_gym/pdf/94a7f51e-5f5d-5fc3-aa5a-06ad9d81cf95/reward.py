"""
FINAL REWARD SCRIPT - SUCCESS
Task: I need to add a 'REVIEWED' stamp annotation to pages 3, 7, and 12 in 'audit_report.pdf' in /home/user/Documents/Finance.
Generated: 2025-11-29 09:54:01
Status: success
Model: o3
Total Steps: 16
"""

"""
Reward Script for PDF Task Verification
Task: Ensure a 'REVIEWED' stamp annotation has been added to pages 3, 7, and 12
       of /home/user/Documents/Finance/audit_report.pdf

Scoring (progressive):
  • 0.7 – Presence of /Stamp annotations on the three exact pages
  • 0.3 – The word REVIEWED appears in the raw PDF bytes at least once per
          required page (capped so extra occurrences give no advantage)
  • Total score = stamp_score + text_score (max 1.0)

Libraries used: PyPDF2 (pre-installed), pathlib (std-lib)
Absolutely no subprocess usage.
"""

from pathlib import Path
from PyPDF2 import PdfReader

# ---------------- CONFIGURATION -----------------
PDF_PATH = "/home/user/Documents/Finance/audit_report.pdf"
TARGET_PAGES = [2, 6, 11]  # zero-based indexes → pages 3, 7, 12
STAMP_KEYWORD = "REVIEWED"
STAMP_WEIGHT = 0.7
TEXT_WEIGHT = 0.3
# ------------------------------------------------

def page_has_stamp(page) -> bool:
    """Return True if the page contains at least one /Stamp annotation."""
    annots = page.get("/Annots") or []
    for ref in annots:
        annot = ref.get_object()
        if annot.get("/Subtype") == "/Stamp":
            return True
    return False


def verify_task(pdf_path: str) -> float:
    pdf_file = Path(pdf_path)

    # Guard: file must exist
    if not pdf_file.exists():
        print(f"✗ PDF not found at {pdf_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load PDF (strict=False to tolerate minor syntax issues)
    try:
        reader = PdfReader(pdf_file, strict=False)
    except Exception as e:
        print(f"✗ Unable to read PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"Loaded PDF with {len(reader.pages)} pages\n")

    # ---------- Requirement 1: Stamp annotations ----------
    stamped = 0
    for idx in TARGET_PAGES:
        if idx >= len(reader.pages):
            print(f"✗ Target page {idx+1} is out of range (document has {len(reader.pages)} pages)")
            continue
        if page_has_stamp(reader.pages[idx]):
            print(f"✓ Stamp annotation detected on page {idx+1}")
            stamped += 1
        else:
            print(f"✗ No stamp annotation on page {idx+1}")

    stamp_score = (stamped / len(TARGET_PAGES)) * STAMP_WEIGHT

    # ---------- Requirement 2: 'REVIEWED' keyword occurrences ----------
    raw_bytes = pdf_file.read_bytes().upper()
    keyword_hits = raw_bytes.count(STAMP_KEYWORD.encode().upper())
    print(f"\nFound '{STAMP_KEYWORD}' {keyword_hits} time(s) in PDF byte stream")

    capped_hits = min(keyword_hits, len(TARGET_PAGES))  # cap to prevent gaming
    text_score = (capped_hits / len(TARGET_PAGES)) * TEXT_WEIGHT

    # ---------- Final score ----------
    total_score = round(min(stamp_score + text_score, 1.0), 3)

    print("\nScore breakdown:")
    print(f"  Stamp presence score : {stamp_score:.3f} / {STAMP_WEIGHT}")
    print(f"  Keyword text score   : {text_score:.3f} / {TEXT_WEIGHT}")
    print(f"  TOTAL SCORE          : {total_score}")

    print(f"REWARD: {total_score}")
    return total_score


if __name__ == "__main__":
    verify_task(PDF_PATH)


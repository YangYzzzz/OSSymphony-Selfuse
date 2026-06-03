"""
FINAL REWARD SCRIPT - SUCCESS
Task: Batch flatten all fillable forms in /home/user/Documents/CompletedForms, saving flattened versions in folder 'Forms_Final'.
Generated: 2025-11-29 10:15:23
Status: success
Model: o3
Total Steps: 10
"""

from pathlib import Path
from PyPDF2 import PdfReader

# -------------------------------------------------------------
# Reward Script : Batch Flatten Verification
# -------------------------------------------------------------
# This script verifies that every fillable form PDF originally
# located in /home/user/Documents/CompletedForms has been
# flattened and saved with the *same filename* inside the
# sub-folder  "Forms_Final".  
# A PDF is considered *flattened* when:
#   1. A corresponding file exists in Forms_Final            (40%)
#   2. The flattened file contains **no** AcroForm fields or
#      widget annotations (i.e., truly non-interactive)       (40%)
#   3. The page-count of the flattened PDF matches the
#      original (ensures no pages were lost)                  (20%)
# A progressive score is produced based on the file-by-file
# ratios for the three checks above.  When ALL originals are
# successfully flattened the script returns exactly 1.0.
# -------------------------------------------------------------

def pdf_has_form_fields(reader: PdfReader) -> bool:
    """Return True if the PDF still contains any AcroForm fields
    or /Widget annotations."""
    # Global AcroForm dictionary
    if reader.get_fields():
        return True

    # Page-level widget annotations
    for page in reader.pages:
        annots = page.get("/Annots")
        if not annots:
            continue
        for annot_ref in annots:
            annot = annot_ref.get_object()
            if annot.get("/Subtype") == "/Widget":
                return True

    return False


def verify_task() -> float:
    base_dir = Path("/home/user/Documents/CompletedForms")
    final_dir = base_dir / "Forms_Final"

    original_pdfs = sorted(base_dir.glob("*.pdf"))
    if not original_pdfs:
        print(f"✗ No source PDFs found in {base_dir}")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found {len(original_pdfs)} original PDF(s) to verify.")

    exist_ok = 0      # flattened file exists
    flattened_ok = 0  # no form fields remaining
    page_ok = 0       # page count preserved

    for orig_path in original_pdfs:
        dest_path = final_dir / orig_path.name
        print(f"\nChecking '{orig_path.name}':")

        # -------------- Existence Check --------------
        if dest_path.exists():
            print("  ✓ Flattened file exists")
            exist_ok += 1
        else:
            print("  ✗ Flattened file missing ->", dest_path)
            continue  # cannot evaluate other criteria without file

        # -------------- Load PDFs --------------
        try:
            orig_reader = PdfReader(str(orig_path))
            dest_reader = PdfReader(str(dest_path))
        except Exception as e:
            print("  ✗ Error opening PDF(s):", e)
            continue

        # -------------- Page Count Check --------------
        if len(orig_reader.pages) == len(dest_reader.pages):
            print("  ✓ Page count preserved")
            page_ok += 1
        else:
            print("  ✗ Page count differs (orig:", len(orig_reader.pages), "dest:", len(dest_reader.pages), ")")

        # -------------- Flatten Check --------------
        if not pdf_has_form_fields(dest_reader):
            print("  ✓ No AcroForm fields present – PDF is flattened")
            flattened_ok += 1
        else:
            print("  ✗ Form fields still present – NOT flattened")

    # -------------------- Scoring --------------------
    total = len(original_pdfs)
    exist_ratio = exist_ok / total
    flattened_ratio = flattened_ok / total
    page_ratio = page_ok / total

    # Weighted progressive scoring
    score = 0.4 * exist_ratio + 0.4 * flattened_ratio + 0.2 * page_ratio
    score = round(min(score, 1.0), 3)

    print("\nSummary Ratios → existence: {:.2f}, flattened: {:.2f}, page-count: {:.2f}".format(exist_ratio, flattened_ratio, page_ratio))
    print(f"REWARD: {score}")

    return score

# -------------------- Execute Verification --------------------
if __name__ == "__main__":
    verify_task()


"""
FINAL REWARD SCRIPT - SUCCESS
Task: Add a freehand drawing annotation circling the problem area in the diagram on page 6 of 'engineering_design.pdf' in /home/user/Projects.
Generated: 2025-11-29 09:54:58
Status: success
Model: o3
Total Steps: 9
"""

from pathlib import Path
from typing import List
from PyPDF2 import PdfReader

"""
Reward script for:
Instruction: "Add a freehand drawing annotation circling the problem area in the diagram on page 6 of 'engineering_design.pdf' in /home/user/Projects."

Verification logic (progressive scoring up to 1.0):
 1. PDF must exist & be readable                       (prerequisite, no points)
 2. Page-6 must contain at least one /Ink annotation   (+0.6)
 3. The /Ink annotation should be sufficiently complex
    (>=8 coordinate pairs → resembles a circle)       (+0.2)
 4. No additional /Ink annotations on other pages      (+0.2)

Total = 1.0 when all four conditions satisfied.
The script prints detailed diagnostics and the final
"REWARD: <score>" line as required.
"""

# ---------- CONFIGURATION ----------
PDF_PATH = Path("/home/user/Projects/engineering_design.pdf")
TARGET_PAGE_NUM = 6           # 1-based page number mentioned in the task
MIN_POINTS_FOR_COMPLEX_SHAPE = 16  # 8 coordinate pairs

# ---------- VERIFICATION HELPERS ----------

def get_ink_annotations(page) -> List[dict]:
    """Return list of /Ink annotation dictionaries on the given page."""
    annotations = page.get("/Annots") or []
    ink_list = []
    for ref in annotations:
        annot = ref.get_object()
        if annot.get("/Subtype") == "/Ink":
            ink_list.append(annot)
    return ink_list

# ---------- MAIN VERIFICATION FUNCTION ----------

def verify_freehand_circle(pdf_path: Path) -> float:
    print(f"Verifying freehand annotation in: {pdf_path}")

    # ---------------- Basic checks ----------------
    if not pdf_path.exists():
        print("✗ PDF is missing – task not completed")
        print("REWARD: 0.0")
        return 0.0

    try:
        reader = PdfReader(str(pdf_path))
    except Exception as exc:
        print(f"✗ Could not open PDF: {exc}")
        print("REWARD: 0.0")
        return 0.0

    total_pages = len(reader.pages)
    print(f"PDF page count: {total_pages}")

    target_idx = TARGET_PAGE_NUM - 1  # zero-based index
    if total_pages <= target_idx:
        print("✗ PDF does not have the required page 6")
        print("REWARD: 0.0")
        return 0.0

    score = 0.0
    max_score = 1.0

    # ---------------- Requirement 1 ----------------
    target_page = reader.pages[target_idx]
    ink_annots = get_ink_annotations(target_page)
    if ink_annots:
        score += 0.6
        print(f"✓ Found {len(ink_annots)} ink annotation(s) on page 6 (+0.6)")
    else:
        print("✗ No ink annotation on page 6 (0 points)")

    # ---------------- Requirement 2 ----------------
    complex_enough = False
    for annot in ink_annots:
        inklist = annot.get("/InkList")
        if inklist and len(inklist[0]) >= MIN_POINTS_FOR_COMPLEX_SHAPE:
            complex_enough = True
            break

    if ink_annots and complex_enough:
        score += 0.2
        print("✓ Ink annotation appears freehand/complex enough (+0.2)")
    elif ink_annots:
        print("✗ Ink annotation too simple to be a circle (0 points)")

    # ---------------- Requirement 3 ----------------
    extra_inks = 0
    for idx, page in enumerate(reader.pages):
        if idx == target_idx:
            continue  # Skip target page
        extra_inks += len(get_ink_annotations(page))

    if ink_annots and extra_inks == 0:
        score += 0.2
        print("✓ No extra ink annotations on other pages (+0.2)")
    elif ink_annots:
        print(f"✗ Found {extra_inks} extra ink annotation(s) on other pages (0 points)")

    final_score = min(score, max_score)
    print(f"REWARD: {final_score}")
    return final_score

# ---------- EXECUTION ENTRY POINT ----------
if __name__ == "__main__":
    verify_freehand_circle(PDF_PATH)

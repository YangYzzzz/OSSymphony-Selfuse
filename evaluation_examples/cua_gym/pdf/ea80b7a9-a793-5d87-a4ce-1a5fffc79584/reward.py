"""
FINAL REWARD SCRIPT - SUCCESS
Task: Remove password protection and also remove the 'DRAFT' watermark from 'protected_draft.pdf' (password: 'temp123') in /home/user/Documents. Save as 'final_clean.pdf'.
Generated: 2025-11-29 09:52:30
Status: success
Model: o3
Total Steps: 16
"""

from pathlib import Path
from PyPDF2 import PdfReader
import re

# ------------ Utility helpers ------------

def normalize_text(text: str) -> str:
    """Lower-case and collapse whitespace so minor layout
    differences don’t affect equality checks."""
    if text is None:
        return ""
    return re.sub(r"\s+", " ", text).strip().lower()


def page_contains_draft_annotation(page) -> bool:
    """Return True if the page contains an annotation/stamp whose
    contents or subtype mentions the word *draft*."""
    annots = page.get("/Annots") or []
    for annot_ref in annots:
        try:
            annot = annot_ref.get_object()
        except Exception:
            continue
        contents = str(annot.get("/Contents") or "")
        subtype  = str(annot.get("/Subtype") or "")
        if "draft" in contents.lower() or "draft" in subtype.lower():
            return True
    return False

# ------------ Core verification ------------

def verify_task() -> float:
    """Verify that password protection was removed and the DRAFT watermark
    (text or annotation) is gone from the PDF, and optionally compare to the
    golden reference provided by the grader."""

    final_pdf  = Path("/home/user/Documents/final_clean.pdf")
    golden_pdf = Path(
        "/home/user/remove_password_protection_and_also_remove_the_draft_watermark_from_protected_draftpdf_password_temp_golden.pdf"
    )

    max_score = 1.0
    score     = 0.0

    print("Verifying task ‘Remove password & DRAFT watermark’\n")

    # -------- 1) File exists --------
    if not final_pdf.exists():
        print(f"✗ Expected output not found: {final_pdf}")
        print("REWARD: 0.0")
        return 0.0
    print(f"✓ Output PDF located: {final_pdf}")

    # -------- 2) Encryption removed --------
    try:
        reader = PdfReader(final_pdf)
    except Exception as e:
        print(f"✗ Cannot open PDF (likely still encrypted): {e}")
        print("REWARD: 0.0")
        return 0.0

    if reader.is_encrypted:
        opened = False
        for pwd in ("", "temp123"):
            try:
                opened = reader.decrypt(pwd) == 1
            except Exception:
                opened = False
            if opened:
                break
        print("✗ PDF still reports as encrypted – no credit for de-protection")
    else:
        print("✓ PDF is unencrypted (0.3)")
        score += 0.3

    pages = reader.pages  # still accessible even if encryption flag remains

    # -------- 3) ‘DRAFT’ text removed --------
    draft_text_present = False
    for page_no, page in enumerate(pages, 1):
        text = (page.extract_text() or "").lower()
        if "draft" in text:
            draft_text_present = True
            print(f"   Found ‘DRAFT’ text on page {page_no}")
    if not draft_text_present:
        print("✓ No ‘DRAFT’ text detected (0.25)")
        score += 0.25
    else:
        print("✗ ‘DRAFT’ text still present – no points for removal")

    # -------- 4) ‘DRAFT’ annotations/stamps removed --------
    draft_annot_present = False
    for page_no, page in enumerate(pages, 1):
        if page_contains_draft_annotation(page):
            draft_annot_present = True
            print(f"   Found ‘DRAFT’ annotation on page {page_no}")
    if not draft_annot_present:
        print("✓ No ‘DRAFT’ annotations/stamps detected (0.25)")
        score += 0.25
    else:
        print("✗ ‘DRAFT’ annotations still present – no points for removal")

    # -------- 5) Content matches golden reference (bonus) --------
    if golden_pdf.exists():
        try:
            gold_reader = PdfReader(golden_pdf)
            if gold_reader.is_encrypted:
                gold_reader.decrypt("")
            if len(gold_reader.pages) != len(pages):
                print(
                    f"✗ Page count mismatch with golden (final={len(pages)}, golden={len(gold_reader.pages)})"
                )
            else:
                identical = True
                for idx, (pf, pg) in enumerate(zip(pages, gold_reader.pages), 1):
                    if normalize_text(pf.extract_text()) != normalize_text(pg.extract_text()):
                        identical = False
                        print(f"   Text differs on page {idx}")
                        break
                if identical:
                    print("✓ PDF content matches golden reference (0.2)")
                    score += 0.2
                else:
                    print("✗ Content differs from golden – no bonus")
        except Exception as e:
            print(f"   Warning: comparison with golden failed: {e}")
    else:
        print("Golden reference not present – skipping 0.2 bonus check")

    # -------- Final score --------
    final_score = round(min(score, max_score), 2)
    print(f"\nTOTAL SCORE: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task()

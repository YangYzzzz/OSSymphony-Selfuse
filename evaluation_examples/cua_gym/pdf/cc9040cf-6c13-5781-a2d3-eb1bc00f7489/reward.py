"""
FINAL REWARD SCRIPT - SUCCESS
Task: I need to add a sticky note annotation saying 'Call author for clarification' on page 15 of 'peer_review.pdf' on Desktop.
Generated: 2025-11-29 09:56:21
Status: success
Model: o3
Total Steps: 4
"""

from __future__ import annotations
"""
Reward Script for PDF Annotation Verification
Task: Ensure that a sticky-note ("/Text" subtype) annotation containing the
exact phrase "Call author for clarification" exists on page 15 of
"peer_review.pdf" located on the Desktop.

Scoring (progressive):
  • +0.3 ⇒ At least one annotation present on page 15.
  • +0.4 ⇒ An annotation on that page whose /Contents text matches the
             required phrase (case-insensitive).
  • +0.3 ⇒ The matching annotation’s /Subtype is "/Text" (i.e., sticky note).
Total possible = 1.0.
The script prints detailed diagnostics and always outputs "REWARD: X.X" where
X.X ∈ [0.0, 1.0].
"""

from pathlib import Path
from typing import Union, Optional
from PyPDF2 import PdfReader

# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

def _safe_to_str(obj: Union[str, bytes, None]) -> str:
    """Convert PDF string/bytes to plain str safely."""
    if obj is None:
        return ""
    if isinstance(obj, bytes):
        try:
            return obj.decode("utf-8", errors="ignore")
        except Exception:
            return str(obj)
    return str(obj)


def verify_sticky_note(
    pdf_path: str | Path,
    target_phrase: str = "Call author for clarification",
    target_page: int = 15,
) -> float:
    """Verify task completion and return a progressive score ∈ [0.0, 1.0]."""

    pdf_path = Path(pdf_path)
    max_score = 1.0
    score = 0.0

    # ---------------------------------------------------------------------
    # Load PDF safely
    # ---------------------------------------------------------------------
    try:
        reader = PdfReader(str(pdf_path))
        print(f"Loaded PDF: {pdf_path} ({len(reader.pages)} pages)")
    except Exception as exc:
        print(f"✗ Failed to load PDF: {exc}")
        print("REWARD: 0.0")
        return 0.0

    # ---------------------------------------------------------------------
    # 1) Ensure the requested page exists
    # ---------------------------------------------------------------------
    if len(reader.pages) < target_page:
        print(
            f"✗ PDF has {len(reader.pages)} pages; page {target_page} is missing."
        )
        print("REWARD: 0.0")
        return 0.0

    page_index = target_page - 1  # zero-based index
    page = reader.pages[page_index]

    # ---------------------------------------------------------------------
    # 2) Collect page annotations
    # ---------------------------------------------------------------------
    annots = page.get("/Annots") or []
    if not annots:
        print(f"✗ No annotations found on page {target_page}.")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found {len(annots)} annotation(s) on page {target_page}.")

    # Track verification flags
    has_annotation = True  # we already know at least one exists
    has_matching_content = False
    has_text_subtype = False

    # ---------------------------------------------------------------------
    # 3) Inspect each annotation
    # ---------------------------------------------------------------------
    phrase_lower = target_phrase.lower()
    for ref in annots:
        try:
            annot = ref.get_object()
        except Exception as exc:
            print(f"  - Warning: Could not dereference annotation: {exc}")
            continue

        subtype: Optional[str] = annot.get("/Subtype")
        contents_raw = annot.get("/Contents")
        contents = _safe_to_str(contents_raw)

        print(
            f"  - Annotation → Subtype: {subtype}, Contents: "
            f"{contents[:60] if contents else '[EMPTY]'}"
        )

        # Content match check (case-insensitive, substring)
        if phrase_lower in contents.lower():
            has_matching_content = True
            if subtype == "/Text":
                has_text_subtype = True

    # ---------------------------------------------------------------------
    # 4) Scoring
    # ---------------------------------------------------------------------
    if has_annotation:
        score += 0.3
        print("✓ Annotation present on target page (+0.3)")

    if has_matching_content:
        score += 0.4
        print("✓ Annotation contains required phrase (+0.4)")
    else:
        print("✗ No annotation with matching content (+0.0)")

    if has_matching_content and has_text_subtype:
        score += 0.3
        print("✓ Matching annotation is a sticky note (/Text) (+0.3)")
    elif has_matching_content:
        print("✗ Matching annotation is not subtype /Text (+0.0)")

    final = min(score, max_score)
    print(f"Total score: {final}/{max_score}")
    print(f"REWARD: {final}")
    return final


# ---------------------------------------------------------------------------
# Main Execution
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Expected PDF location (per task description)
    DEFAULT_PDF_PATH = "/home/user/Desktop/peer_review.pdf"
    verify_sticky_note(DEFAULT_PDF_PATH)


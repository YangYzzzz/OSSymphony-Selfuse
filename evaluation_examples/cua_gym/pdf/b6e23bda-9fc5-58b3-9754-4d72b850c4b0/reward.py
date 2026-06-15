"""
FINAL REWARD SCRIPT - SUCCESS
Task: I need to add multiple comment annotations to 'student_essay.pdf' on Desktop: 'Good point' on page 2, 'Needs citation' on page 4, and 'Expand this' on page 7.
Generated: 2025-11-29 09:57:53
Status: success
Model: o3
Total Steps: 7
"""

from pathlib import Path
from typing import List, Tuple
from PyPDF2 import PdfReader

"""
Reward script for verifying that the user added three specific comment annotations to
"student_essay.pdf" located on the Desktop.

Expected annotations (page numbers are 1-based in the task description):
  • Page 2 : "Good point"
  • Page 4 : "Needs citation"
  • Page 7 : "Expand this"

Scoring:
  – Each correctly placed annotation is worth 1/3 of the total score.
  – The script returns a float between 0.0 and 1.0 (inclusive).

No points are given for merely existing files or default PDF structure – only for the
actual presence of the correct annotations on the correct pages.
"""

def _find_pdf_path() -> Path | None:
    """Return the first existing path that matches expected PDF locations."""
    candidates = [
        # Primary evaluation path from the task description (may or may not exist)
        Path(
            "/home/user/i_need_to_add_multiple_comment_annotations_to_student_essaypdf_on_desktop_good_point_on_page_2_needs_golden.pdf"
        ),
        # Most common location where the working file should be
        Path("/home/user/Desktop/student_essay.pdf"),
        # Fallback in case it was saved elsewhere in the home directory
        Path("/home/user/student_essay.pdf"),
    ]
    for p in candidates:
        if p.exists():
            return p.resolve()
    return None


def _annotation_exists_on_page(page, expected_text: str) -> bool:
    """Return True if a /Text annotation with the exact expected text exists on the page."""
    annots = page.get("/Annots")
    if not annots:
        return False

    for annot_ref in annots:
        annot = annot_ref.get_object()
        contents = annot.get("/Contents")
        if contents is None:
            continue
        try:
            contents_str = str(contents)
        except Exception:
            # If conversion fails, skip this annotation
            continue
        if contents_str.strip().lower() == expected_text.strip().lower():
            return True
    return False


def verify_task() -> float:
    """Main verification routine. Prints diagnostic output and returns the reward score."""

    pdf_path = _find_pdf_path()
    if not pdf_path:
        print("✗ Could not locate the target PDF file in expected locations.")
        print("REWARD: 0.0")
        return 0.0

    print(f"Using PDF file: {pdf_path}")

    # Attempt to load the PDF
    try:
        reader = PdfReader(str(pdf_path))
    except Exception as e:
        print(f"✗ Failed to load PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # (page_index, expected_contents) pairs — page_index is 0-based for PyPDF2
    expected_annotations: List[Tuple[int, str]] = [
        (1, "Good point"),      # Page 2 in 1-based notation
        (3, "Needs citation"),  # Page 4
        (6, "Expand this"),     # Page 7
    ]

    total_expected = len(expected_annotations)
    matches = 0

    for page_idx, text in expected_annotations:
        if page_idx >= len(reader.pages):
            print(
                f"✗ PDF has only {len(reader.pages)} pages; expected page {page_idx + 1} is missing."
            )
            continue

        page = reader.pages[page_idx]
        if _annotation_exists_on_page(page, text):
            print(f"✓ Annotation '{text}' found on page {page_idx + 1}.")
            matches += 1
        else:
            print(f"✗ Annotation '{text}' NOT found on page {page_idx + 1}.")

    # Progressive scoring: each correct annotation contributes equally
    score = matches / total_expected
    print(f"Total correct annotations: {matches}/{total_expected}")
    print(f"REWARD: {score}")
    return score


# Run verification when executed as a script
if __name__ == "__main__":
    verify_task()


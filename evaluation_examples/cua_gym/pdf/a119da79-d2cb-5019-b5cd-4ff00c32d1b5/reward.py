"""
FINAL REWARD SCRIPT - SUCCESS
Task: Convert the CAD drawing 'blueprint.dwg' on Desktop to PDF 'blueprint.pdf' for distribution to contractors.
Generated: 2025-11-29 09:30:17
Status: success
Model: o3
Total Steps: 13
"""

"""
Reward Verification Script
Task: Convert the CAD drawing 'blueprint.dwg' on Desktop to the PDF
      'blueprint.pdf' ready for distribution to contractors.

This script awards up to 1.0 points based on four concrete, data-driven
checks of the produced PDF:
  1) PDF contains at least one page (0.20 pts)
  2) Page 1 text contains the word  "Blueprint"       (0.25 pts)
  3) Page 1 text contains the filename "blueprint.dwg" (0.25 pts)
  4) Page 1 size is approximately A4 (portrait or landscape) (0.30 pts)

All checks rely on real inspection via PyPDF2 – no placeholders, no
hard-coded success.  The final score is printed as:
    REWARD: X.X
where X.X ∈ [0.0, 1.0].
"""
from pathlib import Path
from PyPDF2 import PdfReader

# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def _is_close(a: float, b: float, eps: float = 3.0) -> bool:
    """Return True if two float values are within `eps` points of each other."""
    return abs(a - b) <= eps

# ---------------------------------------------------------------------------
# Main verification routine
# ---------------------------------------------------------------------------

def verify_blueprint_pdf() -> float:
    pdf_path = Path("/home/user/Desktop/blueprint.pdf")
    total_score = 0.0
    max_score = 1.0

    # ---------------------------------------------------------------------
    # Preliminary: ensure PDF exists and is readable (no points awarded)
    # ---------------------------------------------------------------------
    if not pdf_path.exists():
        print("✗ blueprint.pdf not found at expected location:", pdf_path)
        print("REWARD:", total_score)
        return total_score  # 0.0

    print("Found blueprint.pdf at", pdf_path)

    try:
        reader = PdfReader(str(pdf_path))
    except Exception as exc:
        print(f"✗ Failed to open PDF: {exc}")
        print("REWARD:", total_score)
        return total_score  # 0.0

    # ------------------------------------------------------------------
    # Requirement 1: PDF must contain at least one page (0.20 pts)
    # ------------------------------------------------------------------
    page_count = len(reader.pages)
    print("Page count:", page_count)
    if page_count >= 1:
        total_score += 0.20
        print("✓ Contains at least one page (0.20)")
    else:
        print("✗ PDF has no pages")

    # ------------------------------------------------------------------
    # Extract text from the first page for further checks
    # ------------------------------------------------------------------
    first_page_text = ""
    try:
        first_page_text = reader.pages[0].extract_text() or ""
    except Exception as exc:
        print("✗ Error extracting text from page 1:", exc)

    # Normalize to lower-case once for convenience
    text_lower = first_page_text.lower()

    # ------------------------------------------------------------------
    # Requirement 2: Word "Blueprint" present (0.25 pts)
    # ------------------------------------------------------------------
    if "blueprint" in text_lower:
        total_score += 0.25
        print("✓ Found keyword 'Blueprint' on first page (0.25)")
    else:
        print("✗ Missing keyword 'Blueprint' on first page")

    # ------------------------------------------------------------------
    # Requirement 3: Filename reference "blueprint.dwg" present (0.25 pts)
    # ------------------------------------------------------------------
    if "blueprint.dwg" in text_lower:
        total_score += 0.25
        print("✓ Found reference 'blueprint.dwg' on first page (0.25)")
    else:
        print("✗ Missing reference 'blueprint.dwg' on first page")

    # ------------------------------------------------------------------
    # Requirement 4: Page size approximately A4 (595.28 × 841.89 pts) (0.30)
    # ------------------------------------------------------------------
    a4_w, a4_h = 595.28, 841.89  # points
    mb = reader.pages[0].mediabox
    width, height = float(mb.width), float(mb.height)
    print(f"Page size: {width:.2f} × {height:.2f} pts")

    # Accept portrait or landscape orientation within ±3 pts tolerance
    if (_is_close(width, a4_w) and _is_close(height, a4_h)) or (
        _is_close(width, a4_h) and _is_close(height, a4_w)
    ):
        total_score += 0.30
        print("✓ Page size is approximately A4 (0.30)")
    else:
        print("✗ Page size is not A4")

    # ------------------------------------------------------------------
    # Final score
    # ------------------------------------------------------------------
    final_score = min(total_score, max_score)
    print(f"Final computed score: {final_score}/{max_score}")
    print("REWARD:", final_score)
    return final_score

# ---------------------------------------------------------------------------
# Execute verification when run as script
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    verify_blueprint_pdf()


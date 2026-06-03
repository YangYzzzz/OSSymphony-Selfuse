"""
FINAL REWARD SCRIPT - SUCCESS
Task: Convert the fillable form 'interactive_form.pdf' in /home/user/Documents to a static PDF 'static_form.pdf' by flattening all form fields and annotations.
Generated: 2025-11-29 10:03:46
Status: success
Model: o3
Total Steps: 3
"""

from pathlib import Path
from PyPDF2 import PdfReader

# -----------------------------------------------------------------------------
# Reward Script: verify that a fillable form was flattened into a static PDF
# -----------------------------------------------------------------------------
# Task recap:
#   Interactive source: /home/user/Documents/interactive_form.pdf
#   Expected output   : /home/user/Documents/static_form.pdf (all fields/annots flattened)
#
# Verification strategy:
#   1. Confirm the interactive PDF really contains AcroForm fields – otherwise the
#      task would be meaningless.
#   2. Ensure the generated static PDF contains *zero* AcroForm fields.
#   3. Ensure the static PDF contains *zero* annotations (widgets, etc.).
#   4. Verify page-count parity between source and output.
#   5. Award progressive points, reaching 1.0 only when every check passes.
# -----------------------------------------------------------------------------

INTERACTIVE_PATH = Path("/home/user/Documents/interactive_form.pdf")
STATIC_PATH      = Path("/home/user/Documents/static_form.pdf")


def _annotation_count(reader: PdfReader) -> int:
    """Count all /Annots references across the entire PDF."""
    count = 0
    for page in reader.pages:
        annots = page.get("/Annots") or []
        count += len(annots)
    return count


def verify_flatten(interactive_path: Path = INTERACTIVE_PATH, static_path: Path = STATIC_PATH) -> float:
    """Verifies that `static_path` is a flattened version of `interactive_path`.

    Returns a progressive score between 0.0 and 1.0 and prints details.
    """
    total_score = 0.0
    MAX_SCORE   = 1.0

    # ------------------------------------------------------------------
    # Load PDFs (no points for just loading – prerequisite)
    # ------------------------------------------------------------------
    try:
        inter_reader  = PdfReader(str(interactive_path))
        static_reader = PdfReader(str(static_path))
    except Exception as exc:
        print(f"✗ Error opening PDFs: {exc}")
        print("REWARD: 0.0")
        return 0.0

    # ------------------------------------------------------------------
    # 1) Ensure the source really had form fields (0.2 pts)
    # ------------------------------------------------------------------
    inter_fields = inter_reader.get_fields() or {}
    if inter_fields:
        print(f"✓ Interactive PDF has {len(inter_fields)} form field(s)")
        total_score += 0.2
    else:
        print("✗ Interactive PDF contains no form fields – cannot validate flattening")

    # ------------------------------------------------------------------
    # 2) Verify NO form fields remain in static PDF (0.4 pts)
    # ------------------------------------------------------------------
    static_fields = static_reader.get_fields() or {}
    if not static_fields:
        print("✓ Static PDF has no form fields (flattened)")
        total_score += 0.4
    else:
        print(f"✗ Static PDF still contains {len(static_fields)} form field(s)")

    # ------------------------------------------------------------------
    # 3) Verify NO annotations remain (0.3 pts)
    # ------------------------------------------------------------------
    static_annots = _annotation_count(static_reader)
    if static_annots == 0:
        print("✓ Static PDF contains no annotations")
        total_score += 0.3
    else:
        print(f"✗ Static PDF still has {static_annots} annotation(s)")

    # ------------------------------------------------------------------
    # 4) Page-count parity (0.1 pts)
    # ------------------------------------------------------------------
    if len(inter_reader.pages) == len(static_reader.pages) and len(static_reader.pages) > 0:
        print(f"✓ Page count preserved ({len(static_reader.pages)} page(s))")
        total_score += 0.1
    else:
        print(
            f"✗ Page count mismatch (interactive={len(inter_reader.pages)}, static={len(static_reader.pages)})"
        )

    # ------------------------------------------------------------------
    # Final score output
    # ------------------------------------------------------------------
    final_score = min(total_score, MAX_SCORE)
    print(f"REWARD: {final_score}")
    return final_score


# -----------------------------------------------------------------------------
# Execute verification when script is run directly
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    verify_flatten()


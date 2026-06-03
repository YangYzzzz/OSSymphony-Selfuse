"""
FINAL REWARD SCRIPT - SUCCESS
Task: Remove pages 5, 8, and 12 from 'draft_report.pdf' in /home/user/Documents and save as 'final_report.pdf'.
Generated: 2025-11-29 09:44:36
Status: success
Model: o3
Total Steps: 3
"""

from pathlib import Path
import re
from PyPDF2 import PdfReader

# -------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------

def _normalize(text: str) -> str:
    """Collapse whitespace for reliable text comparison."""
    if text is None:
        return ""
    return re.sub(r"\s+", " ", text.strip())


def _extract_texts(reader: PdfReader) -> list[str]:
    """Return a list with extracted text from every page."""
    texts = []
    for page in reader.pages:
        try:
            txt = page.extract_text() or ""
        except Exception:
            txt = ""
        texts.append(txt)
    return texts


def _compare_page_texts(list_a: list[str], list_b: list[str]):
    """Compare two page-text lists; return (bool, message)."""
    if len(list_a) != len(list_b):
        return False, f"Page count differs: {len(list_a)} vs {len(list_b)}"
    for idx, (ta, tb) in enumerate(zip(list_a, list_b), start=1):
        if _normalize(ta) != _normalize(tb):
            return False, f"Text differs on page {idx}"
    return True, "All pages match"


def _expected_from_draft(draft_reader: PdfReader) -> list[str]:
    """Generate the expected page list by removing pages 5, 8, and 12 (1-based)."""
    removal_indices = {4, 7, 11}  # convert to 0-based
    texts = _extract_texts(draft_reader)
    return [txt for idx, txt in enumerate(texts) if idx not in removal_indices]

# -------------------------------------------------------------
# Main verification function
# -------------------------------------------------------------

def verify_task() -> float:
    """Verify that pages 5, 8 & 12 were removed and saved as final_report.pdf."""
    # Scoring weights (must sum to 1.0)
    W_EXIST = 0.2      # final_report.pdf exists & readable
    W_PCOUNT = 0.2     # page count correct
    W_CONTENT = 0.6    # content matches expected

    score = 0.0

    draft_path = Path('/home/user/Documents/draft_report.pdf')
    final_path = Path('/home/user/Documents/final_report.pdf')
    golden_path = Path('/home/user/remove_pages_5_8_and_12_from_draft_reportpdf_in_homeuserdocuments_and_save_as_final_reportpdf_golden.pdf')

    # ---------------------------------------------------------
    # 1. Final PDF must exist and be readable
    # ---------------------------------------------------------
    if not final_path.exists():
        print('✗ final_report.pdf not found')
        print('REWARD: 0.0')
        return 0.0

    try:
        final_reader = PdfReader(str(final_path))
        final_texts = _extract_texts(final_reader)
        final_pages = len(final_texts)
        print(f"✓ Found final_report.pdf with {final_pages} pages (+{W_EXIST})")
        score += W_EXIST
    except Exception as exc:
        print(f"✗ Unable to read final_report.pdf: {exc}")
        print(f"REWARD: {score}")
        return score

    # ---------------------------------------------------------
    # 2. Determine expected page texts
    #    Prefer official golden PDF; fall back to draft removal logic
    # ---------------------------------------------------------
    expected_texts = None
    expectation_source = None

    if golden_path.exists():
        try:
            golden_reader = PdfReader(str(golden_path))
            expected_texts = _extract_texts(golden_reader)
            expectation_source = 'golden'
            print('✓ Loaded golden PDF for comparison')
        except Exception as exc:
            print(f"✗ Failed to read golden PDF: {exc}")

    if expected_texts is None and draft_path.exists():
        try:
            draft_reader = PdfReader(str(draft_path))
            expected_texts = _expected_from_draft(draft_reader)
            expectation_source = 'draft-minus-pages'
            print('✓ Derived expected pages from draft PDF')
        except Exception as exc:
            print(f"✗ Failed to derive expected pages from draft: {exc}")

    if expected_texts is None:
        print('✗ Could not establish expected PDF content')
        print(f"REWARD: {score}")
        return score

    # ---------------------------------------------------------
    # 3. Verify page count
    # ---------------------------------------------------------
    if final_pages == len(expected_texts):
        print(f"✓ Page count matches expected ({final_pages}) (+{W_PCOUNT})")
        score += W_PCOUNT
    else:
        print(f"✗ Page count mismatch: expected {len(expected_texts)}, got {final_pages}")

    # ---------------------------------------------------------
    # 4. Verify page-level text content
    # ---------------------------------------------------------
    pages_match, msg = _compare_page_texts(final_texts, expected_texts)
    if pages_match:
        print(f"✓ Page content matches expected (+{W_CONTENT}) [source: {expectation_source}]")
        score += W_CONTENT
    else:
        print(f"✗ Page content mismatch: {msg}")

    # ---------------------------------------------------------
    # Final score and reporting
    # ---------------------------------------------------------
    final_score = min(score, 1.0)
    print(f"Total score: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score

# Run verification when script is executed directly
if __name__ == '__main__':
    verify_task()


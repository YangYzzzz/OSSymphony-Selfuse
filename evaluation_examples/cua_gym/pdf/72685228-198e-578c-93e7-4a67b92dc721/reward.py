"""
Reward Script: Linearize PDF for fast web viewing
Task ID: pdf_mbc_026
Domain: pdf
Scoring:
  Component 1 (0.25): Output file exists and is a valid PDF
  Component 2 (0.25): Page count matches original (200 pages)
  Component 3 (0.30): Output is linearized
  Component 4 (0.20): Text content matches original (spot-check pages)
"""

import os
import sys

WORKDIR = '/home/user/Documents'
TASK_ID = 'pdf_mbc_026'
ORIGINAL_PATH = os.path.join(WORKDIR, 'large_manual.pdf')
OUTPUT_PATH = os.path.join(WORKDIR, 'large_manual_web.pdf')


def ensure_pikepdf():
    """Install pikepdf if not available."""
    try:
        import pikepdf
        return pikepdf
    except ImportError:
        os.system('pip3 install pikepdf -q')
        import pikepdf
        return pikepdf


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: original file must exist
    if not os.path.exists(ORIGINAL_PATH):
        print(f"CRITICAL: Original file not found: {ORIGINAL_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: output file must exist (gate, not scored yet)
    if not os.path.exists(OUTPUT_PATH):
        print(f"FAIL: Output file not found: {OUTPUT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output is a valid, loadable PDF (0.25 points)
    try:
        import pymupdf
        doc_out = pymupdf.open(OUTPUT_PATH)
        page_count_out = len(doc_out)
        if page_count_out > 0:
            print(f"PASS: Component 1 - Output is a valid PDF with {page_count_out} pages (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 - Output PDF has 0 pages")
            doc_out.close()
            print(f"REWARD: {total_score}")
            return total_score
        doc_out.close()
    except Exception as e:
        print(f"ERROR: Component 1 - Cannot load output PDF: {e}")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Page count matches original (0.25 points)
    try:
        import pymupdf
        doc_orig = pymupdf.open(ORIGINAL_PATH)
        page_count_orig = len(doc_orig)
        doc_orig.close()

        if page_count_out == page_count_orig:
            print(f"PASS: Component 2 - Page count matches original ({page_count_orig} pages) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 - Page count mismatch: output={page_count_out}, original={page_count_orig}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Output is linearized (0.30 points)
    try:
        pikepdf = ensure_pikepdf()
        pdf = pikepdf.open(OUTPUT_PATH)
        is_linearized = pdf.is_linearized
        pdf.close()

        if is_linearized:
            print(f"PASS: Component 3 - Output PDF is linearized (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 - Output PDF is NOT linearized")
    except Exception as e:
        print(f"ERROR: Component 3 - Could not check linearization: {e}")

    # Component 4: Text content matches original (spot-check) (0.20 points)
    try:
        import pymupdf
        doc_orig = pymupdf.open(ORIGINAL_PATH)
        doc_out = pymupdf.open(OUTPUT_PATH)

        # Spot-check pages: first, middle, last
        check_pages = [0, 1, 99, 199]
        matches = 0
        checked = 0
        for p in check_pages:
            if p < len(doc_orig) and p < len(doc_out):
                orig_text = doc_orig[p].get_text().strip()
                out_text = doc_out[p].get_text().strip()
                checked += 1
                if orig_text == out_text:
                    matches += 1
                else:
                    print(f"  INFO: Page {p} text differs (orig len={len(orig_text)}, out len={len(out_text)})")

        doc_orig.close()
        doc_out.close()

        if checked > 0 and matches == checked:
            print(f"PASS: Component 4 - Text content matches on all {checked} spot-checked pages (0.20 pts)")
            total_score += 0.20
        elif checked > 0:
            partial = 0.20 * (matches / checked)
            print(f"PARTIAL: Component 4 - Text matches on {matches}/{checked} pages ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 - Could not check any pages")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

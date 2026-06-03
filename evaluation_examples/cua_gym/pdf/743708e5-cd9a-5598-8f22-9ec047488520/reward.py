"""
FINAL REWARD SCRIPT - SUCCESS
Task: Add a watermark with text 'CONFIDENTIAL' in red color to all pages of 'report.pdf' on Desktop and save as 'report_confidential.pdf'.
Generated: 2025-11-29 09:41:14
Status: success
Model: o3
Total Steps: 1
"""

import re
import hashlib
from pathlib import Path
from PyPDF2 import PdfReader

"""
Reward Script: verify that a red “CONFIDENTIAL” watermark was added to every page of
Desktop/report.pdf and saved as Desktop/report_confidential.pdf.

Scoring rubric (progressive – total 1.0):
    • 0.20  – correct output filename present
    • 0.20  – page-count matches original/golden
    • 0.30  – every page’s extracted text contains the word CONFIDENTIAL
    • 0.30  – every page’s content stream contains red colour operator (1 0 0 rg/RG)
    • 1.00  – OR byte-for-byte match with provided golden PDF (short-circuit)

The script prints diagnostics for each check and always outputs
  "REWARD: <score>"  (float between 0.0-1.0) on completion.
"""

# ------------ helper utilities -------------------------------------------------

def _md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):  # efficient streaming
            h.update(chunk)
    return h.hexdigest()


def _page_bytes(page):
    """Return concatenated raw bytes of a page’s content streams."""
    try:
        contents = page.get_contents()
        if contents is None:
            return b""
        if isinstance(contents, list):
            return b"".join(obj.get_data() for obj in contents)
        return contents.get_data()
    except Exception:
        # Fallback for older/internal APIs
        try:
            return page._get_contents() or b""
        except Exception:
            return b""


# ------------------ main verification routine ---------------------------------

def verify_watermark() -> float:
    # Paths
    out_pdf = Path("/home/user/Desktop/report_confidential.pdf")
    orig_pdf = Path("/home/user/Desktop/report.pdf")
    golden_pdf = Path(
        "/home/user/add_a_watermark_with_text_confidential_in_red_color_to_all_pages_of_reportpdf_on_desktop_and_save_as_golden.pdf"
    )

    # Weights
    W_NAME = 0.20
    W_PAGES = 0.20
    W_TEXT = 0.30
    W_COLOR = 0.30
    score = 0.0

    # 0.  Existence check (no points, but hard-fail if missing)
    if not out_pdf.exists():
        print(f"✗ Output file missing: {out_pdf}")
        print("REWARD: 0.0")
        return 0.0
    print(f"✓ Found output file: {out_pdf}")

    # 1.  Perfect match shortcut ----------------------------------------------
    if golden_pdf.exists():
        if _md5(out_pdf) == _md5(golden_pdf):
            print("✓ Output PDF matches golden file byte-for-byte – full credit")
            print("REWARD: 1.0")
            return 1.0
        else:
            print("ℹ️  Output differs from golden – running granular checks")
    else:
        print("ℹ️  Golden file not present – running granular checks")

    # 2.  Filename correctness --------------------------------------------------
    if out_pdf.name == "report_confidential.pdf":
        print("✓ Output filename correct")
        score += W_NAME
    else:
        print("✗ Output filename incorrect")

    # 3.  Read PDFs -------------------------------------------------------------
    try:
        reader_out = PdfReader(str(out_pdf))
        page_count_out = len(reader_out.pages)
        print(f"✓ Loaded output PDF – {page_count_out} pages")
    except Exception as e:
        print(f"✗ Could not read output PDF: {e}")
        print(f"REWARD: {score}")
        return score

    # 4.  Page count comparison -------------------------------------------------
    page_count_ok = False
    if orig_pdf.exists():
        try:
            if len(PdfReader(str(orig_pdf)).pages) == page_count_out:
                page_count_ok = True
        except Exception:
            pass
    elif golden_pdf.exists():
        try:
            if len(PdfReader(str(golden_pdf)).pages) == page_count_out:
                page_count_ok = True
        except Exception:
            pass

    if page_count_ok:
        print("✓ Page count matches original/golden")
        score += W_PAGES
    else:
        print("✗ Page count mismatch")

    # 5.  Watermark text presence ---------------------------------------------
    all_have_text = True
    for idx, pg in enumerate(reader_out.pages, start=1):
        txt = (pg.extract_text() or "").upper()
        if "CONFIDENTIAL" not in txt:
            print(f"✗ Page {idx} missing 'CONFIDENTIAL' in extracted text")
            all_have_text = False
            break
    if all_have_text and page_count_out:
        print("✓ 'CONFIDENTIAL' text found on every page")
        score += W_TEXT
    else:
        print("✗ Not every page contains the watermark text")

    # 6.  Red colour operator inspection --------------------------------------
    red_rg = re.compile(rb"\b1\s+0\s+0\s+(rg|RG)\b")  # device-RGB red
    all_red = True
    for idx, pg in enumerate(reader_out.pages, start=1):
        if not red_rg.search(_page_bytes(pg)):
            print(f"✗ Page {idx} lacks red colour graphics operator 1 0 0 rg/RG")
            all_red = False
            break
    if all_red and page_count_out:
        print("✓ Red colour operator present on every page")
        score += W_COLOR
    else:
        print("✗ Red colour operator missing on one or more pages")

    # 7.  Final score -----------------------------------------------------------
    final = min(score, 1.0)
    print(f"Total score: {final}/1.0")
    print(f"REWARD: {final}")
    return final


if __name__ == "__main__":
    verify_watermark()


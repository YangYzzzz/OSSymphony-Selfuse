"""
FINAL REWARD SCRIPT - SUCCESS
Task: Convert the webpage at 'file:///home/user/Documents/report.html' to PDF 'report_web.pdf' on Desktop.
Generated: 2025-11-29 09:29:17
Status: success
Model: o3
Total Steps: 10
"""

from pathlib import Path
import re
import html
from PyPDF2 import PdfReader

###############################################################################
# Reward Script: Verify HTML ➜ PDF conversion task
# Task: Convert the webpage at
#        'file:///home/user/Documents/report.html'
#       to the PDF  'report_web.pdf' on the Desktop.
#
# Scoring rubric (progressive – max 1.0):
#   • 0.20  – PDF exists *and* can be opened by PyPDF2
#   • 0.30  – PDF contains the expected title text
#   • 0.50  – Body text from the HTML is present (line-by-line ratio)
#
# A perfect conversion therefore scores 1.0.  Missing elements lose points
# proportionally, allowing partial credit.
###############################################################################

def _normalise(text: str) -> str:
    """Lower-case and collapse whitespace for robust substring checks."""
    return re.sub(r"\s+", " ", (text or "").strip()).lower()


def _strip_html(source_html: str) -> list[str]:
    """Very simple tag removal to obtain visible text lines from an HTML file."""
    raw = html.unescape(re.sub(r"<[^>]+>", "", source_html))
    lines = [ln.strip() for ln in raw.splitlines()]
    # Keep non-empty lines only
    return [ln for ln in lines if ln]


def verify_html_to_pdf_conversion() -> float:
    # Paths
    produced_pdf = Path.home() / "Desktop" / "report_web.pdf"
    html_path    = Path("/home/user/Documents/report.html")

    total_score = 0.0
    max_score   = 1.0

    # ---------------------------------------------------------------------
    # 1) PDF existence & readability (0.20)
    # ---------------------------------------------------------------------
    if not produced_pdf.exists():
        print(f"✗ Produced PDF NOT found at {produced_pdf}")
        print("REWARD: 0.0")
        return 0.0

    try:
        reader = PdfReader(str(produced_pdf))
        num_pages = len(reader.pages)
        print(f"✓ Produced PDF found – {num_pages} page(s)")
        total_score += 0.20
    except Exception as exc:
        print(f"✗ Unable to open PDF with PyPDF2: {exc}")
        print("REWARD: 0.0")
        return 0.0

    # Gather full visible text from all pages for downstream checks
    pdf_full_text = "".join(page.extract_text() or "" for page in reader.pages)
    pdf_text_norm = _normalise(pdf_full_text)

    # ---------------------------------------------------------------------
    # 2) Title verification (0.30)
    # ---------------------------------------------------------------------
    title_variants = [
        "quarterly report",          # main heading
        "html → pdf",                # unicode arrow variant
        "html -> pdf",               # ascii arrow
        "html \u279c pdf"            # literal representation
    ]
    if any(variant in pdf_text_norm for variant in title_variants):
        print("✓ Expected title text detected in PDF")
        total_score += 0.30
    else:
        print("✗ Expected title text NOT found in PDF")

    # ---------------------------------------------------------------------
    # 3) Body-content verification (up to 0.50)
    # ---------------------------------------------------------------------
    if html_path.exists():
        html_lines = _strip_html(html_path.read_text(encoding="utf-8"))
        found_lines = sum(1 for ln in html_lines if _normalise(ln) in pdf_text_norm)
        ratio       = found_lines / len(html_lines) if html_lines else 0.0
        content_pts = 0.50 * ratio  # proportional credit
        total_score += content_pts
        print(f"✓ HTML content match: {found_lines}/{len(html_lines)} line(s) – {content_pts:.2f} point(s)")
        missing = len(html_lines) - found_lines
        if missing:
            print(f"  Missing {missing} line(s) of expected body text")
    else:
        print("! HTML source file missing – skipping body-text verification")

    # ---------------------------------------------------------------------
    # Final result
    # ---------------------------------------------------------------------
    final = min(total_score, max_score)
    print(f"REWARD: {final}")
    return final


# Execute verification when run as a script
if __name__ == "__main__":
    verify_html_to_pdf_conversion()

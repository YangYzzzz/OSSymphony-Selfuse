"""
FINAL REWARD SCRIPT - SUCCESS
Task: Please convert the PDF 'legal_document.pdf' on Desktop to plain text 'legal_document.txt', preserving line breaks and paragraph structure.
Generated: 2025-11-29 09:30:55
Status: success
Model: o3
Total Steps: 1
"""

from pathlib import Path
from PyPDF2 import PdfReader
import re

"""
Reward Script: Verify PDF→TXT conversion for "legal_document"
Task Requirement Recap:
1. A TXT file named "legal_document.txt" must be produced next to (or near) the source PDF.
2. TXT content must faithfully reproduce the PDF text – preserving line breaks / paragraph structure.

Verification Strategy:
• Locate the source PDF deterministically (Desktop path or given golden path).
• Locate the generated TXT file (Desktop first, then other common folders).
• Extract text from every PDF page with PyPDF2.
• Normalise both PDF-extracted text and TXT text line-by-line (collapse interior whitespace, retain blank lines).
• Compute a line-by-line equality ratio: matches / max(len(pdf_lines), len(txt_lines)).
• Scoring:
    – 0.2 points once the TXT file exists (generation check).
    – Up to 0.8 further points proportionally to the line-match ratio (full 1.0 only when every line matches).
• Print detailed diagnostics and final "REWARD: X.X" line.
"""

##############################
# Helper functions
##############################

def _locate_pdf() -> Path | None:
    """Return Path to the PDF if found in common locations."""
    candidates = [
        Path("/home/user/Desktop/legal_document.pdf"),
        Path(
            "/home/user/please_convert_the_pdf_legal_documentpdf_on_desktop_to_plain_text_legal_documenttxt_preserving_line__golden.pdf"
        ),
        Path("/home/user/legal_document.pdf"),
    ]
    return next((p for p in candidates if p.exists()), None)


def _locate_txt() -> Path | None:
    """Return Path to the TXT if found in common locations."""
    candidates = [
        Path("/home/user/Desktop/legal_document.txt"),
        Path("/home/user/legal_document.txt"),
        Path("/home/user/Documents/legal_document.txt"),
    ]
    for p in candidates:
        if p.exists():
            return p
    # Fallback: any *.txt on Desktop containing the keyword
    desktop = Path("/home/user/Desktop")
    if desktop.exists():
        for p in desktop.glob("*.txt"):
            if "legal_document" in p.name.lower():
                return p
    return None


def _extract_pdf_text(pdf_path: Path) -> str:
    """Concatenate text of all pages using PyPDF2."""
    reader = PdfReader(str(pdf_path))
    page_texts = [(page.extract_text() or "") for page in reader.pages]
    return "\n".join(page_texts)


def _normalise_lines(text: str) -> list[str]:
    """Normalise whitespace per line but keep line boundaries intact."""
    norm_lines = []
    for line in text.splitlines():
        # collapse multiple whitespace to single space, trim ends
        cleaned = re.sub(r"\s+", " ", line.strip())
        norm_lines.append(cleaned)
    return norm_lines


def _line_match_ratio(pdf_lines: list[str], txt_lines: list[str]) -> float:
    """Return ratio of exact line matches over the longer sequence length."""
    matches = sum(1 for a, b in zip(pdf_lines, txt_lines) if a == b)
    denom = max(len(pdf_lines), len(txt_lines)) or 1
    return matches / denom

##############################
# Main verification function
##############################

def verify_conversion() -> float:
    score = 0.0

    pdf_path = _locate_pdf()
    if not pdf_path:
        print("✗ Source PDF not found – cannot verify task.")
        print("REWARD: 0.0")
        return 0.0
    print(f"✓ Found PDF: {pdf_path}")

    txt_path = _locate_txt()
    if not txt_path:
        print("✗ TXT output not found – task incomplete.")
        print("REWARD: 0.0")
        return 0.0
    print(f"✓ Found TXT: {txt_path}")

    # TXT exists – award presence points
    score += 0.2

    # Load contents
    try:
        pdf_text = _extract_pdf_text(pdf_path)
    except Exception as e:
        print(f"✗ Failed to extract text from PDF: {e}")
        print(f"REWARD: {score}")
        return score  # only presence points

    try:
        txt_content = txt_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"✗ Could not read TXT file: {e}")
        print(f"REWARD: {score}")
        return score

    if not txt_content.strip():
        print("✗ TXT file is empty – no conversion content detected.")
        print(f"REWARD: {score}")
        return score

    # Normalise and compare line-by-line
    pdf_lines = _normalise_lines(pdf_text)
    txt_lines = _normalise_lines(txt_content)

    ratio = _line_match_ratio(pdf_lines, txt_lines)
    print(f"Line-match ratio: {ratio:.2%}")

    # Award proportional points (up to 0.8)
    score += ratio * 0.8
    score = min(score, 1.0)

    print(f"REWARD: {score}")
    return score

##############################
# Script entry-point
##############################
if __name__ == "__main__":
    verify_conversion()

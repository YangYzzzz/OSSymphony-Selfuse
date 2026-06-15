"""
FINAL REWARD SCRIPT - SUCCESS
Task: I need to extract text from the technical specification PDF 'specs_v2.3.pdf' in /home/user/Projects/Documentation, removing all headers, footers, and page numbers, and save to 'clean_specs.txt'.
Generated: 2025-11-29 09:12:28
Status: success
Model: o3
Total Steps: 12
"""

"""
Reward script for verifying extraction of cleaned text from 'specs_v2.3.pdf'.
It checks that:
1. The header line that appears at the top of every PDF page has been removed.
2. Footer / page-number lines have been stripped out.
3. The remaining text matches exactly the expected clean text determined directly from the PDF.
Progressive scoring (0–1.0) is used:
  • 0.2  Header successfully removed
  • 0.2  Footer / page numbers successfully removed
  • 0.6  Cleaned file content matches expected (partial credit proportional to line-by-line agreement)
The script prints detailed diagnostics and finally prints
    REWARD: <score>
Exactly 1.0 is awarded only when every requirement is satisfied.
"""

from pathlib import Path
import re
from PyPDF2 import PdfReader

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def get_header_phrase(pdf_path: Path) -> str:
    """Return the first non-empty line found in the first page – assumed header."""
    reader = PdfReader(str(pdf_path))
    for page in reader.pages:
        text = page.extract_text() or ""
        for line in text.split("\n"):
            clean = line.strip()
            if clean:
                return clean
    return ""

def compute_clean_text(pdf_path: Path) -> list[str]:
    """Return a list of lines representing the expected cleaned text."""
    header_phrase = get_header_phrase(pdf_path)
    reader = PdfReader(str(pdf_path))
    cleaned_lines: list[str] = []

    for page in reader.pages:
        raw_text = page.extract_text() or ""
        lines = [ln.strip() for ln in raw_text.split("\n") if ln.strip()]
        if not lines:
            continue
        # Remove header (exact match or containing header phrase)
        if lines and (lines[0] == header_phrase or header_phrase in lines[0]):
            lines = lines[1:]
        # Remove footer / page number lines
        while lines and (
            re.search(r"Confidential", lines[-1], re.I)
            or re.match(r"Page\s*\d+", lines[-1])
            or "Company Internal" in lines[-1]
        ):
            lines.pop()
        cleaned_lines.extend(lines)

    return cleaned_lines

def normalise(lines: list[str]) -> list[str]:
    """Trim whitespace and drop empty lines."""
    return [ln.strip() for ln in lines if ln.strip()]

# ------------------------------------------------------------
# Verification routine
# ------------------------------------------------------------

def verify_extraction() -> float:
    pdf_path = Path("/home/user/Projects/Documentation/specs_v2.3.pdf")
    if not pdf_path.exists():
        print(f"✗ Source PDF not found at {pdf_path}")
        print("REWARD: 0.0")
        return 0.0

    # Expected cleaned text derived straight from the PDF
    expected_lines = compute_clean_text(pdf_path)
    print(f"Computed expected cleaned content: {len(expected_lines)} lines")

    # Locate the candidate TXT file (default location first, otherwise search-all)
    txt_path = pdf_path.parent / "clean_specs.txt"
    if not txt_path.exists():
        alt = list(Path("/home/user").rglob("clean_specs.txt"))
        if alt:
            txt_path = alt[0]
            print(f"Using alternate found file: {txt_path}")
        else:
            print("✗ 'clean_specs.txt' not found anywhere")
            print("REWARD: 0.0")
            return 0.0

    # Read candidate file
    file_lines = normalise(txt_path.read_text(encoding="utf-8", errors="ignore").split("\n"))
    header_phrase = get_header_phrase(pdf_path)

    total_score = 0.0  # progressive scoring

    # 1) Header removed (0.2)
    if not any(header_phrase in line for line in file_lines):
        print("✓ Header phrase removed from TXT")
        total_score += 0.2
    else:
        print("✗ Header phrase still present in TXT")

    # 2) Footer & page numbers removed (0.2)
    footer_present = any(
        re.search(r"Confidential", ln, re.I) or re.match(r"Page\s*\d+", ln)
        for ln in file_lines
    )
    if not footer_present:
        print("✓ Footer and page numbers removed from TXT")
        total_score += 0.2
    else:
        print("✗ Footer/page number lines still present in TXT")

    # 3) Content matches expected cleaned text (up to 0.6)
    if file_lines == expected_lines:
        print("✓ Cleaned TXT content matches expected exactly")
        total_score += 0.6
    else:
        # partial credit based on line-by-line agreement from start of doc
        common = sum(1 for a, b in zip(file_lines, expected_lines) if a == b)
        similarity = common / len(expected_lines) if expected_lines else 0.0
        partial_points = 0.6 * similarity
        total_score += partial_points
        print(f"Partial content match: {similarity*100:.1f}%  ->  {partial_points:.2f} points")

    final_score = round(min(total_score, 1.0), 2)
    print(f"REWARD: {final_score}")
    return final_score

# ------------------------------------------------------------
# Execute when run as a script
# ------------------------------------------------------------
if __name__ == "__main__":
    verify_extraction()

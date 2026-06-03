"""
FINAL REWARD SCRIPT - SUCCESS
Task: Extract text from the corrupted PDF 'damaged_file.pdf' on Desktop and save whatever is recoverable to 'recovered_text.txt'.
Generated: 2025-11-29 09:15:12
Status: success
Model: o3
Total Steps: 6
"""

# Reward script for: Extract text from the corrupted PDF 'damaged_file.pdf' on Desktop
# and save whatever is recoverable to 'recovered_text.txt'
# -----------------------------------------------------------
# This script awards a progressive score based on how much of the
# PDF’s extractable text actually appears in the recovered TXT file.
# A full 1.0 reward is given only when ALL extractable text is present.
# -----------------------------------------------------------

import re
from pathlib import Path
from difflib import SequenceMatcher
from PyPDF2 import PdfReader


def _normalize(text: str) -> str:
    """Collapse whitespace and lowercase for robust comparison."""
    text = text.replace("\x00", "")  # strip null bytes sometimes found in corrupt files
    text = re.sub(r"\s+", " ", text)  # collapse all whitespace to single spaces
    return text.strip().lower()


def _coverage_ratio(baseline: str, recovered: str) -> float:
    """Return 0-1 ratio of baseline text that is present (order-preserving) in recovered text."""
    if not baseline:
        return 0.0
    matcher = SequenceMatcher(None, baseline, recovered, autojunk=False)
    matched = sum(block.size for block in matcher.get_matching_blocks())
    return max(0.0, min(matched / len(baseline), 1.0))


def verify_text_extraction(pdf_path: str, recovered_path: str) -> float:
    print(f"Verifying text extraction from '{pdf_path}' → '{recovered_path}' …")

    # 1. Read all text we CAN recover from the PDF using PyPDF2
    try:
        reader = PdfReader(pdf_path)
        pdf_text_parts = []
        for idx, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text() or ""
            except Exception as exc:
                print(f"✗ Page {idx+1} extraction error: {exc}")
                page_text = ""
            print(f"Page {idx+1}: {len(page_text)} chars extracted")
            pdf_text_parts.append(page_text)
        pdf_text = "\n".join(pdf_text_parts)
        print(f"Total extractable characters from PDF: {len(pdf_text)}")
    except Exception as exc:
        print(f"✗ Unable to open/read PDF: {exc}")
        print("REWARD: 0.0")
        return 0.0

    # 2. Ensure recovered TXT exists
    txt_file = Path(recovered_path)
    if not txt_file.exists():
        print(f"✗ Missing recovered file: {recovered_path}")
        print("REWARD: 0.0")
        return 0.0

    recovered_text = txt_file.read_text(encoding="utf-8", errors="ignore")
    print(f"Recovered file size: {len(recovered_text)} characters")

    # 3. Normalise both texts
    base_norm = _normalize(pdf_text)
    rec_norm = _normalize(recovered_text)

    if not rec_norm:
        print("✗ Recovered file is empty after normalisation")
        print("REWARD: 0.0")
        return 0.0

    # 4. Compute coverage ratio and assign score
    coverage = _coverage_ratio(base_norm, rec_norm)
    print(f"Coverage of PDF text found in recovered file: {coverage:.2%}")

    # Progressive score equals coverage (capped to 1.0)
    score = round(coverage, 4)
    print(f"REWARD: {score}")
    return score


if __name__ == "__main__":
    PDF_PATH = "/home/user/Desktop/damaged_file.pdf"
    RECOVERED_PATH = "/home/user/Desktop/recovered_text.txt"
    verify_text_extraction(PDF_PATH, RECOVERED_PATH)

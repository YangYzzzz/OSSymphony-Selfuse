"""
FINAL REWARD SCRIPT - SUCCESS
Task: Extract all text content from the research paper 'neural_networks_2019.pdf' on my Desktop and save it as 'extracted_text.txt' in the same location.
Generated: 2025-11-29 09:11:37
Status: success
Model: o3
Total Steps: 6
"""

from pathlib import Path
import re
from PyPDF2 import PdfReader


def normalize_text(text: str) -> str:
    """Collapse whitespace, lower‐case, and strip ends for stable comparison."""
    return re.sub(r"\s+", " ", text).strip().lower()


def extract_pdf_text(pdf_path: Path) -> str:
    """Extract raw text from every page of a PDF (deterministic with PyPDF2)."""
    reader = PdfReader(str(pdf_path))
    pages_text = []
    for idx, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        print(f"Page {idx + 1}: {len(page_text)} chars extracted")
        pages_text.append(page_text)
    return "\n".join(pages_text)


def verify_extraction() -> float:
    """Verify that all text from the PDF was exported to extracted_text.txt.

    Scoring (progressive):
      • 0.2  – extracted_text.txt exists in Desktop.
      • 0.1  – file is non-trivial (>50 chars).
      • 0.7  – ≥95 % unique-word coverage AND length ratio within 10 % (complete).
      • 0.4  – 80–95 % coverage  (mostly complete).
      • 0.2  – 50–80 % coverage  (partially complete).
    """

    desktop = Path.home() / "Desktop"
    pdf_path = desktop / "neural_networks_2019.pdf"
    txt_path = desktop / "extracted_text.txt"

    total_score = 0.0

    # ---------- Presence checks ----------
    if not txt_path.exists():
        print(f"✗ Missing extracted text file: {txt_path}")
        print("REWARD: 0.0")
        return 0.0
    print(f"✓ Found extracted text file: {txt_path}")
    total_score += 0.2

    if not pdf_path.exists():
        print(f"✗ Missing source PDF: {pdf_path}")
        print(f"REWARD: {total_score}")
        return total_score

    # ---------- Read contents ----------
    try:
        pdf_raw = extract_pdf_text(pdf_path)
    except Exception as e:
        print(f"✗ Error reading PDF: {e}")
        print(f"REWARD: {total_score}")
        return total_score

    try:
        txt_raw = txt_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"✗ Error reading extracted text file: {e}")
        print(f"REWARD: {total_score}")
        return total_score

    # ---------- Basic size sanity ----------
    if len(txt_raw.strip()) > 50:
        print("✓ Extracted text file is non-trivial")
        total_score += 0.1
    else:
        print("✗ Extracted text file appears too small (<50 chars)")
        print(f"REWARD: {total_score}")
        return total_score

    # ---------- Normalized comparison ----------
    norm_pdf = normalize_text(pdf_raw)
    norm_txt = normalize_text(txt_raw)

    pdf_words = re.findall(r"\b\w+\b", norm_pdf)
    txt_words = re.findall(r"\b\w+\b", norm_txt)

    if not pdf_words:
        print("✗ No words extracted from PDF – cannot continue verification")
        print(f"REWARD: {total_score}")
        return total_score

    pdf_set = set(pdf_words)
    txt_set = set(txt_words)

    coverage = len(pdf_set & txt_set) / len(pdf_set)
    length_ratio = len(txt_words) / len(pdf_words)

    print(f"Coverage: {coverage * 100:.2f}% (unique-word overlap)")
    print(f"Length ratio (extracted/pdf): {length_ratio:.2f}")

    # ---------- Scoring based on coverage ----------
    if coverage >= 0.95 and 0.9 <= length_ratio <= 1.1:
        print("✓ Extraction appears COMPLETE (≥95% coverage)")
        total_score += 0.7
    elif coverage >= 0.80:
        print("✓ Extraction MOSTLY complete (80–95% coverage)")
        total_score += 0.4
    elif coverage >= 0.50:
        print("✓ Extraction PARTIALLY complete (50–80% coverage)")
        total_score += 0.2
    else:
        print("✗ Extraction coverage below 50% – insufficient")

    final_score = min(total_score, 1.0)
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_extraction()


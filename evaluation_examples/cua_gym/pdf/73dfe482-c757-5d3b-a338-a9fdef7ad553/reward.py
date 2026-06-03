"""
FINAL REWARD SCRIPT - SUCCESS
Task: Extract text from the product catalog 'catalog_2024.pdf' in /home/user/Documents/Sales, including product names and descriptions, and save to 'products_list.txt'.
Generated: 2025-11-29 09:14:59
Status: success
Model: o3
Total Steps: 1
"""

import re
from pathlib import Path
from typing import List
from PyPDF2 import PdfReader

"""
Reward Script for: Extract text from the product catalog 'catalog_2024.pdf' located in
/home/user/Documents/Sales, including product names and descriptions, and save the
result to 'products_list.txt'.

Scoring principles (progressive):
1. products_list.txt exists AND is non-trivial in size  .................... 0.2
2. ≥30 % token overlap with source PDF .................................... 0.2
3. ≥50 % token overlap with source PDF .................................... 0.2
4. ≥80 % token overlap with source PDF .................................... 0.2
5. ≥95 % token overlap with source PDF .................................... 0.2

A perfect extraction (≥95 % overlap) yields the full 1.0 reward.
"""

def _tokenise(text: str) -> List[str]:
    """Simple tokenizer: keep alphabetic tokens of length ≥3, case-insensitive."""
    return re.findall(r"[A-Za-z]{3,}", text.lower())


def verify_task(pdf_path: str, txt_path: str) -> float:
    max_score = 1.0
    score = 0.0

    # ------------------------------------------------------------------
    # 1. Verify the TXT export exists and isn’t empty
    # ------------------------------------------------------------------
    txt_file = Path(txt_path)
    if not txt_file.exists():
        print(f"✗ Missing exported file: {txt_path}")
        print("REWARD: 0.0")
        return 0.0

    size = txt_file.stat().st_size
    print(f"Found '{txt_path}' (size: {size} bytes)")
    if size > 50:  # minimal threshold to ensure non-trivial content
        print("✓ Export file exists with substantial content (0.2)")
        score += 0.2
    else:
        print("✗ Export file too small (<50 B) – no points for size criterion")

    # ------------------------------------------------------------------
    # 2. Extract text from the source PDF deterministically with PyPDF2
    # ------------------------------------------------------------------
    try:
        reader = PdfReader(pdf_path)
        pdf_text = "\n".join(page.extract_text() or "" for page in reader.pages)
        print(f"PDF loaded: {len(reader.pages)} pages; {len(pdf_text)} characters extracted")
    except Exception as e:
        print(f"✗ Error reading PDF: {e}")
        print(f"REWARD: {score}")
        return score  # cannot continue token comparison

    # ------------------------------------------------------------------
    # 3. Token comparison between PDF and TXT output
    # ------------------------------------------------------------------
    txt_content = txt_file.read_text(encoding="utf-8", errors="ignore")

    pdf_tokens  = set(_tokenise(pdf_text))
    txt_tokens  = _tokenise(txt_content)

    if not txt_tokens:
        print("✗ No extractable tokens found in products_list.txt – extraction failed")
        print(f"REWARD: {score}")
        return score

    matched_tokens = [tok for tok in txt_tokens if tok in pdf_tokens]
    overlap_ratio = len(matched_tokens) / len(txt_tokens)
    print(f"Token overlap: {len(matched_tokens)}/{len(txt_tokens)} = {overlap_ratio:.2%}")

    # Progressive scoring based on overlap ratio
    thresholds = [(0.30, 0.2, "Basic ≥30%"),
                  (0.50, 0.2, "Moderate ≥50%"),
                  (0.80, 0.2, "High ≥80%"),
                  (0.95, 0.2, "Excellent ≥95%")]

    for thresh, pts, label in thresholds:
        if overlap_ratio >= thresh:
            print(f"✓ {label} token overlap (+{pts})")
            score += pts

    final_score = min(score, max_score)
    print(f"REWARD: {final_score}")
    return final_score

# ----------------------------------------------------------------------
# Execute verification when run as a script
# ----------------------------------------------------------------------
if __name__ == "__main__":
    PDF_PATH = "/home/user/Documents/Sales/catalog_2024.pdf"
    TXT_PATH = "/home/user/Documents/Sales/products_list.txt"
    verify_task(PDF_PATH, TXT_PATH)

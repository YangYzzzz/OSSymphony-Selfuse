"""
FINAL REWARD SCRIPT - SUCCESS
Task: Convert the scanned form 'application_filled_scan.pdf' in /home/user/Documents to a searchable PDF with OCR, then extract form field values to 'form_data.txt'.
Generated: 2025-11-29 10:07:46
Status: success
Model: o3
Total Steps: 9
"""

from __future__ import annotations
"""
Reward script for task:
Convert the scanned form 'application_filled_scan.pdf' in /home/user/Documents to a
searchable PDF with OCR, then extract form field values to 'form_data.txt'.

Scoring logic (total 1.0):
  • 0.6 points – PDF is OCR-searchable and contains the three expected values
      – 0.2  Non-empty extractable text available (proves OCR layer)
      – 0.4  Presence of the 3 specific field values (0.1333̅ each)
  • 0.4 points – Extracted text file lists the same three key/value pairs
      – 0.1333̅ points per correct line  "Key: Value"

The script prints detailed diagnostics and the final line
    REWARD: X.X
where X.X is the progressive score (exactly 1.0 when everything is correct).
"""

import os
from pathlib import Path
from typing import List, Dict
from PyPDF2 import PdfReader

# --------------------------- PDF VERIFICATION ---------------------------------

def verify_ocr_pdf(pdf_path: str, samples: List[str]) -> float:
    """Verify that `pdf_path` contains selectable text and all `samples` strings.

    Returns a score between 0-0.6.
    """
    if not os.path.exists(pdf_path):
        print(f"✗ OCR PDF not found: {pdf_path}")
        return 0.0

    reader = PdfReader(pdf_path)
    full_text = ""
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        print(f"Page {i+1}: extracted {len(text)} characters")
        full_text += text + "\n"

    full_text_lower = full_text.lower()
    score = 0.0

    # 0.2 pts for any substantial text (proves OCR layer exists)
    if len(full_text.strip()) > 20:
        score += 0.2
        print("✓ Non-empty selectable text detected (0.2)")
    else:
        print("✗ Text extraction too short – OCR layer missing")
        return score  # further checks meaningless if no OCR

    # 0.4 pts distributed across expected strings
    found = 0
    for s in samples:
        if s.lower() in full_text_lower:
            print(f"✓ Found '{s}' in PDF")
            found += 1
        else:
            print(f"✗ Missing '{s}' in PDF")
    score += 0.4 * (found / len(samples))

    return round(min(score, 0.6), 4)

# ----------------------- TEXT FILE VERIFICATION -------------------------------

def verify_extracted_txt(txt_path: str, expected_kv: Dict[str, str]) -> float:
    """Verify that the text file lists each key/value pair as 'Key: Value'.

    Returns a score between 0-0.4.
    """
    path = Path(txt_path)
    if not path.exists():
        print(f"✗ Expected text file not found: {txt_path}")
        return 0.0

    content = path.read_text(encoding="utf-8", errors="ignore").lower()
    print(f"TXT length: {len(content)} characters")

    found = 0
    for k, v in expected_kv.items():
        pattern = f"{k.lower()}: {v.lower()}"
        if pattern in content:
            print(f"✓ Found line '{pattern}'")
            found += 1
        else:
            print(f"✗ Missing line '{pattern}'")

    score = 0.4 * (found / len(expected_kv))
    return round(score, 4)

# ------------------------------ MAIN DRIVER -----------------------------------

def verify_task() -> float:
    pdf_path = "/home/user/Documents/application_filled_scan.pdf"
    txt_path = "/home/user/Documents/form_data.txt"

    expected_strings = [
        "John Doe",
        "1990-01-01",
        "john.doe@example.com",
    ]

    expected_pairs = {
        "Name": "John Doe",
        "Date of Birth": "1990-01-01",
        "Email": "john.doe@example.com",
    }

    print("--- Checking OCR PDF ---")
    pdf_score = verify_ocr_pdf(pdf_path, expected_strings)
    print(f"OCR PDF score: {pdf_score}\n")

    print("--- Checking extracted TXT ---")
    txt_score = verify_extracted_txt(txt_path, expected_pairs)
    print(f"TXT score: {txt_score}\n")

    total = round(min(pdf_score + txt_score, 1.0), 4)
    print(f"Total score: {total}")
    print(f"REWARD: {total}")
    return total

# Execute when run as a script
if __name__ == "__main__":
    verify_task()

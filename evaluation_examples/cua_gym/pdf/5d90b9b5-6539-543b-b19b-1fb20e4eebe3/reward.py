"""
FINAL REWARD SCRIPT - SUCCESS
Task: Convert the scanned multilingual document 'multilingual_notice.pdf' on Desktop (English, Spanish, Chinese) to searchable PDF using multi-language OCR.
Generated: 2025-11-29 10:12:18
Status: success
Model: o3
Total Steps: 12
"""

from pathlib import Path
import re
from PyPDF2 import PdfReader

def verify_multilingual_ocr(pdf_path: str) -> float:
    """Verify that the given PDF has a proper multi-language OCR text layer.

    Scoring (progressive up to 1.0):
        • 0.1 – Every page yields >10 extractable characters (indicates text layer exists)
        • 0.3 – English keyword "Important Notice" present
        • 0.3 – Spanish keyword "Aviso Importante" present
        • 0.3 – Chinese keyword "通知" present
    The score is capped at 1.0.
    """
    max_score = 1.0
    score = 0.0

    pdf = Path(pdf_path)
    print(f"Verifying multilingual OCR for: {pdf}")

    # Basic existence check (no points – prerequisite only)
    if not pdf.exists():
        print("✗ PDF file is missing – task failed")
        print("REWARD: 0.0")
        return 0.0

    # Attempt to open the PDF
    try:
        reader = PdfReader(str(pdf))
    except Exception as e:
        print(f"✗ Unable to open PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    num_pages = len(reader.pages)
    print(f"- Detected {num_pages} page(s)")

    # Requirement 1: each page must contain some extractable text, >10 chars
    page_texts = []
    all_have_text = True
    for i, page in enumerate(reader.pages, start=1):
        txt = page.extract_text() or ""
        txt_len = len(txt.strip())
        page_texts.append(txt)
        print(f"  Page {i}: extracted {txt_len} character(s)")
        if txt_len < 10:
            all_have_text = False

    if all_have_text:
        print("✓ All pages have meaningful extractable text (+0.1)")
        score += 0.1
    else:
        print("✗ One or more pages lack sufficient extractable text")

    # Combine text for language keyword searches
    full_text = "\n".join(page_texts)

    # Language-specific keyword checks
    keyword_checks = [
        ("English", "Important Notice", 0.3),
        ("Spanish", "Aviso Importante", 0.3),
        ("Chinese", "通知", 0.3),
    ]

    for language, keyword, pts in keyword_checks:
        if re.search(re.escape(keyword), full_text, flags=re.IGNORECASE):
            print(f"✓ {language} keyword '{keyword}' found (+{pts})")
            score += pts
        else:
            print(f"✗ {language} keyword '{keyword}' NOT found")

    final_score = min(score, max_score)
    print(f"Final score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score

if __name__ == "__main__":
    # Expected location of the converted, searchable PDF
    pdf_to_check = "/home/user/Desktop/multilingual_notice.pdf"
    verify_multilingual_ocr(pdf_to_check)

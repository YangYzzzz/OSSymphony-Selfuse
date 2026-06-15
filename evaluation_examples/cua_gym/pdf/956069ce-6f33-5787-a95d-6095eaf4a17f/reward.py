"""
FINAL REWARD SCRIPT - SUCCESS
Task: Convert the Word document 'report_draft.docx' on Desktop to PDF and save it as 'report_final.pdf' in the same location.
Generated: 2025-11-29 09:25:39
Status: success
Model: o3
Total Steps: 14
"""

from PyPDF2 import PdfReader
from pathlib import Path
import re


def _normalize(text: str) -> str:
    """Collapse whitespace and lowercase the extracted text for reliable comparison."""
    return re.sub(r"\s+", " ", (text or "").strip()).lower()


def verify_task() -> float:
    """Reward script to verify Word→PDF conversion task.

    Scoring (progressive up to 1.0):
    • 0.2 – The produced PDF exists at the required location
    • 0.2 – Page-count matches the golden reference PDF
    • 0.6 – Per-page textual content matches the golden reference (ratio-based)
    """

    produced_pdf = Path("/home/user/Desktop/report_final.pdf")
    golden_pdf = Path(
        "/home/user/convert_the_word_document_report_draftdocx_on_desktop_to_pdf_and_save_it_as_report_finalpdf_in_the_s_golden.pdf"
    )

    score = 0.0  # progressive score

    # 1) Produced PDF must exist
    if produced_pdf.exists():
        print(f"✓ Found produced PDF: {produced_pdf}")
        score += 0.2
    else:
        print(f"✗ Missing produced PDF at {produced_pdf}")
        print(f"REWARD: {score}")
        return score  # cannot continue without the file

    # 2) Load both PDFs safely
    try:
        prod_reader = PdfReader(str(produced_pdf))
        print(f"Produced PDF pages: {len(prod_reader.pages)}")
    except Exception as e:
        print(f"✗ Unable to read produced PDF: {e}")
        print(f"REWARD: {score}")
        return score

    if not golden_pdf.exists():
        print(f"✗ Golden reference PDF missing at {golden_pdf}")
        print(f"REWARD: {score}")
        return score

    try:
        gold_reader = PdfReader(str(golden_pdf))
        print(f"Golden PDF pages: {len(gold_reader.pages)}")
    except Exception as e:
        print(f"✗ Unable to read golden PDF: {e}")
        print(f"REWARD: {score}")
        return score

    # 3) Page-count verification
    if len(prod_reader.pages) == len(gold_reader.pages):
        print("✓ Page count matches golden reference")
        score += 0.2
    else:
        print(
            f"✗ Page count mismatch (Produced: {len(prod_reader.pages)} vs Golden: {len(gold_reader.pages)})"
        )

    # 4) Per-page text comparison (shares remaining 0.6)
    total_pages = len(gold_reader.pages)
    matched_pages = 0
    for idx in range(min(len(prod_reader.pages), total_pages)):
        prod_text = _normalize(prod_reader.pages[idx].extract_text())
        gold_text = _normalize(gold_reader.pages[idx].extract_text())
        if prod_text == gold_text:
            matched_pages += 1
        else:
            print(f"Page {idx + 1}: text differs from golden reference")

    if matched_pages:
        text_score = 0.6 * (matched_pages / total_pages)
        score += text_score
        if matched_pages == total_pages:
            print("✓ All page texts match golden reference")
        else:
            print(f"✓ {matched_pages}/{total_pages} pages text match golden reference")
    else:
        print("✗ None of the page texts match the golden reference")

    final = round(min(score, 1.0), 2)
    print(f"REWARD: {final}")
    return final


if __name__ == "__main__":
    verify_task()

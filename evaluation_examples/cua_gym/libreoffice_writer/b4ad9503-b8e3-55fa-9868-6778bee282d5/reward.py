"""
FINAL REWARD SCRIPT - SUCCESS
Task: Export this document as a PDF and keep the same base name.
Generated: 2025-10-14 09:55:20
Status: success
Model: azure-o3
Total Steps: 13
"""

import os
import glob
from docx import Document
from PyPDF2 import PdfReader


def verify_pdf_export():
    """Reward script for task: Export the DOCX to a PDF with the same base name.

    Returns a progressive score (0.0–1.0) based on:
      1. Presence of a PDF that keeps the original DOCX base name (0.4)
      2. PDF readability / at least one page (0.3)
      3. Textual overlap between DOCX and PDF content (up to 0.3)
    """

    base_docx = "/home/user/export_this_document_as_a_pdf_and_keep_the_same_base_name.docx"
    expected_pdf = os.path.splitext(base_docx)[0] + ".pdf"

    total_score = 0.0
    max_score = 1.0

    # ------------------------------------------------------------------
    # Criterion 1 – Correct-named PDF exists (major requirement)
    # ------------------------------------------------------------------
    pdf_path = None
    if os.path.exists(expected_pdf):
        pdf_path = expected_pdf
        print(f"✓ PDF with correct base name found: {pdf_path}")
        total_score += 0.4
    else:
        # Partial credit if *some* PDF exists in the same directory
        pdf_candidates = glob.glob(os.path.join(os.path.dirname(base_docx), "*.pdf"))
        if pdf_candidates:
            pdf_path = pdf_candidates[0]
            print(f"✗ Expected PDF name not found, but another PDF found: {pdf_path}")
            total_score += 0.2
        else:
            print("✗ No PDF file found; cannot proceed further.")
            print(f"REWARD: {total_score}")
            return total_score

    # ------------------------------------------------------------------
    # Criterion 2 – PDF is readable & has ≥1 page
    # ------------------------------------------------------------------
    try:
        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)
        if num_pages > 0:
            print(f"✓ PDF is readable with {num_pages} page(s)")
            total_score += 0.3
        else:
            print("✗ PDF has zero pages")
    except Exception as e:
        print(f"✗ Failed to read PDF: {e}")
        print(f"REWARD: {total_score}")
        return total_score

    # ------------------------------------------------------------------
    # Criterion 3 – Textual overlap between DOCX & PDF
    # ------------------------------------------------------------------
    try:
        # Collect meaningful paragraphs (≥10 chars, first 30) from DOCX
        doc = Document(base_docx)
        doc_paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        meaningful = [p for p in doc_paragraphs if len(p) >= 10][:30]

        # Extract text from the PDF
        pdf_text_combined = "".join(page.extract_text() or "" for page in reader.pages)
        pdf_lower = pdf_text_combined.lower()

        matched = sum(1 for p in meaningful if p.lower() in pdf_lower)
        ratio = matched / len(meaningful) if meaningful else 0
        print(f"Paragraph match ratio: {matched}/{len(meaningful)} = {ratio:.2f}")

        if ratio >= 0.6:
            print("✓ High textual overlap – content correctly exported")
            total_score += 0.3
        elif ratio >= 0.2:
            print("⚠️  Partial textual overlap detected")
            total_score += 0.15
        else:
            # If text extraction fails but file size big enough, minimal credit
            if (not pdf_text_combined.strip()) and os.path.getsize(pdf_path) > 20 * 1024:
                print("⚠️  Text extraction failed but PDF size suggests content; granting minimal credit")
                total_score += 0.05
            else:
                print("✗ Low textual overlap; content mismatch")
    except Exception as e:
        print(f"✗ Error during content comparison: {e}")

    # ------------------------------------------------------------------
    # Final score
    # ------------------------------------------------------------------
    final_score = min(total_score, max_score)
    print(f"Total score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_pdf_export()

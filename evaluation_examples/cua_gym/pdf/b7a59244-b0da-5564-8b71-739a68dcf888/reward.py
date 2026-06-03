"""
FINAL REWARD SCRIPT - SUCCESS
Task: Fill in the shipping label form 'shipping_label.pdf' on Desktop with Sender: 'John Doe, 123 Main St', Recipient: 'Jane Smith, 456 Oak Ave', Weight: '5 lbs', and save as 'label_filled.pdf'.
Generated: 2025-11-29 10:03:15
Status: success
Model: o3
Total Steps: 9
"""

from pathlib import Path
from PyPDF2 import PdfReader


def verify_label_filled() -> float:
    """Verify that the shipping label form was filled correctly.

    Expected artefact:
      ~/Desktop/label_filled.pdf  – must contain the filled-in text:
        • Sender:    "John Doe, 123 Main St"
        • Recipient: "Jane Smith, 456 Oak Ave"
        • Weight:    "5 lbs"

    Scoring (progressive – totals exactly 1.0):
        Sender present      → +0.33
        Recipient present   → +0.33
        Weight present      → +0.34
    """
    pdf_path = Path.home() / "Desktop" / "label_filled.pdf"
    max_score = 1.0
    score = 0.0  # progressive accumulator

    # ---------- Prerequisite checks (no points) ----------
    if not pdf_path.exists():
        print(f"✗ Required file not found: {pdf_path}")
        print("REWARD: 0.0")
        return 0.0
    print(f"✓ Found file: {pdf_path}")

    try:
        reader = PdfReader(str(pdf_path))
    except Exception as e:
        print(f"✗ Unable to read PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(reader.pages) == 0:
        print("✗ PDF contains zero pages")
        print("REWARD: 0.0")
        return 0.0
    print(f"✓ PDF contains {len(reader.pages)} page(s)")

    # ---------- Content verification (earns points) ----------
    extracted_text = "\n".join((page.extract_text() or "") for page in reader.pages).lower()

    expected_snippets = {
        "john doe, 123 main st": 0.33,   # Sender
        "jane smith, 456 oak ave": 0.33, # Recipient
        "5 lbs": 0.34                    # Weight
    }

    for snippet, weight in expected_snippets.items():
        if snippet in extracted_text:
            print(f"✓ Found '{snippet}' ( +{weight} )")
            score += weight
        else:
            print(f"✗ Missing '{snippet}' ( +0 )")

    final_score = min(score, max_score)
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_label_filled()

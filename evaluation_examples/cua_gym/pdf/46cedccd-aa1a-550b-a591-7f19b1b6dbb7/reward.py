"""
Reward Script: OCR scanned invoice to create searchable PDF overlay
Task ID: pdf_mbc_074
Domain: pdf
Scoring:
  Component 1: Output file exists at correct path (0.15)
  Component 2: Text layer present with substantial content (0.25)
  Component 3: Invoice number INV-2024-0847 is searchable (0.25)
  Component 4: Key invoice content preserved in text layer (0.20)
  Component 5: Scanned image preserved in the PDF (0.15)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_074'

# The task asks to save the searchable PDF here
OUTPUT_PATH = os.path.join(WORKDIR, 'Documents', 'scanned_invoice_searchable.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: file must be a valid PDF we can open
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if doc.page_count < 1:
        print("CRITICAL: PDF has no pages")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    page = doc[0]

    # Component 1: Output file is a valid PDF with at least 1 page (0.15 points)
    # This differentiates initial (no searchable file) from golden (has searchable file).
    # The initial env only has scanned_invoice.pdf, NOT scanned_invoice_searchable.pdf.
    try:
        if doc.page_count >= 1 and doc.is_pdf:
            print(f"PASS: Component 1 -- Valid PDF at {file_path} with {doc.page_count} page(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Invalid PDF or no pages")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Text layer present with substantial content (0.25 points)
    # Initial PDF has text length 0 (pure scanned image). Golden should have >100 chars.
    try:
        text = page.get_text("text").strip()
        text_len = len(text)
        if text_len > 100:
            print(f"PASS: Component 2 -- Text layer has {text_len} characters (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- Text layer too short: {text_len} chars (need >100)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Invoice number INV-2024-0847 is searchable (0.25 points)
    # This is the specific ground truth from the task context.
    # Initial PDF has 0 search results; golden should find it.
    try:
        search_results = page.search_for("INV-2024-0847")
        if len(search_results) >= 1:
            print(f"PASS: Component 3 -- Invoice number INV-2024-0847 found ({len(search_results)} hit(s)) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- Invoice number INV-2024-0847 not found in text layer")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Key invoice content preserved in text layer (0.20 points)
    # Verify multiple key strings from the invoice are present in the OCR text.
    # These are content-specific checks that only pass when OCR has been performed.
    try:
        text = page.get_text("text")
        key_strings = [
            "Meridian Supply Co",   # Company name
            "INVOICE",              # Document type
            "$1,101.27",            # Total amount (or close variant)
            "Cascade Engineering",  # Bill-to company
        ]
        found_count = 0
        for s in key_strings:
            if s in text:
                found_count += 1
                print(f"  Found key string: '{s}'")
            else:
                print(f"  Missing key string: '{s}'")

        if found_count == len(key_strings):
            print(f"PASS: Component 4 -- All {len(key_strings)} key strings found (0.20 pts)")
            total_score += 0.20
        elif found_count >= 2:
            partial = round(0.20 * found_count / len(key_strings), 2)
            print(f"PARTIAL: Component 4 -- {found_count}/{len(key_strings)} key strings found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- Only {found_count}/{len(key_strings)} key strings found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Scanned image preserved in the PDF (0.15 points)
    # The task says "scanned image is preserved". The PDF should still contain
    # at least one image (the original scan). Both initial and golden have an image,
    # but this component is gated by the file being the searchable output (Component 1).
    # On initial_env, the searchable file doesn't exist, so we never reach here.
    try:
        images = page.get_images()
        if len(images) >= 1:
            print(f"PASS: Component 5 -- Scanned image preserved ({len(images)} image(s)) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 -- No images found in PDF (scan not preserved)")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: verify the searchable PDF output
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)

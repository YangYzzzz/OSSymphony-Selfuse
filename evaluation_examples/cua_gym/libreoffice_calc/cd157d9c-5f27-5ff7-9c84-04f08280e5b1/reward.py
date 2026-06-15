"""
Reward Script: Convert scanned receipt image PDF to searchable PDF using OCR
Task ID: pdf_fin_015
Domain: pdf
Scoring:
  - Component 1 (0.15): Searchable PDF file exists with a text layer
  - Component 2 (0.25): Text layer has substantial content (>100 chars)
  - Component 3 (0.30): Key receipt keywords present (restaurant, items, total)
  - Component 4 (0.15): Dollar amounts extracted from receipt
  - Component 5 (0.15): Page structure preserved (1 page, image still present)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_015'

SEARCHABLE_PATH = os.path.join(WORKDIR, 'finance', 'scanned_receipt_searchable.pdf')


def verify_task(file_path):
    """
    Verify that the scanned receipt PDF has been converted to a searchable PDF.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: Searchable PDF not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf
        except ImportError:
            print("CRITICAL: Neither pymupdf nor fitz available")
            print("REWARD: 0.0")
            return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract text from the document
    try:
        page = doc[0]
        extracted_text = page.get_text("text")
    except Exception as e:
        print(f"CRITICAL: Cannot extract text from page 0: {e}")
        extracted_text = ""

    # Component 1: Searchable PDF has a text layer (0.15 points)
    # This fails on initial_env because the file does not exist there.
    try:
        text_len = len(extracted_text.strip())
        if text_len > 0:
            print(f"PASS: Component 1 — text layer present, {text_len} chars (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — no text layer found (0 chars extracted)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Text layer has substantial content (0.25 points)
    # A properly OCR'd receipt should yield well over 100 characters
    try:
        text_len = len(extracted_text.strip())
        if text_len > 100:
            print(f"PASS: Component 2 — substantial text content, {text_len} chars > 100 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — text too short: {text_len} chars (need > 100)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Key receipt keywords present (0.30 points)
    # The receipt should contain recognizable restaurant receipt terms.
    # We check for multiple keyword groups; partial credit within component.
    try:
        text_lower = extracted_text.lower()
        keyword_groups = [
            # Restaurant/header info
            (["golden fork", "restaurant"], "restaurant name"),
            # Receipt structure keywords
            (["subtotal", "tax", "total"], "receipt totals"),
            # Food items (at least some should be recognized)
            (["salmon", "salad", "risotto", "burger", "tiramisu", "espresso", "wine", "fries"], "food items"),
        ]
        groups_passed = 0
        for keywords, group_name in keyword_groups:
            if any(kw in text_lower for kw in keywords):
                print(f"  PASS: keyword group '{group_name}' found")
                groups_passed += 1
            else:
                print(f"  FAIL: keyword group '{group_name}' not found in extracted text")

        if groups_passed == len(keyword_groups):
            print(f"PASS: Component 3 — all {len(keyword_groups)} keyword groups found (0.30 pts)")
            total_score += 0.30
        elif groups_passed >= 2:
            partial = round(0.30 * groups_passed / len(keyword_groups), 2)
            print(f"PARTIAL: Component 3 — {groups_passed}/{len(keyword_groups)} keyword groups ({partial} pts)")
            total_score += partial
        elif groups_passed == 1:
            print(f"PARTIAL: Component 3 — only {groups_passed}/{len(keyword_groups)} keyword groups (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — no keyword groups found in extracted text")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Dollar amounts present in extracted text (0.15 points)
    # The receipt contains amounts like $12.50, $56.00, $229.74 etc.
    try:
        dollar_pattern = re.findall(r'\$\d+\.\d{2}', extracted_text)
        if len(dollar_pattern) >= 3:
            print(f"PASS: Component 4 — {len(dollar_pattern)} dollar amounts found (0.15 pts)")
            total_score += 0.15
        elif len(dollar_pattern) >= 1:
            print(f"PARTIAL: Component 4 — only {len(dollar_pattern)} dollar amounts (0.07 pts)")
            total_score += 0.07
        else:
            print(f"FAIL: Component 4 — no dollar amounts found in text")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Page structure preserved (0.15 points)
    # Should be single page and contain the original image
    try:
        page_count = doc.page_count
        images = page.get_images()
        page_ok = page_count == 1
        image_ok = len(images) >= 1

        if page_ok and image_ok:
            print(f"PASS: Component 5 — 1 page, {len(images)} image(s) preserved (0.15 pts)")
            total_score += 0.15
        elif page_ok:
            print(f"PARTIAL: Component 5 — 1 page but no images found (0.07 pts)")
            total_score += 0.07
        else:
            print(f"FAIL: Component 5 — page_count={page_count} (expected 1), images={len(images)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(SEARCHABLE_PATH):
    print(f"File not found: {SEARCHABLE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(SEARCHABLE_PATH)

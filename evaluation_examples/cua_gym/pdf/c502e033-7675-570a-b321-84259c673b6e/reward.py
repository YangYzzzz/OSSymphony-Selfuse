"""
Reward Script: Create a PDF receipt for Downtown Office Supplies
Task ID: pdf_fin_010
Domain: pdf
Scoring:
  - Component 1 (0.15): Store name and receipt header (date + receipt #)
  - Component 2 (0.30): All three line items with correct amounts
  - Component 3 (0.20): Correct subtotal, tax, and total
  - Component 4 (0.15): 'PAID' stamp text present in red color
  - Component 5 (0.10): Single page document
  - Component 6 (0.10): Total amount $158.16 in bold
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_010'
FILE_PATH = os.path.join(WORKDIR, 'finance', 'receipt_20240315.pdf')


def get_text_spans(pdf_path):
    """Extract all text spans with font/color info from page 0."""
    import pymupdf
    doc = pymupdf.open(pdf_path)
    page = doc[0]
    data = page.get_text("dict")
    doc.close()
    spans = []
    for block in data["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                c = span["color"]
                rgb = (c >> 16 & 0xFF, c >> 8 & 0xFF, c & 0xFF)
                spans.append({
                    "text": span["text"],
                    "font": span["font"],
                    "size": span["size"],
                    "color_rgb": rgb,
                    "flags": span["flags"],
                    "bold": bool(span["flags"] & 16),
                })
    return spans


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: file must exist and be loadable
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import pymupdf
        doc = pymupdf.open(file_path)
        full_text = doc[0].get_text("text")
        page_count = doc.page_count
        doc.close()
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        spans = get_text_spans(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot extract text spans: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Store name and receipt header info (0.15 points)
    # Checks: "Downtown Office Supplies", date "2024-03-15", receipt # "REC-8847"
    try:
        has_store = "Downtown Office Supplies" in full_text
        has_date = "2024-03-15" in full_text
        has_receipt_num = "REC-8847" in full_text
        header_count = sum([has_store, has_date, has_receipt_num])
        if header_count == 3:
            print(f"PASS: Component 1 -- Store name, date, receipt # all present (0.15 pts)")
            total_score += 0.15
        else:
            missing = []
            if not has_store:
                missing.append("store name")
            if not has_date:
                missing.append("date 2024-03-15")
            if not has_receipt_num:
                missing.append("receipt # REC-8847")
            print(f"FAIL: Component 1 -- Missing: {', '.join(missing)} ({header_count}/3)")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: All three line items with correct amounts (0.30 points)
    # Items: Printer Paper (5 reams) $45.00, Ink Cartridges (3) $89.97, File Folders (box) $12.50
    try:
        items_found = 0
        # Check each item name AND its amount in the full text
        item_checks = [
            ("Printer Paper", "45.00"),
            ("Ink Cartridges", "89.97"),
            ("File Folders", "12.50"),
        ]
        for item_name, amount in item_checks:
            if item_name in full_text and amount in full_text:
                items_found += 1
            else:
                print(f"  INFO: Item '{item_name}' (${amount}) -- name={'found' if item_name in full_text else 'MISSING'}, amount={'found' if amount in full_text else 'MISSING'}")

        if items_found == 3:
            print(f"PASS: Component 2 -- All 3 line items with correct amounts (0.30 pts)")
            total_score += 0.30
        elif items_found >= 1:
            partial = round(0.10 * items_found, 2)
            print(f"PARTIAL: Component 2 -- {items_found}/3 items found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- No line items found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Correct subtotal, tax, and total (0.20 points)
    # Subtotal $147.47, Tax $10.69, Total $158.16
    try:
        has_subtotal = "147.47" in full_text
        has_tax = "10.69" in full_text
        has_total = "158.16" in full_text
        money_count = sum([has_subtotal, has_tax, has_total])
        if money_count == 3:
            print(f"PASS: Component 3 -- Subtotal, tax, total all correct (0.20 pts)")
            total_score += 0.20
        else:
            missing = []
            if not has_subtotal:
                missing.append("subtotal $147.47")
            if not has_tax:
                missing.append("tax $10.69")
            if not has_total:
                missing.append("total $158.16")
            print(f"FAIL: Component 3 -- Missing: {', '.join(missing)} ({money_count}/3)")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: 'PAID' stamp in red color (0.15 points)
    # Red means RGB close to (255, 0, 0) - red channel high, green and blue low
    try:
        paid_red_spans = [
            span for span in spans
            if "PAID" in span["text"]
            and span["color_rgb"][0] > 200
            and span["color_rgb"][1] < 50
            and span["color_rgb"][2] < 50
        ]
        for span in spans:
            if "PAID" in span["text"]:
                r, g, b = span["color_rgb"]
                print(f"  INFO: Found 'PAID' with color RGB=({r},{g},{b})")

        if len(paid_red_spans) > 0:
            print(f"PASS: Component 4 -- 'PAID' stamp in red (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 -- 'PAID' text not found in red")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Single page document (0.10 points)
    # Task says "Single page document"
    try:
        if page_count == 1:
            print(f"PASS: Component 5 -- Single page document (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 -- Expected 1 page, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: Total amount $158.16 in bold (0.10 points)
    try:
        total_bold_spans = [
            span for span in spans
            if "158.16" in span["text"] and span["bold"]
        ]

        if len(total_bold_spans) > 0:
            print(f"PASS: Component 6 -- Total $158.16 in bold (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 -- Total $158.16 not found in bold")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

"""
Reward Script: Credit Memo PDF Verification
Task ID: pdf_fin_087
Domain: pdf
Scoring:
  Component 1 (0.15): Issuer and credit memo number present
  Component 2 (0.15): Customer and original invoice reference present
  Component 3 (0.25): All 3 line items with correct descriptions
  Component 4 (0.20): Correct total credit amount ($965.00)
  Component 5 (0.25): Blue 'CREDIT' stamp text
"""

import os
import sys

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_087'
FILE_PATH = os.path.join(WORKDIR, 'finance', 'credit_memo_CM2024_015.pdf')


def verify_task(file_path):
    """
    Verify credit memo PDF with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid PDF
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import pymupdf
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

    # Extract full text for text-based checks
    try:
        full_text = ""
        for page in doc:
            full_text += page.get_text("text")
    except Exception as e:
        print(f"CRITICAL: Cannot extract text: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Issuer and credit memo number (0.15 points)
    # Task requires: From 'Pacific Wholesale Distributors', Credit Memo #CM-2024-015
    try:
        has_issuer = "Pacific Wholesale Distributors" in full_text
        has_memo_num = "CM-2024-015" in full_text
        if has_issuer and has_memo_num:
            print(f"PASS: Component 1 — Issuer and credit memo # found (0.15 pts)")
            total_score += 0.15
        else:
            missing = []
            if not has_issuer:
                missing.append("'Pacific Wholesale Distributors'")
            if not has_memo_num:
                missing.append("'CM-2024-015'")
            print(f"FAIL: Component 1 — Missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Customer and original invoice (0.15 points)
    # Task requires: Customer 'Coastal Retail Group', Original Invoice INV-2024-0842
    try:
        has_customer = "Coastal Retail Group" in full_text
        has_invoice = "INV-2024-0842" in full_text
        if has_customer and has_invoice:
            print(f"PASS: Component 2 — Customer and original invoice found (0.15 pts)")
            total_score += 0.15
        else:
            missing = []
            if not has_customer:
                missing.append("'Coastal Retail Group'")
            if not has_invoice:
                missing.append("'INV-2024-0842'")
            print(f"FAIL: Component 2 — Missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 3 line items with correct descriptions (0.25 points)
    # Task requires:
    #   - 'Damaged Goods Return (15 units @ $42.00)' ($630.00)
    #   - 'Pricing Adjustment per Contract' ($250.00)
    #   - 'Shipping Overcharge' ($85.00)
    try:
        line_items_found = 0
        items = [
            ("Damaged Goods Return", "630"),
            ("Pricing Adjustment", "250"),
            ("Shipping Overcharge", "85"),
        ]
        for desc, amount in items:
            if desc in full_text and amount in full_text:
                line_items_found += 1
            else:
                print(f"  INFO: Line item '{desc}' (${amount}) — desc_found={desc in full_text}, amount_found={amount in full_text}")

        if line_items_found == 3:
            print(f"PASS: Component 3 — All 3 line items found with amounts (0.25 pts)")
            total_score += 0.25
        elif line_items_found >= 1:
            partial = round(0.25 * line_items_found / 3, 3)
            print(f"PARTIAL: Component 3 — {line_items_found}/3 line items found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No line items found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Correct total credit amount $965.00 (0.20 points)
    try:
        has_total_label = "Total Credit" in full_text or "Total credit" in full_text or "TOTAL CREDIT" in full_text
        has_total_value = "$965.00" in full_text or "965.00" in full_text
        if has_total_label and has_total_value:
            print(f"PASS: Component 4 — Total credit $965.00 found (0.20 pts)")
            total_score += 0.20
        elif has_total_value:
            print(f"PARTIAL: Component 4 — Value 965.00 found but missing 'Total Credit' label (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — Total credit $965.00 not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Blue 'CREDIT' stamp text (0.25 points)
    # Task requires: 'CREDIT' stamp in blue
    # Golden has: 'CREDIT' text in color (0, 102, 204) which is blue, size ~48, bold
    try:
        page = doc[0]
        d = page.get_text("dict")
        # Scan all spans for a standalone "CREDIT" stamp with blue color
        credit_stamp_color = None  # will hold (r, g, b) if found

        for block in d["blocks"]:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    txt = span["text"].strip()
                    # Look for standalone "CREDIT" (not "CREDIT MEMO")
                    if txt == "CREDIT":
                        c = span["color"]
                        r = (c >> 16) & 0xFF
                        g = (c >> 8) & 0xFF
                        b_val = c & 0xFF
                        credit_stamp_color = (r, g, b_val)
                        print(f"  INFO: Found 'CREDIT' stamp — color RGB=({r},{g},{b_val}), size={span.get('size', 0)}")

        if credit_stamp_color is not None and credit_stamp_color[2] > 100 and credit_stamp_color[2] > credit_stamp_color[0] and credit_stamp_color[2] > credit_stamp_color[1]:
            print(f"PASS: Component 5 — Blue 'CREDIT' stamp found (0.25 pts)")
            total_score += 0.25
        elif credit_stamp_color is not None:
            print(f"PARTIAL: Component 5 — 'CREDIT' stamp found but not blue (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — 'CREDIT' stamp text not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

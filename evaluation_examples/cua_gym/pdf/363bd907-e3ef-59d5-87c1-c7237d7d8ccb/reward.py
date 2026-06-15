"""
Reward Script: Purchase Order PDF verification
Task ID: pdf_fin_079
Domain: pdf
Scoring:
  Component 1: Header info (company, PO#, date) — 0.20
  Component 2: Vendor info — 0.15
  Component 3: Ship-to info — 0.10
  Component 4: Line items (3 items with correct data) — 0.25
  Component 5: Financial totals (subtotal/shipping/tax/total) — 0.20
  Component 6: Payment terms — 0.10
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_079'
FILE_PATH = os.path.join(WORKDIR, 'finance', 'po_2024_0089.pdf')


def verify_task(file_path):
    """
    Verify purchase order PDF with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: load PDF
    try:
        import pymupdf
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all text from the PDF
    try:
        full_text = ""
        for page in doc:
            full_text += page.get_text("text")
        doc.close()
    except Exception as e:
        print(f"CRITICAL: Cannot extract text from PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Normalize text for easier matching
    text_lower = full_text.lower()
    # Collapse whitespace for pattern matching
    text_collapsed = re.sub(r'\s+', ' ', full_text).strip()
    text_collapsed_lower = text_collapsed.lower()

    # Component 1: Header info — company name, PO number, date (0.20 pts)
    try:
        header_score = 0.0
        has_company = "midwest manufacturing" in text_collapsed_lower
        has_po_number = "2024-0089" in full_text
        has_date = "march 18, 2024" in text_collapsed_lower or "march 18,2024" in text_collapsed_lower

        if has_company:
            header_score += 0.07
            print("PASS: Company name 'MidWest Manufacturing' found")
        else:
            print("FAIL: Company name 'MidWest Manufacturing' not found")

        if has_po_number:
            header_score += 0.07
            print("PASS: PO number '2024-0089' found")
        else:
            print("FAIL: PO number '2024-0089' not found")

        if has_date:
            header_score += 0.06
            print("PASS: Date 'March 18, 2024' found")
        else:
            print("FAIL: Date 'March 18, 2024' not found")

        if header_score > 0:
            print(f"PASS: Component 1 — Header info ({header_score:.2f} pts)")
            total_score += header_score
        else:
            print("FAIL: Component 1 — No header info found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Vendor info (0.15 pts)
    try:
        vendor_score = 0.0
        has_vendor_name = "steel supply co" in text_collapsed_lower
        has_vendor_addr = "450 industrial blvd" in text_collapsed_lower
        has_vendor_city = "detroit" in text_collapsed_lower and "mi" in text_collapsed_lower and "48201" in full_text

        if has_vendor_name:
            vendor_score += 0.05
            print("PASS: Vendor name 'Steel Supply Co.' found")
        else:
            print("FAIL: Vendor name 'Steel Supply Co.' not found")

        if has_vendor_addr:
            vendor_score += 0.05
            print("PASS: Vendor address '450 Industrial Blvd' found")
        else:
            print("FAIL: Vendor address '450 Industrial Blvd' not found")

        if has_vendor_city:
            vendor_score += 0.05
            print("PASS: Vendor city 'Detroit, MI 48201' found")
        else:
            print("FAIL: Vendor city 'Detroit, MI 48201' not found")

        if vendor_score > 0:
            print(f"PASS: Component 2 — Vendor info ({vendor_score:.2f} pts)")
            total_score += vendor_score
        else:
            print("FAIL: Component 2 — No vendor info found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Ship-to info (0.10 pts)
    try:
        ship_score = 0.0
        has_ship_name = "midwest manufacturing" in text_collapsed_lower
        has_ship_addr = "100 factory lane" in text_collapsed_lower
        has_ship_city = "chicago" in text_collapsed_lower and "il" in text_collapsed_lower and "60601" in full_text

        # Ship-to requires both the name AND the address to appear — but we need to distinguish
        # from the header company name. Check that the address and city appear in the text.
        if has_ship_addr and has_ship_city:
            ship_score += 0.10
            print("PASS: Ship-to address '100 Factory Lane, Chicago, IL 60601' found")
        else:
            if not has_ship_addr:
                print("FAIL: Ship-to address '100 Factory Lane' not found")
            if not has_ship_city:
                print("FAIL: Ship-to city 'Chicago, IL 60601' not found")

        if ship_score > 0:
            print(f"PASS: Component 3 — Ship-to info ({ship_score:.2f} pts)")
            total_score += ship_score
        else:
            print("FAIL: Component 3 — Ship-to info incomplete")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Line items — 3 items with correct descriptions and amounts (0.25 pts)
    try:
        items_score = 0.0

        # Item 1: Steel Plate 4x8, 10 units @ $450.00 = $4,500.00
        has_item1_desc = "steel plate 4x8" in text_collapsed_lower or "steel plate" in text_collapsed_lower
        has_item1_amount = "$4,500" in full_text or "4,500.00" in full_text or "4500" in full_text
        if has_item1_desc and has_item1_amount:
            items_score += 0.083
            print("PASS: Item 1 — Steel Plate 4x8 with amount $4,500.00")
        else:
            print(f"FAIL: Item 1 — Steel Plate 4x8 (desc={has_item1_desc}, amount={has_item1_amount})")

        # Item 2: Steel Rod 1in, 50 units @ $28.00 = $1,400.00
        has_item2_desc = "steel rod 1in" in text_collapsed_lower or "steel rod" in text_collapsed_lower
        has_item2_amount = "$1,400" in full_text or "1,400.00" in full_text or "1400" in full_text
        if has_item2_desc and has_item2_amount:
            items_score += 0.083
            print("PASS: Item 2 — Steel Rod 1in with amount $1,400.00")
        else:
            print(f"FAIL: Item 2 — Steel Rod 1in (desc={has_item2_desc}, amount={has_item2_amount})")

        # Item 3: Welding Wire, 20 spools @ $65.00 = $1,300.00
        has_item3_desc = "welding wire" in text_collapsed_lower
        has_item3_amount = "$1,300" in full_text or "1,300.00" in full_text or "1300" in full_text
        if has_item3_desc and has_item3_amount:
            items_score += 0.084
            print("PASS: Item 3 — Welding Wire with amount $1,300.00")
        else:
            print(f"FAIL: Item 3 — Welding Wire (desc={has_item3_desc}, amount={has_item3_amount})")

        if items_score > 0:
            print(f"PASS: Component 4 — Line items ({items_score:.3f} pts)")
            total_score += items_score
        else:
            print("FAIL: Component 4 — No line items found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Financial totals (0.20 pts)
    try:
        fin_score = 0.0

        # Subtotal: $6,200.00
        has_subtotal = ("$6,200" in full_text or "6,200.00" in full_text or "6200" in full_text) and "subtotal" in text_lower
        if has_subtotal:
            fin_score += 0.05
            print("PASS: Subtotal $6,200.00 found")
        else:
            print("FAIL: Subtotal $6,200.00 not found")

        # Shipping: $350.00
        has_shipping = ("$350" in full_text or "350.00" in full_text) and "shipping" in text_lower
        if has_shipping:
            fin_score += 0.05
            print("PASS: Shipping $350.00 found")
        else:
            print("FAIL: Shipping $350.00 not found")

        # Tax: $387.50 (6.25%)
        has_tax = ("$387.50" in full_text or "387.50" in full_text) and ("6.25%" in full_text or "6.25" in full_text)
        if has_tax:
            fin_score += 0.05
            print("PASS: Tax $387.50 (6.25%) found")
        else:
            print("FAIL: Tax $387.50 (6.25%) not found")

        # Total: $6,937.50
        has_total = "$6,937.50" in full_text or "6,937.50" in full_text or "6937.50" in full_text
        if has_total:
            fin_score += 0.05
            print("PASS: Total $6,937.50 found")
        else:
            print("FAIL: Total $6,937.50 not found")

        if fin_score > 0:
            print(f"PASS: Component 5 — Financial totals ({fin_score:.2f} pts)")
            total_score += fin_score
        else:
            print("FAIL: Component 5 — No financial totals found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Payment terms — Net 30 (0.10 pts)
    try:
        has_terms = "net 30" in text_lower
        if has_terms:
            print("PASS: Component 6 — Payment terms 'Net 30' found (0.10 pts)")
            total_score += 0.10
        else:
            print("FAIL: Component 6 — Payment terms 'Net 30' not found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score:.3f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

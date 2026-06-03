"""
Reward Script: Inventory Valuation Report PDF
Task ID: pdf_fin_090
Domain: pdf
Scoring:
  Component 1 (0.20): PDF exists AND contains title "Inventory Valuation Report - March 31, 2024"
  Component 2 (0.30): Table has 15 inventory items with correct column headers
  Component 3 (0.15): Total inventory value present at bottom
  Component 4 (0.25): Pie chart present with 3 category labels (Raw Materials, WIP, Finished Goods)
  Component 5 (0.10): FIFO valuation method referenced in document
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_090'
TARGET_FILE = os.path.join(WORKDIR, 'finance', 'inventory_valuation.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be loadable
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import pymupdf
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all text from all pages
    all_text = ""
    page_texts = []
    for i in range(doc.page_count):
        t = doc[i].get_text("text")
        page_texts.append(t)
        all_text += t + "\n"

    all_text_lower = all_text.lower()

    # Component 1: Title present (0.20 points)
    # The PDF must contain the title "Inventory Valuation Report - March 31, 2024"
    # This is task-introduced: initial_env has no PDF at all
    try:
        title_found = ("inventory valuation report" in all_text_lower and "march 31, 2024" in all_text_lower)

        if title_found:
            print(f"PASS: Component 1 - Title 'Inventory Valuation Report - March 31, 2024' found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 - Title not found. Text preview: {all_text[:200]}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Table with 15 inventory items and correct columns (0.30 points)
    # Must have columns: Item Code, Description, Quantity, Unit Cost, Total Value, Valuation Method
    # Must have 15 data rows
    try:
        # Check for column headers
        headers_required = ["item code", "description", "quantity", "unit cost", "total value", "valuation method"]
        headers_found = sum(1 for h in headers_required if h in all_text_lower)
        headers_ok = headers_found >= 5  # allow minor variation in header naming

        # Count inventory item rows by looking for item code patterns (RM-xxxx, WP-xxxx, FG-xxxx)
        item_codes = re.findall(r'\b(?:RM|WP|FG)-\d{4}\b', all_text)
        # Deduplicate (same code might appear in text)
        unique_codes = set(item_codes)
        items_count = len(unique_codes)

        sub_score = 0.0
        # Sub-score for headers (0.10)
        if headers_ok:
            sub_score += 0.10
            print(f"  Headers: {headers_found}/{len(headers_required)} found")
        else:
            print(f"  FAIL: Only {headers_found}/{len(headers_required)} column headers found")

        # Sub-score for item count (0.20)
        if items_count >= 15:
            sub_score += 0.20
            print(f"  Items: {items_count} unique item codes found (>= 15)")
        elif items_count >= 10:
            sub_score += 0.10
            print(f"  PARTIAL: {items_count} unique item codes found (>= 10 but < 15)")
        else:
            print(f"  FAIL: Only {items_count} unique item codes found (expected >= 15)")

        if sub_score > 0:
            print(f"PASS: Component 2 - Table structure ({sub_score:.2f} pts)")
            total_score += sub_score
        else:
            print(f"FAIL: Component 2 - Table structure insufficient")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Total inventory value present (0.15 points)
    # The report must have a total/grand total value at the bottom of the table
    try:
        # Look for "total" keyword (including "grand total") near a large dollar amount
        # Text extraction may put them on separate lines, so search within nearby lines
        has_total_keyword = bool(re.search(r'(?:grand\s+)?total', all_text_lower))
        # Check for dollar amounts that look like totals (> $50,000)
        dollar_amounts = re.findall(r'\$[\d,]+\.\d{2}', all_text)
        large_amounts = [a for a in dollar_amounts if float(a.replace('$', '').replace(',', '')) > 50000]

        if has_total_keyword and len(large_amounts) > 0:
            print(f"PASS: Component 3 - Total value found. 'Total' keyword present, large amounts: {large_amounts[:3]} (0.15 pts)")
            total_score += 0.15
        elif len(large_amounts) > 0:
            # Partial: large amounts exist even if "total" keyword not found
            print(f"PARTIAL: Component 3 - Large amounts found but 'total' keyword missing (0.07 pts)")
            total_score += 0.07
        else:
            print(f"FAIL: Component 3 - No total inventory value found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Pie chart with 3 category segments (0.25 points)
    # The chart should show Raw Materials, WIP, Finished Goods with percentage breakdown
    # reportlab charts render as vector drawings, not images
    try:
        # Check for vector drawings (pie chart segments) on page with chart content
        chart_page_idx = None
        for i in range(doc.page_count):
            page_text_lower = page_texts[i].lower()
            if "raw materials" in page_text_lower and ("wip" in page_text_lower or "work-in-progress" in page_text_lower) and "finished goods" in page_text_lower:
                # Check if this page has drawings (vector pie chart)
                drawings = doc[i].get_drawings()
                if len(drawings) >= 3:
                    chart_page_idx = i
                    break

        if chart_page_idx is not None:
            page = doc[chart_page_idx]
            drawings = page.get_drawings()
            page_text_lower = page_texts[chart_page_idx].lower()

            sub_score = 0.0
            # Pie chart has vector drawings (at least 3 segments)
            if len(drawings) >= 3:
                sub_score += 0.10
                print(f"  Pie chart: {len(drawings)} vector drawings found on page {chart_page_idx}")

            # Check for category labels with percentages
            has_raw_materials = "raw materials" in page_text_lower
            has_wip = "wip" in page_text_lower or "work-in-progress" in page_text_lower or "work in progress" in page_text_lower
            has_finished_goods = "finished goods" in page_text_lower
            categories_found = sum([has_raw_materials, has_wip, has_finished_goods])

            if categories_found >= 3:
                sub_score += 0.10
                print(f"  Categories: all 3 found (Raw Materials, WIP, Finished Goods)")
            elif categories_found >= 2:
                sub_score += 0.05
                print(f"  Categories: {categories_found}/3 found")

            # Check for percentage values on the chart page
            pct_matches = re.findall(r'\d+(?:\.\d+)?%', page_texts[chart_page_idx])
            if len(pct_matches) >= 3:
                sub_score += 0.05
                print(f"  Percentages on chart page: {pct_matches}")
            elif len(pct_matches) >= 1:
                sub_score += 0.02
                print(f"  Partial percentages: {pct_matches}")

            if sub_score > 0:
                print(f"PASS: Component 4 - Pie chart ({sub_score:.2f} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 4 - Pie chart not detected")
        else:
            # Fallback: check if chart labels exist anywhere in document even without drawings
            has_chart_labels = (
                "raw materials" in all_text_lower
                and ("wip" in all_text_lower or "work-in-progress" in all_text_lower)
                and "finished goods" in all_text_lower
            )
            # Check for percentage pattern on any page beyond page 0 (table page)
            if doc.page_count >= 2 and has_chart_labels:
                later_pages_text = "".join(page_texts[1:]).lower()
                if "raw materials" in later_pages_text and "finished goods" in later_pages_text:
                    print(f"PARTIAL: Component 4 - Category labels found but chart structure unclear (0.10 pts)")
                    total_score += 0.10
                else:
                    print(f"FAIL: Component 4 - No pie chart page found")
            else:
                print(f"FAIL: Component 4 - No pie chart page found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: FIFO valuation method referenced (0.10 points)
    # The document should explicitly mention FIFO as the valuation method
    try:
        fifo_mentions = len(re.findall(r'fifo|first[- ]in[, ]*first[- ]out', all_text_lower))
        if fifo_mentions >= 2:
            print(f"PASS: Component 5 - FIFO mentioned {fifo_mentions} times (0.10 pts)")
            total_score += 0.10
        elif fifo_mentions >= 1:
            print(f"PARTIAL: Component 5 - FIFO mentioned only {fifo_mentions} time (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 5 - FIFO not mentioned in document")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(TARGET_FILE):
    print(f"File not found: {TARGET_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(TARGET_FILE)

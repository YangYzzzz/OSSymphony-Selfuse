"""
Reward Script: Create a research budget PDF with table, categories, line items, and grand total
Task ID: pdf_cr_031
Domain: pdf
Scoring:
  Component 1 (0.15): PDF exists at correct path with 1 page
  Component 2 (0.15): Title 'Research Budget FY2024' present
  Component 3 (0.25): All 4 category headers present (Personnel, Equipment, Travel, Supplies)
  Component 4 (0.25): All 9 line items with amounts present
  Component 5 (0.10): Grand Total row with $265,000
  Component 6 (0.10): Bold formatting on Grand Total row
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_031'
FILE_PATH = os.path.join(WORKDIR, 'Desktop', 'budget.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PDF has exactly 1 page (0.15 points)
    try:
        page_count = doc.page_count
        if page_count >= 1:
            print(f"PASS: Component 1 -- PDF has {page_count} page(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Expected at least 1 page, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Extract full text for subsequent checks
    try:
        page = doc[0]
        full_text = page.get_text("text")
    except Exception as e:
        print(f"CRITICAL: Cannot extract text from page 0: {e}")
        doc.close()
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Title 'Research Budget FY2024' present (0.15 points)
    try:
        if "Research Budget FY2024" in full_text:
            print(f"PASS: Component 2 -- Title 'Research Budget FY2024' found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 -- Title 'Research Budget FY2024' not found in text")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: All 4 category headers present (0.25 points)
    try:
        categories = ["Personnel", "Equipment", "Travel", "Supplies"]
        found_categories = []
        for cat in categories:
            if cat in full_text:
                found_categories.append(cat)

        cat_ratio = len(found_categories) / len(categories)
        if cat_ratio == 1.0:
            print(f"PASS: Component 3 -- All 4 category headers found: {found_categories} (0.25 pts)")
            total_score += 0.25
        elif cat_ratio > 0:
            partial = round(0.25 * cat_ratio, 4)
            missing = [c for c in categories if c not in found_categories]
            print(f"PARTIAL: Component 3 -- {len(found_categories)}/4 categories found, missing: {missing} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- No category headers found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: All 9 line items with amounts present (0.25 points)
    try:
        line_items = [
            ("Principal Investigator", "$85,000"),
            ("Research Assistant (2x)", "$60,000"),
            ("Lab Technician", "$45,000"),
            ("Spectrometer", "$25,000"),
            ("Computing Cluster", "$15,000"),
            ("Conference (3x)", "$9,000"),
            ("Field Work", "$6,000"),
            ("Lab Materials", "$12,000"),
            ("Software Licenses", "$8,000"),
        ]
        found_items = 0
        for item_name, amount in line_items:
            if item_name in full_text and amount in full_text:
                found_items += 1
            else:
                if item_name not in full_text:
                    print(f"  DETAIL: Missing line item name: '{item_name}'")
                elif amount not in full_text:
                    print(f"  DETAIL: Missing amount for '{item_name}': '{amount}'")

        item_ratio = found_items / len(line_items)
        if item_ratio == 1.0:
            print(f"PASS: Component 4 -- All 9 line items with amounts found (0.25 pts)")
            total_score += 0.25
        elif item_ratio > 0:
            partial = round(0.25 * item_ratio, 4)
            print(f"PARTIAL: Component 4 -- {found_items}/9 line items found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- No line items with amounts found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Grand Total with $265,000 (0.10 points)
    try:
        has_grand_total = "Grand Total" in full_text
        has_amount = "$265,000" in full_text or "265,000" in full_text
        if has_grand_total and has_amount:
            print(f"PASS: Component 5 -- Grand Total with $265,000 found (0.10 pts)")
            total_score += 0.10
        else:
            if not has_grand_total:
                print(f"FAIL: Component 5 -- 'Grand Total' text not found")
            if not has_amount:
                print(f"FAIL: Component 5 -- '$265,000' amount not found")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: Bold formatting on Grand Total row (0.10 points)
    try:
        text_dict = page.get_text("dict")
        bold_grand_total_spans = 0
        for block in text_dict.get("blocks", []):
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    span_text = span.get("text", "").strip()
                    font_name = span.get("font", "")
                    # Check if Grand Total text or its amount is bold
                    if ("Grand Total" in span_text or span_text == "$265,000"):
                        if "Bold" in font_name or "bold" in font_name.lower():
                            bold_grand_total_spans += 1

        if bold_grand_total_spans > 0:
            print(f"PASS: Component 6 -- Grand Total row has bold formatting ({bold_grand_total_spans} bold span(s)) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 -- Grand Total row lacks bold formatting")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    doc.close()

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

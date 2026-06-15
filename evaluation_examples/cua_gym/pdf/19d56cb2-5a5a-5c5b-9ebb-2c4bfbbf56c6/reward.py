"""
Reward Script: Create a receipt template PDF with header, fields, table, and grand total
Task ID: pdf_pw_033
Domain: pdf
Scoring:
  Component 1: PDF exists and is single-page Letter size (0.15)
  Component 2: Header 'TechVentures LLC' centered at top in 20pt bold (0.25)
  Component 3: Horizontal line below header (0.10)
  Component 4: Receipt fields (Receipt #, Date, Customer) present (0.15)
  Component 5: Table with 4 columns (Item, Qty, Unit Price, Total) and 5+ empty rows (0.25)
  Component 6: 'Grand Total:' text at bottom-right area (0.10)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_033'
PDF_PATH = os.path.join(WORKDIR, 'forms', 'receipt_template.pdf')


def verify_task(file_path):
    # Lazy import pymupdf only when needed (file exists)
    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf
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

    # Component 1: PDF is single-page Letter size (0.15 points)
    try:
        page_count = doc.page_count
        if page_count == 1:
            page = doc[0]
            w, h = page.rect.width, page.rect.height
            # Letter size: 612 x 792 (with tolerance)
            if abs(w - 612) < 5 and abs(h - 792) < 5:
                print(f"PASS: Component 1 - Single page, Letter size ({w:.0f}x{h:.0f}) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 - Page size {w:.0f}x{h:.0f}, expected ~612x792")
        else:
            print(f"FAIL: Component 1 - Page count {page_count}, expected 1")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Header 'TechVentures LLC' centered at top in 20pt bold (0.25 points)
    try:
        page = doc[0]
        # Search for the header text
        instances = page.search_for("TechVentures LLC")
        if instances:
            rect = instances[0]
            # Check it's at the top of the page (y < 100)
            top_ok = rect.y0 < 100
            # Check it's approximately centered (text center vs page center)
            text_center_x = (rect.x0 + rect.x1) / 2
            page_center_x = page.rect.width / 2
            centered_ok = abs(text_center_x - page_center_x) < 50

            # Check font: 20pt bold via span analysis
            td = page.get_text("dict")
            header_spans = [
                span
                for block in td.get("blocks", []) if block.get("type") == 0
                for line in block.get("lines", [])
                for span in line.get("spans", [])
                if "TechVentures LLC" in span.get("text", "")
            ]
            header_bold = any(
                ("Bold" in s.get("font", "") or "bold" in s.get("font", "") or (s.get("flags", 0) & 16))
                for s in header_spans
            )
            header_size_ok = any(
                abs(s.get("size", 0) - 20) < 1.5
                for s in header_spans
            )

            if top_ok and centered_ok and header_bold and header_size_ok:
                print(f"PASS: Component 2 - Header 'TechVentures LLC' centered at top, 20pt bold (0.25 pts)")
                total_score += 0.25
            else:
                reasons = []
                if not top_ok:
                    reasons.append(f"not at top (y0={rect.y0:.1f})")
                if not centered_ok:
                    reasons.append(f"not centered (text_cx={text_center_x:.1f}, page_cx={page_center_x:.1f})")
                if not header_bold:
                    reasons.append("not bold")
                if not header_size_ok:
                    reasons.append("not 20pt")
                print(f"FAIL: Component 2 - Header issues: {', '.join(reasons)}")
        else:
            print("FAIL: Component 2 - 'TechVentures LLC' text not found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Horizontal line below header (0.10 points)
    try:
        page = doc[0]
        drawings = page.get_drawings()
        # Look for a horizontal line below the header area (y between 50 and 150)
        # and spanning a significant width (> 200 points)
        found_hline = any(
            abs(item[1].y - item[2].y) < 3
            and abs(item[2].x - item[1].x) > 200
            and 50 < (item[1].y + item[2].y) / 2 < 150
            for d in drawings
            for item in d.get("items", [])
            if item[0] == "l"
        )

        if found_hline:
            print(f"PASS: Component 3 - Horizontal line below header found (0.10 pts)")
            total_score += 0.10
        else:
            print("FAIL: Component 3 - No horizontal line found below header")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Receipt fields (Receipt #, Date, Customer) present (0.15 points)
    try:
        page = doc[0]
        full_text = page.get_text("text")
        fields_found = 0
        required_fields = ["Receipt #:", "Date:", "Customer:"]
        for field in required_fields:
            if field in full_text:
                fields_found += 1
            else:
                print(f"  INFO: Field '{field}' not found in text")

        if fields_found == 3:
            print(f"PASS: Component 4 - All 3 receipt fields present (0.15 pts)")
            total_score += 0.15
        elif fields_found > 0:
            partial = round(0.15 * fields_found / 3, 2)
            print(f"PARTIAL: Component 4 - {fields_found}/3 fields found ({partial} pts)")
            total_score += partial
        else:
            print("FAIL: Component 4 - No receipt fields found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Table with 4 columns (Item, Qty, Unit Price, Total) and header + 5 empty rows (0.25 points)
    try:
        page = doc[0]
        tables_finder = page.find_tables()
        table_list = list(tables_finder)

        if len(table_list) >= 1:
            # Find a table with 4 columns
            best_table = None
            for t in table_list:
                rows = t.extract()
                if rows and len(rows[0]) == 4:
                    best_table = rows
                    break

            if best_table is not None:
                rows = best_table
                # Check header row has correct column names
                header = [cell.strip() if cell else "" for cell in rows[0]]
                expected_cols = ["Item", "Qty", "Unit Price", "Total"]
                header_match = all(
                    exp.lower() in h.lower()
                    for exp, h in zip(expected_cols, header)
                )
                # Check at least 5 data rows (empty or not) below header
                data_rows = len(rows) - 1  # subtract header

                sub_score = 0.0
                if header_match:
                    sub_score += 0.15
                    print(f"  INFO: Table header matches: {header}")
                else:
                    print(f"  INFO: Table header mismatch: expected {expected_cols}, got {header}")

                if data_rows >= 5:
                    sub_score += 0.10
                    print(f"  INFO: Table has {data_rows} data rows (>= 5)")
                else:
                    print(f"  INFO: Table has only {data_rows} data rows, expected >= 5")

                if sub_score > 0:
                    print(f"PASS: Component 5 - Table verified ({sub_score} pts)")
                    total_score += sub_score
                else:
                    print("FAIL: Component 5 - Table structure incorrect")
            else:
                print("FAIL: Component 5 - No table with 4 columns found")
        else:
            print("FAIL: Component 5 - No tables found in PDF")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: 'Grand Total:' text at bottom-right area (0.10 points)
    try:
        page = doc[0]
        instances = page.search_for("Grand Total")
        if instances:
            rect = instances[0]
            # Should be in the right half of page (x > page_width/3) and below table area
            page_w = page.rect.width
            in_right = rect.x0 > page_w / 3
            # Should be below the table (y > 350 for a typical layout)
            below_table = rect.y0 > 300

            if in_right and below_table:
                print(f"PASS: Component 6 - 'Grand Total:' at bottom-right (x0={rect.x0:.1f}, y0={rect.y0:.1f}) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 - 'Grand Total:' position wrong (x0={rect.x0:.1f}, y0={rect.y0:.1f})")
        else:
            print("FAIL: Component 6 - 'Grand Total:' text not found")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(PDF_PATH):
    print(f"File not found: {PDF_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(PDF_PATH)

"""
Reward Script: Create a 3-page PDF report with title, table, and closing text
Task ID: pdf_gf1_040
Domain: pdf
Scoring:
  - Component 1 (0.20): File exists as valid PDF with exactly 3 pages
  - Component 2 (0.20): Page 1 contains 'Monthly Sales Report' and '2024-03'
  - Component 3 (0.20): Page 2 contains table headers 'Product', 'Units Sold', 'Revenue'
  - Component 4 (0.20): Page 2 table has at least 3 data rows
  - Component 5 (0.20): Page 3 contains 'End of Report'
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_040'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    import pymupdf
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must be a valid PDF
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Exactly 3 pages (0.20 points)
    try:
        page_count = doc.page_count
        if page_count == 3:
            print(f"PASS: Component 1 — PDF has exactly 3 pages (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Expected 3 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Page 1 contains 'Monthly Sales Report' and '2024-03' (0.20 points)
    try:
        if doc.page_count >= 1:
            page1_text = doc[0].get_text("text")
            has_title = "Monthly Sales Report" in page1_text
            has_date = "2024-03" in page1_text
            if has_title and has_date:
                print(f"PASS: Component 2 — Page 1 contains 'Monthly Sales Report' and '2024-03' (0.20 pts)")
                total_score += 0.20
            else:
                missing = []
                if not has_title:
                    missing.append("'Monthly Sales Report'")
                if not has_date:
                    missing.append("'2024-03'")
                print(f"FAIL: Component 2 — Page 1 missing: {', '.join(missing)}. Found text: {repr(page1_text[:200])}")
        else:
            print(f"FAIL: Component 2 — PDF has no pages")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Page 2 contains table headers 'Product', 'Units Sold', 'Revenue' (0.20 points)
    try:
        if doc.page_count >= 2:
            page2_text = doc[1].get_text("text")
            has_product = "Product" in page2_text
            has_units = "Units Sold" in page2_text
            has_revenue = "Revenue" in page2_text
            if has_product and has_units and has_revenue:
                print(f"PASS: Component 3 — Page 2 contains all table headers (0.20 pts)")
                total_score += 0.20
            else:
                missing = []
                if not has_product:
                    missing.append("'Product'")
                if not has_units:
                    missing.append("'Units Sold'")
                if not has_revenue:
                    missing.append("'Revenue'")
                print(f"FAIL: Component 3 — Page 2 missing headers: {', '.join(missing)}")
        else:
            print(f"FAIL: Component 3 — PDF has fewer than 2 pages")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Page 2 table has at least 3 data rows (0.20 points)
    try:
        if doc.page_count >= 2:
            page2 = doc[1]
            # Try table extraction first
            tables_found = False
            try:
                table_finder = page2.find_tables()
                tables = list(table_finder)
                if tables:
                    rows = tables[0].extract()
                    # First row is header, rest are data rows
                    data_rows = len(rows) - 1 if len(rows) > 0 else 0
                    if data_rows >= 3:
                        print(f"PASS: Component 4 — Table has {data_rows} data rows (>= 3 required) (0.20 pts)")
                        total_score += 0.20
                        tables_found = True
                    else:
                        print(f"FAIL: Component 4 — Table has only {data_rows} data rows, need >= 3")
                        tables_found = True
            except Exception:
                pass

            # Fallback: count text lines that look like data rows
            if not tables_found:
                page2_text = doc[1].get_text("text")
                lines = [l.strip() for l in page2_text.split('\n') if l.strip()]
                # Count lines after headers that contain data-like content
                # The headers are Product, Units Sold, Revenue
                # Data rows would be additional non-header content lines
                header_keywords = {'Product', 'Units Sold', 'Revenue', 'Sales Data'}
                data_lines = [l for l in lines if l not in header_keywords and not all(c in 'Product Units Sold Revenue Sales Data' for c in l)]
                # Each data row in text mode might be spread across multiple lines
                # A rough heuristic: at least 9 non-header tokens for 3 rows x 3 cols
                non_header_lines = [l for l in lines if l not in header_keywords]
                if len(non_header_lines) >= 3:
                    print(f"PASS: Component 4 — Found {len(non_header_lines)} non-header text lines suggesting >= 3 data rows (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 4 — Only {len(non_header_lines)} non-header lines found, need >= 3 data rows")
        else:
            print(f"FAIL: Component 4 — PDF has fewer than 2 pages")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Page 3 contains 'End of Report' (0.20 points)
    try:
        if doc.page_count >= 3:
            page3_text = doc[2].get_text("text")
            if "End of Report" in page3_text:
                print(f"PASS: Component 5 — Page 3 contains 'End of Report' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 5 — Page 3 missing 'End of Report'. Found text: {repr(page3_text[:200])}")
        else:
            print(f"FAIL: Component 5 — PDF has fewer than 3 pages")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/generated_report.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

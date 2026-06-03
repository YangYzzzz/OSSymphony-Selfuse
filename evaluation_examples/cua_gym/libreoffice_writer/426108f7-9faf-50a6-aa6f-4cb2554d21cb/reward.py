"""
Reward Script: Reformat nested JSON product catalog into hierarchical Writer report
Task ID: osworld_multi_apps_json_reformat_writer_010
Domain: libreoffice_writer (ODT format)
Scoring:
  Component 1: Hierarchical headings structure (H1 categories + H2 sub-categories)  — 0.30 pts
  Component 2: Product tables (6 tables, one per sub-category, correct headers)      — 0.30 pts
  Component 3: Summary section presence with total products and stock value           — 0.20 pts
  Component 4: Category summary table with counts and values                         — 0.20 pts
  Total: 1.0
"""

import os

FILE_PATH = '/home/user/Documents/product_catalog.odt'
TASK_ID = 'osworld_multi_apps_json_reformat_writer_010'


def get_text(element):
    """Recursively extract plain text from an ODF element."""
    texts = []
    for node in element.childNodes:
        if node.nodeType == node.TEXT_NODE:
            texts.append(node.data)
        elif hasattr(node, 'childNodes'):
            texts.append(get_text(node))
    return ''.join(texts)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the ODT file
    try:
        from odf.opendocument import load
        from odf.text import P, H
        from odf.table import Table, TableRow, TableCell
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # --- Component 1: Hierarchical heading structure (0.30 points) ---
    # Task requires: Heading 1 for 3 categories (Electronics, Clothing, Books)
    #                Heading 2 for 6 sub-categories
    # Initial file has only 1 heading (H1 'Product Catalog Data') and 0 tables
    try:
        headings = doc.getElementsByType(H)
        h1_texts = []
        h2_texts = []
        for h in headings:
            level = h.getAttribute('outlinelevel')
            text = get_text(h).strip()
            if level == '1':
                h1_texts.append(text)
            elif level == '2':
                h2_texts.append(text)

        # Check for the 3 required category H1 headings (plus Summary is also H1)
        required_categories = ['Electronics', 'Clothing', 'Books']
        found_categories = [c for c in required_categories if c in h1_texts]

        # Check for the 6 required sub-category H2 headings
        required_subcats = ['Smartphones', 'Laptops', "Men's Wear", "Women's Wear", 'Technology', 'Fiction']
        found_subcats = [s for s in required_subcats if s in h2_texts]

        # Scoring: partial credit
        # 3 categories found + at least 4 sub-categories found = full points
        cat_ratio = len(found_categories) / 3
        subcat_ratio = len(found_subcats) / 6

        if len(found_categories) == 3 and len(found_subcats) >= 6:
            print(f"PASS: Component 1 — All 3 category headings (H1) and 6 sub-category headings (H2) present (0.30 pts)")
            total_score += 0.30
        elif len(found_categories) >= 2 and len(found_subcats) >= 3:
            partial = round(0.30 * (cat_ratio * 0.5 + subcat_ratio * 0.5), 2)
            print(f"PARTIAL: Component 1 — Found {len(found_categories)}/3 H1 categories, {len(found_subcats)}/6 H2 sub-categories ({partial} pts)")
            print(f"  H1 found: {h1_texts}")
            print(f"  H2 found: {h2_texts}")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — Expected 3 H1 category headings and 6 H2 sub-category headings")
            print(f"  H1 found: {h1_texts}")
            print(f"  H2 found: {h2_texts}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --- Component 2: Product tables (0.30 points) ---
    # Task requires: a product table per sub-category (6 tables) with columns: id, name, price, stock, tags
    try:
        tables = doc.getElementsByType(Table)

        # Count tables that have expected product table headers
        expected_headers = {'id', 'name', 'price', 'stock', 'tags'}
        product_tables_found = 0
        total_rows_across_product_tables = 0

        summary_table = None  # Track separate category-summary table

        for table in tables:
            rows = table.getElementsByType(TableRow)
            if not rows:
                continue
            # Check header row
            header_row = rows[0]
            cells = header_row.getElementsByType(TableCell)
            header_texts = [get_text(c).strip().lower() for c in cells]

            if all(h in header_texts for h in expected_headers):
                product_tables_found += 1
                # Count data rows (excluding header)
                total_rows_across_product_tables += len(rows) - 1
            elif 'category' in header_texts and 'product count' in header_texts:
                summary_table = table

        print(f"  Product tables found: {product_tables_found}, Total product rows: {total_rows_across_product_tables}")

        if product_tables_found >= 6 and total_rows_across_product_tables >= 20:
            print(f"PASS: Component 2 — {product_tables_found} product tables with correct headers found, {total_rows_across_product_tables} product rows (0.30 pts)")
            total_score += 0.30
        elif product_tables_found >= 4 and total_rows_across_product_tables >= 15:
            partial = round(0.30 * (product_tables_found / 6), 2)
            print(f"PARTIAL: Component 2 — {product_tables_found}/6 product tables found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Expected 6 product tables (id/name/price/stock/tags), found {product_tables_found}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # --- Component 3: Summary section with total products and total stock value (0.20 points) ---
    # Task requires: a grand summary section at the end with total products, total stock value
    # Ground truth: Total Products: 26, Total Stock Value: $1,094,874.16 (or similar)
    try:
        headings = doc.getElementsByType(H)
        h1_texts_lower = []
        for h in headings:
            level = h.getAttribute('outlinelevel')
            text = get_text(h).strip().lower()
            if level == '1':
                h1_texts_lower.append(text)

        has_summary_heading = 'summary' in h1_texts_lower

        # Look for summary text in paragraphs
        paras = doc.getElementsByType(P)
        all_para_texts = [get_text(p).strip() for p in paras]

        # Check for total products mention (any paragraph with 'total' and a number >= 20)
        import re
        total_products_found = False
        total_stock_value_found = False

        for text in all_para_texts:
            text_lower = text.lower()
            # Check total products
            if 'total products' in text_lower or 'total product' in text_lower:
                # Look for a number in this text
                nums = re.findall(r'\d+', text)
                if nums and any(int(n) >= 20 for n in nums):
                    total_products_found = True
                    print(f"  Total products found: {repr(text)}")
            # Check total stock value
            if 'total stock value' in text_lower or 'stock value' in text_lower:
                if '$' in text or any(c.isdigit() for c in text):
                    total_stock_value_found = True
                    print(f"  Total stock value found: {repr(text)}")

        if has_summary_heading and total_products_found and total_stock_value_found:
            print(f"PASS: Component 3 — Summary heading + total products + total stock value all present (0.20 pts)")
            total_score += 0.20
        elif has_summary_heading and (total_products_found or total_stock_value_found):
            print(f"PARTIAL: Component 3 — Summary heading present, but missing {'total products' if not total_products_found else 'total stock value'} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — Summary heading: {has_summary_heading}, total products: {total_products_found}, total stock value: {total_stock_value_found}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # --- Component 4: Category summary table with counts and values (0.20 points) ---
    # Task requires: a table of all categories with product count and total value
    # Ground truth: 3 rows — Electronics (9 products, $806,635.26), Clothing (8, $178,200.70), Books (9, $110,038.20)
    try:
        tables = doc.getElementsByType(Table)
        category_summary_table = None

        for table in tables:
            rows = table.getElementsByType(TableRow)
            if not rows:
                continue
            header_row = rows[0]
            cells = header_row.getElementsByType(TableCell)
            header_texts = [get_text(c).strip().lower() for c in cells]

            # Look for a table with 'category' and ('product count' or 'count') and ('total value' or 'value')
            has_category = 'category' in header_texts
            has_count = any('count' in h for h in header_texts)
            has_value = any('value' in h for h in header_texts)

            if has_category and has_count and has_value:
                category_summary_table = table
                break

        if category_summary_table is not None:
            rows = category_summary_table.getElementsByType(TableRow)
            data_rows = rows[1:]  # Skip header
            row_count = len(data_rows)

            # Check that 3 rows exist (Electronics, Clothing, Books)
            found_row_categories = []
            for row in data_rows:
                cells = row.getElementsByType(TableCell)
                if cells:
                    cat_text = get_text(cells[0]).strip()
                    found_row_categories.append(cat_text)

            required_cats = ['Electronics', 'Clothing', 'Books']
            all_cats_present = all(c in found_row_categories for c in required_cats)

            if row_count >= 3 and all_cats_present:
                print(f"PASS: Component 4 — Category summary table with {row_count} rows, all 3 categories present (0.20 pts)")
                print(f"  Categories: {found_row_categories}")
                total_score += 0.20
            elif row_count >= 2:
                partial = 0.10
                print(f"PARTIAL: Component 4 — Category summary table found but only {row_count} rows, categories: {found_row_categories} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — Category summary table found but insufficient rows: {row_count}")
        else:
            print(f"FAIL: Component 4 — No category summary table found (expected columns: Category, Product Count, Total Value)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Entrypoint
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

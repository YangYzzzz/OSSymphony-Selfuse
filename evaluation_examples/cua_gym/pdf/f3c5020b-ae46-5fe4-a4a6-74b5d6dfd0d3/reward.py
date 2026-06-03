"""
Reward Script: Create a 2-page PDF with title, table, and bar chart
Task ID: pdf_gf2_040
Domain: pdf
Scoring:
  Component 1: PDF has exactly 2 pages (0.15)
  Component 2: Page 1 title 'Monthly Summary - April 2026' in 24pt bold (0.20)
  Component 3: Page 1 table with correct headers and 5 data rows (0.30)
  Component 4: Page 2 contains bar chart with category labels and revenue axis values (0.20)
  Component 5: Page 1 has horizontal rule / line drawing (0.15)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_040'

# Expected table data
EXPECTED_HEADERS = ['Category', 'Units', 'Revenue']
EXPECTED_ROWS = [
    ('Electronics', '450', '89500'),
    ('Clothing', '820', '41000'),
    ('Food', '1200', '24000'),
    ('Books', '340', '10200'),
    ('Other', '180', '5400'),
]
EXPECTED_CATEGORIES = ['Electronics', 'Clothing', 'Food', 'Books', 'Other']
EXPECTED_REVENUES = [89500, 41000, 24000, 10200, 5400]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print("CRITICAL: Cannot load file %s: %s" % (file_path, e))
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PDF has exactly 2 pages (0.15 points)
    # This is task-introduced: initial_env has no PDF at all
    try:
        page_count = doc.page_count
        if page_count == 2:
            print("PASS: Component 1 — PDF has exactly 2 pages (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 1 — Expected 2 pages, found %d" % page_count)
    except Exception as e:
        print("ERROR: Component 1 — %s" % e)

    # Component 2: Page 1 title 'Monthly Summary - April 2026' in 24pt bold (0.20 points)
    try:
        page1 = doc[0]
        blocks = page1.get_text('dict')['blocks']
        title_found = False
        title_bold = False
        title_size_ok = False
        for block in blocks:
            if 'lines' not in block:
                continue
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    if 'Monthly Summary' in text and 'April 2026' in text:
                        title_found = True
                        sz = span['size']
                        flags = span['flags']
                        is_bold = bool(flags & (2**4))
                        title_bold = is_bold
                        # Allow some tolerance on font size (22-26pt)
                        title_size_ok = (22.0 <= sz <= 26.0)

        if title_found and title_bold and title_size_ok:
            print("PASS: Component 2 — Title found, bold, ~24pt (0.20 pts)")
            total_score += 0.20
        elif title_found and title_bold:
            print("PARTIAL: Component 2 — Title found and bold but size not ~24pt (0.10 pts)")
            total_score += 0.10
        elif title_found:
            print("PARTIAL: Component 2 — Title found but not bold or wrong size (0.05 pts)")
            total_score += 0.05
        else:
            print("FAIL: Component 2 — Title 'Monthly Summary - April 2026' not found on page 1")
    except Exception as e:
        print("ERROR: Component 2 — %s" % e)

    # Component 3: Page 1 table with correct headers and 5 data rows (0.30 points)
    try:
        page1 = doc[0]
        page1_text = page1.get_text()

        # Check headers present
        headers_found = 0
        for h in EXPECTED_HEADERS:
            if h in page1_text:
                headers_found += 1

        # Check data rows present
        rows_found = 0
        for row in EXPECTED_ROWS:
            cat, units, rev = row
            if cat in page1_text and units in page1_text and rev in page1_text:
                rows_found += 1

        sub_score = 0.0
        if headers_found == 3:
            sub_score += 0.10
            print("PASS: Component 3a — All 3 headers found")
        else:
            print("FAIL: Component 3a — Found %d/3 headers" % headers_found)

        if rows_found == 5:
            sub_score += 0.20
            print("PASS: Component 3b — All 5 data rows found with correct values")
        elif rows_found >= 3:
            sub_score += 0.10
            print("PARTIAL: Component 3b — Found %d/5 data rows" % rows_found)
        else:
            print("FAIL: Component 3b — Found %d/5 data rows" % rows_found)

        total_score += sub_score
        print("Component 3 total: %.2f/0.30 pts" % sub_score)
    except Exception as e:
        print("ERROR: Component 3 — %s" % e)

    # Component 4: Page 2 contains bar chart with category labels and revenue values (0.20 points)
    try:
        page2 = doc[1]
        page2_text = page2.get_text()

        # Check that category labels appear on page 2 (chart x-axis labels)
        categories_on_p2 = 0
        for cat in EXPECTED_CATEGORIES:
            if cat in page2_text:
                categories_on_p2 += 1

        # Check for numeric axis values on page 2 (at least some revenue-scale numbers)
        has_axis_values = False
        for val in ['20000', '40000', '60000', '80000', '100000']:
            if val in page2_text:
                has_axis_values = True
                break

        # Check for chart drawings on page 2 (bars are drawn as shapes)
        page2_drawings = page2.get_drawings()
        has_drawings = len(page2_drawings) >= 5  # at least 5 bar rectangles

        sub_score = 0.0
        if categories_on_p2 >= 4:
            sub_score += 0.08
            print("PASS: Component 4a — %d/5 category labels on page 2" % categories_on_p2)
        else:
            print("FAIL: Component 4a — Only %d/5 category labels on page 2" % categories_on_p2)

        if has_axis_values:
            sub_score += 0.06
            print("PASS: Component 4b — Revenue axis values found on page 2")
        else:
            print("FAIL: Component 4b — No revenue axis values found on page 2")

        if has_drawings:
            sub_score += 0.06
            print("PASS: Component 4c — Page 2 has %d drawings (chart elements)" % len(page2_drawings))
        else:
            print("FAIL: Component 4c — Page 2 has only %d drawings (expected >= 5)" % len(page2_drawings))

        total_score += sub_score
        print("Component 4 total: %.2f/0.20 pts" % sub_score)
    except Exception as e:
        print("ERROR: Component 4 — %s" % e)

    # Component 5: Page 1 has a horizontal rule / line drawing (0.15 points)
    # The task asks for a horizontal rule between title and table
    try:
        page1 = doc[0]
        page1_drawings = page1.get_drawings()
        has_horizontal_line = False
        for d in page1_drawings:
            # A horizontal line has items with 'l' (line) type
            # and approximately same y coordinates
            for item in d.get('items', []):
                if item[0] == 'l':  # line segment
                    p1, p2 = item[1], item[2]
                    # Horizontal if y-coords are close
                    if abs(p1.y - p2.y) < 2 and abs(p1.x - p2.x) > 100:
                        has_horizontal_line = True
                        break
                elif item[0] == 're':  # thin rectangle can also be a rule
                    rect = item[1]
                    if rect.height < 3 and rect.width > 100:
                        has_horizontal_line = True
                        break
            if has_horizontal_line:
                break

        # Also check if there are table-like drawings (grid lines count towards drawings)
        # If page1 has many drawings (table borders + rule), that's also evidence
        if has_horizontal_line:
            print("PASS: Component 5 — Horizontal rule found on page 1 (0.15 pts)")
            total_score += 0.15
        elif len(page1_drawings) >= 10:
            # Many drawings likely means table grid + rule present
            print("PASS: Component 5 — Page 1 has %d drawings indicating table grid + rule (0.15 pts)" % len(page1_drawings))
            total_score += 0.15
        else:
            print("FAIL: Component 5 — No horizontal rule detected on page 1 (drawings: %d)" % len(page1_drawings))
    except Exception as e:
        print("ERROR: Component 5 — %s" % e)

    doc.close()

    final_score = min(total_score, 1.0)
    print("\nScore: %.2f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


# Default: test against canonical artifact path
file_path = '%s/Documents/summary_sheet.pdf' % WORKDIR
if not os.path.exists(file_path):
    print("File not found: %s" % file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)

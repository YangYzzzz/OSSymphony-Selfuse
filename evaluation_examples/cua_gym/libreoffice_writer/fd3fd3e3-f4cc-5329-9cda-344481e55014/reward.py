"""
Reward Script: Create annual report document from multi-sheet Calc workbook
Task ID: osworld_multi_apps_doc_calc_to_writer_009
Domain: libreoffice_writer
Scoring:
  - Component 1: Cover page content (0.2 pts)
  - Component 2: Table of Contents exists with quarter entries (0.2 pts)
  - Component 3: 4 quarter section headings (H1 level) (0.3 pts)
  - Component 4: 4 tables with correct data (0.2 pts)
  - Component 5: Page breaks between sections (0.1 pts)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doc_calc_to_writer_009'
FILE_PATH = '/home/user/Documents/annual_report_2024.odt'

# ODT XML namespaces
NS_OFFICE = 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'
NS_TEXT = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
NS_TABLE = 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'
NS_FO = 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0'
NS_STYLE = 'urn:oasis:names:tc:opendocument:xmlns:style:1.0'


def load_odt_content(file_path):
    """Load and parse content.xml from an ODT file. Returns (content_root, auto_styles_elem) or raises."""
    with zipfile.ZipFile(file_path, 'r') as z:
        content_xml = z.read('content.xml').decode('utf-8')
    root = ET.fromstring(content_xml)
    body = root.find(f'.//{{{NS_OFFICE}}}body')
    text_body = body.find(f'{{{NS_OFFICE}}}text')
    auto_styles = root.find(f'.//{{{NS_OFFICE}}}automatic-styles')
    return text_body, auto_styles


def get_text_content(element):
    """Get all text content from an XML element."""
    return ''.join(element.itertext()).strip()


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be a valid ODT
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        text_body, auto_styles = load_odt_content(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load ODT file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all top-level elements and their text content
    top_elements = list(text_body)
    all_paragraphs_text = []
    for elem in top_elements:
        tag = elem.tag.split('}')[-1]
        text_c = get_text_content(elem)
        style_name = elem.get(f'{{{NS_TEXT}}}style-name', '')
        all_paragraphs_text.append((tag, text_c, style_name))

    # -----------------------------------------------------------------------
    # Component 1: Cover page content (0.2 points)
    # The cover page should contain "Annual Report 2024", a company name,
    # and a date reference. These are absent from initial_env (no ODT file).
    # -----------------------------------------------------------------------
    try:
        all_text_concat = ' '.join(t for _, t, _ in all_paragraphs_text)

        has_annual_report_title = 'Annual Report 2024' in all_text_concat
        has_company_name = any(
            len(t) > 3 and t not in ('', 'Annual Report 2024')
            for tag, t, style in all_paragraphs_text[:10]
            if tag == 'p' and t
        )
        has_date_or_year = any(
            '2024' in t and t != 'Annual Report 2024'
            for _, t, _ in all_paragraphs_text[:10]
        )

        if has_annual_report_title and has_company_name and has_date_or_year:
            print(f"PASS: Component 1 — Cover page has title, company name, and date (0.2 pts)")
            total_score += 0.2
        elif has_annual_report_title:
            print(f"PASS PARTIAL: Component 1 — Cover page has title but missing company/date (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — Cover page missing 'Annual Report 2024' title")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Table of Contents with quarter entries (0.2 points)
    # A TOC section should reference Q1, Q2, Q3, Q4 summaries.
    # -----------------------------------------------------------------------
    try:
        quarters = ['Q1 Summary', 'Q2 Summary', 'Q3 Summary', 'Q4 Summary']

        toc_heading_count = sum(
            1 for _, text_c, _ in all_paragraphs_text
            if 'Table of Contents' in text_c or 'table of contents' in text_c.lower()
        )
        toc_entries_found = sum(
            1 for q in quarters
            if any(
                q in text_c and tag == 'p' and ('Page' in text_c or '...' in text_c or 'page' in text_c.lower())
                for tag, text_c, style in all_paragraphs_text
            )
        )

        toc_heading_found = toc_heading_count > 0

        if toc_heading_found and toc_entries_found >= 4:
            print(f"PASS: Component 2 — TOC heading found and all 4 quarter entries present (0.2 pts)")
            total_score += 0.2
        elif toc_heading_found and toc_entries_found >= 2:
            print(f"PASS PARTIAL: Component 2 — TOC heading found with {toc_entries_found}/4 entries (0.1 pts)")
            total_score += 0.1
        elif toc_heading_found:
            print(f"FAIL: Component 2 — TOC heading found but no quarter entries with page references")
        else:
            print(f"FAIL: Component 2 — No 'Table of Contents' section found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: 4 quarter section H1 headings (0.3 points)
    # Each quarter (Q1-Q4) must have an H1 heading named "Qx Summary".
    # -----------------------------------------------------------------------
    try:
        found_headings = set()
        for tag, text_c, style in all_paragraphs_text:
            if tag == 'h':
                for q in ['Q1 Summary', 'Q2 Summary', 'Q3 Summary', 'Q4 Summary']:
                    if q == text_c:
                        found_headings.add(q)

        # Also check outline level = 1 for the headings
        h_elements = text_body.findall(f'.//{{{NS_TEXT}}}h')
        h1_headings = []
        for h in h_elements:
            level = h.get(f'{{{NS_TEXT}}}outline-level', '0')
            text_c = get_text_content(h)
            if level == '1':
                h1_headings.append(text_c)

        required_headings = ['Q1 Summary', 'Q2 Summary', 'Q3 Summary', 'Q4 Summary']
        headings_found_count = sum(1 for req in required_headings if req in h1_headings)

        if headings_found_count == 4:
            print(f"PASS: Component 3 — All 4 H1 section headings found: {h1_headings} (0.3 pts)")
            total_score += 0.3
        elif headings_found_count >= 2:
            partial = 0.15
            print(f"PASS PARTIAL: Component 3 — {headings_found_count}/4 H1 headings found (0.15 pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Expected 4 H1 headings (Q1-Q4 Summary), found: {h1_headings}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: 4 tables with correct structure (0.2 points)
    # Each section should have a table with 6 rows (header + 5 data rows)
    # containing the quarterly performance data from the source spreadsheet.
    # -----------------------------------------------------------------------
    try:
        tables = text_body.findall(f'.//{{{NS_TABLE}}}table')
        valid_tables = 0
        expected_row_count = 6  # 1 header + 5 data rows

        for t in tables:
            rows = t.findall(f'.//{{{NS_TABLE}}}table-row')
            if len(rows) >= 5:  # at least 5 rows (flexible)
                # Check the table has 4 columns (Metric, Target, Actual, Variance)
                first_row_cells = rows[0].findall(f'.//{{{NS_TABLE}}}table-cell')
                if len(first_row_cells) >= 4:
                    first_row_texts = [get_text_content(c) for c in first_row_cells]
                    # Check header row contains expected column names
                    header_text = ' '.join(first_row_texts).lower()
                    if ('metric' in header_text or 'revenue' in header_text) and len(rows) >= 5:
                        valid_tables += 1

        if valid_tables >= 4:
            print(f"PASS: Component 4 — {valid_tables} valid tables found with correct structure (0.2 pts)")
            total_score += 0.2
        elif valid_tables >= 2:
            print(f"PASS PARTIAL: Component 4 — {valid_tables}/4 valid tables found (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 4 — Expected 4 tables with correct data, found {valid_tables} valid tables")
            print(f"  Total tables found: {len(tables)}")
            for i, t in enumerate(tables):
                rows = t.findall(f'.//{{{NS_TABLE}}}table-row')
                print(f"  Table {i+1}: {len(rows)} rows")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -----------------------------------------------------------------------
    # Component 5: Page breaks between sections (0.1 points)
    # Sections should be separated by page breaks. In ODT, this is encoded
    # as paragraph styles with fo:break-before="page".
    # -----------------------------------------------------------------------
    try:
        # Find auto styles with page break
        page_break_styles = set()
        if auto_styles is not None:
            for style_elem in auto_styles:
                style_name = style_elem.get(f'{{{NS_STYLE}}}name', '')
                for prop in style_elem:
                    break_before = prop.get(f'{{{NS_FO}}}break-before', '')
                    if break_before == 'page':
                        page_break_styles.add(style_name)

        # Count paragraphs/headings using page-break-before styles
        page_break_count = 0
        for elem in top_elements:
            elem_style = elem.get(f'{{{NS_TEXT}}}style-name', '')
            if elem_style in page_break_styles:
                page_break_count += 1

        # We need at least 3 page breaks (between 4 sections + TOC)
        if page_break_count >= 3:
            print(f"PASS: Component 5 — {page_break_count} page breaks found (sufficient for sections) (0.1 pts)")
            total_score += 0.1
        elif page_break_count >= 1:
            print(f"PASS PARTIAL: Component 5 — Only {page_break_count} page break(s) found, expected >= 3 (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 5 — No page breaks found between sections")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.1f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Execute verification
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

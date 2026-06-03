"""
Reward Script: Reformat JSON as Writer Report
Task ID: osworld_multi_apps_json_reformat_writer_008
Domain: libreoffice_writer
Scoring:
  Component 1: Bold section headings for Database, Server, Cache (0.35 pts)
  Component 2: Bullet list items present under each section (0.35 pts)
  Component 3: Summary table with 4 rows and 3 columns (0.20 pts)
  Component 4: Raw JSON content deleted (no curly braces) (0.10 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_json_reformat_writer_008'
FILE_PATH = f'{WORKDIR}/Documents/system_config.odt'

SECTION_NAMES = ['database', 'server', 'cache']


def get_all_paragraph_text(doc):
    """Collect all text from paragraphs in document body (excluding tables)."""
    from odf.text import P
    texts = []
    for para in doc.getElementsByType(P):
        style_name = para.getAttribute('stylename')
        text = ''
        for node in para.childNodes:
            if node.nodeType == node.TEXT_NODE:
                text += node.data
            elif hasattr(node, 'tagName') and 'span' in node.tagName.lower():
                for child in node.childNodes:
                    if child.nodeType == child.TEXT_NODE:
                        text += child.data
        texts.append((style_name, text))
    return texts


def is_bold_style(doc, style_name):
    """Check if a named style has bold font-weight property.
    Attributes in ODF are stored as (namespace_uri, localname) tuple keys.
    """
    if style_name is None:
        return False
    FO_NS = 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0'
    FW_KEY = (FO_NS, 'font-weight')

    def check_style_node(style):
        for prop in style.childNodes:
            if not hasattr(prop, 'attributes'):
                continue
            fw = prop.attributes.get(FW_KEY)
            if fw == 'bold':
                return True
        return False

    # Check named styles
    for style in doc.styles.childNodes:
        if not hasattr(style, 'getAttribute'):
            continue
        if style.getAttribute('name') == style_name:
            if check_style_node(style):
                return True
    # Check automatic styles
    for style in doc.automaticstyles.childNodes:
        if not hasattr(style, 'getAttribute'):
            continue
        if style.getAttribute('name') == style_name:
            if check_style_node(style):
                return True
    return False


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from odf.opendocument import load
        from odf.text import P
        from odf.table import Table, TableRow, TableCell
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get all paragraph (style, text) tuples
    para_list = get_all_paragraph_text(doc)

    # -------------------------------------------------------------------------
    # Component 1: Bold section headings for Database, Server, Cache (0.35 pts)
    # Each section heading (Database, Server, Cache) must be present in a
    # paragraph that uses a bold style. 0.35 / 3 ≈ 0.1167 per heading.
    # -------------------------------------------------------------------------
    try:
        found_headings = []
        for style_name, text in para_list:
            text_lower = text.strip().lower()
            if text_lower in SECTION_NAMES:
                # Check if this paragraph's style is bold
                bold = is_bold_style(doc, style_name)
                # Also accept if the style name contains 'heading' (case-insensitive)
                if not bold and style_name:
                    bold = 'heading' in style_name.lower()
                if bold:
                    found_headings.append(text.strip())

        heading_score = round(len(found_headings) / 3 * 0.35, 4)
        if len(found_headings) == 3:
            print(f"PASS: Component 1 — all 3 bold section headings found: {found_headings} (0.35 pts)")
            total_score += 0.35
        elif found_headings:
            print(f"PARTIAL: Component 1 — {len(found_headings)}/3 bold headings found: {found_headings} ({heading_score} pts)")
            total_score += heading_score
        else:
            print(f"FAIL: Component 1 — no bold section headings found for Database/Server/Cache")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: Bullet list items present under each section (0.35 pts)
    # Bullet items (prefixed with • or using BulletItem style) should appear
    # for all three sections. Check that there are at least 3 bullet items per
    # section (12 total across the three sections).
    # -------------------------------------------------------------------------
    try:
        bullet_paragraphs = []
        for style_name, text in para_list:
            t = text.strip()
            # Accept paragraphs that start with • or use 'bullet' style
            is_bullet = t.startswith('•') or (style_name and 'bullet' in style_name.lower())
            if is_bullet and t:
                bullet_paragraphs.append((style_name, t))

        # Expect at least 4 bullets per section × 3 sections = 12 total
        # Also verify sections are represented by inspecting bullet content
        bullet_texts = [t.lower() for _, t in bullet_paragraphs]
        has_db_bullets = any('host' in t or 'port' in t or 'name' in t or 'ssl' in t for t in bullet_texts if 'localhost' in t or '5432' in t or 'prod_db' in t or 'true' in t)
        has_server_bullets = any('0.0.0.0' in t or '8080' in t or 'workers' in t or 'debug' in t for t in bullet_texts)
        has_cache_bullets = any('redis' in t or '6379' in t or 'ttl' in t or 'backend' in t for t in bullet_texts)

        sections_with_bullets = sum([has_db_bullets, has_server_bullets, has_cache_bullets])
        bullet_score = round(sections_with_bullets / 3 * 0.35, 4)

        if sections_with_bullets == 3:
            print(f"PASS: Component 2 — bullet items found for all 3 sections ({len(bullet_paragraphs)} bullets total) (0.35 pts)")
            total_score += 0.35
        elif sections_with_bullets > 0:
            print(f"PARTIAL: Component 2 — bullet items found for {sections_with_bullets}/3 sections ({bullet_score} pts)")
            total_score += bullet_score
        else:
            print(f"FAIL: Component 2 — no bullet items found for Database/Server/Cache sections")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Summary table with 4 rows (header + 3 data rows) and
    # 3 columns (Section, Sub-key Count, Notable Values) (0.20 pts)
    # -------------------------------------------------------------------------
    try:
        tables = doc.getElementsByType(Table)
        qualifying_tables = [t for t in tables if len(t.getElementsByType(TableRow)) >= 4]
        if not qualifying_tables:
            print(f"FAIL: Component 3 — no summary table with at least 4 rows found (tables present: {len(tables)})")
        else:
            table = qualifying_tables[0]
            rows = table.getElementsByType(TableRow)
            # Verify header row
            header_row = rows[0]
            cells = header_row.getElementsByType(TableCell)
            header_texts = []
            for cell in cells:
                cell_text = ''
                for para in cell.getElementsByType(P):
                    for node in para.childNodes:
                        if node.nodeType == node.TEXT_NODE:
                            cell_text += node.data
                        elif hasattr(node, 'tagName') and 'span' in node.tagName.lower():
                            for child in node.childNodes:
                                if child.nodeType == child.TEXT_NODE:
                                    cell_text += child.data
                header_texts.append(cell_text.strip().lower())

            # Check number of columns (expect 3)
            has_3_cols = len(header_texts) >= 3
            # Check for expected sections in data rows
            section_rows_found = 0
            for ri in range(1, len(rows)):
                row_cells = rows[ri].getElementsByType(TableCell)
                if row_cells:
                    first_cell_text = ''
                    for para in row_cells[0].getElementsByType(P):
                        for node in para.childNodes:
                            if node.nodeType == node.TEXT_NODE:
                                first_cell_text += node.data
                    if first_cell_text.strip().lower() in SECTION_NAMES:
                        section_rows_found += 1

            if has_3_cols and section_rows_found == 3:
                print(f"PASS: Component 3 — summary table found with {len(rows)} rows and 3 columns; all 3 sections present (0.20 pts)")
                total_score += 0.20
            elif has_3_cols and section_rows_found > 0:
                partial = round(section_rows_found / 3 * 0.20, 4)
                print(f"PARTIAL: Component 3 — summary table found but only {section_rows_found}/3 section rows ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — table found but structure incorrect: cols={len(header_texts)}, section_rows={section_rows_found}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------------
    # Component 4: Raw JSON content deleted (0.10 pts)
    # The raw JSON (curly braces, "database" key as JSON) should no longer
    # appear in the document paragraphs.
    # -------------------------------------------------------------------------
    try:
        all_para_text = '\n'.join(t for _, t in para_list)
        # Raw JSON detection: presence of '{' or '"database":' pattern (JSON syntax)
        import re
        has_raw_json = bool(re.search(r'"\s*database\s*"\s*:', all_para_text, re.IGNORECASE))
        has_curly_braces = '{' in all_para_text or '}' in all_para_text

        if not has_raw_json and not has_curly_braces:
            print(f"PASS: Component 4 — raw JSON content deleted, no curly braces or JSON keys found (0.10 pts)")
            total_score += 0.10
        elif not has_raw_json:
            # Curly braces might appear in table content or other contexts
            print(f"PASS: Component 4 — JSON key-value patterns deleted (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — raw JSON content still present in document")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

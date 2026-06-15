"""
Reward Script: Extract Impress presentation text to Writer document
Task ID: osworld_multi_apps_impress_text_to_writer_008
Domain: libreoffice_writer
Scoring:
  - Component 1: Document index at beginning with slide titles + page numbers (0.25)
  - Component 2: Heading 1 for deck title, Heading 2 for each slide (0.30)
  - Component 3: Two Writer tables recreating slides 7 and 9 data (0.25)
  - Component 4: Code snippets with Courier New 10pt font (0.20)
Total: 1.0
"""

import os
import re
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_impress_text_to_writer_008'
ODT_PATH = '/home/user/Documents/technical_pres_complete_extract.odt'

# Namespaces for ODT XML parsing
NS_TEXT   = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
NS_OFFICE = 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'
NS_TABLE  = 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'
NS_STYLE  = 'urn:oasis:names:tc:opendocument:xmlns:style:1.0'
NS_FO     = 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0'

# Expected slide titles from the 10-slide presentation
EXPECTED_SLIDE_TITLES = [
    'Modern Software Architecture Patterns',  # slide 1 (deck title → H1)
    'Agenda',                                  # slide 2
    'Introduction to Architecture Patterns',   # slide 3
    'Microservices Architecture',              # slide 4 (has code snippet)
    'Event-Driven Architecture',               # slide 5
    'SOLID Design Principles',                 # slide 6 (has code snippet)
    'Performance Benchmarks',                  # slide 7 (has table)
    'Domain-Driven Design (DDD)',              # slide 8
    'Deployment and Reliability Metrics',      # slide 9 (has table)
    'Conclusion and Key Takeaways',            # slide 10
]

# Expected table headers: slide 7 (Performance Benchmarks) and slide 9 (Deployment and Reliability Metrics)
TABLE1_EXPECTED_COLS = 4  # Architecture Pattern, Avg Latency, Throughput, P99 Latency
TABLE2_EXPECTED_COLS = 4  # Service/Component, Deploy Frequency, MTTR, Error Rate

# Known code snippet markers from slides 4 and 6
CODE_SNIPPET_MARKERS = [
    '# Service definition example',        # slide 4 code header
    '# Dependency Inversion example',      # slide 6 code header
]


def parse_odt(odt_path):
    """Parse ODT file and return (content_root, styles_root, auto_styles_map)."""
    with zipfile.ZipFile(odt_path, 'r') as zf:
        with zf.open('content.xml') as f:
            content_root = ET.parse(f).getroot()
        with zf.open('styles.xml') as f:
            styles_root = ET.parse(f).getroot()
    return content_root, styles_root


def get_doc_body_children(content_root):
    """Return list of direct children of office:text body element."""
    body = content_root.find(f'.//{{{NS_OFFICE}}}body')
    if body is None:
        return []
    doc_text = body.find(f'{{{NS_OFFICE}}}text')
    if doc_text is None:
        return []
    return list(doc_text)


def get_style_parent_chain(content_root, styles_root, style_name):
    """Get parent-style-name chain for a given style, checking both automatic and named styles."""
    # Check automatic styles in content.xml
    auto_styles = content_root.find(f'.//{{{NS_OFFICE}}}automatic-styles')
    if auto_styles is not None:
        for style in auto_styles.findall(f'{{{NS_STYLE}}}style'):
            if style.attrib.get(f'{{{NS_STYLE}}}name') == style_name:
                parent = style.attrib.get(f'{{{NS_STYLE}}}parent-style-name', '')
                return [style_name, parent] if parent else [style_name]
    # Check named styles in styles.xml
    for style in styles_root.findall(f'.//{{{NS_STYLE}}}style'):
        if style.attrib.get(f'{{{NS_STYLE}}}name') == style_name:
            parent = style.attrib.get(f'{{{NS_STYLE}}}parent-style-name', '')
            return [style_name, parent] if parent else [style_name]
    return [style_name]


def is_heading_style(content_root, styles_root, style_name, heading_level):
    """
    Return True if style_name maps to Heading 1 (level=1) or Heading 2 (level=2).
    Handles P1->Heading_20_1 and P2->Heading_20_2 automatic style chains.
    """
    h1_styles = {'Heading_20_1', 'Heading 1', 'P1'}
    h2_styles = {'Heading_20_2', 'Heading 2', 'P2'}

    chain = get_style_parent_chain(content_root, styles_root, style_name)
    if heading_level == 1:
        return bool(set(chain) & h1_styles)
    elif heading_level == 2:
        return bool(set(chain) & h2_styles)
    return False


def get_auto_style_font(content_root, style_name):
    """
    Returns (font_name, font_size_pt) for a text span style from automatic styles.
    font_size_pt is a string like '10pt' or None.
    """
    auto_styles = content_root.find(f'.//{{{NS_OFFICE}}}automatic-styles')
    if auto_styles is None:
        return None, None
    for style in auto_styles.findall(f'{{{NS_STYLE}}}style'):
        if style.attrib.get(f'{{{NS_STYLE}}}name') == style_name:
            tp = style.find(f'{{{NS_STYLE}}}text-properties')
            if tp is not None:
                font = tp.attrib.get(f'{{{NS_STYLE}}}font-name', '') or \
                       tp.attrib.get(f'{{{NS_FO}}}font-family', '')
                size = tp.attrib.get(f'{{{NS_FO}}}font-size', '')
                return font, size
    return None, None


def verify_task(odt_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be a valid ODT
    if not os.path.exists(odt_path):
        print(f"CRITICAL: File not found: {odt_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        content_root, styles_root = parse_odt(odt_path)
        children = get_doc_body_children(content_root)
        if not children:
            print("CRITICAL: ODT body has no content")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODT file: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"ODT loaded successfully. Total body elements: {len(children)}")

    # -------------------------------------------------------------------------
    # Component 1: Index section at beginning (0.25 points)
    # The index must appear at the document start, labeled with a heading,
    # and list all 10 slide titles with page numbers.
    # -------------------------------------------------------------------------
    try:
        # Index heading must be one of the first elements
        index_heading_pos = -1
        for i, child in enumerate(children[:5]):  # within first 5 elements
            tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if tag == 'h':
                text = ''.join(child.itertext()).strip()
                if 'index' in text.lower() or 'table of contents' in text.lower() or 'contents' in text.lower():
                    index_heading_pos = i
                    break

        if index_heading_pos < 0:
            print(f"FAIL: Component 1 — No index/TOC heading found in first 5 elements")
        else:
            # Count how many of the 10 slide titles appear in the index section
            # Index entries are the paragraphs immediately following the index heading
            found_titles = set()
            for i in range(index_heading_pos + 1, min(index_heading_pos + 20, len(children))):
                child = children[i]
                tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                text = ''.join(child.itertext()).strip()
                # Once we hit a heading at level 1 (the deck title), index section ends
                if tag == 'h':
                    style_name = child.attrib.get(f'{{{NS_TEXT}}}style-name', '')
                    if is_heading_style(content_root, styles_root, style_name, 1):
                        break
                # Check if this paragraph contains a slide title
                for title in EXPECTED_SLIDE_TITLES:
                    if title.lower() in text.lower():
                        found_titles.add(title)

            found_count = len(found_titles)
            # Also check if entries have page number indicators (digits or dots in text)
            page_num_entries = 0
            for i in range(index_heading_pos + 1, min(index_heading_pos + 20, len(children))):
                child = children[i]
                tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                if tag == 'h':
                    style_name = child.attrib.get(f'{{{NS_TEXT}}}style-name', '')
                    if is_heading_style(content_root, styles_root, style_name, 1):
                        break
                text = ''.join(child.itertext()).strip()
                # page number indicator: text has digits at end (page ref)
                if re.search(r'\d+\s*$', text) and text:
                    page_num_entries += 1

            # Score: need index heading + at least 8/10 slide titles + at least 8 page number refs
            has_titles = found_count >= 8
            has_page_refs = page_num_entries >= 8

            if has_titles and has_page_refs:
                print(f"PASS: Component 1 — Index heading found; {found_count}/10 slide titles with {page_num_entries} page refs (0.25 pts)")
                total_score += 0.25
            elif has_titles:
                print(f"PASS (partial): Component 1 — Index heading + {found_count}/10 titles but only {page_num_entries} page refs (0.15 pts)")
                total_score += 0.15
            elif index_heading_pos >= 0:
                print(f"FAIL: Component 1 — Index heading found but only {found_count}/10 slide titles in index (need 8+)")
            else:
                print(f"FAIL: Component 1 — Index structure incomplete: found_titles={found_count}, page_refs={page_num_entries}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: Heading 1 for deck title, Heading 2 for each slide (0.30 points)
    # Deck title = "Modern Software Architecture Patterns" → Heading 1
    # Slides 2-10 titles → Heading 2
    # -------------------------------------------------------------------------
    try:
        h1_texts = []
        h2_texts = []

        for child in children:
            tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if tag != 'h':
                continue
            style_name = child.attrib.get(f'{{{NS_TEXT}}}style-name', '')
            outline_level = child.attrib.get(f'{{{NS_TEXT}}}outline-level', '0')
            text = ''.join(child.itertext()).strip()

            # Check if it's a Heading 1 (outline level 1 or style maps to H1)
            if outline_level == '1' or is_heading_style(content_root, styles_root, style_name, 1):
                h1_texts.append(text)
            # Check if it's a Heading 2 (outline level 2 or style maps to H2)
            elif outline_level == '2' or is_heading_style(content_root, styles_root, style_name, 2):
                h2_texts.append(text)

        # The deck title must appear as H1 (exclude 'Index' heading from scoring)
        deck_title = 'Modern Software Architecture Patterns'
        deck_title_as_h1 = deck_title.lower() in [t.lower() for t in h1_texts]

        # Slide titles 2-10 (9 slides) should appear as H2
        slide_titles_as_h2 = sum(
            1 for title in EXPECTED_SLIDE_TITLES[1:]  # exclude deck title
            if any(title.lower() in h2.lower() for h2 in h2_texts)
        )

        if deck_title_as_h1 and slide_titles_as_h2 >= 8:
            print(f"PASS: Component 2 — Deck title as H1; {slide_titles_as_h2}/9 slide titles as H2 (0.30 pts)")
            total_score += 0.30
        elif deck_title_as_h1 and slide_titles_as_h2 >= 5:
            pts = 0.20
            print(f"PASS (partial): Component 2 — Deck title as H1; {slide_titles_as_h2}/9 slide titles as H2 ({pts} pts)")
            total_score += pts
        elif slide_titles_as_h2 >= 8:
            pts = 0.15
            print(f"PASS (partial): Component 2 — Deck title not as H1; {slide_titles_as_h2}/9 H2 headings found ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 2 — deck_title_as_h1={deck_title_as_h1}, slide_h2_count={slide_titles_as_h2}/9")
            print(f"  H1 texts found: {h1_texts}")
            print(f"  H2 texts found (first 5): {h2_texts[:5]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Two Writer tables (slides 7 and 9) (0.25 points)
    # Table 1 (slide 7 - Performance Benchmarks): 4 columns, ~6 rows
    # Table 2 (slide 9 - Deployment and Reliability Metrics): 4 columns, ~6 rows
    # -------------------------------------------------------------------------
    try:
        doc_text_elem = content_root.find(f'.//{{{NS_OFFICE}}}body/{{{NS_OFFICE}}}text')
        tables = doc_text_elem.findall(f'{{{NS_TABLE}}}table') if doc_text_elem is not None else []

        print(f"Tables found: {len(tables)}")
        table_scores = []

        for tidx, table in enumerate(tables):
            rows = table.findall(f'{{{NS_TABLE}}}table-row')
            if not rows:
                table_scores.append(False)
                continue
            # Check number of columns in first row
            first_row_cells = rows[0].findall(f'{{{NS_TABLE}}}table-cell')
            # Also count repeated cells
            col_count = 0
            for cell in rows[0].findall(f'{{{NS_TABLE}}}table-cell'):
                rep = int(cell.attrib.get(f'{{{NS_TABLE}}}number-columns-repeated', '1'))
                col_count += rep
            row_count = len(rows)
            first_row_text = [
                ''.join(cell.itertext()).strip()
                for cell in rows[0].findall(f'{{{NS_TABLE}}}table-cell')
            ]
            print(f"  Table {tidx+1}: {row_count} rows, ~{col_count} cols, header={first_row_text}")

            # Valid table: 4 columns, at least 5 rows (header + 4 data rows)
            is_valid = (col_count == 4 and row_count >= 5)
            table_scores.append(is_valid)

        valid_tables = sum(1 for v in table_scores if v)

        if valid_tables >= 2:
            print(f"PASS: Component 3 — {valid_tables} valid 4-column tables found (0.25 pts)")
            total_score += 0.25
        elif valid_tables == 1:
            print(f"PASS (partial): Component 3 — Only {valid_tables}/2 valid tables found (0.12 pts)")
            total_score += 0.12
        else:
            print(f"FAIL: Component 3 — No valid 4-column tables found (got {len(tables)} tables total)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------------
    # Component 4: Code snippets in Courier New 10pt font (0.20 points)
    # Slides 4 and 6 have code snippet text boxes. These must be rendered
    # with Courier New 10pt font in the Writer document.
    # -------------------------------------------------------------------------
    try:
        doc_text_elem = content_root.find(f'.//{{{NS_OFFICE}}}body/{{{NS_OFFICE}}}text')

        # Find all text spans with Courier New font
        courier_lines = []
        for para in doc_text_elem.findall(f'.//{{{NS_TEXT}}}p'):
            for span in para.findall(f'.//{{{NS_TEXT}}}span'):
                span_style = span.attrib.get(f'{{{NS_TEXT}}}style-name', '')
                font, size = get_auto_style_font(content_root, span_style)
                if font and 'courier' in font.lower():
                    span_text = ''.join(span.itertext()).strip()
                    if span_text:
                        courier_lines.append((span_text, font, size))

        print(f"Courier New span lines found: {len(courier_lines)}")

        # Check for both code snippet markers
        found_code_markers = []
        for marker in CODE_SNIPPET_MARKERS:
            for (text, font, size) in courier_lines:
                if marker.lower() in text.lower():
                    found_code_markers.append(marker)
                    break

        # Check font size is 10pt for courier lines
        size_correct = any(size == '10pt' for (_, font, size) in courier_lines if font and 'courier' in font.lower())

        # Score based on: courier lines exist + both markers found + correct size
        if len(courier_lines) >= 10 and len(found_code_markers) >= 2 and size_correct:
            print(f"PASS: Component 4 — {len(courier_lines)} Courier New lines, both code markers found, size=10pt (0.20 pts)")
            total_score += 0.20
        elif len(courier_lines) >= 5 and len(found_code_markers) >= 1:
            print(f"PASS (partial): Component 4 — {len(courier_lines)} Courier New lines, {len(found_code_markers)}/2 markers, size_correct={size_correct} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — courier_lines={len(courier_lines)}, markers={found_code_markers}, size_correct={size_correct}")
            if courier_lines:
                print(f"  Sample courier lines: {courier_lines[:3]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test canonical artifact path
if not os.path.exists(ODT_PATH):
    print(f"File not found: {ODT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(ODT_PATH)

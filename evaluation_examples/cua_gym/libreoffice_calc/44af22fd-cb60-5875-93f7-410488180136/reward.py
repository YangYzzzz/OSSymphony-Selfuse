"""
Reward Script: UK Skilled Worker Visa Immigration Guide
Task ID: osworld_multi_apps_travel_permit_research_008
Domain: libreoffice_writer (ODT)
Scoring:
  Component 1: Required sections present in document (0.4 points)
  Component 2: Fee breakdown table with at least 3 fee line items (0.3 points)
  Component 3: References section citing at least 2 authoritative sources (0.3 points)
  Total: 1.0
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_travel_permit_research_008'
FILE_PATH = f'{WORKDIR}/uk_skilled_worker_visa_guide.odt'


def get_all_text_content(doc):
    """Extract all text from the document, including headings and paragraphs."""
    from odf.text import P, H
    texts = []
    for elem in doc.getElementsByType(H):
        text = ''
        for node in elem.childNodes:
            if node.nodeType == node.TEXT_NODE:
                text += node.data
            elif hasattr(node, 'childNodes'):
                for child in node.childNodes:
                    if child.nodeType == child.TEXT_NODE:
                        text += child.data
        if text.strip():
            texts.append(text.strip())
    for elem in doc.getElementsByType(P):
        text = ''
        for node in elem.childNodes:
            if node.nodeType == node.TEXT_NODE:
                text += node.data
            elif hasattr(node, 'childNodes'):
                for child in node.childNodes:
                    if child.nodeType == child.TEXT_NODE:
                        text += child.data
        if text.strip():
            texts.append(text.strip())
    return texts


def get_cell_text(cell):
    """Extract text from an ODF table cell."""
    from odf.text import P
    paras = cell.getElementsByType(P)
    return ' '.join(
        ''.join(
            node.data if node.nodeType == node.TEXT_NODE
            else ''.join(c.data for c in node.childNodes if c.nodeType == c.TEXT_NODE)
            for node in p.childNodes
        ).strip()
        for p in paras
    ).strip()


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: file must exist and be loadable
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        from odf.opendocument import load
        from odf.text import P, H
        from odf.table import Table, TableRow, TableCell
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load ODT file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get all text content from the document
    all_texts = get_all_text_content(doc)
    combined_text = ' '.join(all_texts).lower()

    # Component 1: Required sections present (0.4 points)
    # Task requires: Eligibility, Sponsor Requirements, English Language Requirements,
    # Required Documents Checklist, Application Timeline, Refusal and Appeals section
    # Each section worth ~0.067 points; 6 sections total = 0.4 points
    try:
        required_sections = [
            ('eligibility', ['eligibility']),
            ('sponsor', ['sponsor']),
            ('english language', ['english language', 'language requirement']),
            ('documents checklist', ['document', 'checklist']),
            ('application timeline', ['timeline', 'processing']),
            ('refusal', ['refusal', 'refused', 'appeal']),
        ]
        section_points_each = 0.4 / len(required_sections)
        sections_found = []
        sections_missing = []

        for section_name, keywords in required_sections:
            found = any(kw in combined_text for kw in keywords)
            if found:
                sections_found.append(section_name)
            else:
                sections_missing.append(section_name)

        if sections_found:
            section_score = len(sections_found) * section_points_each
            total_score += section_score
            print(f"PASS: Component 1 — Sections found: {sections_found} ({section_score:.3f} pts)")
        if sections_missing:
            print(f"FAIL: Component 1 — Sections missing: {sections_missing}")
    except Exception as e:
        print(f"ERROR: Component 1 (sections check) — {e}")

    # Component 2: Fee breakdown table with at least 3 fee line items (0.3 points)
    # The task requires a fee breakdown table (application fee + healthcare surcharge + other costs)
    try:
        tables = doc.getElementsByType(Table)

        def find_fee_table_line_items(tables):
            """Return (fee_table_count, max_fee_line_items) across all tables."""
            fee_table_count = 0
            max_items = 0
            for table in tables:
                rows = table.getElementsByType(TableRow)
                table_texts = []
                for row in rows:
                    cells = row.getElementsByType(TableCell)
                    row_text = ' '.join(get_cell_text(cell) for cell in cells).lower()
                    table_texts.append(row_text)
                full_table_text = ' '.join(table_texts)
                # Identify fee table by content: must mention fee/amount/surcharge with currency
                if any(kw in full_table_text for kw in ['fee', 'surcharge', 'amount']) and '£' in full_table_text:
                    fee_table_count += 1
                    data_rows = sum(
                        1 for row_text in table_texts[1:]  # skip header row
                        if row_text.strip() and any(
                            kw in row_text for kw in ['£', 'surcharge', 'service', 'charge', 'varies']
                        )
                    )
                    if data_rows > max_items:
                        max_items = data_rows
            return fee_table_count, max_items

        fee_table_count, fee_line_items = find_fee_table_line_items(tables)

        if fee_table_count >= 1 and fee_line_items >= 3:
            print(f"PASS: Component 2 — Fee table found with {fee_line_items} line items (0.3 pts)")
            total_score += 0.3
        elif fee_table_count >= 1 and fee_line_items > 0:
            print(f"FAIL: Component 2 — Fee table found but only {fee_line_items} line items (need >= 3)")
        else:
            print(f"FAIL: Component 2 — No fee breakdown table with currency amounts found (tables checked: {len(list(tables))})")
    except Exception as e:
        print(f"ERROR: Component 2 (fee table check) — {e}")

    # Component 3: References section citing at least 2 sources (0.3 points)
    # The task requires at least 2 authoritative sources (gov.uk plus one other)
    try:
        # Look for references section and source citations
        references_section_found = any(
            kw in combined_text for kw in ['references', 'sources', 'bibliography']
        )

        # Count citations - look for gov.uk and other authoritative sources
        govuk_cited = 'gov.uk' in combined_text
        # Check for at least 2 source URLs/citations (look for http or numbered citations)
        import re
        urls_found = re.findall(r'https?://\S+', ' '.join(all_texts))
        # Also check for numbered citations like "1." "2."
        numbered_refs = re.findall(r'^\s*[•\-]?\s*\d+\.', ' '.join(all_texts), re.MULTILINE)
        source_count = len(set(urls_found))

        has_two_sources = (
            (govuk_cited and source_count >= 2) or
            source_count >= 2 or
            len(numbered_refs) >= 2
        )

        if references_section_found and has_two_sources:
            print(f"PASS: Component 3 — References section found with {source_count} source URLs "
                  f"(gov.uk cited: {govuk_cited}) (0.3 pts)")
            total_score += 0.3
        elif references_section_found and not has_two_sources:
            print(f"FAIL: Component 3 — References section found but fewer than 2 sources "
                  f"(URLs: {source_count}, gov.uk: {govuk_cited})")
        else:
            print(f"FAIL: Component 3 — No references/sources section found")
    except Exception as e:
        print(f"ERROR: Component 3 (references check) — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.3f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Entry point: verify the ODT file at canonical path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

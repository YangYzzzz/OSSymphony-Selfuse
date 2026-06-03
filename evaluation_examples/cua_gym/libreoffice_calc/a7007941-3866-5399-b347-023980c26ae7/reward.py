"""
Reward Script: Multi-Destination Visa Guide (Schengen + UK + USA)
Task ID: osworld_multi_apps_travel_permit_research_012
Domain: libreoffice_writer (ODT format)
Scoring:
  - Component 1: File exists at Desktop/multi_destination_visa_guide.odt (gate)
  - Component 2: Overview section present (0.15)
  - Component 3: Side-by-side comparison table with 3 visa columns (0.30)
  - Component 4: Individual detailed sections for all 3 visa types (0.25)
  - Component 5: Sample trip timeline with deadlines (0.15)
  - Component 6: Contingency advice section (0.10)
  - Component 7: References from official government sources (0.05)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_travel_permit_research_012'
FILE_PATH = '/home/user/Desktop/multi_destination_visa_guide.odt'

TEXT_NS = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
TABLE_NS = 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'


def extract_odt_content(odt_path):
    """Extract all text content and structure from an ODT file using zipfile + XML."""
    with zipfile.ZipFile(odt_path, 'r') as z:
        with z.open('content.xml') as f:
            content = f.read().decode('utf-8')
    return ET.fromstring(content)


def get_all_text_lower(root):
    """Get full text content of the document (lowercased) for keyword searching."""
    texts = []
    for elem in root.iter():
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag in ('h', 'p'):
            text = ''.join(elem.itertext()).strip()
            if text:
                texts.append(text.lower())
    return ' '.join(texts)


def get_headings(root):
    """Return list of (level, text) tuples for all headings."""
    headings = []
    for elem in root.findall('.//{%s}h' % TEXT_NS):
        level = elem.get('{%s}outline-level' % TEXT_NS, '1')
        text = ''.join(elem.itertext()).strip()
        headings.append((int(level), text.lower()))
    return headings


def get_tables(root):
    """Return list of tables, each as list of rows (list of cell text strings)."""
    tables = []
    for tbl in root.findall('.//{%s}table' % TABLE_NS):
        rows = []
        for row_elem in tbl.findall('.//{%s}table-row' % TABLE_NS):
            # Avoid nested table rows
            cells = []
            for cell_elem in row_elem.findall('{%s}table-cell' % TABLE_NS):
                cell_text = ' '.join(
                    ''.join(p.itertext()).strip()
                    for p in cell_elem.findall('.//{%s}p' % TEXT_NS)
                ).strip()
                cells.append(cell_text.lower())
            if cells:
                rows.append(cells)
        if rows:
            tables.append(rows)
    return tables


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: file must exist
    if not os.path.isfile(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load ODT content
    try:
        root = extract_odt_content(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODT file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    full_text = get_all_text_lower(root)
    headings = get_headings(root)
    heading_texts = [h[1] for h in headings]
    tables = get_tables(root)

    # Component 1: Overview section with trip scenario description (0.15 points)
    # Task requires: "Overview (trip scenario description)"
    try:
        has_overview_heading = any('overview' in h for h in heading_texts)
        has_trip_scenario = any('trip scenario' in h or 'scenario' in h for h in heading_texts) or \
                            'trip scenario' in full_text
        has_indian_traveler = 'indian' in full_text and (
            'passport holder' in full_text or 'indian citizen' in full_text
        )
        has_multi_destination = (
            'schengen' in full_text and 'uk' in full_text and 'usa' in full_text
        ) or (
            'schengen' in full_text and 'united kingdom' in full_text and 'united states' in full_text
        )

        if has_overview_heading and has_trip_scenario and has_indian_traveler and has_multi_destination:
            print(f"PASS: Component 1 — Overview section with trip scenario for Indian passport holders (0.15 pts)")
            total_score += 0.15
        else:
            missing = []
            if not has_overview_heading:
                missing.append("overview heading")
            if not has_trip_scenario:
                missing.append("trip scenario section")
            if not has_indian_traveler:
                missing.append("Indian traveler reference")
            if not has_multi_destination:
                missing.append("all 3 destinations mentioned")
            print(f"FAIL: Component 1 — Overview section incomplete. Missing: {missing}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Side-by-side comparison table with 3 visa columns (0.30 points)
    # Task requires: "Comparison Table (3 columns: Schengen/UK/USA × rows: eligibility, documents, cost,
    #                processing time, validity)"
    try:
        comparison_table_found = False
        comparison_rows_score = 0.0

        for tbl in tables:
            if len(tbl) < 2:
                continue
            # Check first row has 3 visa type headers
            if len(tbl[0]) >= 3:
                first_row_text = ' '.join(tbl[0])
                if 'schengen' in first_row_text and ('uk' in first_row_text or 'united kingdom' in first_row_text or 'visitor' in first_row_text):
                    comparison_table_found = True
                    # Check required row topics
                    all_rows_text = ' '.join(' '.join(row) for row in tbl)
                    required_topics = ['eligibility', 'document', 'cost', 'fee', 'processing', 'validity']
                    topics_found = [topic for topic in required_topics if topic in all_rows_text]
                    # Award partial: need at least 4 of 6 topics
                    comparison_rows_score = min(len(topics_found) / 5.0, 1.0)
                    print(f"  Table found with {len(tbl)} rows and {len(tbl[0])} columns")
                    print(f"  Topics found: {topics_found} ({len(topics_found)}/6)")
                    break

        if comparison_table_found and comparison_rows_score >= 0.8:
            print(f"PASS: Component 2 — Comparison table with Schengen/UK/USA columns and required rows (0.30 pts)")
            total_score += 0.30
        elif comparison_table_found and comparison_rows_score >= 0.5:
            print(f"PARTIAL: Component 2 — Comparison table found but missing some rows (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — No valid comparison table found with all 3 visa types")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Individual detailed sections for all 3 visa types (0.25 points)
    # Task requires: "Individual Sections for each visa (detailed requirements)"
    try:
        # Each section should have heading + eligibility + required documents content
        schengen_section = any(
            'schengen' in h and ('visa' in h or 'type c' in h or '3.' in h)
            for h in heading_texts
        )
        uk_section = any(
            ('uk' in h or 'united kingdom' in h) and ('visa' in h or 'visitor' in h or '3.' in h)
            for h in heading_texts
        )
        us_section = any(
            ('us ' in h or 'usa' in h or 'united states' in h or 'b1' in h or 'b2' in h)
            and ('visa' in h or '3.' in h)
            for h in heading_texts
        )

        # Check for detailed content in each section
        schengen_detail = 'travel insurance' in full_text and ('€30,000' in full_text or '30000' in full_text or 'eur' in full_text)
        uk_detail = 'vaf1a' in full_text or ('gov.uk' in full_text and 'standard visitor' in full_text)
        us_detail = 'ds-160' in full_text and ('mrv' in full_text or 'b1/b2' in full_text or 'b2' in full_text)

        sections_with_detail = sum([
            schengen_section and schengen_detail,
            uk_section and uk_detail,
            us_section and us_detail
        ])

        if sections_with_detail == 3:
            print(f"PASS: Component 3 — All 3 individual visa sections with detailed requirements (0.25 pts)")
            total_score += 0.25
        elif sections_with_detail == 2:
            print(f"PARTIAL: Component 3 — 2 of 3 individual visa sections with detail (0.17 pts)")
            total_score += 0.17
        elif sections_with_detail == 1:
            print(f"PARTIAL: Component 3 — 1 of 3 individual visa sections with detail (0.08 pts)")
            total_score += 0.08
        else:
            missing = []
            if not (schengen_section and schengen_detail):
                missing.append("Schengen")
            if not (uk_section and uk_detail):
                missing.append("UK")
            if not (us_section and us_detail):
                missing.append("USA")
            print(f"FAIL: Component 3 — Individual sections missing or lacking detail for: {missing}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Sample trip timeline with visa application deadlines (0.15 points)
    # Task requires: "Sample Timeline diagram or table (e.g., T-90 days: apply Schengen, ...)"
    try:
        has_timeline_heading = any(
            'timeline' in h or 'sample trip' in h or 'deadline' in h
            for h in heading_texts
        )
        # Check for timeline-style content with T-minus notation or day references
        has_timeline_content = (
            ('t - ' in full_text or 't-' in full_text or 'months before' in full_text or 'days before' in full_text)
            and ('schengen' in full_text or 'apply' in full_text)
        )
        # Check for timeline table
        timeline_table_found = False
        for tbl in tables:
            all_rows_text = ' '.join(' '.join(row) for row in tbl)
            if ('t - ' in all_rows_text or 'months before' in all_rows_text or 'days before' in all_rows_text) \
                    and 'apply' in all_rows_text:
                timeline_table_found = True
                print(f"  Timeline table found with {len(tbl)} rows")
                break

        if has_timeline_heading and (has_timeline_content or timeline_table_found):
            print(f"PASS: Component 4 — Sample trip timeline with visa application deadlines (0.15 pts)")
            total_score += 0.15
        elif has_timeline_heading or timeline_table_found:
            print(f"PARTIAL: Component 4 — Timeline section present but content limited (0.08 pts)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 4 — No sample trip timeline with application deadlines found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Contingency advice section (0.10 points)
    # Task requires: "Contingency Advice section"
    try:
        has_contingency_heading = any(
            'contingency' in h or 'if' in h and 'denied' in h or 'if' in h and 'refused' in h
            for h in heading_texts
        )
        has_denial_content = (
            ('denied' in full_text or 'refused' in full_text or 'denial' in full_text or 'refusal' in full_text)
            and ('schengen' in full_text or 'uk' in full_text or 'us ' in full_text or 'usa' in full_text)
        )
        # Check that all 3 visa denial scenarios are covered
        denial_schengen = 'schengen' in full_text and ('denied' in full_text or 'refused' in full_text)
        denial_uk = ('uk' in full_text or 'united kingdom' in full_text) and ('denied' in full_text or 'refused' in full_text)
        denial_us = ('usa' in full_text or 'united states' in full_text or 'us b' in full_text) and ('denied' in full_text or 'refused' in full_text)

        if has_contingency_heading and denial_schengen and denial_uk and denial_us:
            print(f"PASS: Component 5 — Contingency advice section covering all 3 visa denial scenarios (0.10 pts)")
            total_score += 0.10
        elif has_contingency_heading or (denial_schengen and denial_uk):
            print(f"PARTIAL: Component 5 — Contingency section present but not all scenarios covered (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 5 — No contingency advice section found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Official government sources cited in References (0.05 points)
    # Task requires: "All 3 visa types cited from official government sources in References"
    try:
        has_references_heading = any(
            'reference' in h or 'official' in h and 'source' in h
            for h in heading_texts
        )
        # Check for official gov URLs for all 3 visa types
        has_schengen_ref = 'home-affairs.ec.europa.eu' in full_text or 'schengenvisainfo' in full_text
        has_uk_ref = 'gov.uk/standard-visitor' in full_text or 'gov.uk' in full_text
        has_us_ref = 'travel.state.gov' in full_text or 'usembassy.gov' in full_text or 'ceac.state.gov' in full_text

        if has_references_heading and has_schengen_ref and has_uk_ref and has_us_ref:
            print(f"PASS: Component 6 — References section with official government sources for all 3 visas (0.05 pts)")
            total_score += 0.05
        elif has_references_heading and (has_schengen_ref or has_uk_ref or has_us_ref):
            print(f"PARTIAL: Component 6 — References section present but not all 3 visa sources cited (0.02 pts)")
            total_score += 0.02
        else:
            print(f"FAIL: Component 6 — No references section with official government sources")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Entrypoint
if not os.path.isfile(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

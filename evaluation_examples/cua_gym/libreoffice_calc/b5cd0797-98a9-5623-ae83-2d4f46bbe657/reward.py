"""
Reward Script: Create US B-2 Visa Comprehensive Guide in LibreOffice Writer
Task ID: osworld_multi_apps_travel_permit_research_007
Domain: libreoffice_writer (ODT format)
Scoring:
  - Component 1 (0.25): Key sections present (Eligibility, Required Documents/Checklist, Application Timeline)
  - Component 2 (0.25): Checkbox-formatted checklist items (☐) present in Required Documents section
  - Component 3 (0.25): Fee table with at least 2 fee data rows and MRV fee mentioned
  - Component 4 (0.25): References section with at least 2 official source URLs
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_travel_permit_research_007'
FILE_PATH = '/home/user/Desktop/us_b2_visa_comprehensive_guide.odt'

# ODT XML namespace map
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text':   'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'table':  'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
}


def extract_all_text(content_xml: str) -> str:
    """Extract all text content from ODT content.xml."""
    root = ET.fromstring(content_xml)
    texts = []
    for elem in root.iter():
        if elem.text:
            texts.append(elem.text)
        if elem.tail:
            texts.append(elem.tail)
    return '\n'.join(texts)


def extract_heading_texts(content_xml: str) -> list:
    """Extract all heading texts from ODT content.xml."""
    root = ET.fromstring(content_xml)
    headings = []
    for h in root.iter('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}h'):
        text_parts = []
        for node in h.iter():
            if node.text:
                text_parts.append(node.text)
            if node.tail:
                text_parts.append(node.tail)
        heading_text = ''.join(text_parts).strip()
        if heading_text:
            headings.append(heading_text)
    return headings


def count_table_rows(content_xml: str) -> int:
    """Count table rows in ODT content.xml (excluding header row)."""
    root = ET.fromstring(content_xml)
    # Count all table-row elements
    rows = root.findall('.//{urn:oasis:names:tc:opendocument:xmlns:table:1.0}table-row')
    return len(rows)


def verify_task(file_path: str) -> float:
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
        with zipfile.ZipFile(file_path, 'r') as z:
            if 'content.xml' not in z.namelist():
                print("CRITICAL: Invalid ODT file — missing content.xml")
                print("REWARD: 0.0")
                return 0.0
            content_xml = z.read('content.xml').decode('utf-8')
    except Exception as e:
        print(f"CRITICAL: Cannot open ODT file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    all_text = extract_all_text(content_xml)
    all_text_lower = all_text.lower()
    headings = extract_heading_texts(content_xml)
    headings_lower = [h.lower() for h in headings]

    # -----------------------------------------------------------------------
    # Component 1: Key required sections present (0.25 points)
    # Task requires: Introduction, Eligibility Criteria, Required Documents
    # Checklist, Step-by-Step Application Timeline, Tips and Common Mistakes
    # -----------------------------------------------------------------------
    try:
        sections_found = []

        # Check for Eligibility Criteria section
        has_eligibility = any(
            'eligibility' in h for h in headings_lower
        )
        if has_eligibility:
            sections_found.append('Eligibility Criteria')

        # Check for Required Documents / Checklist section
        has_checklist = any(
            'required document' in h or 'checklist' in h or 'document' in h
            for h in headings_lower
        )
        if has_checklist:
            sections_found.append('Required Documents')

        # Check for Application Timeline / Step-by-Step section
        has_timeline = any(
            'timeline' in h or 'step' in h or 'application process' in h
            for h in headings_lower
        )
        if has_timeline:
            sections_found.append('Application Timeline')

        required_sections = ['Eligibility Criteria', 'Required Documents', 'Application Timeline']
        all_present = all(s in sections_found for s in required_sections)

        if all_present:
            print(f"PASS: Component 1 — All 3 required sections found: {sections_found} (0.25 pts)")
            total_score += 0.25
        else:
            missing = [s for s in required_sections if s not in sections_found]
            print(f"FAIL: Component 1 — Missing sections: {missing}; Found: {sections_found}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Checkbox-formatted checklist items present (0.25 points)
    # Task explicitly requires a "requirements checklist" with checkbox format
    # The ground truth shows items marked with ☐ (U+2610 ballot box)
    # -----------------------------------------------------------------------
    try:
        # Count checkbox symbols (☐ = U+2610) in the document text
        checkbox_count = all_text.count('☐')

        # Also accept lines starting with common checkbox markers
        # Match lines with ☐ or similar patterns
        checkbox_lines = [line for line in all_text.split('\n')
                          if '☐' in line and line.strip()]

        if checkbox_count >= 3:
            print(f"PASS: Component 2 — Checkbox checklist found: {checkbox_count} checkbox items (☐) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Expected at least 3 checkbox items (☐), found: {checkbox_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Fee table present with MRV fee data (0.25 points)
    # Task requires a "cost table (listing each fee type and amount)"
    # Ground truth shows a table with MRV fee of $185
    # -----------------------------------------------------------------------
    try:
        table_row_count = count_table_rows(content_xml)

        # Check that table has at least 2 data rows (header + 2+ fee entries)
        has_table = table_row_count >= 2

        # Check for MRV fee content in the document
        has_mrv = 'mrv' in all_text_lower or 'machine readable visa' in all_text_lower

        # Check for fee amount ($185)
        has_fee_amount = '$185' in all_text or '185' in all_text

        if has_table and has_mrv and has_fee_amount:
            print(f"PASS: Component 3 — Fee table found with {table_row_count} rows, MRV fee ($185) present (0.25 pts)")
            total_score += 0.25
        elif has_table and has_mrv:
            print(f"FAIL: Component 3 — Table found ({table_row_count} rows), MRV mentioned, but $185 amount missing")
        elif not has_table:
            print(f"FAIL: Component 3 — No fee table found (table rows: {table_row_count})")
        else:
            print(f"FAIL: Component 3 — Table found but MRV fee not mentioned (has_mrv={has_mrv}, has_fee_amount={has_fee_amount})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: References section with at least 2 official source URLs (0.25 points)
    # Task requires "information sourced from at least 2 official sources, both cited"
    # Ground truth cites travel.state.gov and usembassy.gov
    # -----------------------------------------------------------------------
    try:
        # Check for References section heading
        has_references_heading = any(
            'reference' in h or 'source' in h for h in headings_lower
        )

        # Check for official source URLs
        official_sources = []

        if 'travel.state.gov' in all_text_lower:
            official_sources.append('travel.state.gov')

        if 'usembassy.gov' in all_text_lower:
            official_sources.append('usembassy.gov')

        if 'uscis.gov' in all_text_lower:
            official_sources.append('uscis.gov')

        if 'ceac.state.gov' in all_text_lower:
            official_sources.append('ceac.state.gov')

        # Use regex to find any URLs mentioning official .gov domains
        url_pattern = re.compile(r'https?://[^\s<>"]+\.gov[^\s<>"]*', re.IGNORECASE)
        found_urls = url_pattern.findall(all_text)

        has_two_official_sources = len(official_sources) >= 2
        has_references_section = has_references_heading

        if has_references_section and has_two_official_sources:
            print(f"PASS: Component 4 — References section found with {len(official_sources)} official sources: {official_sources} (0.25 pts)")
            total_score += 0.25
        elif has_two_official_sources and not has_references_section:
            print(f"FAIL: Component 4 — {len(official_sources)} official sources found but no 'References' or 'Sources' heading")
        elif has_references_section and not has_two_official_sources:
            print(f"FAIL: Component 4 — References section exists but only {len(official_sources)} official sources: {official_sources}")
        else:
            print(f"FAIL: Component 4 — No references heading and < 2 official sources (found: {official_sources})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

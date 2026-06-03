"""
Reward Script: Convert product_launch.odp presentation to Writer briefing document.
Task ID: osworld_multi_apps_doc_pres_to_writer_008
Domain: libreoffice_writer
Scoring:
  - Component 1: Output file product_launch_brief.odt exists in Documents (0.0 — gate only)
  - Component 2: Title page content — title text 'Product X — Launch Briefing' present (0.2 pts)
  - Component 3: Table of Contents heading present (0.2 pts)
  - Component 4: All 6 content section H1 headings present (0.3 pts)
  - Component 5: Bullet list items from slides present (0.3 pts)

The reward script analyzes the ODT file using zipfile + xml.etree.ElementTree,
since the 'odf' Python library is not available on the VM.
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doc_pres_to_writer_008'
OUTPUT_FILE = '/home/user/Documents/product_launch_brief.odt'

TEXT_NS = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
OFFICE_NS = 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'
STYLE_NS = 'urn:oasis:names:tc:opendocument:xmlns:style:1.0'
FO_NS = 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0'

EXPECTED_SECTION_TITLES = [
    'Product Overview',
    'Key Features',
    'Market Analysis',
    'Go-to-Market Strategy',
    'Timeline',
    'Budget & Resources',
]

EXPECTED_BULLETS = [
    'Category: Smart Home Device',
    'Target: Home users',
    'Price point: $149',
    'Voice control',
    'App connectivity',
    'Energy monitoring',
    '$5B market',
    '23% YoY growth',
    'Key competitors: A, B, C',
    'Phase 1: Online launch',
    'Phase 2: Retail',
    'Phase 3: International',
    'Q1: Development complete',
    'Q2: Beta testing',
    'Q3: Launch',
    'Total budget: $2.5M',
    'Team: 12 FTE',
]


def get_all_text(elem):
    """Recursively extract all text from an XML element."""
    parts = []
    if elem.text:
        parts.append(elem.text)
    for child in elem:
        parts.append(get_all_text(child))
        if child.tail:
            parts.append(child.tail)
    return ''.join(parts)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: load the ODT file
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            if 'content.xml' not in zf.namelist():
                print("CRITICAL: content.xml not found in ODT archive")
                print("REWARD: 0.0")
                return 0.0
            content_xml = zf.read('content.xml').decode('utf-8')
    except Exception as e:
        print("CRITICAL: Cannot open ODT file %s: %s" % (file_path, e))
        print("REWARD: 0.0")
        return 0.0

    # Parse XML
    try:
        root = ET.fromstring(content_xml)
        body = root.find('{%s}body/{%s}text' % (OFFICE_NS, OFFICE_NS))
        if body is None:
            print("CRITICAL: Cannot find document body in content.xml")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print("CRITICAL: Cannot parse content.xml: %s" % e)
        print("REWARD: 0.0")
        return 0.0

    # Collect all headings and paragraph texts from the document
    h1_titles = []
    para_texts = []
    list_items = []

    try:
        for elem in body:
            tag = elem.tag.split('}')[-1]
            if tag == 'h':
                outline = elem.get('{%s}outline-level' % TEXT_NS, '1')
                txt = get_all_text(elem).strip()
                if outline == '1':
                    h1_titles.append(txt)
            elif tag == 'p':
                txt = get_all_text(elem).strip()
                if txt:
                    para_texts.append(txt)
            elif tag == 'list':
                for li in elem:
                    for lc in li:
                        txt = get_all_text(lc).strip()
                        if txt:
                            list_items.append(txt)
    except Exception as e:
        print("ERROR: Failed to iterate document body: %s" % e)

    # Component 2: Title page — main title text present (0.2 points)
    # The title "Product X — Launch Briefing" should appear as a paragraph (title page)
    try:
        title_text = 'Product X \u2014 Launch Briefing'
        title_found = any(title_text in txt for txt in para_texts)
        if title_found:
            print("PASS: Component 2 — Title 'Product X \u2014 Launch Briefing' found in document (0.2 pts)")
            total_score += 0.2
        else:
            # Also check if it appears in headings (some implementations use a heading for title)
            title_in_headings = any(title_text in txt for txt in h1_titles)
            if title_in_headings:
                print("PASS: Component 2 — Title found in heading (0.2 pts)")
                total_score += 0.2
            else:
                print("FAIL: Component 2 — Title 'Product X \u2014 Launch Briefing' not found. Para texts: %s" % para_texts[:5])
    except Exception as e:
        print("ERROR: Component 2 — %s" % e)

    # Component 3: Table of Contents heading present (0.2 points)
    # The document should have a heading labelled 'Table of Contents'
    try:
        toc_heading_found = any('Table of Contents' in t for t in h1_titles)
        # Also check if there's a text:table-of-content XML element
        toc_element_count = sum(1 for _ in body.iter('{%s}table-of-content' % TEXT_NS))
        toc_element_found = toc_element_count > 0
        if toc_heading_found or toc_element_found:
            print("PASS: Component 3 — Table of Contents present (heading=%s, element=%s) (0.2 pts)" % (
                toc_heading_found, toc_element_found))
            total_score += 0.2
        else:
            print("FAIL: Component 3 — No Table of Contents found. Headings: %s" % h1_titles)
    except Exception as e:
        print("ERROR: Component 3 — %s" % e)

    # Component 4: All 6 content section H1 headings present (0.3 points)
    # Each of the 6 slide titles (slides 2-7) should be an H1 heading
    try:
        found_sections = [s for s in EXPECTED_SECTION_TITLES if any(s in t for t in h1_titles)]
        missing_sections = [s for s in EXPECTED_SECTION_TITLES if s not in found_sections]
        num_found = len(found_sections)
        if num_found == len(EXPECTED_SECTION_TITLES):
            print("PASS: Component 4 — All 6 section headings found (0.3 pts)")
            total_score += 0.3
        elif num_found >= 4:
            # Partial credit: 4-5 out of 6 sections
            partial = 0.15
            print("PARTIAL: Component 4 — %d/6 section headings found (%s pts). Missing: %s" % (
                num_found, partial, missing_sections))
            if num_found >= 4:
                total_score += partial
        else:
            print("FAIL: Component 4 — Only %d/6 section headings found. Missing: %s" % (
                num_found, missing_sections))
    except Exception as e:
        print("ERROR: Component 4 — %s" % e)

    # Component 5: Bullet list items from slides present (0.3 points)
    # Representative bullet points from each slide should appear as list items
    try:
        found_bullets = [b for b in EXPECTED_BULLETS if any(b in li for li in list_items)]
        missing_bullets = [b for b in EXPECTED_BULLETS if b not in found_bullets]
        num_found_b = len(found_bullets)
        bullet_ratio = num_found_b / len(EXPECTED_BULLETS)
        if bullet_ratio >= 1.0:
            print("PASS: Component 5 — All %d bullet items found (0.3 pts)" % len(EXPECTED_BULLETS))
            total_score += 0.3
        elif bullet_ratio >= 0.7:
            partial_b = round(0.3 * bullet_ratio, 2)
            print("PARTIAL: Component 5 — %d/%d bullet items found (%s pts). Missing: %s" % (
                num_found_b, len(EXPECTED_BULLETS), partial_b, missing_bullets[:3]))
            if bullet_ratio >= 0.7:
                total_score += partial_b
        else:
            print("FAIL: Component 5 — Only %d/%d bullet items found. Missing: %s" % (
                num_found_b, len(EXPECTED_BULLETS), missing_bullets[:5]))
    except Exception as e:
        print("ERROR: Component 5 — %s" % e)

    final_score = round(min(total_score, 1.0), 4)
    print("\nScore: %s/1.0" % total_score)
    print("REWARD: %s" % final_score)
    return final_score


# Entry point: test against canonical artifact path
if not os.path.exists(OUTPUT_FILE):
    print("File not found: %s" % OUTPUT_FILE)
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_FILE)

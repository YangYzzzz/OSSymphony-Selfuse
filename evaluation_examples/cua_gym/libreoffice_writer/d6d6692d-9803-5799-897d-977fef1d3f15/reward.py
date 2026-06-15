"""
Reward Script: rl_papers.odt — RL papers from arXiv with bold titles, authors, and hyperlinks
Task ID: osworld_multi_apps_hf_papers_writer_009
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5 pts): At least 6 paper entries exist (counted by arxiv.org/abs/ hyperlinks)
  Component 2 (0.25 pts): Each of the first 6 entries has a bold/T_bold-styled title
  Component 3 (0.25 pts): Each of the first 6 entries has a valid arxiv.org/abs/ hyperlink
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import re

WORKDIR = '/home/user'
TASK_ID = 'rl_papers'
FILE_PATH = f'{WORKDIR}/{TASK_ID}.odt'

# XML namespaces used in ODF documents
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'style':  'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'text':   'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'fo':     'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
    'xlink':  'http://www.w3.org/1999/xlink',
}


def get_text_content(element):
    """Extract all text from an XML element recursively."""
    parts = []
    if element.text:
        parts.append(element.text)
    for child in element:
        parts.extend(get_text_content(child))
        if child.tail:
            parts.append(child.tail)
    return parts


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Checks that rl_papers.odt has >= 6 RL paper entries with:
    - Bold title
    - Authors line
    - Clickable hyperlink to arxiv.org/abs/PAPER_ID
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the ODT file (it is a ZIP archive)
    try:
        with zipfile.ZipFile(file_path) as z:
            with z.open('content.xml') as f:
                content_xml = f.read().decode('utf-8')
    except Exception as e:
        print(f"CRITICAL: Cannot open ODT file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse the XML
    try:
        root = ET.fromstring(content_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot parse content.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect automatic styles to detect bold text spans
    bold_styles = set()
    try:
        auto_styles = root.find('.//office:automatic-styles', NS)
        if auto_styles is not None:
            for style_elem in auto_styles.findall('style:style', NS):
                family = style_elem.get('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}family', '')
                style_name = style_elem.get('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}name', '')
                # Check text-properties for font-weight bold
                text_props = style_elem.find('style:text-properties', NS)
                if text_props is not None:
                    fw = text_props.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}font-weight', '')
                    if fw.lower() == 'bold':
                        bold_styles.add(style_name)
    except Exception as e:
        print(f"WARN: Could not parse automatic styles: {e}")

    # Gather all hyperlinks (text:a) pointing to arxiv.org/abs/
    hyperlinks = []
    try:
        body = root.find('.//office:body/office:text', NS)
        if body is not None:
            for a_elem in body.iter('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}a'):
                href = a_elem.get('{http://www.w3.org/1999/xlink}href', '')
                link_text = ''.join(get_text_content(a_elem)).strip()
                hyperlinks.append((href, link_text))
    except Exception as e:
        print(f"WARN: Could not gather hyperlinks: {e}")

    # Filter only valid arxiv.org/abs/ links
    arxiv_links = [
        (href, link_text) for (href, link_text) in hyperlinks
        if re.match(r'https?://arxiv\.org/abs/\S+', href)
    ]
    num_papers = len(arxiv_links)
    print(f"INFO: Found {num_papers} arxiv.org/abs/ hyperlinks")

    # Component 1: At least 6 paper entries exist (0.5 points)
    # A paper entry = a paragraph with an arxiv.org/abs/ hyperlink
    try:
        if num_papers >= 6:
            print(f"PASS: Component 1 — {num_papers} paper entries found (>= 6 required) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Only {num_papers} arxiv.org/abs/ hyperlinks found, need >= 6")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Each of the first 6 entries has a bold title (0.25 points)
    # We look for paragraphs containing text:span with a bold style (T_bold or similar),
    # appearing before each arxiv link paragraph. We check that at least 6 bold title spans exist.
    bold_title_count = 0
    try:
        if body is not None:
            for span_elem in body.iter('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span'):
                style_name = span_elem.get('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name', '')
                span_text = ''.join(get_text_content(span_elem)).strip()
                if style_name in bold_styles and span_text:
                    bold_title_count += 1
                    print(f"INFO: Bold span found: style={style_name!r}, text={span_text[:60]!r}")

        if bold_title_count >= 6:
            print(f"PASS: Component 2 — {bold_title_count} bold title spans found (>= 6 required) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Only {bold_title_count} bold title spans found, need >= 6")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Each of the first 6 entries has a valid arxiv.org/abs/ hyperlink (0.25 points)
    # We check that link text matches or resembles the href URL,
    # AND that the href itself is a proper arxiv.org/abs/ URL
    valid_links = 0
    try:
        for href, link_text in arxiv_links[:6]:
            paper_id_match = re.search(r'arxiv\.org/abs/(\S+)', href)
            if paper_id_match:
                paper_id = paper_id_match.group(1)
                # The link is a real URL pointing to arxiv.org/abs/<paper_id>
                valid_links += 1
                print(f"INFO: Valid arxiv hyperlink: {href!r}")

        if valid_links >= 6:
            print(f"PASS: Component 3 — {valid_links} valid arxiv.org/abs/ hyperlinks found (>= 6) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Only {valid_links} valid arxiv.org/abs/ hyperlinks, need >= 6")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

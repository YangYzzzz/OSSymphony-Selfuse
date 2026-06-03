"""
Reward Script: Add title page and copyright page to master document
Task ID: writer_rm_077
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): Title text 'Advanced Machine Learning' present
  Component 2 (0.20): Author/year text 'Dr. Sarah Mitchell, 2026' present
  Component 3 (0.20): Copyright text present
  Component 4 (0.15): Title & copyright appear before first subdocument section
  Component 5 (0.15): Page breaks separate title page, copyright page, and chapters
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_077'

# ODF namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'xlink': 'http://www.w3.org/1999/xlink',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the ODM file (ODF ZIP archive)
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            content_xml = z.read('content.xml').decode('utf-8')
        root = ET.fromstring(content_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all child elements of office:text in order
    office_body = root.find('.//office:body', NS)
    office_text = office_body.find('office:text', NS) if office_body else None
    if office_text is None:
        print("CRITICAL: No office:text element found")
        print("REWARD: 0.0")
        return 0.0

    # Collect all elements and their text content in document order
    # We need: text paragraphs before the first text:section (subdocument)
    elements = list(office_text)

    # Separate pre-section content from sections
    pre_section_texts = []  # list of (element_tag, text_content, style_name)
    first_section_idx = None

    for i, elem in enumerate(elements):
        local_tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if local_tag == 'section':
            if first_section_idx is None:
                first_section_idx = i
        elif local_tag == 'p':
            text_content = elem.text or ''
            # Also check for child text
            for child in elem:
                if child.text:
                    text_content += child.text
                if child.tail:
                    text_content += child.tail
            style_name = elem.get(f'{{{NS["text"]}}}style-name', '')
            pre_section_texts.append({
                'text': text_content.strip(),
                'style': style_name,
                'index': i,
            })

    # Filter pre-section paragraphs (only those before first section)
    if first_section_idx is not None:
        pre_section_paras = [p for p in pre_section_texts if p['index'] < first_section_idx]
    else:
        pre_section_paras = pre_section_texts

    # Get all non-empty text before first section
    pre_section_nonempty = [p for p in pre_section_paras if p['text']]

    print(f"INFO: Found {len(pre_section_paras)} paragraphs before first subdocument")
    print(f"INFO: {len(pre_section_nonempty)} non-empty paragraphs before first subdocument")
    for p in pre_section_nonempty:
        print(f"  - style='{p['style']}' text='{p['text'][:80]}'")

    # Component 1: Title text 'Advanced Machine Learning' present (0.30 points)
    try:
        title_found = any(
            'Advanced Machine Learning' in p['text']
            for p in pre_section_nonempty
        )
        if title_found:
            print(f"PASS: Component 1 - Title 'Advanced Machine Learning' found (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 - Title 'Advanced Machine Learning' not found in pre-section text")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Author/year text 'Dr. Sarah Mitchell, 2026' present (0.20 points)
    try:
        author_found = any(
            'Dr. Sarah Mitchell' in p['text'] and '2026' in p['text']
            for p in pre_section_nonempty
        )
        if author_found:
            print(f"PASS: Component 2 - Author/year 'Dr. Sarah Mitchell, 2026' found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 - Author/year text not found in pre-section text")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Copyright text present (0.20 points)
    try:
        copyright_found = any(
            'Copyright' in p['text'] and '2026' in p['text'] and 'Sarah Mitchell' in p['text'] and 'All rights reserved' in p['text']
            for p in pre_section_nonempty
        )
        if copyright_found:
            print(f"PASS: Component 3 - Copyright notice found (0.20 pts)")
            total_score += 0.20
        else:
            # Partial: at least some copyright-like text
            partial_copyright = any(
                'Copyright' in p['text'] and 'Sarah Mitchell' in p['text']
                for p in pre_section_nonempty
            )
            if partial_copyright:
                print(f"PARTIAL: Component 3 - Partial copyright found (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 - Copyright notice not found in pre-section text")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Title and copyright appear BEFORE first subdocument (0.15 points)
    # We need: title text appears, then copyright text appears, then first section
    try:
        title_idx = None
        copyright_idx = None
        for p in pre_section_nonempty:
            if 'Advanced Machine Learning' in p['text'] and title_idx is None:
                title_idx = p['index']
            if 'Copyright' in p['text'] and 'Sarah Mitchell' in p['text'] and copyright_idx is None:
                copyright_idx = p['index']

        if title_idx is not None and copyright_idx is not None and first_section_idx is not None:
            if title_idx < copyright_idx < first_section_idx:
                print(f"PASS: Component 4 - Title (idx {title_idx}) before copyright (idx {copyright_idx}) before chapters (idx {first_section_idx}) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 - Ordering incorrect: title={title_idx}, copyright={copyright_idx}, first_section={first_section_idx}")
        else:
            print(f"FAIL: Component 4 - Missing elements: title_idx={title_idx}, copyright_idx={copyright_idx}, first_section_idx={first_section_idx}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Page breaks separate title page, copyright page, chapters (0.15 points)
    # Look for page break properties in paragraph styles or direct fo:break-before="page"
    try:
        # Check automatic styles for page break styles
        auto_styles = root.find('.//office:automatic-styles', NS)
        page_break_styles = set()
        if auto_styles is not None:
            for style_elem in auto_styles:
                style_name = style_elem.get(f'{{{NS["style"]}}}name', '')
                # Check paragraph-properties for break-before="page"
                para_props = style_elem.find('style:paragraph-properties', NS)
                if para_props is not None:
                    break_before = para_props.get(f'{{{NS["fo"]}}}break-before', '')
                    break_after = para_props.get(f'{{{NS["fo"]}}}break-after', '')
                    if break_before == 'page' or break_after == 'page':
                        page_break_styles.add(style_name)

        # Count page break paragraphs before first section
        page_breaks_before_section = 0
        if first_section_idx is not None:
            for elem in elements[:first_section_idx]:
                local_tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                if local_tag == 'p':
                    style = elem.get(f'{{{NS["text"]}}}style-name', '')
                    if style in page_break_styles:
                        page_breaks_before_section += 1

        print(f"INFO: Page break styles found: {page_break_styles}")
        print(f"INFO: Page breaks before first section: {page_breaks_before_section}")

        if page_breaks_before_section >= 2:
            print(f"PASS: Component 5 - {page_breaks_before_section} page breaks found separating title/copyright/chapters (0.15 pts)")
            total_score += 0.15
        elif page_breaks_before_section >= 1:
            print(f"PARTIAL: Component 5 - Only {page_breaks_before_section} page break found (0.07 pts)")
            total_score += 0.07
        else:
            print(f"FAIL: Component 5 - No page breaks found before chapters")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/ML_Textbook_Master.odm'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Restore version 'Before reformatting' from version history
Task ID: writer_lec_073
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.30): Appendix section removed (extra heading + paragraphs gone)
  - Component 2 (0.30): Paragraph formatting reverted (no custom indent/line-height)
  - Component 3 (0.20): Heading formatting reverted (no custom centered alignment / colors)
  - Component 4 (0.20): Core content preserved (5 original headings + key body text present)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_073'

# ODF namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
}


def get_text(element):
    """Extract all text from an ODF element recursively."""
    text = ''
    if element.text:
        text += element.text
    for child in element:
        text += get_text(child)
        if child.tail:
            text += child.tail
    return text


def parse_odt(file_path):
    """Parse an ODT file and return content.xml root and styles info."""
    with zipfile.ZipFile(file_path, 'r') as zf:
        content_xml = zf.read('content.xml')
    root = ET.fromstring(content_xml)
    return root


def get_headings(root):
    """Get all text:h elements with their text and outline level."""
    body = root.find('.//office:body/office:text', NS)
    headings = []
    if body is not None:
        for h in body.findall('.//text:h', NS):
            level = h.get(f'{{{NS["text"]}}}outline-level', '1')
            text = get_text(h)
            style = h.get(f'{{{NS["text"]}}}style-name', '')
            headings.append({'level': level, 'text': text, 'style': style})
    return headings


def get_paragraphs(root):
    """Get all text:p elements in the body with their text and style."""
    body = root.find('.//office:body/office:text', NS)
    paragraphs = []
    if body is not None:
        for p in body.findall('.//text:p', NS):
            text = get_text(p)
            style = p.get(f'{{{NS["text"]}}}style-name', '')
            paragraphs.append({'text': text, 'style': style})
    return paragraphs


def get_auto_styles(root):
    """Get automatic styles and their properties."""
    styles = {}
    auto_styles = root.find('.//office:automatic-styles', NS)
    if auto_styles is not None:
        for style_elem in auto_styles:
            name = style_elem.get(f'{{{NS["style"]}}}name', '')
            parent = style_elem.get(f'{{{NS["style"]}}}parent-style-name', '')
            props = {}
            for prop_child in style_elem:
                for attr_key, attr_val in prop_child.attrib.items():
                    props[attr_key] = attr_val
            styles[name] = {'parent': parent, 'props': props}
    return styles


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        root = parse_odt(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    headings = get_headings(root)
    paragraphs = get_paragraphs(root)
    auto_styles = get_auto_styles(root)

    heading_texts = [h['text'] for h in headings]
    print(f"DEBUG: Found {len(headings)} headings: {heading_texts}")
    print(f"DEBUG: Found {len(paragraphs)} paragraphs")
    print(f"DEBUG: Found {len(auto_styles)} automatic styles: {list(auto_styles.keys())}")

    # Component 1: Appendix section removed (0.30 points)
    # The initial file has an "Appendix A: Quarterly Revenue Breakdown" heading
    # and 2 extra paragraphs about quarterly revenue. The golden file does NOT.
    try:
        has_appendix_heading = any('appendix' in h['text'].lower() for h in headings)
        has_quarterly_text = any('Q1:' in p['text'] and 'Q4:' in p['text'] for p in paragraphs)

        if not has_appendix_heading and not has_quarterly_text:
            print(f"PASS: Component 1 -- Appendix section removed (0.30 pts)")
            total_score += 0.30
        elif not has_appendix_heading:
            print(f"PARTIAL: Component 1 -- Appendix heading removed but quarterly text remains (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Appendix section still present (heading={has_appendix_heading}, quarterly={has_quarterly_text})")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Paragraph formatting reverted (0.30 points)
    # Initial file uses style 'P3' with custom margin-left=0.762cm and line-height=150%.
    # Golden file uses 'Standard' style with no such customizations.
    # We check: body paragraphs should NOT have custom indent/line-height styles.
    try:
        body_para_styles = [p['style'] for p in paragraphs if p['text'].strip()]

        # Check if any paragraph uses a style with custom margin-left or line-height
        has_custom_formatting = False
        for style_name in body_para_styles:
            if style_name in auto_styles:
                props = auto_styles[style_name].get('props', {})
                fo_margin = props.get(f'{{{NS["fo"]}}}margin-left', '')
                fo_line_height = props.get(f'{{{NS["fo"]}}}line-height', '')
                if fo_margin and fo_margin != '0cm':
                    has_custom_formatting = True
                    print(f"DEBUG: Style {style_name} has custom margin-left: {fo_margin}")
                if fo_line_height and fo_line_height != '100%':
                    has_custom_formatting = True
                    print(f"DEBUG: Style {style_name} has custom line-height: {fo_line_height}")

        if not has_custom_formatting:
            print(f"PASS: Component 2 -- Paragraph formatting reverted to standard (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 -- Paragraphs still have custom formatting (indent/line-height)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Heading formatting reverted (0.20 points)
    # Initial file has headings with centered alignment (P1, P2 styles)
    # and custom text colors (#1a5276, #2c3e50) via T1, T2 span styles.
    # Golden file uses default heading styles without these customizations.
    try:
        has_centered_headings = False
        has_custom_heading_colors = False

        # Check heading styles for centered alignment
        for h in headings:
            h_style = h['style']
            if h_style in auto_styles:
                props = auto_styles[h_style].get('props', {})
                text_align = props.get(f'{{{NS["fo"]}}}text-align', '')
                if text_align == 'center':
                    has_centered_headings = True
                    print(f"DEBUG: Heading '{h['text'][:30]}' has centered alignment via style {h_style}")

        # Check for custom color text styles (T1, T2 with specific colors)
        for sname, sdata in auto_styles.items():
            props = sdata.get('props', {})
            color = props.get(f'{{{NS["fo"]}}}color', '')
            if color in ('#1a5276', '#2c3e50'):
                has_custom_heading_colors = True
                print(f"DEBUG: Style {sname} has custom color: {color}")

        if not has_centered_headings and not has_custom_heading_colors:
            print(f"PASS: Component 3 -- Heading formatting reverted (0.20 pts)")
            total_score += 0.20
        elif not has_centered_headings or not has_custom_heading_colors:
            print(f"PARTIAL: Component 3 -- Partially reverted (centered={has_centered_headings}, colors={has_custom_heading_colors}) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 -- Heading formatting still has custom styles")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Core content preserved (0.20 points)
    # The 5 original headings and key body text must still be present.
    # This ensures the version restore didn't corrupt the document.
    try:
        expected_headings = [
            'Annual Report 2025',
            'Executive Summary',
            'Financial Overview',
            'Department Highlights',
            'Outlook for 2026',
        ]

        # Check that expected headings are present
        found_headings = 0
        for expected in expected_headings:
            if any(expected.lower() in h['text'].lower() for h in headings):
                found_headings += 1
            else:
                print(f"DEBUG: Missing expected heading: {expected}")

        # Check key body text snippets
        all_text = ' '.join(p['text'] for p in paragraphs)
        key_phrases = [
            '$47.2 million',
            '99.97%',
            '45,000 new leads',
        ]
        found_phrases = sum(1 for phrase in key_phrases if phrase in all_text)

        # Both headings (5/5) and key text (3/3) must be present
        # This is a compound check: content preserved AND appendix removed (checked in C1)
        headings_ok = found_headings == len(expected_headings)
        text_ok = found_phrases == len(key_phrases)

        # Only award if heading count is correct (5, not 6)
        # This ensures we're checking content preservation in the REVERTED state
        heading_count_correct = len(headings) == len(expected_headings)

        if headings_ok and text_ok and heading_count_correct:
            print(f"PASS: Component 4 -- Core content preserved with correct structure (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 -- heading_count={len(headings)} (expected {len(expected_headings)}), headings_present={found_headings}/{len(expected_headings)}, phrases={found_phrases}/{len(key_phrases)}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook for LibreOffice Writer
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.odt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)

"""
Reward Script: Different headers for left and right pages in Writer document
Task ID: writer_fs_060
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.35): Left page header contains 'Chapter Title' left-aligned
  - Component 2 (0.35): Right page header contains 'Author Name' right-aligned
  - Component 3 (0.15): Left and right headers are differentiated (style:header-left exists)
  - Component 4 (0.15): Header style is enabled in page layout
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_060'

# ODF namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
}


def get_text_content(element):
    """Recursively extract all text from an XML element."""
    texts = []
    if element.text:
        texts.append(element.text)
    for child in element:
        texts.extend(get_text_content(child))
        if child.tail:
            texts.append(child.tail)
    return texts


def get_paragraph_alignment(para_elem):
    """Get alignment from a text:p element by checking its style in the document."""
    style_name = para_elem.get(f'{{{NS["text"]}}}style-name', '')
    return style_name


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the ODF file and parse styles.xml
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            if 'styles.xml' not in z.namelist():
                print("CRITICAL: No styles.xml found in ODF file")
                print("REWARD: 0.0")
                return 0.0
            styles_xml = z.read('styles.xml').decode('utf-8')
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        root = ET.fromstring(styles_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot parse styles.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Build a map of style names to their paragraph alignment
    style_alignments = {}
    # Search in office:styles
    for style_elem in root.iter(f'{{{NS["style"]}}}style'):
        sname = style_elem.get(f'{{{NS["style"]}}}name', '')
        para_props = style_elem.find(f'{{{NS["style"]}}}paragraph-properties', NS)
        if para_props is not None:
            align = para_props.get(f'{{{NS["fo"]}}}text-align', '')
            style_alignments[sname] = align

    print(f"DEBUG: Found style alignments: {style_alignments}")

    # Find the master page(s)
    master_styles = root.find(f'{{{NS["office"]}}}master-styles')
    if master_styles is None:
        print("CRITICAL: No master-styles found")
        print("REWARD: 0.0")
        return 0.0

    master_page = master_styles.find(f'{{{NS["style"]}}}master-page')
    if master_page is None:
        print("CRITICAL: No master-page found")
        print("REWARD: 0.0")
        return 0.0

    # Find header elements
    header_default = master_page.find(f'{{{NS["style"]}}}header')
    header_left = master_page.find(f'{{{NS["style"]}}}header-left')

    # Component 1: Left page header contains 'Chapter Title' left-aligned (0.35 points)
    try:
        if header_left is not None:
            left_texts = get_text_content(header_left)
            left_full_text = ' '.join(left_texts).strip()
            print(f"DEBUG: Left header text: '{left_full_text}'")

            has_chapter_title = 'chapter title' in left_full_text.lower()

            # Check alignment - look at paragraph style
            left_paras = header_left.findall(f'{{{NS["text"]}}}p')
            left_aligned = False
            for p in left_paras:
                p_style = p.get(f'{{{NS["text"]}}}style-name', '')
                p_text = ' '.join(get_text_content(p)).strip()
                if p_text and 'chapter title' in p_text.lower():
                    # Check style alignment
                    align = style_alignments.get(p_style, '')
                    # 'start' means left-aligned in LTR context
                    if align in ('start', 'left', ''):
                        left_aligned = True
                    # Also check inline paragraph-properties
                    inline_props = p.find(f'{{{NS["style"]}}}paragraph-properties', NS)
                    if inline_props is not None:
                        inline_align = inline_props.get(f'{{{NS["fo"]}}}text-align', '')
                        if inline_align in ('start', 'left'):
                            left_aligned = True

            if has_chapter_title and left_aligned:
                print(f"PASS: Component 1 -- Left header has 'Chapter Title' left-aligned (0.35 pts)")
                total_score += 0.35
            elif has_chapter_title:
                print(f"PARTIAL: Component 1 -- Left header has 'Chapter Title' but alignment unclear (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 -- Left header text is '{left_full_text}', expected 'Chapter Title'")
        else:
            print("FAIL: Component 1 -- No left-specific header (style:header-left) found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Right page header contains 'Author Name' right-aligned (0.35 points)
    try:
        if header_default is not None:
            right_texts = get_text_content(header_default)
            right_full_text = ' '.join(right_texts).strip()
            print(f"DEBUG: Right/default header text: '{right_full_text}'")

            has_author_name = 'author name' in right_full_text.lower()

            # Check alignment
            right_paras = header_default.findall(f'{{{NS["text"]}}}p')
            right_aligned = False
            for p in right_paras:
                p_style = p.get(f'{{{NS["text"]}}}style-name', '')
                p_text = ' '.join(get_text_content(p)).strip()
                if p_text and 'author name' in p_text.lower():
                    align = style_alignments.get(p_style, '')
                    if align in ('end', 'right'):
                        right_aligned = True
                    inline_props = p.find(f'{{{NS["style"]}}}paragraph-properties', NS)
                    if inline_props is not None:
                        inline_align = inline_props.get(f'{{{NS["fo"]}}}text-align', '')
                        if inline_align in ('end', 'right'):
                            right_aligned = True

            if has_author_name and right_aligned:
                print(f"PASS: Component 2 -- Right header has 'Author Name' right-aligned (0.35 pts)")
                total_score += 0.35
            elif has_author_name:
                print(f"PARTIAL: Component 2 -- Right header has 'Author Name' but alignment unclear (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 -- Right header text is '{right_full_text}', expected 'Author Name'")
        else:
            print("FAIL: Component 2 -- No default header (style:header) found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Headers are differentiated - both style:header AND style:header-left exist (0.15 points)
    try:
        if header_default is not None and header_left is not None:
            # Verify they have different content (not same header on both sides)
            default_text = ' '.join(get_text_content(header_default)).strip()
            left_text = ' '.join(get_text_content(header_left)).strip()
            if default_text != left_text and default_text and left_text:
                print(f"PASS: Component 3 -- Different headers for left ('{left_text}') and right ('{default_text}') (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 -- Headers have same content or are empty: left='{left_text}', right='{default_text}'")
        else:
            print(f"FAIL: Component 3 -- Missing header elements: default={'found' if header_default is not None else 'missing'}, left={'found' if header_left is not None else 'missing'}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Header style is enabled in page layout (0.15 points)
    try:
        auto_styles = root.find(f'{{{NS["office"]}}}automatic-styles')
        header_style_found = False
        if auto_styles is not None:
            for page_layout in auto_styles.iter(f'{{{NS["style"]}}}page-layout'):
                header_style = page_layout.find(f'{{{NS["style"]}}}header-style')
                if header_style is not None:
                    # Check it has properties (not empty)
                    header_props = header_style.find(f'{{{NS["style"]}}}header-footer-properties')
                    if header_props is not None:
                        header_style_found = True

        if header_style_found:
            print(f"PASS: Component 4 -- Header style enabled in page layout (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 -- No header-style with properties found in page layout")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: persist app state then verify
def persist_app_state():
    """Try to save any unsaved changes via Ctrl+S."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")

persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.odt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

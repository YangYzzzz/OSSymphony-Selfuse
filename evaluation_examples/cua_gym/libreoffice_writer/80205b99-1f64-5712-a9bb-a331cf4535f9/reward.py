"""
Reward Script: Apply journal style guide to manuscript_draft.odt
Task ID: osworld_multi_apps_reminder_doc_update_writer_007
Domain: libreoffice_writer

Scoring rubric (total 1.0):
  Component 1: A4 page size (21cm x 29.7cm)                 — 0.15 points
  Component 2: 12pt Times New Roman font for body text       — 0.20 points
  Component 3: Double line spacing (200%) in body text       — 0.20 points
  Component 4: All margins set to 2.54cm                     — 0.15 points
  Component 5: Figure captions are 10pt italic               — 0.20 points
  Component 6: Word count field present in footer            — 0.10 points

Initial state: Letter size, Calibri 11pt, 150% spacing, 3cm margins, non-italic captions, no footer
Golden state:  A4, Times New Roman 12pt, 200% spacing, 2.54cm margins, 10pt italic captions, word count footer
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user/Documents'
TASK_ID = 'osworld_multi_apps_reminder_doc_update_writer_007'

# ODT XML namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
}


def parse_odt_xml(file_path, xml_name):
    """Extract and parse a named XML file from an ODT archive."""
    with zipfile.ZipFile(file_path, 'r') as z:
        raw = z.read(xml_name)
    return ET.fromstring(raw)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Basic file existence check (precondition gate)
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load the ODT files
    try:
        styles_root = parse_odt_xml(file_path, 'styles.xml')
        content_root = parse_odt_xml(file_path, 'content.xml')
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODT file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: A4 page size (21cm x 29.7cm)  — 0.15 points
    # Initial: 21.59cm x 27.94cm (Letter), Golden: 21cm x 29.7cm (A4)
    try:
        page_layout_props = styles_root.find(
            './/style:page-layout/style:page-layout-properties', NS
        )
        if page_layout_props is not None:
            width = page_layout_props.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}page-width', '')
            height = page_layout_props.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}page-height', '')
            # A4: exactly 21cm wide, 29.7cm tall (allow minor float tolerance)
            try:
                w_val = float(width.replace('cm', ''))
                h_val = float(height.replace('cm', ''))
                if abs(w_val - 21.0) < 0.15 and abs(h_val - 29.7) < 0.15:
                    print(f"PASS: Component 1 — A4 page size found: {width} x {height} (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 1 — Expected A4 (21cm x 29.7cm), found {width} x {height}")
            except ValueError:
                print(f"FAIL: Component 1 — Cannot parse page dimensions: width={width}, height={height}")
        else:
            print("FAIL: Component 1 — No page-layout-properties found in styles.xml")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 12pt Times New Roman font in body text style — 0.20 points
    # Initial: Calibri 11pt, Golden: Times New Roman 12pt
    try:
        body_text_style = content_root.find(
            './/style:style[@style:name="BodyText"]/style:text-properties', NS
        )
        if body_text_style is not None:
            font_name = body_text_style.get('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}font-name', '')
            font_size = body_text_style.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}font-size', '')
            font_ok = 'times new roman' in font_name.lower()
            size_ok = font_size == '12pt'
            if font_ok and size_ok:
                print(f"PASS: Component 2 — Body text is {font_name} {font_size} (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — Expected Times New Roman 12pt, found font={font_name}, size={font_size}")
        else:
            print("FAIL: Component 2 — BodyText style not found in content.xml")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Double line spacing (200%) in body text style — 0.20 points
    # Initial: 150%, Golden: 200%
    try:
        body_para_props = content_root.find(
            './/style:style[@style:name="BodyText"]/style:paragraph-properties', NS
        )
        if body_para_props is not None:
            line_height = body_para_props.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}line-height', '')
            if line_height == '200%':
                print(f"PASS: Component 3 — Body text line-height is {line_height} (double spacing) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — Expected 200% line-height, found {line_height}")
        else:
            print("FAIL: Component 3 — BodyText paragraph properties not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All margins set to 2.54cm — 0.15 points
    # Initial: 3cm, Golden: 2.54cm
    try:
        page_layout_props = styles_root.find(
            './/style:page-layout/style:page-layout-properties', NS
        )
        if page_layout_props is not None:
            margin_left = page_layout_props.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}margin-left', '')
            margin_right = page_layout_props.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}margin-right', '')
            margin_top = page_layout_props.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}margin-top', '')
            margin_bottom = page_layout_props.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}margin-bottom', '')
            margins = [margin_left, margin_right, margin_top, margin_bottom]
            margin_values_ok = all(m == '2.54cm' for m in margins)
            if margin_values_ok:
                print(f"PASS: Component 4 — All margins are 2.54cm (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — Expected all margins 2.54cm, found L={margin_left} R={margin_right} T={margin_top} B={margin_bottom}")
        else:
            print("FAIL: Component 4 — No page-layout-properties found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Figure captions are 10pt italic (CaptionStyle) — 0.20 points
    # Initial: Calibri 11pt non-italic, Golden: Times New Roman 10pt italic
    try:
        caption_text_props = content_root.find(
            './/style:style[@style:name="CaptionStyle"]/style:text-properties', NS
        )
        if caption_text_props is not None:
            caption_size = caption_text_props.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}font-size', '')
            caption_style = caption_text_props.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}font-style', '')
            size_ok = caption_size == '10pt'
            italic_ok = caption_style == 'italic'
            if size_ok and italic_ok:
                print(f"PASS: Component 5 — Caption style is {caption_size} {caption_style} (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 5 — Expected 10pt italic captions, found size={caption_size}, style={caption_style}")
        else:
            print("FAIL: Component 5 — CaptionStyle not found in content.xml")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Word count field in footer — 0.10 points
    # Initial: No footer, Golden: footer with <text:word-count/> field
    try:
        # Look for word-count element in styles.xml master-styles/footer
        word_count_el = styles_root.find(
            './/{urn:oasis:names:tc:opendocument:xmlns:text:1.0}word-count'
        )
        if word_count_el is not None:
            print("PASS: Component 6 — Word count field found in footer (0.10 pts)")
            total_score += 0.10
        else:
            print("FAIL: Component 6 — No word count field (<text:word-count>) found in document footer")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in a given env
file_path = f'{WORKDIR}/manuscript_draft.odt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

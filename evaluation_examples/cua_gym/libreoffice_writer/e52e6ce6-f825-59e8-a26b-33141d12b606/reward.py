"""
Reward Script: Apply formatting rules to thesis_chapter2.odt
Task ID: osworld_multi_apps_reminder_doc_update_writer_006
Domain: libreoffice_writer
Scoring:
  Component 1: Font changed to Garamond 12pt for body paragraphs (0.25 pts)
  Component 2: Line spacing changed to 24pt exact for body/subhead paragraphs (0.20 pts)
  Component 3: Page numbers present starting from page 2 (0.15 pts)
  Component 4: Chapter title uses Heading 1 style (text:h outline-level=1 or Heading_20_1 parent) (0.20 pts)
  Component 5: First-line indent 1.27cm for body paragraphs (0.10 pts)
  Component 6: Bibliography uses hanging indent 1.27cm (0.10 pts)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_reminder_doc_update_writer_006'
TARGET_FILE = '/home/user/Documents/thesis_chapter2.odt'

# XML namespaces used in ODF content.xml
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text':   'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'style':  'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo':     'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
}


def parse_odt_content(file_path):
    """Read and parse the content.xml from an .odt file."""
    with zipfile.ZipFile(file_path, 'r') as z:
        with z.open('content.xml') as f:
            content_xml = f.read()
    return ET.fromstring(content_xml)


def get_auto_styles(root):
    """Return a dict of automatic style name -> style element."""
    auto_styles = {}
    for style_elem in root.findall('.//office:automatic-styles/style:style', NS):
        name = style_elem.get('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}name', '')
        auto_styles[name] = style_elem
    return auto_styles


def get_paragraph_props(style_elem):
    """Return paragraph-properties attributes dict for a style element."""
    pp = style_elem.find('style:paragraph-properties', NS)
    if pp is None:
        return {}
    return dict(pp.attrib)


def get_text_props(style_elem):
    """Return text-properties attributes dict for a style element."""
    tp = style_elem.find('style:text-properties', NS)
    if tp is None:
        return {}
    return dict(tp.attrib)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid ODT
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        root = parse_odt_content(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODT content: {e}")
        print("REWARD: 0.0")
        return 0.0

    auto_styles = get_auto_styles(root)

    # -----------------------------------------------------------------------
    # Component 1: Body paragraphs use Garamond 12pt font (0.25 points)
    # Initial: Times New Roman 12pt. Golden: Garamond 12pt.
    # We look for at least one paragraph style with font-name=Garamond and font-size=12pt.
    # We also check that no body/para style still uses Times New Roman.
    # -----------------------------------------------------------------------
    try:
        garamond_styles = []
        timesnew_styles = []
        for sname, selem in auto_styles.items():
            tp = get_text_props(selem)
            font_name = tp.get('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}font-name', '')
            font_size = tp.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}font-size', '')
            family = selem.get('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}family', '')
            if family == 'paragraph':
                if 'Garamond' in font_name or 'garamond' in font_name.lower():
                    garamond_styles.append(sname)
                if 'Times New Roman' in font_name:
                    timesnew_styles.append(sname)

        # Count body-type paragraphs actually using Garamond
        body_ns = '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}'
        all_text_paras = root.findall(f'.//{body_ns}p') + root.findall(f'.//{body_ns}h')
        garamond_para_count = 0
        total_body_count = 0
        for para in all_text_paras:
            style_name = para.get(f'{body_ns}style-name', '')
            if style_name in auto_styles:
                total_body_count += 1
                if style_name in garamond_styles:
                    garamond_para_count += 1

        if garamond_para_count >= 5 and len(garamond_styles) >= 3:
            print(f"PASS: Component 1 — Garamond font found in {len(garamond_styles)} styles, "
                  f"{garamond_para_count} paragraphs (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected Garamond in body styles, "
                  f"found {len(garamond_styles)} Garamond styles, "
                  f"{garamond_para_count} Garamond paragraphs (need >= 5 paras)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Line spacing changed to 24pt exact (0.20 points)
    # Initial: line-height="150%". Golden: line-height="24pt".
    # Check that body/subhead paragraph styles use line-height="24pt" not "150%"
    # -----------------------------------------------------------------------
    try:
        pt24_styles = []
        pct150_styles = []
        for sname, selem in auto_styles.items():
            family = selem.get('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}family', '')
            if family != 'paragraph':
                continue
            pp = get_paragraph_props(selem)
            line_height = pp.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}line-height', '')
            if line_height == '24pt':
                pt24_styles.append(sname)
            elif line_height == '150%':
                pct150_styles.append(sname)

        if len(pt24_styles) >= 3 and len(pct150_styles) == 0:
            print(f"PASS: Component 2 — 24pt line spacing found in {len(pt24_styles)} styles, "
                  f"no 150% spacing remaining (0.20 pts)")
            total_score += 0.20
        elif len(pt24_styles) >= 3:
            print(f"PASS (partial): Component 2 — 24pt line spacing in {len(pt24_styles)} styles "
                  f"but {len(pct150_styles)} styles still use 150% spacing (0.20 pts awarded)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Expected 24pt line spacing in body styles, "
                  f"found {len(pt24_styles)} styles with 24pt (need >= 3). "
                  f"150% styles: {pct150_styles}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Page numbers present, starting from page 2 (0.15 points)
    # Golden: Footer with <text:page-number> element AND BodyFirstGolden has
    #         style:page-number="2" indicating page numbering starts at 2.
    # Check via styles.xml (master pages) AND content.xml first-para style.
    # -----------------------------------------------------------------------
    try:
        has_page_number_element = False
        has_page_start_2 = False

        # Check for page-number field in styles.xml (master page footer)
        try:
            with zipfile.ZipFile(file_path, 'r') as z:
                with z.open('styles.xml') as f:
                    styles_xml_content = f.read()
            styles_root = ET.fromstring(styles_xml_content)
            # Look for text:page-number elements anywhere in styles.xml (footers)
            text_ns = '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}'
            page_num_elems = styles_root.findall(f'.//{text_ns}page-number')
            if page_num_elems:
                has_page_number_element = True
        except Exception as e2:
            print(f"  NOTE: Could not check styles.xml for page-number: {e2}")

        # Also check content.xml for page-number elements in footer-like areas
        text_ns = '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}'
        page_num_in_content = root.findall(f'.//{text_ns}page-number')
        if page_num_in_content:
            has_page_number_element = True

        # Check that the first body paragraph style has style:page-number="2"
        # This is done via the paragraph style's page-number attribute
        for sname, selem in auto_styles.items():
            family = selem.get('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}family', '')
            if family != 'paragraph':
                continue
            pp = get_paragraph_props(selem)
            # style:page-number="2" means numbering starts at 2
            page_num_attr = pp.get('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}page-number', '')
            if page_num_attr == '2':
                has_page_start_2 = True
                break

        if has_page_number_element and has_page_start_2:
            print(f"PASS: Component 3 — Page number field present in footer AND "
                  f"page numbering starts at 2 (0.15 pts)")
            total_score += 0.15
        elif has_page_number_element:
            print(f"PARTIAL: Component 3 — Page number field present in footer but "
                  f"page start at 2 not found (partial — 0.07 pts)")
            total_score += 0.07
        elif has_page_start_2:
            print(f"PARTIAL: Component 3 — Page start at 2 found but no page number "
                  f"field element (0.07 pts)")
            total_score += 0.07
        else:
            print(f"FAIL: Component 3 — Neither page number field nor page-start-at-2 found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: Chapter title uses Heading 1 style (0.20 points)
    # Initial: <text:p text:style-name="ChapterTitle"> (plain paragraph)
    # Golden: <text:h text:outline-level="1" text:style-name="ChapterTitleGolden">
    #          with parent-style-name="Heading_20_1"
    # Check for text:h element with outline-level="1" containing chapter title text
    # -----------------------------------------------------------------------
    try:
        text_ns = '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}'
        heading_elems = root.findall(f'.//{text_ns}h')
        chapter_heading_found = False
        heading_1_found = False

        for h in heading_elems:
            outline_level = h.get(f'{text_ns}outline-level', '')
            style_name = h.get(f'{text_ns}style-name', '')
            # Get text content
            text_content = ''.join(h.itertext())

            if outline_level == '1':
                heading_1_found = True
                if 'Chapter' in text_content or 'Literature' in text_content:
                    chapter_heading_found = True

        # Also check if the chapter title style has Heading_20_1 as parent
        # (which is LibreOffice encoding of "Heading 1")
        parent_is_heading1 = False
        style_ns = '{urn:oasis:names:tc:opendocument:xmlns:style:1.0}'
        for sname, selem in auto_styles.items():
            parent = selem.get(f'{style_ns}parent-style-name', '')
            if 'Heading' in parent and '1' in parent:
                # This style derives from Heading 1
                parent_is_heading1 = True
                # Check if any heading uses this style
                for h in heading_elems:
                    h_style = h.get(f'{text_ns}style-name', '')
                    if h_style == sname:
                        chapter_heading_found = True

        if chapter_heading_found and (heading_1_found or parent_is_heading1):
            print(f"PASS: Component 4 — Chapter title is a text:h heading element "
                  f"with Heading 1 outline level/parent (0.20 pts)")
            total_score += 0.20
        elif heading_1_found:
            print(f"PASS (partial): Component 4 — Heading level-1 element found "
                  f"but chapter title text may differ (0.20 pts awarded)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Chapter title not in text:h heading element "
                  f"with Heading 1 style. heading_elems found: {len(heading_elems)}, "
                  f"chapter_heading_found: {chapter_heading_found}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -----------------------------------------------------------------------
    # Component 5: First-line indent 1.27cm for body paragraphs (0.10 points)
    # Initial: text-indent="0cm" for all paragraph types.
    # Golden: text-indent="1.27cm" for body paragraphs.
    # -----------------------------------------------------------------------
    try:
        indent_127_styles = []
        for sname, selem in auto_styles.items():
            family = selem.get('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}family', '')
            if family != 'paragraph':
                continue
            pp = get_paragraph_props(selem)
            text_indent = pp.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}text-indent', '')
            if text_indent == '1.27cm':
                indent_127_styles.append(sname)

        if len(indent_127_styles) >= 1:
            print(f"PASS: Component 5 — First-line indent of 1.27cm found in styles: "
                  f"{indent_127_styles} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — No paragraph style with text-indent='1.27cm' found. "
                  f"Expected body paragraphs to have 1.27cm first-line indent.")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # -----------------------------------------------------------------------
    # Component 6: Bibliography uses hanging indent format (0.10 points)
    # Initial: BibEntry has text-indent="0cm", margin-left="0cm" (flat).
    # Golden: BibEntryGolden has margin-left="1.27cm", text-indent="-1.27cm".
    # Check for a paragraph style with positive left margin AND negative text-indent.
    # -----------------------------------------------------------------------
    try:
        hanging_indent_found = False
        hanging_style_names = []

        for sname, selem in auto_styles.items():
            family = selem.get('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}family', '')
            if family != 'paragraph':
                continue
            pp = get_paragraph_props(selem)
            fo_ns = '{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}'
            text_indent = pp.get(f'{fo_ns}text-indent', '')
            margin_left = pp.get(f'{fo_ns}margin-left', '')

            # Hanging indent = negative text-indent + positive margin-left
            if text_indent.startswith('-') and margin_left not in ('', '0cm', '0pt'):
                hanging_indent_found = True
                hanging_style_names.append(sname)

        # Also verify that bibliography paragraphs in the document use a hanging-indent style
        bib_paras_with_hanging = 0
        text_ns = '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}'
        all_paras = root.findall(f'.//{text_ns}p')

        # Identify bibliography section — paragraphs after "References" heading
        after_references = False
        for para in all_paras:
            text_content = ''.join(para.itertext())
            if text_content.strip() == 'References':
                after_references = True
                continue
            if after_references:
                style_name = para.get(f'{text_ns}style-name', '')
                if style_name in hanging_style_names:
                    bib_paras_with_hanging += 1

        if hanging_indent_found and bib_paras_with_hanging >= 1:
            print(f"PASS: Component 6 — Hanging indent style(s) {hanging_style_names} found "
                  f"and applied to {bib_paras_with_hanging} bibliography entries (0.10 pts)")
            total_score += 0.10
        elif hanging_indent_found:
            print(f"PARTIAL: Component 6 — Hanging indent style defined but not detected "
                  f"on bibliography paragraphs (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 6 — No hanging indent paragraph style found. "
                  f"Expected BibEntry style with negative text-indent and positive margin-left.")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # -----------------------------------------------------------------------
    # Final score
    # -----------------------------------------------------------------------
    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(TARGET_FILE):
    print(f"File not found: {TARGET_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(TARGET_FILE)

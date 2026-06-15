"""
Reward Script: Apply style checklist to presentation_draft.odt
Task ID: osworld_multi_apps_doc_follow_instructions_003
Domain: libreoffice_writer (ODT)
Scoring:
  - Component 1 (0.35): Page margins set to 2cm on all sides
  - Component 2 (0.30): Document language set to English (US) in text styles
  - Component 3 (0.35): Footer with centered page numbers present
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doc_follow_instructions_003'
FILE_PATH = f'{WORKDIR}/Documents/presentation_draft.odt'

# Namespace map for ODF XML parsing
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'style':  'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo':     'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
    'text':   'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
}


def parse_cm(value_str):
    """Parse a CSS/ODF dimension string like '2cm' into a float (centimetres)."""
    if value_str is None:
        return None
    v = value_str.strip().lower()
    if v.endswith('cm'):
        return float(v[:-2])
    if v.endswith('mm'):
        return float(v[:-2]) / 10.0
    if v.endswith('in'):
        return float(v[:-2]) * 2.54
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load ODT zip and parse styles.xml and content.xml
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            styles_xml = z.read('styles.xml').decode('utf-8')
            content_xml = z.read('content.xml').decode('utf-8')
        styles_root = ET.fromstring(styles_xml)
        content_root = ET.fromstring(content_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -------------------------------------------------------------------------
    # Component 1: Page margins set to 2cm on all sides (0.35 points)
    # The task requires changing margins from default 2.54cm to 2cm all sides.
    # Check the fo:margin-* attributes on <style:page-layout-properties> in styles.xml.
    # -------------------------------------------------------------------------
    try:
        margin_ok = False
        # Search in office:automatic-styles and office:master-styles
        for page_layout in styles_root.findall(
            './/style:page-layout/style:page-layout-properties', NS
        ):
            mt = parse_cm(page_layout.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}margin-top'))
            mb = parse_cm(page_layout.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}margin-bottom'))
            ml = parse_cm(page_layout.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}margin-left'))
            mr = parse_cm(page_layout.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}margin-right'))
            print(f"  Page margins found: top={mt}, bottom={mb}, left={ml}, right={mr}")
            # Allow small floating-point tolerance (within 0.05cm)
            if (mt is not None and mb is not None and ml is not None and mr is not None
                    and abs(mt - 2.0) < 0.05
                    and abs(mb - 2.0) < 0.05
                    and abs(ml - 2.0) < 0.05
                    and abs(mr - 2.0) < 0.05):
                margin_ok = True
                break

        if margin_ok:
            print("PASS: Component 1 — Page margins are 2cm on all sides (0.35 pts)")
            total_score += 0.35
        else:
            print("FAIL: Component 1 — Page margins are NOT 2cm on all sides (expected 2.0cm each)")
    except Exception as e:
        print(f"ERROR: Component 1 (margins) — {e}")

    # -------------------------------------------------------------------------
    # Component 2: Document language set to English (US) (0.30 points)
    # The task requires setting the document language to English (US).
    # In ODT this appears as fo:language="en" fo:country="US" in text-properties
    # of paragraph styles within content.xml automatic-styles.
    # We check that at least one paragraph style has the correct language.
    # -------------------------------------------------------------------------
    try:
        lang_ok = False
        fo_ns = 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0'
        # Look in content.xml automatic-styles
        for text_props in content_root.findall(
            './/style:style/style:text-properties', NS
        ):
            lang = text_props.get(f'{{{fo_ns}}}language')
            country = text_props.get(f'{{{fo_ns}}}country')
            if lang == 'en' and country == 'US':
                lang_ok = True
                break

        # Also check styles.xml in case language is set there
        if not lang_ok:
            for text_props in styles_root.findall(
                './/style:style/style:text-properties', NS
            ):
                lang = text_props.get(f'{{{fo_ns}}}language')
                country = text_props.get(f'{{{fo_ns}}}country')
                if lang == 'en' and country == 'US':
                    lang_ok = True
                    break

        if lang_ok:
            print("PASS: Component 2 — Document language is set to English (US) (0.30 pts)")
            total_score += 0.30
        else:
            print("FAIL: Component 2 — Document language NOT set to English (US)")
    except Exception as e:
        print(f"ERROR: Component 2 (language) — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Footer with centered page numbers present (0.35 points)
    # The task requires adding page numbers in the footer (centered).
    # In ODT this appears as <style:footer> inside <style:master-page> in styles.xml,
    # containing a <text:page-number> element inside a centered paragraph.
    # -------------------------------------------------------------------------
    try:
        footer_ok = False
        page_num_ok = False
        footer_centered = False

        text_ns = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
        style_ns = 'urn:oasis:names:tc:opendocument:xmlns:style:1.0'
        fo_ns = 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0'

        for master_page in styles_root.findall('.//style:master-page', NS):
            footer_el = master_page.find(f'{{{style_ns}}}footer')
            if footer_el is not None:
                footer_ok = True
                # Check for page number field
                page_num_els = footer_el.findall(f'.//{{{text_ns}}}page-number')
                if page_num_els:
                    page_num_ok = True

                # Check for centered alignment — look for a style with text-align center
                # or inline style on paragraph
                for para_el in footer_el.findall(f'{{{text_ns}}}p'):
                    # Check via style reference
                    para_style_name = para_el.get(f'{{{text_ns}}}style-name') or para_el.get('style-name')
                    if para_style_name:
                        # Look up that style in automatic-styles
                        for s in styles_root.findall('.//style:style', NS):
                            if s.get(f'{{{style_ns}}}name') == para_style_name or s.get('name') == para_style_name:
                                para_props = s.find(f'{{{style_ns}}}paragraph-properties')
                                if para_props is not None:
                                    align = para_props.get(f'{{{fo_ns}}}text-align')
                                    if align == 'center':
                                        footer_centered = True

        # If centering not yet confirmed, try looking up FooterP style via style:name attribute
        if footer_ok and page_num_ok and not footer_centered:
            # Collect all style names from paragraphs in footer
            footer_style_names = set()
            for master_page in styles_root.findall('.//style:master-page', NS):
                footer_el_inner = master_page.find(f'{{{style_ns}}}footer')
                if footer_el_inner is not None:
                    for para_el in footer_el_inner.findall(f'{{{text_ns}}}p'):
                        # style-name may be in style namespace or text namespace
                        sname = (para_el.get(f'{{{style_ns}}}style-name')
                                 or para_el.get(f'{{{text_ns}}}style-name'))
                        if sname:
                            footer_style_names.add(sname)

            print(f"  Footer paragraph style names: {footer_style_names}")

            # Look up those styles in automatic-styles for paragraph alignment
            for s in styles_root.findall('.//style:style', NS):
                sname = s.get(f'{{{style_ns}}}name')
                if sname in footer_style_names:
                    para_props = s.find(f'{{{style_ns}}}paragraph-properties')
                    if para_props is not None:
                        align = para_props.get(f'{{{fo_ns}}}text-align')
                        print(f"  Style '{sname}' paragraph alignment: {align}")
                        if align == 'center':
                            footer_centered = True

        print(f"  Footer element found: {footer_ok}")
        print(f"  Page number field found: {page_num_ok}")
        print(f"  Footer paragraph centered: {footer_centered}")

        if footer_ok and page_num_ok and footer_centered:
            print("PASS: Component 3 — Footer with centered page numbers is present (0.35 pts)")
            total_score += 0.35
        elif footer_ok and page_num_ok:
            # Partial — footer and page number present but alignment unclear
            print("PARTIAL: Component 3 — Footer with page numbers present but centering not confirmed (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Footer/page number missing (footer={footer_ok}, page_num={page_num_ok})")
    except Exception as e:
        print(f"ERROR: Component 3 (footer/page numbers) — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

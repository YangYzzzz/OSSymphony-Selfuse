"""
Reward Script: Insert Appendix_Data.odt subdocument with landscape orientation
Task ID: writer_rm_083
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): Appendix_Data section exists as subdocument in master doc
  Component 2 (0.25): Landscape page layout defined in master doc styles
  Component 3 (0.25): Page break paragraph style triggers landscape page
  Component 4 (0.20): Original 5 chapter sections preserved
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_083'

# ODF namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
    'xlink': 'http://www.w3.org/1999/xlink',
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
}

EXPECTED_CHAPTERS = [
    'Chapter1_Executive_Summary',
    'Chapter2_Market_Analysis',
    'Chapter3_Financial_Performance',
    'Chapter4_Strategic_Initiatives',
    'Chapter5_Future_Outlook',
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the ODM as a ZIP and parse content.xml and styles.xml
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            content_xml = z.read('content.xml').decode('utf-8')
            styles_xml = z.read('styles.xml').decode('utf-8')
        content_root = ET.fromstring(content_xml)
        styles_root = ET.fromstring(styles_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot load/parse {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Appendix_Data section exists as subdocument (0.30 points)
    # The golden master doc has a text:section named "Appendix_Data" with a
    # text:section-source xlink:href pointing to Appendix_Data.odt.
    try:
        sections = content_root.findall('.//text:section', NS)
        appendix_found = False
        for sec in sections:
            sec_name = sec.get(f'{{{NS["text"]}}}name', '')
            # Check if this section references Appendix_Data.odt
            src = sec.find('text:section-source', NS)
            if src is not None:
                href = src.get(f'{{{NS["xlink"]}}}href', '')
                if 'Appendix_Data' in href or 'appendix_data' in href.lower():
                    appendix_found = True
                    break
            # Also accept section named with Appendix_Data even without explicit source check
            if 'Appendix_Data' in sec_name or 'appendix_data' in sec_name.lower():
                appendix_found = True
                break

        if appendix_found:
            print(f"PASS: Component 1 -- Appendix_Data subdocument section found (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 -- No Appendix_Data subdocument section found in master doc")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Landscape page layout defined in styles.xml (0.25 points)
    # The golden file has a style:page-layout with landscape orientation in styles.xml.
    try:
        landscape_layout_found = False
        landscape_layout_name = None

        # Search in styles.xml automatic-styles for page-layout with landscape
        for pl in styles_root.findall('.//style:page-layout', NS):
            props = pl.find('style:page-layout-properties', NS)
            if props is not None:
                orientation = props.get(f'{{{NS["style"]}}}print-orientation', '')
                if orientation == 'landscape':
                    landscape_layout_found = True
                    landscape_layout_name = pl.get(f'{{{NS["style"]}}}name', '')
                    break

        if landscape_layout_found:
            print(f"PASS: Component 2 -- Landscape page layout '{landscape_layout_name}' found in styles.xml (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- No landscape page layout found in styles.xml")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Page break paragraph style triggers landscape page (0.25 points)
    # The golden file has either:
    #   a) A paragraph style in content.xml automatic-styles with style:master-page-name
    #      referencing a landscape master page, AND a paragraph using that style before the appendix section.
    #   b) Or some other mechanism to switch to landscape at the appendix boundary.
    # We check: there exists a paragraph style that references a master page backed by a landscape layout.
    try:
        landscape_break_found = False

        # First, build a map: master-page-name -> page-layout-name from styles.xml
        master_to_layout = {}
        for mp in styles_root.findall('.//style:master-page', NS):
            mp_name = mp.get(f'{{{NS["style"]}}}name', '')
            layout_name = mp.get(f'{{{NS["style"]}}}page-layout-name', '')
            master_to_layout[mp_name] = layout_name

        # Identify which master pages use a landscape layout
        landscape_masters = set()
        for mp_name, layout_name in master_to_layout.items():
            for pl in styles_root.findall('.//style:page-layout', NS):
                if pl.get(f'{{{NS["style"]}}}name', '') == layout_name:
                    props = pl.find('style:page-layout-properties', NS)
                    if props is not None:
                        orient = props.get(f'{{{NS["style"]}}}print-orientation', '')
                        if orient == 'landscape':
                            landscape_masters.add(mp_name)

        # Now check content.xml automatic-styles for a paragraph style with master-page-name in landscape_masters
        auto_styles = content_root.find('office:automatic-styles', NS)
        if auto_styles is not None:
            for st in auto_styles.findall('style:style', NS):
                family = st.get(f'{{{NS["style"]}}}family', '')
                if family == 'paragraph':
                    mp_ref = st.get(f'{{{NS["style"]}}}master-page-name', '')
                    if mp_ref in landscape_masters:
                        # Also verify that a paragraph in the body uses this style
                        style_name = st.get(f'{{{NS["style"]}}}name', '')
                        body = content_root.find('.//office:text', NS)
                        if body is not None:
                            for elem in body.iter():
                                tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                                if tag in ('p', 'h'):
                                    used_style = elem.get(f'{{{NS["text"]}}}style-name', '')
                                    if used_style == style_name:
                                        landscape_break_found = True
                                        break
                        if landscape_break_found:
                            break

        if landscape_break_found:
            print(f"PASS: Component 3 -- Page break to landscape master page configured (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- No page break paragraph style referencing landscape master page")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Original 5 chapter sections preserved AND appendix added (0.20 points)
    # This is a compound check: all 5 original chapters still exist AND the appendix section
    # is present. This ensures the task added a subdocument without breaking existing structure.
    # Anchored to task change: only passes when appendix_found is True (from Component 1 logic).
    try:
        section_names = set()
        for sec in content_root.findall('.//text:section', NS):
            name = sec.get(f'{{{NS["text"]}}}name', '')
            section_names.add(name)

        missing = [ch for ch in EXPECTED_CHAPTERS if ch not in section_names]
        has_appendix_section = any('Appendix_Data' in n or 'appendix_data' in n.lower() for n in section_names)

        if not missing and has_appendix_section:
            print(f"PASS: Component 4 -- All 5 chapters preserved AND Appendix_Data section present (0.20 pts)")
            total_score += 0.20
        elif missing:
            print(f"FAIL: Component 4 -- Missing chapter sections: {missing}")
        else:
            print(f"FAIL: Component 4 -- Appendix_Data section not yet added to master doc")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/Report_Master.odm'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

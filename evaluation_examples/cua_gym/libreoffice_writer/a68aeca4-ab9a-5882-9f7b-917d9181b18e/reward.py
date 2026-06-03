"""
Reward Script: Create a master document (.odm) from four ODT chapter files
Task ID: writer_rm_085
Domain: libreoffice_writer
Scoring:
  Component 1: ODM file exists with correct mimetype (0.2 pts)
  Component 2: All 4 subdocuments referenced via text:section-source (0.3 pts)
  Component 3: Subdocuments in correct order (0.2 pts)
  Component 4: Heading 1 style defined (0.1 pts)
  Component 5: Heading 2 style defined (0.1 pts)
  Component 6: Body Text style defined (0.1 pts)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_085'
ODM_PATH = f'{WORKDIR}/TechReport_Master.odm'

# Expected subdocuments in order
EXPECTED_SUBDOCS = [
    'Chen_Networking.odt',
    'Patel_Security.odt',
    'Garcia_Database.odt',
    'Kim_Frontend.odt',
]

# ODF namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
    'xlink': 'http://www.w3.org/1999/xlink',
}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ========================================================
    # Component 1: ODM file exists with correct mimetype (0.2 pts)
    # ========================================================
    try:
        if not os.path.exists(ODM_PATH):
            print(f"FAIL: Component 1 -- TechReport_Master.odm not found at {ODM_PATH}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        with zipfile.ZipFile(ODM_PATH, 'r') as z:
            mimetype = z.read('mimetype').decode('utf-8').strip()

        if mimetype == 'application/vnd.oasis.opendocument.text-master':
            print(f"PASS: Component 1 -- ODM exists with correct mimetype (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- Wrong mimetype: '{mimetype}', expected 'application/vnd.oasis.opendocument.text-master'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Parse content.xml for subdocument checks
    try:
        with zipfile.ZipFile(ODM_PATH, 'r') as z:
            content_xml = z.read('content.xml').decode('utf-8')
        content_tree = ET.fromstring(content_xml)
    except Exception as e:
        print(f"ERROR: Cannot parse content.xml -- {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Find all text:section-source elements and extract xlink:href values
    # These represent the subdocument references in the master document
    section_sources = content_tree.findall('.//text:section-source', NS)
    found_subdocs = []
    for src in section_sources:
        href = src.get(f'{{{NS["xlink"]}}}href', '')
        if href:
            # href may be a relative path like "Chen_Networking.odt" or absolute
            basename = os.path.basename(href)
            found_subdocs.append(basename)

    print(f"  Found subdocument references: {found_subdocs}")

    # ========================================================
    # Component 2: All 4 subdocuments referenced (0.3 pts)
    # ========================================================
    try:
        found_set = set(found_subdocs)
        expected_set = set(EXPECTED_SUBDOCS)
        missing = expected_set - found_set
        if len(missing) == 0:
            print(f"PASS: Component 2 -- All 4 subdocuments referenced (0.3 pts)")
            total_score += 0.3
        else:
            # Partial credit: proportional to how many found
            matched = len(expected_set) - len(missing)
            partial = round(0.3 * matched / 4, 2)
            if partial > 0:
                print(f"PARTIAL: Component 2 -- {matched}/4 subdocuments found, missing: {missing} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 -- Missing subdocuments: {missing}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # ========================================================
    # Component 3: Subdocuments in correct order (0.2 pts)
    # ========================================================
    try:
        if found_subdocs == EXPECTED_SUBDOCS:
            print(f"PASS: Component 3 -- Subdocuments in correct order (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 -- Order mismatch. Found: {found_subdocs}, expected: {EXPECTED_SUBDOCS}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Parse styles.xml for heading style checks
    try:
        with zipfile.ZipFile(ODM_PATH, 'r') as z:
            styles_xml = z.read('styles.xml').decode('utf-8')
        styles_tree = ET.fromstring(styles_xml)
    except Exception as e:
        print(f"ERROR: Cannot parse styles.xml -- {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Collect all style:style elements from office:styles
    office_styles = styles_tree.find('.//office:styles', NS)
    style_map = {}
    if office_styles is not None:
        for s in office_styles.findall('style:style', NS):
            display_name = s.get(f'{{{NS["style"]}}}display-name', '')
            style_name = s.get(f'{{{NS["style"]}}}name', '')
            style_map[display_name] = s
            style_map[style_name] = s

    # Also check automatic-styles in styles.xml
    auto_styles = styles_tree.find('.//office:automatic-styles', NS)
    if auto_styles is not None:
        for s in auto_styles.findall('style:style', NS):
            display_name = s.get(f'{{{NS["style"]}}}display-name', '')
            style_name = s.get(f'{{{NS["style"]}}}name', '')
            if display_name:
                style_map[display_name] = s
            if style_name:
                style_map[style_name] = s

    print(f"  Available style names: {list(style_map.keys())}")

    def check_style_has_text_props(style_elem, style_display_name):
        """Check that a style defines text properties (font, size, etc.)."""
        if style_elem is None:
            return False, f"Style '{style_display_name}' not found"
        text_props = style_elem.find('style:text-properties', NS)
        if text_props is None:
            return False, f"Style '{style_display_name}' has no text-properties"
        # Check for at least font-size being defined
        font_size = text_props.get(f'{{{NS["fo"]}}}font-size', '')
        font_name = text_props.get(f'{{{NS["style"]}}}font-name', '')
        if font_size:
            return True, f"font-name='{font_name}', font-size='{font_size}'"
        return False, f"Style '{style_display_name}' text-properties missing font-size"

    # ========================================================
    # Component 4: Heading 1 style defined (0.1 pts)
    # ========================================================
    try:
        h1 = style_map.get('Heading 1') or style_map.get('Heading_20_1')
        ok, detail = check_style_has_text_props(h1, 'Heading 1')
        if ok:
            # Additionally verify it's bold and has a reasonable heading size
            text_props = h1.find('style:text-properties', NS)
            font_weight = text_props.get(f'{{{NS["fo"]}}}font-weight', '')
            if font_weight == 'bold':
                print(f"PASS: Component 4 -- Heading 1 style defined with bold, {detail} (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 4 -- Heading 1 not bold (font-weight='{font_weight}')")
        else:
            print(f"FAIL: Component 4 -- {detail}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # ========================================================
    # Component 5: Heading 2 style defined (0.1 pts)
    # ========================================================
    try:
        h2 = style_map.get('Heading 2') or style_map.get('Heading_20_2')
        ok, detail = check_style_has_text_props(h2, 'Heading 2')
        if ok:
            text_props = h2.find('style:text-properties', NS)
            font_weight = text_props.get(f'{{{NS["fo"]}}}font-weight', '')
            if font_weight == 'bold':
                print(f"PASS: Component 5 -- Heading 2 style defined with bold, {detail} (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 5 -- Heading 2 not bold (font-weight='{font_weight}')")
        else:
            print(f"FAIL: Component 5 -- {detail}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # ========================================================
    # Component 6: Body Text style defined (0.1 pts)
    # ========================================================
    try:
        bt = style_map.get('Body Text') or style_map.get('Body_20_Text')
        ok, detail = check_style_has_text_props(bt, 'Body Text')
        if ok:
            print(f"PASS: Component 6 -- Body Text style defined, {detail} (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 6 -- {detail}")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

"""
Reward Script: Save document as .ott template named 'Research_Paper_Template.ott'
Task ID: writer_bs_063
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): OTT file exists at LibreOffice template directory
  Component 2 (0.25): File has correct OTT mimetype (opendocument text-template)
  Component 3 (0.25): Custom heading styles (Heading 1-3) are preserved
  Component 4 (0.25): Page layout has 2.54cm left/right margins + header/footer enabled
"""

import os
import zipfile
import xml.etree.ElementTree as ET

# Possible locations for the OTT template file
TEMPLATE_PATHS = [
    '/home/user/.config/libreoffice/user/template/Research_Paper_Template.ott',
    '/home/user/Templates/Research_Paper_Template.ott',
]

TASK_ID = 'writer_bs_063'

# ODF namespaces
NS_STYLE = 'urn:oasis:names:tc:opendocument:xmlns:style:1.0'
NS_FO = 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0'
NS_OFFICE = 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'


def find_ott_file():
    """Search for the OTT file in known template locations."""
    for path in TEMPLATE_PATHS:
        if os.path.isfile(path):
            return path
    # Also search recursively under common locations
    search_dirs = [
        '/home/user/.config/libreoffice',
        '/home/user/Templates',
        '/home/user/Desktop',
        '/home/user/Documents',
        '/home/user',
    ]
    for d in search_dirs:
        if not os.path.isdir(d):
            continue
        for root_dir, dirs, files in os.walk(d):
            for f in files:
                if f == 'Research_Paper_Template.ott':
                    return os.path.join(root_dir, f)
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: OTT file exists at a template directory (0.25 points)
    try:
        ott_path = find_ott_file()
        if ott_path is not None:
            print(f"PASS: Component 1 - OTT file found at {ott_path} (0.25 pts)")
            total_score += 0.25
        else:
            print("FAIL: Component 1 - Research_Paper_Template.ott not found in any template location")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    if ott_path is None:
        # No file to check further
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Correct OTT mimetype (0.25 points)
    try:
        with zipfile.ZipFile(ott_path, 'r') as z:
            if 'mimetype' in z.namelist():
                mime = z.read('mimetype').decode('utf-8').strip()
                if mime == 'application/vnd.oasis.opendocument.text-template':
                    print(f"PASS: Component 2 - Correct mimetype: {mime} (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 2 - Expected OTT mimetype, found: {mime}")
            else:
                print("FAIL: Component 2 - No mimetype entry in OTT zip archive")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Custom heading styles preserved (Heading 1, 2, 3) (0.25 points)
    try:
        with zipfile.ZipFile(ott_path, 'r') as z:
            styles_xml = z.read('styles.xml').decode('utf-8')
            root = ET.fromstring(styles_xml)

            heading_styles_found = set()
            target_headings = {'Heading_20_1', 'Heading_20_2', 'Heading_20_3'}

            for style in root.iter(f'{{{NS_STYLE}}}style'):
                sname = style.attrib.get(f'{{{NS_STYLE}}}name', '')
                if sname in target_headings:
                    # Verify the style has text-properties (i.e., customized)
                    tp = style.find(f'{{{NS_STYLE}}}text-properties')
                    if tp is not None:
                        heading_styles_found.add(sname)

            if target_headings.issubset(heading_styles_found):
                print(f"PASS: Component 3 - All 3 custom Heading styles found: {heading_styles_found} (0.25 pts)")
                total_score += 0.25
            else:
                missing = target_headings - heading_styles_found
                print(f"FAIL: Component 3 - Missing heading styles: {missing}, found: {heading_styles_found}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Page layout with 2.54cm margins + header/footer enabled (0.25 points)
    try:
        with zipfile.ZipFile(ott_path, 'r') as z:
            styles_xml = z.read('styles.xml').decode('utf-8')
            root = ET.fromstring(styles_xml)

            # Check margins in page-layout-properties
            margins_ok = any(
                '2.54' in prop.attrib.get(f'{{{NS_FO}}}margin-left', '')
                and '2.54' in prop.attrib.get(f'{{{NS_FO}}}margin-right', '')
                for pl in root.iter(f'{{{NS_STYLE}}}page-layout')
                for prop in pl.iter(f'{{{NS_STYLE}}}page-layout-properties')
            )

            # Check header and footer in master page
            header_ok = any(
                mp.find(f'{{{NS_STYLE}}}header') is not None
                for mp in root.iter(f'{{{NS_STYLE}}}master-page')
            )
            footer_ok = any(
                mp.find(f'{{{NS_STYLE}}}footer') is not None
                for mp in root.iter(f'{{{NS_STYLE}}}master-page')
            )

            if margins_ok and header_ok and footer_ok:
                print(f"PASS: Component 4 - Margins 2.54cm + header/footer enabled (0.25 pts)")
                total_score += 0.25
            else:
                details = f"margins_ok={margins_ok}, header={header_ok}, footer={footer_ok}"
                print(f"FAIL: Component 4 - {details}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

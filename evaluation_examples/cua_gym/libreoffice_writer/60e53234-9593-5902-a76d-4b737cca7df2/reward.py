"""
Reward Script: Create a page style called 'Title Page' with specific properties
Task ID: writer_bs_073
Domain: libreoffice_writer (ODT format)
Scoring:
  Component 1: 'Title Page' master page exists (0.25)
  Component 2: A4 portrait orientation (0.15)
  Component 3: 3cm margins on all sides (0.25)
  Component 4: No header enabled (0.10)
  Component 5: No footer enabled (0.10)
  Component 6: Next style set to Default Page Style (0.15)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_073'

# ODF namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
    'loext': 'urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'draw': 'urn:oasis:names:tc:opendocument:xmlns:drawing:1.0',
}

# Helper to get attribute with namespace
def ns_attr(ns_prefix, attr_name):
    return f'{{{NS[ns_prefix]}}}{attr_name}'


def parse_cm(value_str):
    """Parse a cm value string like '3cm' into a float."""
    if value_str and value_str.endswith('cm'):
        try:
            return float(value_str[:-2])
        except ValueError:
            return None
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        zf = zipfile.ZipFile(file_path)
        tree = ET.parse(zf.open('styles.xml'))
        root = tree.getroot()
        zf.close()
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find all master pages
    master_pages = {}
    for mp in root.iter(ns_attr('style', 'master-page')):
        name = mp.get(ns_attr('style', 'name'), '')
        display_name = mp.get(ns_attr('style', 'display-name'), name)
        layout_name = mp.get(ns_attr('style', 'page-layout-name'), '')
        next_style = mp.get(ns_attr('style', 'next-style-name'), '')
        master_pages[display_name] = {
            'internal_name': name,
            'layout_name': layout_name,
            'next_style': next_style,
            'element': mp,
        }

    # Find all page layouts
    page_layouts = {}
    for pl in root.iter(ns_attr('style', 'page-layout')):
        pl_name = pl.get(ns_attr('style', 'name'), '')
        page_layouts[pl_name] = pl

    # Component 1: 'Title Page' master page exists (0.25 points)
    try:
        title_page_found = 'Title Page' in master_pages
        if title_page_found:
            print(f"PASS: Component 1 -- 'Title Page' master page exists (0.25 pts)")
            total_score += 0.25
        else:
            # Also check internal names for variants like "Title_20_Page" or "TitlePage"
            found_via_internal = False
            for dn, info in master_pages.items():
                iname = info['internal_name'].lower().replace('_20_', ' ').replace('_', ' ')
                if 'title page' in iname.lower() or 'title page' in dn.lower():
                    found_via_internal = True
                    title_page_found = True
                    # Treat this display name as the Title Page entry
                    master_pages['Title Page'] = info
                    print(f"PASS: Component 1 -- 'Title Page' master page exists (via internal name '{info['internal_name']}') (0.25 pts)")
                    total_score += 0.25
                    break
            if not found_via_internal:
                print(f"FAIL: Component 1 -- 'Title Page' master page not found. Available: {list(master_pages.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    if not title_page_found:
        # No Title Page style at all -- remaining checks cannot pass
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    tp_info = master_pages['Title Page']
    layout_name = tp_info['layout_name']
    layout = page_layouts.get(layout_name)

    if layout is None:
        print(f"FAIL: Could not find page layout '{layout_name}' for Title Page")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Get page-layout-properties
    plp = layout.find(ns_attr('style', 'page-layout-properties'))
    if plp is None:
        print(f"FAIL: No page-layout-properties found in layout '{layout_name}'")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: A4 portrait orientation (0.15 points)
    try:
        page_width = parse_cm(plp.get(ns_attr('fo', 'page-width'), ''))
        page_height = parse_cm(plp.get(ns_attr('fo', 'page-height'), ''))
        orientation = plp.get(ns_attr('style', 'print-orientation'), '')

        # A4 is 21.0cm x 29.7cm, allow small tolerance
        is_a4 = (page_width is not None and page_height is not None and
                 abs(page_width - 21.0) < 0.1 and abs(page_height - 29.7) < 0.1)
        is_portrait = orientation == 'portrait'

        if is_a4 and is_portrait:
            print(f"PASS: Component 2 -- A4 portrait ({page_width}cm x {page_height}cm, {orientation}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 -- Expected A4 portrait, got {page_width}cm x {page_height}cm, orientation={orientation}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: 3cm margins on all sides (0.25 points)
    try:
        margin_top = parse_cm(plp.get(ns_attr('fo', 'margin-top'), ''))
        margin_bottom = parse_cm(plp.get(ns_attr('fo', 'margin-bottom'), ''))
        margin_left = parse_cm(plp.get(ns_attr('fo', 'margin-left'), ''))
        margin_right = parse_cm(plp.get(ns_attr('fo', 'margin-right'), ''))

        margins = {
            'top': margin_top,
            'bottom': margin_bottom,
            'left': margin_left,
            'right': margin_right,
        }

        # Allow small tolerance (0.05cm)
        all_3cm = all(v is not None and abs(v - 3.0) < 0.05 for v in margins.values())

        if all_3cm:
            print(f"PASS: Component 3 -- All margins are 3cm ({margins}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- Expected 3cm margins, got {margins}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: No header enabled (0.10 points)
    # In ODF, header is enabled when the page-layout has a header-style with
    # header-footer-properties that have a non-zero min-height, OR when the
    # master-page has a style:header child element with content.
    try:
        header_style = layout.find(ns_attr('style', 'header-style'))
        # Check if header-style has any properties (children) -- empty means disabled
        header_has_props = False
        if header_style is not None:
            for child in header_style:
                header_has_props = True
                break

        # Also check if master page has header element with text content
        mp_elem = tp_info['element']
        mp_header = mp_elem.find(ns_attr('style', 'header'))
        mp_has_header_content = False
        if mp_header is not None:
            # Check if it has any text content
            header_text = ''.join(mp_header.itertext()).strip()
            if header_text:
                mp_has_header_content = True

        if not header_has_props and not mp_has_header_content:
            print(f"PASS: Component 4 -- Header is disabled (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 -- Header appears to be enabled (props={header_has_props}, content={mp_has_header_content})")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: No footer enabled (0.10 points)
    try:
        footer_style = layout.find(ns_attr('style', 'footer-style'))
        footer_has_props = False
        if footer_style is not None:
            for child in footer_style:
                footer_has_props = True
                break

        mp_footer = mp_elem.find(ns_attr('style', 'footer'))
        mp_has_footer_content = False
        if mp_footer is not None:
            footer_text = ''.join(mp_footer.itertext()).strip()
            if footer_text:
                mp_has_footer_content = True

        if not footer_has_props and not mp_has_footer_content:
            print(f"PASS: Component 5 -- Footer is disabled (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 -- Footer appears to be enabled (props={footer_has_props}, content={mp_has_footer_content})")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: Next style set to Default Page Style ('Standard') (0.15 points)
    try:
        next_style = tp_info['next_style']
        # 'Standard' is the internal name for 'Default Page Style' in LO
        if next_style == 'Standard':
            print(f"PASS: Component 6 -- Next style is 'Standard' (Default Page Style) (0.15 pts)")
            total_score += 0.15
        elif next_style.lower().replace(' ', '') in ('defaultpagestyle', 'default'):
            print(f"PASS: Component 6 -- Next style is '{next_style}' (Default Page Style variant) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 -- Expected next style 'Standard', got '{next_style}'")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved changes in LibreOffice
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.odt'
if not os.path.exists(file_path):
    # Also try .docx extension
    file_path_docx = f'{WORKDIR}/{TASK_ID}.docx'
    if os.path.exists(file_path_docx):
        file_path = file_path_docx
    else:
        print(f"File not found: {file_path} (also tried .docx)")
        print("REWARD: 0.0")
        exit(0)

verify_task(file_path)

"""
Reward Script: Insert nested sections in a Writer document
Task ID: writer_fs_077
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): Outer section 'Chapter_3' exists
  Component 2 (0.25): Inner section 'Section_3A' exists nested inside Chapter_3
  Component 3 (0.25): Inner section 'Section_3B' exists nested inside Chapter_3
  Component 4 (0.15): Section_3A has 2-column layout
  Component 5 (0.10): Section_3B has 1-column layout (explicit)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_077'

# ODF namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
}


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def parse_sections_and_styles(file_path):
    """
    Parse the ODF content.xml to extract:
    - section_tree: dict mapping section_name -> {parent, children, style_name}
    - styles: dict mapping style_name -> {column_count, column_gap}
    """
    with zipfile.ZipFile(file_path, 'r') as z:
        content_xml = z.read('content.xml').decode('utf-8')

    root = ET.fromstring(content_xml)

    # Parse automatic styles for section column info
    styles = {}
    auto_styles = root.find('.//office:automatic-styles', NS)
    if auto_styles is not None:
        for style_el in auto_styles.findall('style:style', NS):
            sname = style_el.get('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}name')
            sfamily = style_el.get('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}family')
            if sfamily == 'section':
                col_count = None
                section_props = style_el.find('style:section-properties', NS)
                if section_props is not None:
                    columns_el = section_props.find('style:columns', NS)
                    if columns_el is not None:
                        cc = columns_el.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}column-count')
                        if cc is not None:
                            col_count = int(cc)
                styles[sname] = {'column_count': col_count}

    # Parse sections from body
    sections = {}  # name -> {parent, style_name, children}

    def walk_sections(element, parent_name=None):
        for child in element:
            tag = child.tag
            if tag == '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}section':
                sec_name = child.get('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}name')
                sec_style = child.get('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name')
                sections[sec_name] = {
                    'parent': parent_name,
                    'style_name': sec_style,
                    'children': [],
                }
                if parent_name and parent_name in sections:
                    sections[parent_name]['children'].append(sec_name)
                # Recurse into this section for nested sections
                walk_sections(child, sec_name)

    body = root.find('.//office:body/office:text', NS)
    if body is not None:
        walk_sections(body, None)

    return sections, styles


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        sections, styles = parse_sections_and_styles(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"DEBUG: Found sections: {list(sections.keys())}")
    print(f"DEBUG: Found section styles: {styles}")

    # Component 1: Outer section 'Chapter_3' exists (0.25 points)
    try:
        if 'Chapter_3' in sections:
            ch3 = sections['Chapter_3']
            if ch3['parent'] is None:
                print(f"PASS: Component 1 — 'Chapter_3' section exists at top level (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 — 'Chapter_3' exists but is not top-level (parent={ch3['parent']})")
        else:
            print(f"FAIL: Component 1 — 'Chapter_3' section not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'Section_3A' exists nested inside 'Chapter_3' (0.25 points)
    try:
        if 'Section_3A' in sections:
            s3a = sections['Section_3A']
            if s3a['parent'] == 'Chapter_3':
                print(f"PASS: Component 2 — 'Section_3A' nested inside 'Chapter_3' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — 'Section_3A' exists but parent is '{s3a['parent']}', not 'Chapter_3'")
        else:
            print(f"FAIL: Component 2 — 'Section_3A' section not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'Section_3B' exists nested inside 'Chapter_3' (0.25 points)
    try:
        if 'Section_3B' in sections:
            s3b = sections['Section_3B']
            if s3b['parent'] == 'Chapter_3':
                print(f"PASS: Component 3 — 'Section_3B' nested inside 'Chapter_3' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — 'Section_3B' exists but parent is '{s3b['parent']}', not 'Chapter_3'")
        else:
            print(f"FAIL: Component 3 — 'Section_3B' section not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Section_3A has 2-column layout (0.15 points)
    try:
        if 'Section_3A' in sections:
            style_name = sections['Section_3A']['style_name']
            if style_name and style_name in styles:
                col_count = styles[style_name].get('column_count')
                if col_count == 2:
                    print(f"PASS: Component 4 — 'Section_3A' has 2-column layout (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 4 — 'Section_3A' column count is {col_count}, expected 2")
            else:
                print(f"FAIL: Component 4 — 'Section_3A' style '{style_name}' has no column info")
        else:
            print(f"FAIL: Component 4 — 'Section_3A' not found, cannot check columns")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Section_3B has 1-column layout (0.10 points)
    try:
        if 'Section_3B' in sections:
            style_name = sections['Section_3B']['style_name']
            # Determine column count: explicit style or default (1 column)
            col_count = None
            if style_name and style_name in styles:
                col_count = styles[style_name].get('column_count')
            else:
                col_count = 1  # no explicit column style means default single column
            if col_count == 1:
                print(f"PASS: Component 5 — 'Section_3B' has 1-column layout (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — 'Section_3B' column count is {col_count}, expected 1")
        else:
            print(f"FAIL: Component 5 — 'Section_3B' not found, cannot check columns")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist unsaved GUI state before verification
persist_app_state("libreoffice_writer")

# Test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.odt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Replace subdocument 'Ch4_OldVersion.odt' with 'Ch4_Revised.odt' in master document
Task ID: writer_rm_071
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Section 4 xlink:href points to Ch4_Revised.odt
  Component 2 (0.3): All 5 sections present in correct order with correct hrefs
  Component 3 (0.3): No remaining reference to Ch4_OldVersion.odt in any section href
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_071'

# Namespace map for ODM/ODF XML
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'xlink': 'http://www.w3.org/1999/xlink',
}


def extract_sections(file_path):
    """
    Parse content.xml from the ODM file and return a list of
    (section_name, xlink_href) tuples in document order.
    """
    sections = []
    with zipfile.ZipFile(file_path) as z:
        with z.open('content.xml') as f:
            tree = ET.parse(f)
    root = tree.getroot()
    # Find all text:section elements (they contain text:section-source children)
    for section_el in root.iter('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}section'):
        sec_name = section_el.attrib.get('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}name', '')
        # Find the section-source child to get the href
        href = ''
        for src in section_el.iter('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}section-source'):
            href = src.attrib.get('{http://www.w3.org/1999/xlink}href', '')
            break
        sections.append((sec_name, href))
    return sections


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        sections = extract_sections(file_path)
        print(f"INFO: Found {len(sections)} sections in master document")
        for i, (name, href) in enumerate(sections):
            print(f"  Section {i+1}: name='{name}', href='{href}'")
    except Exception as e:
        print(f"CRITICAL: Cannot parse master document {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Expected section hrefs in order
    expected_hrefs = ['Ch1.odt', 'Ch2.odt', 'Ch3.odt', 'Ch4_Revised.odt', 'Ch5.odt']

    # Component 1: Section 4 xlink:href points to Ch4_Revised.odt (0.4 points)
    try:
        if len(sections) >= 4:
            sec4_href = sections[3][1]  # 0-indexed, 4th section
            if sec4_href == 'Ch4_Revised.odt':
                print(f"PASS: Component 1 — Section 4 href is 'Ch4_Revised.odt' (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — Section 4 href is '{sec4_href}', expected 'Ch4_Revised.odt'")
        else:
            print(f"FAIL: Component 1 — Only {len(sections)} sections found, need at least 4")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 5 sections in correct order with correct hrefs (0.3 points)
    try:
        if len(sections) == 5:
            actual_hrefs = [href for _, href in sections]
            if actual_hrefs == expected_hrefs:
                print(f"PASS: Component 2 — All 5 sections in correct order (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Section hrefs {actual_hrefs} != expected {expected_hrefs}")
        else:
            print(f"FAIL: Component 2 — Found {len(sections)} sections, expected 5")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: No remaining reference to Ch4_OldVersion.odt in any section href (0.3 points)
    try:
        old_refs = [href for _, href in sections if 'Ch4_OldVersion' in href]
        if len(old_refs) == 0:
            print(f"PASS: Component 3 — No references to Ch4_OldVersion.odt remain (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Found {len(old_refs)} references to Ch4_OldVersion.odt")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
file_path = f'{WORKDIR}/Guide_Master.odm'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Move 'References.odt' to end of master document
Task ID: writer_rm_084
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): References.odt is the last subdocument in the ODM
  Component 2 (0.5): Full subdocument order matches expected sequence
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_084'

# Expected subdocument order after task completion
EXPECTED_ORDER = [
    'Abstract.odt',
    'Introduction.odt',
    'Methods.odt',
    'Results.odt',
    'Conclusion.odt',
    'References.odt',
]


def parse_odm_section_order(file_path):
    """
    Parse an ODM (ODF master document) file and extract the ordered list
    of subdocument hrefs from text:section / text:section-source elements.
    """
    ns = {
        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
        'xlink': 'http://www.w3.org/1999/xlink',
    }
    with zipfile.ZipFile(file_path, 'r') as z:
        content_xml = z.read('content.xml')

    root = ET.fromstring(content_xml)
    sections = root.findall('.//text:section', ns)

    hrefs = []
    for section in sections:
        src = section.find('text:section-source', ns)
        if src is not None:
            href = src.get('{http://www.w3.org/1999/xlink}href')
            if href:
                hrefs.append(href)
    return hrefs


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file exists and is a valid ODM zip
    try:
        hrefs = parse_odm_section_order(file_path)
        print(f"INFO: Found {len(hrefs)} subdocument links: {hrefs}")
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODM file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(hrefs) == 0:
        print("CRITICAL: No subdocument sections found in ODM")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: References.odt is the LAST subdocument (0.5 points)
    # Initial state has References at position 3 (index 2) -> FAIL
    # Golden state has References at the end (last position) -> PASS
    try:
        if hrefs[-1] == 'References.odt':
            print(f"PASS: Component 1 — References.odt is the last subdocument (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Expected last subdocument to be 'References.odt', found '{hrefs[-1]}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Full order matches expected sequence exactly (0.5 points)
    # Initial order: Abstract, Introduction, References, Methods, Results, Conclusion -> FAIL
    # Golden order: Abstract, Introduction, Methods, Results, Conclusion, References -> PASS
    try:
        if hrefs == EXPECTED_ORDER:
            print(f"PASS: Component 2 — Full subdocument order matches expected sequence (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — Order mismatch")
            print(f"  Expected: {EXPECTED_ORDER}")
            print(f"  Found:    {hrefs}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
file_path = f'{WORKDIR}/Paper_Master.odm'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

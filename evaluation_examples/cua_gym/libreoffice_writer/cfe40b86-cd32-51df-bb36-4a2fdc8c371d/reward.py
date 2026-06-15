"""
Reward Script: Reorder subdocuments in master document
Task ID: writer_rm_054
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): Second section links to Literature_Review.odt
  Component 2 (0.3): Third section links to Methodology.odt
  Component 3 (0.2): Full order is Introduction, Literature_Review, Methodology, Results, Conclusion
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_054'

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the ODM master document (ODF zip archive)
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            content_xml = z.read('content.xml').decode('utf-8')
        root = ET.fromstring(content_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Define namespaces
    ns = {
        'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
        'xlink': 'http://www.w3.org/1999/xlink',
    }

    # Extract ordered list of subdocument hrefs from text:section elements
    try:
        body = root.find('.//office:body/office:text', ns)
        sections = body.findall('text:section', ns)
        subdoc_order = []
        for sec in sections:
            source = sec.find('text:section-source', ns)
            if source is not None:
                href = source.get('{http://www.w3.org/1999/xlink}href', '')
                subdoc_order.append(href)
        print(f"INFO: Found {len(subdoc_order)} subdocument sections: {subdoc_order}")
    except Exception as e:
        print(f"CRITICAL: Cannot parse sections: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(subdoc_order) < 3:
        print(f"FAIL: Expected at least 5 subdocuments, found {len(subdoc_order)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Second section links to Literature_Review.odt (0.5 points)
    # In initial state, position 2 is Methodology.odt — this check FAILS on initial, PASSES on golden
    try:
        second_href = subdoc_order[1]
        if second_href == 'Literature_Review.odt':
            print(f"PASS: Component 1 — Second section is Literature_Review.odt (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Expected Literature_Review.odt at position 2, found: {second_href}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Third section links to Methodology.odt (0.3 points)
    # In initial state, position 3 is Literature_Review.odt — this check FAILS on initial, PASSES on golden
    try:
        third_href = subdoc_order[2]
        if third_href == 'Methodology.odt':
            print(f"PASS: Component 2 — Third section is Methodology.odt (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected Methodology.odt at position 3, found: {third_href}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Full correct order preserved (0.2 points)
    # Verifies the complete order including that Introduction, Results, Conclusion stayed in place
    # In initial state, this FAILS because positions 2 and 3 are swapped
    try:
        expected_order = [
            'Introduction.odt',
            'Literature_Review.odt',
            'Methodology.odt',
            'Results.odt',
            'Conclusion.odt',
        ]
        if subdoc_order == expected_order:
            print(f"PASS: Component 3 — Full order matches expected: {expected_order} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Order mismatch. Expected: {expected_order}, Found: {subdoc_order}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.odm'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Remove subdocument 'Appendix_C.odt' from master document
Task ID: writer_rm_053
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Appendix_C.odt is NOT linked in the master document
  Component 2 (0.3): Master document has exactly 4 subdocument sections
  Component 3 (0.2): Remaining subdocuments are the correct 4 files
  Component 4 (0.1): Appendix_C.odt file still exists on disk (not deleted)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_053'

# Namespaces used in ODF content.xml
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'xlink': 'http://www.w3.org/1999/xlink',
}

EXPECTED_REMAINING = {'Chapter1.odt', 'Chapter2.odt', 'Chapter3.odt', 'Appendix_A.odt'}


def get_subdocument_links(odm_path):
    """Extract all subdocument xlink:href values from an ODM master document."""
    links = []
    try:
        with zipfile.ZipFile(odm_path, 'r') as z:
            content_xml = z.read('content.xml').decode('utf-8')
        root = ET.fromstring(content_xml)
        # Find all text:section-source elements
        for section_source in root.iter('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}section-source'):
            href = section_source.get('{http://www.w3.org/1999/xlink}href')
            if href:
                links.append(href)
    except Exception as e:
        print(f"ERROR: Failed to parse ODM file: {e}")
    return links


def verify_task(odm_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: ODM file must exist and be a valid zip
    if not os.path.exists(odm_path):
        print(f"CRITICAL: Master document not found: {odm_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        links = get_subdocument_links(odm_path)
        print(f"INFO: Found subdocument links: {links}")
    except Exception as e:
        print(f"CRITICAL: Cannot parse master document: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Appendix_C.odt is NOT linked in the master document (0.4 points)
    try:
        appendix_c_linked = any('Appendix_C.odt' in link for link in links)
        if not appendix_c_linked:
            print(f"PASS: Component 1 — Appendix_C.odt is not linked in master document (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Appendix_C.odt is still linked in master document")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Master document has exactly 4 subdocument sections (0.3 points)
    try:
        num_links = len(links)
        if num_links == 4:
            print(f"PASS: Component 2 — Master has exactly 4 subdocument links (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected 4 subdocument links, found {num_links}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Remaining subdocuments are the correct 4 files (0.2 points)
    try:
        actual_set = set(links)
        if actual_set == EXPECTED_REMAINING:
            print(f"PASS: Component 3 — Remaining subdocuments match expected set (0.2 pts)")
            total_score += 0.2
        else:
            missing = EXPECTED_REMAINING - actual_set
            extra = actual_set - EXPECTED_REMAINING
            print(f"FAIL: Component 3 — Subdocument mismatch. Missing: {missing}, Extra: {extra}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Appendix_C.odt is unlinked from master BUT still exists on disk (0.1 points)
    # This is a compound check: only awards points if Appendix_C.odt is NOT linked (task change)
    # AND the file still exists on disk (preservation requirement).
    try:
        appendix_c_path = os.path.join(WORKDIR, 'Appendix_C.odt')
        appendix_c_unlinked = not any('Appendix_C.odt' in link for link in links)
        appendix_c_on_disk = os.path.exists(appendix_c_path)
        if appendix_c_unlinked and appendix_c_on_disk:
            print(f"PASS: Component 4 — Appendix_C.odt unlinked from master and still exists on disk (0.1 pts)")
            total_score += 0.1
        elif not appendix_c_unlinked:
            print(f"FAIL: Component 4 — Appendix_C.odt is still linked in master")
        else:
            print(f"FAIL: Component 4 — Appendix_C.odt was deleted from disk (should only be unlinked)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
odm_path = os.path.join(WORKDIR, 'Report_Master.odm')
if not os.path.exists(odm_path):
    print(f"File not found: {odm_path}")
    print("REWARD: 0.0")
else:
    verify_task(odm_path)

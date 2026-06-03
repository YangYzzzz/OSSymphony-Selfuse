"""
Reward Script: Verify master document with three linked sub-documents
Task ID: writer_tech_053
Domain: libreoffice_writer
Scoring:
  Gate: ODM file must be a valid ODF document (0 points - precondition)
  Gate: Sub-documents must exist (0 points - precondition)
  Component 1 (0.30): ODM contains exactly 3 text:section elements
  Component 2 (0.40): Sections reference correct sub-document filenames in order
  Component 3 (0.30): Each section has a valid text:section-source with xlink:href
"""

import os
import zipfile
from xml.etree import ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_053'

EXPECTED_SUBDOCS = [
    'chapter1_intro.docx',
    'chapter2_setup.docx',
    'chapter3_reference.docx',
]

NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'xlink': 'http://www.w3.org/1999/xlink',
    'manifest': 'urn:oasis:names:tc:opendocument:xmlns:manifest:1.0',
}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: ODM file must be a valid ODF document (precondition, 0 points)
    try:
        if not zipfile.is_zipfile(file_path):
            print(f"GATE FAIL: {file_path} is not a valid ZIP/ODF file")
            print("REWARD: 0.0")
            return 0.0
        with zipfile.ZipFile(file_path) as zf:
            names = zf.namelist()
            if 'mimetype' not in names or 'content.xml' not in names:
                print("GATE FAIL: ODM missing mimetype or content.xml")
                print("REWARD: 0.0")
                return 0.0
            mimetype = zf.read('mimetype').decode().strip()
            if 'opendocument' not in mimetype.lower():
                print(f"GATE FAIL: Not an ODF file, mimetype={mimetype}")
                print("REWARD: 0.0")
                return 0.0
        print(f"GATE PASS: Valid ODF document, mimetype={mimetype}")
    except Exception as e:
        print(f"GATE ERROR: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse content.xml for scoring checks
    sections = []
    section_hrefs = []
    try:
        with zipfile.ZipFile(file_path) as zf:
            content_xml = zf.read('content.xml').decode()
        root = ET.fromstring(content_xml)

        # Find all text:section elements
        all_sections = root.findall('.//text:section', NS)
        sections = all_sections

        # Extract xlink:href from text:section-source children
        for sec in sections:
            source = sec.find('text:section-source', NS)
            if source is not None:
                href = source.get('{http://www.w3.org/1999/xlink}href', '')
                section_hrefs.append(href)
            else:
                section_hrefs.append(None)

        print(f"INFO: Found {len(sections)} sections with hrefs: {section_hrefs}")
    except Exception as e:
        print(f"ERROR: Parsing content.xml - {e}")

    # Component 1: ODM contains exactly 3 text:section elements (0.30 points)
    try:
        if len(sections) == 3:
            print(f"PASS: Component 1 - Exactly 3 sections found (0.30 pts)")
            total_score += 0.30
        elif len(sections) > 0:
            # Partial: some sections exist but not the right count
            partial = round(0.30 * min(len(sections), 3) / 3, 2)
            print(f"PARTIAL: Component 1 - Expected 3 sections, found {len(sections)} ({partial} pts)")
            total_score += partial
        else:
            print("FAIL: Component 1 - No sections found in ODM")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Sections reference correct sub-document filenames in order (0.40 points)
    try:
        if len(section_hrefs) >= 3:
            # Normalize hrefs - strip path prefixes, keep just filename
            normalized_hrefs = []
            for h in section_hrefs[:3]:
                if h is not None:
                    normalized_hrefs.append(os.path.basename(h))
                else:
                    normalized_hrefs.append(None)

            matches = 0
            for i, expected in enumerate(EXPECTED_SUBDOCS):
                if i < len(normalized_hrefs) and normalized_hrefs[i] == expected:
                    matches += 1
                    print(f"  Section {i+1}: {normalized_hrefs[i]} == {expected} OK")
                else:
                    actual = normalized_hrefs[i] if i < len(normalized_hrefs) else 'MISSING'
                    print(f"  Section {i+1}: {actual} != {expected} MISMATCH")

            if matches == 3:
                print(f"PASS: Component 2 - All 3 sections reference correct files in order (0.40 pts)")
                total_score += 0.40
            elif matches > 0:
                partial = round(0.40 * matches / 3, 2)
                print(f"PARTIAL: Component 2 - {matches}/3 correct references ({partial} pts)")
                total_score += partial
            else:
                print("FAIL: Component 2 - No correct references found")
        else:
            print(f"FAIL: Component 2 - Not enough sections with hrefs (found {len(section_hrefs)})")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Each section has a valid text:section-source with xlink:href (0.30 points)
    try:
        valid_sources = 0
        for i, sec in enumerate(sections[:3]):
            source = sec.find('text:section-source', NS)
            if source is not None:
                href = source.get('{http://www.w3.org/1999/xlink}href', '')
                if href:
                    valid_sources += 1
                    print(f"  Section {i+1}: has section-source with href='{href}'")
                else:
                    print(f"  Section {i+1}: has section-source but empty href")
            else:
                print(f"  Section {i+1}: missing section-source element")

        if valid_sources == 3:
            print(f"PASS: Component 3 - All 3 sections have valid section-source elements (0.30 pts)")
            total_score += 0.30
        elif valid_sources > 0:
            partial = round(0.30 * valid_sources / 3, 2)
            print(f"PARTIAL: Component 3 - {valid_sources}/3 valid section-sources ({partial} pts)")
            total_score += partial
        else:
            print("FAIL: Component 3 - No valid section-source elements found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(round(total_score, 2), 1.0)
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

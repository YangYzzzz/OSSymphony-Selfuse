"""
Reward Script: Create a master document for company policy handbook with 5 subdocuments
Task ID: writer_rm_064
Domain: libreoffice_writer
Scoring:
  Component 1 (0.15): ODM file exists and is a valid ZIP
  Component 2 (0.15): Correct ODM mimetype (application/vnd.oasis.opendocument.text-master)
  Component 3 (0.50): All 5 subdocument sections present with correct xlink:href (0.10 each)
  Component 4 (0.20): Subdocuments in correct order
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_064'

# Expected subdocuments in order
EXPECTED_SUBDOCS = [
    'HR_Policies.odt',
    'IT_Policies.odt',
    'Finance_Policies.odt',
    'Safety_Policies.odt',
    'Ethics_Policies.odt',
]

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: ODM file exists and is a valid ZIP archive (0.15 points)
    try:
        if os.path.exists(file_path) and zipfile.is_zipfile(file_path):
            print(f"PASS: Component 1 — ODM file exists and is valid ZIP (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — ODM file missing or not a valid ZIP: {file_path}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Correct ODM mimetype (0.15 points)
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            if 'mimetype' not in z.namelist():
                print(f"FAIL: Component 2 — No mimetype entry in archive")
            else:
                mimetype = z.read('mimetype').decode('utf-8').strip()
                # Accept both text-master and text-master-master (LibreOffice variants)
                valid_mimetypes = [
                    'application/vnd.oasis.opendocument.text-master',
                    'application/vnd.oasis.opendocument.text-master-master',
                ]
                if mimetype in valid_mimetypes:
                    print(f"PASS: Component 2 — Correct mimetype: {mimetype} (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 2 — Expected master document mimetype, found: {mimetype}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Parse content.xml for Components 3 and 4
    found_subdocs = []
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            if 'content.xml' not in z.namelist():
                print(f"FAIL: Components 3-4 — No content.xml in archive")
            else:
                content_xml = z.read('content.xml').decode('utf-8')
                root = ET.fromstring(content_xml)

                # Define namespaces
                ns = {
                    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
                    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
                    'xlink': 'http://www.w3.org/1999/xlink',
                }

                # Find all text:section elements that have text:section-source children
                # These represent subdocument references in a master document
                sections = root.findall('.//text:section', ns)
                for section in sections:
                    section_source = section.find('text:section-source', ns)
                    if section_source is not None:
                        href = section_source.get(f'{{{ns["xlink"]}}}href', '')
                        # href might be relative path or just filename
                        filename = os.path.basename(href) if href else ''
                        if filename:
                            found_subdocs.append(filename)
                        else:
                            # Also check section name as fallback
                            section_name = section.get(f'{{{ns["text"]}}}name', '')
                            if section_name:
                                found_subdocs.append(section_name + '.odt')

                if not found_subdocs:
                    print(f"FAIL: Components 3-4 — No subdocument section-source references found in content.xml")
    except Exception as e:
        print(f"ERROR: Parsing content.xml — {e}")

    # Component 3: All 5 subdocument sections present (0.10 each, total 0.50)
    try:
        for subdoc in EXPECTED_SUBDOCS:
            if subdoc in found_subdocs:
                print(f"PASS: Component 3 — Subdocument '{subdoc}' found (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 — Subdocument '{subdoc}' not found. Found: {found_subdocs}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Correct order of subdocuments (0.20 points)
    try:
        if len(found_subdocs) >= len(EXPECTED_SUBDOCS):
            # Check order: the expected subdocs should appear in the correct sequence
            # Filter found_subdocs to only include expected ones, preserving order
            filtered = [s for s in found_subdocs if s in EXPECTED_SUBDOCS]
            if filtered == EXPECTED_SUBDOCS:
                print(f"PASS: Component 4 — Subdocuments in correct order (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — Incorrect order. Expected: {EXPECTED_SUBDOCS}, Found: {filtered}")
        else:
            print(f"FAIL: Component 4 — Not all subdocuments present ({len(found_subdocs)}/{len(EXPECTED_SUBDOCS)}), cannot verify order")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    # Round to avoid floating point issues
    final_score = round(final_score, 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Policy_Handbook_Master.odm'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Create a master document (.odm) from ODT subdocuments
Task ID: writer_rm_074
Domain: libreoffice_writer
Scoring:
  Component 1 (0.15): ODM file exists
  Component 2 (0.20): Valid ZIP with correct ODM mimetype
  Component 3 (0.25): Contains exactly 5 section links
  Component 4 (0.20): Correct ODT file references
  Component 5 (0.20): Correct order of subdocuments
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_074'

EXPECTED_ODT_ORDER = [
    'Cover_Page.odt',
    'Table_of_Authorities.odt',
    'Statement_of_Facts.odt',
    'Argument.odt',
    'Conclusion.odt',
]

NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'xlink': 'http://www.w3.org/1999/xlink',
}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    odm_path = os.path.join(WORKDIR, 'Legal_Brief_Master.odm')

    # Component 1: ODM file exists (0.15 points)
    # This is a task-introduced change: the ODM file does not exist in initial_env.
    try:
        if os.path.isfile(odm_path):
            print(f"PASS: Component 1 — Legal_Brief_Master.odm exists (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Legal_Brief_Master.odm not found at {odm_path}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Valid ZIP archive with correct ODM mimetype (0.20 points)
    try:
        if not zipfile.is_zipfile(odm_path):
            print(f"FAIL: Component 2 — File is not a valid ZIP archive")
        else:
            with zipfile.ZipFile(odm_path, 'r') as z:
                if 'mimetype' not in z.namelist():
                    print(f"FAIL: Component 2 — No mimetype entry in ZIP")
                else:
                    mimetype = z.read('mimetype').decode('utf-8').strip()
                    if mimetype == 'application/vnd.oasis.opendocument.text-master':
                        print(f"PASS: Component 2 — Valid ODM mimetype (0.20 pts)")
                        total_score += 0.20
                    else:
                        print(f"FAIL: Component 2 — Expected ODM mimetype, found: {repr(mimetype)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Parse content.xml for Components 3-5
    sections = []
    try:
        with zipfile.ZipFile(odm_path, 'r') as z:
            if 'content.xml' not in z.namelist():
                print(f"FAIL: Components 3-5 — No content.xml in ODM")
                print(f"\nScore: {total_score}/1.0")
                print(f"REWARD: {min(total_score, 1.0)}")
                return min(total_score, 1.0)
            content_xml = z.read('content.xml').decode('utf-8')

        root = ET.fromstring(content_xml)
        # Find all text:section elements that contain a text:section-source child
        for section_elem in root.iter(f"{{{NS['text']}}}section"):
            source_elem = section_elem.find(f"{{{NS['text']}}}section-source", NS)
            if source_elem is not None:
                href = source_elem.get(f"{{{NS['xlink']}}}href", '')
                sections.append(href)
    except Exception as e:
        print(f"ERROR: Parsing content.xml — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {min(total_score, 1.0)}")
        return min(total_score, 1.0)

    print(f"  Found section links: {sections}")

    # Component 3: Contains exactly 5 section links (0.25 points)
    try:
        if len(sections) == 5:
            print(f"PASS: Component 3 — Exactly 5 section links found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Expected 5 section links, found {len(sections)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Correct ODT file references (0.20 points)
    # Extract just the filenames (strip any path prefix)
    try:
        linked_filenames = [os.path.basename(s) for s in sections]
        expected_set = set(EXPECTED_ODT_ORDER)
        actual_set = set(linked_filenames)
        if expected_set == actual_set:
            print(f"PASS: Component 4 — All 5 expected ODT files are referenced (0.20 pts)")
            total_score += 0.20
        else:
            missing = expected_set - actual_set
            extra = actual_set - expected_set
            print(f"FAIL: Component 4 — File mismatch. Missing: {missing}, Extra: {extra}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Correct order of subdocuments (0.20 points)
    try:
        linked_filenames = [os.path.basename(s) for s in sections]
        if linked_filenames == EXPECTED_ODT_ORDER:
            print(f"PASS: Component 5 — Subdocuments in correct order (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 5 — Order mismatch. Expected: {EXPECTED_ODT_ORDER}, Found: {linked_filenames}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

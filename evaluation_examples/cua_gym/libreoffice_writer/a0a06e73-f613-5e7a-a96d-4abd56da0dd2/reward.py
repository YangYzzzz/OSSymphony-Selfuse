"""
Reward Script: Create a master document (.odm) with five subdocument links
Task ID: writer_acad_053
Domain: libreoffice_writer
Scoring:
  Component 1 (0.15): ODM file exists
  Component 2 (0.15): Valid ODM format (correct mimetype)
  Component 3 (0.20): Contains exactly 5 text:section elements
  Component 4 (0.30): All 5 subdocument links point to correct chapter files
  Component 5 (0.20): Subdocument links are in correct order (chapter1-5)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_acad_053'

EXPECTED_CHAPTERS = [
    'chapter1.docx',
    'chapter2.docx',
    'chapter3.docx',
    'chapter4.docx',
    'chapter5.docx',
]

EXPECTED_MIMETYPE = 'application/vnd.oasis.opendocument.text-master'

# Namespace map for ODF XML
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'xlink': 'http://www.w3.org/1999/xlink',
}


def find_odm_file():
    """Find the master document (.odm) file in WORKDIR."""
    # First check the canonical path
    canonical = os.path.join(WORKDIR, f'{TASK_ID}.odm')
    if os.path.exists(canonical):
        return canonical
    # Search for any .odm file
    for f in os.listdir(WORKDIR):
        if f.endswith('.odm'):
            return os.path.join(WORKDIR, f)
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: ODM file exists (0.15 points)
    try:
        odm_path = find_odm_file()
        if odm_path is not None:
            print(f"PASS: Component 1 -- ODM file found at {odm_path} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- No .odm file found in {WORKDIR}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Valid ODM format with correct mimetype (0.15 points)
    try:
        zf = zipfile.ZipFile(odm_path, 'r')
        mimetype = zf.read('mimetype').decode('utf-8').strip()
        if mimetype == EXPECTED_MIMETYPE:
            print(f"PASS: Component 2 -- Correct mimetype: {mimetype} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 -- Expected mimetype '{EXPECTED_MIMETYPE}', got '{mimetype}'")
    except zipfile.BadZipFile:
        print(f"FAIL: Component 2 -- File is not a valid ZIP/ODM archive")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score
    except KeyError:
        print(f"FAIL: Component 2 -- No 'mimetype' entry in the archive")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Parse content.xml for remaining checks
    try:
        content_xml = zf.read('content.xml').decode('utf-8')
        root = ET.fromstring(content_xml)
        zf.close()
    except Exception as e:
        print(f"ERROR: Cannot parse content.xml -- {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Find all text:section elements
    sections = root.findall('.//text:section', NS)
    # Extract xlink:href from text:section-source children
    linked_files = []
    for sec in sections:
        source = sec.find('text:section-source', NS)
        if source is not None:
            href = source.get(f'{{{NS["xlink"]}}}href', '')
            # Strip any path prefix, keep just the filename
            linked_files.append(os.path.basename(href))

    print(f"DEBUG: Found {len(sections)} sections, linked files: {linked_files}")

    # Component 3: Contains exactly 5 text:section elements with subdoc links (0.20 points)
    try:
        if len(linked_files) == 5:
            print(f"PASS: Component 3 -- Exactly 5 subdocument sections found (0.20 pts)")
            total_score += 0.20
        elif len(linked_files) > 0:
            # Partial credit: proportional to how many of 5 sections exist
            partial = 0.20 * min(len(linked_files), 5) / 5
            print(f"PARTIAL: Component 3 -- Found {len(linked_files)} sections, expected 5 ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- No subdocument sections found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: All 5 subdocument links point to correct chapter files (0.30 points)
    try:
        correct_links = 0
        for expected in EXPECTED_CHAPTERS:
            if expected in linked_files:
                correct_links += 1
            else:
                print(f"FAIL: Component 4 -- Missing link to '{expected}'")

        if correct_links == 5:
            print(f"PASS: Component 4 -- All 5 chapter files correctly linked (0.30 pts)")
            total_score += 0.30
        elif correct_links > 0:
            partial = 0.30 * correct_links / 5
            print(f"PARTIAL: Component 4 -- {correct_links}/5 correct links ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- No correct chapter links found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Subdocument links are in correct order (0.20 points)
    try:
        if linked_files == EXPECTED_CHAPTERS:
            print(f"PASS: Component 5 -- Subdocuments in correct order (0.20 pts)")
            total_score += 0.20
        elif set(linked_files) == set(EXPECTED_CHAPTERS):
            print(f"FAIL: Component 5 -- All chapters present but in wrong order: {linked_files}")
        else:
            print(f"FAIL: Component 5 -- Links don't match expected chapters: {linked_files}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
